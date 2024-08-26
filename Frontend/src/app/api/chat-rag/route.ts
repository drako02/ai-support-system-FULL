// src/app/api/chat-rag/route.ts
import { NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(request: Request) {
  try {
    // Parse the request body
      const requestBody = await request.json();

    // Forward the request to FastAPI
    const response = await axios.post('http://localhost:8000/chat',  requestBody);

    // Return the response from FastAPI
    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Error forwarding request to FastAPI:', error);
    return NextResponse.json({ error: 'An error occurred while processing your request.' }, { status: 500 });

  }
}
