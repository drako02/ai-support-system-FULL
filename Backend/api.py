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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

pc = Pinecone(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment='us-east-1'
)

print("working")

index_name = "rag-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'  
        )
    )

print("working 2")

index = pc.Index(index_name)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

pdf_text = extract_text_from_pdf("dsa_notes.pdf")

text_chunks = pdf_text.split("\n\n")  

print("working 3")

embeddings_model = OpenAIEmbeddings(model = 'text-embedding-3-small')


print("working 4")

for i, chunk in enumerate(text_chunks):
    embedding = embeddings_model.embed_query(chunk)
    index.upsert([(str(i), embedding, {"text": chunk[:40000]})])

print("working 5")

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(query_request: QueryRequest):
    try:
        query_embedding = embeddings_model.embed_query(query_request.query)
        
        result = index.query(vector=query_embedding, top_k=3, include_metadata=True)
        retrieved_docs = [match['metadata']['text'] for match in result['matches']]

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  
            messages=[
                {"role": "user", "content": query_request.query},
                {"role": "system", "content": f"Context: {' '.join(retrieved_docs)}"},
            ],
            max_tokens= 200,
        )

        response_text = chat_completion.choices[0].message.content

        return {"response": response_text}
    except Exception as e:
        print(f"Error occurred: {str(e)}")  
        raise HTTPException(status_code=500, detail="Internal Server Error") 

print("working 1")