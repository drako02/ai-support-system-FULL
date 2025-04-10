# AI Support System

This project is designed to provide AI-driven support by processing PDF documents and generating chat-based responses. It is divided into two main parts: a FastAPI backend and a Next.js frontend. This README focuses on the backend and explains its architecture and functionalities in detail.

## Table of Contents

- [Overview](#overview)
- [Backend Architecture](#backend-architecture)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The AI Support System uses artificial intelligence to answer user queries by processing and retrieving context from a PDF document. The backend achieves this by:

- Extracting text from a PDF file.
- Splitting the text into manageable chunks.
- Generating embeddings for each text chunk using a custom OpenAI embedding model.
- Indexing the embeddings with Pinecone for fast similarity searches.
- Accepting queries that are embedded, and then retrieving the most relevant text chunks to provide context for a chat completion request to OpenAI's GPT-3.5 model.

## Backend Architecture

The backend is built with [FastAPI](https://fastapi.tiangolo.com/), using the following main components:

### Environment Setup

- **Environment Variables**:  
  Uses Python's `dotenv` to load variables from a `.env` file. Notably, `OPENAI_API_KEY` and `PINECONE_API_KEY` are loaded to securely access external services.

### API Initialization

- **FastAPI Application and Middleware**:  
  A FastAPI app is created with CORS middleware configured to allow requests from `http://localhost:3000`. This ensures that the frontend can communicate with the backend without CORS issues.

### External Service Initialization

- **OpenAI Client**:  
  The OpenAI client is initialized using the API key from environment variables. This client is later used to generate chat responses.

- **Pinecone Index**:  
  The code initializes a connection to Pinecone and creates an index (`rag-index`) with a specified dimension (1536) and metric type (euclidean) if it does not already exist. This index is used to store text embeddings for efficient similarity searches.

### PDF Processing

- **Extracting Text**:  
  The function `extract_text_from_pdf(pdf_path)` reads a PDF file (in this case, `dsa_notes.pdf`) using the PyPDF2 library and extracts its text content. The text is then split into chunks using line breaks as delimiters.

### Embeddings and Indexing

- **Embeddings Generation**:  
  An embeddings model (`OpenAIEmbeddings`) from the `langchain_openai` package is used to generate embeddings for each text chunk. This transforms each chunk into a vector representation.

- **Indexing with Pinecone**:  
  Each text chunk is upserted into the Pinecone index along with its generated embedding. This allows the backend to later query for text chunks that are similar to an incoming query's embedding.

### Query Endpoint

- **/chat Endpoint**:  
  The backend defines a POST endpoint `/chat` which:
  1. Receives a query wrapped in a Pydantic model.
  2. Generates an embedding for the received query.
  3. Searches the Pinecone index for the top 3 matching text chunks.
  4. Sends a request to the OpenAI API with the user's query and the retrieved context to generate a chat response.
  5. Returns the response text to the client.

Error handling is in place: if any step fails while processing the request, the API returns a `500 Internal Server Error`.

## Project Structure

```
/ai-support-system-FULL
│
├── Backend
│   ├── api.py            # FastAPI backend, PDF processing, indexing, and chat endpoint
│   └── requirements.txt  # List of Python dependencies
│
├── Frontend
│   └── ...               # Next.js application files
│
└── .gitignore            # Files and folders to ignore in Git
```

## Setup and Installation

### Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/) (for the frontend)
- [Pinecone API Key](https://www.pinecone.io/start/)
- [OpenAI API Key](https://openai.com/api/)

### Backend Setup

1. Navigate to the `Backend` directory:
   ```bash
   cd /home/drako/personal-project/ai-support-system-FULL/Backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
   *Ensure that your `requirements.txt` includes dependencies like fastapi, uvicorn, PyPDF2, python-dotenv, openai, pinecone-client, langchain-openai, etc.*

4. Create a `.env` file and add your credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   ```

### Frontend Setup

Refer to the [Frontend Setup](#frontend-setup) section in the complete documentation for details specific to the Next.js application.

## Running the Application

### Backend

From the `Backend` directory, run the FastAPI server:
```bash
uvicorn api:app --reload
```
This will start the server on [http://localhost:8000](http://localhost:8000).

### Frontend

Follow the relevant instructions to start the Next.js development server.

## API Endpoints

### POST /chat

- **Description**:  
  Processes a chat query by retrieving context from the indexed PDF and generating a response via OpenAI's GPT-3.5 model.

- **Request Body**:
  ```json
  {
    "query": "Your question here"
  }
  ```

- **Response**:
  ```json
  {
    "response": "Generated chat response text"
  }
  ```

### How It Works

1. **Query Processing**: When a request is received, the query is embedded using the embeddings model.
2. **Context Retrieval**: The backend uses Pinecone to search and retrieve the most similar text chunks from the PDF.
3. **Chat Generation**: The OpenAI client is used to pass both the user query and the relevant context to generate a comprehensive chat response.

## Troubleshooting

- **API Failures**:  
  Check the console logs for error messages. Verify that your API keys and file paths (such as to `dsa_notes.pdf`) are correct.

- **Service Connectivity**:  
  Ensure that both Pinecone and OpenAI services are accessible from your environment.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)