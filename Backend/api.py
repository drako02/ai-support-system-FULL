import os
import PyPDF2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()




os.environ["OPENAI_API_KEY"]=os.getenv('OPENAI_API_KEY')

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/"],  # Adjust based on your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI()

# Initialize Pinecone client
pc = Pinecone(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment='us-east-1'
)

print("working")

index_name = "rag-index"

# Create Pinecone index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # This should match the dimension of your embeddings
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'  # Adjust to your preferred region
        )
    )

print("working 2")

index = pc.Index(index_name)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Load and process the PDF file
pdf_text = extract_text_from_pdf("dsa_notes.pdf")

# Split the extracted text into chunks (e.g., by paragraphs or sentences)
text_chunks = pdf_text.split("\n\n")  # Example: Split by double newlines for paragraphs

print("working 3")

# Initialize OpenAI Embeddings model
embeddings_model = OpenAIEmbeddings(model = 'text-embedding-3-small')


print("working 4")

# Embed and upsert chunks into Pinecone
for i, chunk in enumerate(text_chunks):
    embedding = embeddings_model.embed_query(chunk)
    index.upsert([(str(i), embedding, {"text": chunk[:40000]})])

print("working 5")

# Request model
class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(query_request: QueryRequest):
    try:
        # Convert query to embedding
        query_embedding = embeddings_model.embed_query(query_request.query)
        
        # Retrieve top 3 most similar documents from Pinecone
        result = index.query(vector=query_embedding, top_k=3, include_metadata=True)
        retrieved_docs = [match['metadata']['text'] for match in result['matches']]

        # Generate a response using OpenAI's GPT model
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # Specify the appropriate model
            messages=[
                {"role": "user", "content": query_request.query},
                {"role": "system", "content": f"Context: {' '.join(retrieved_docs)}"},
            ],
            max_tokens= 200,
        )

        response_text = chat_completion.choices[0].message.content

        return {"response": response_text}
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail="Internal Server Error") # Keep error 

print("working 1")