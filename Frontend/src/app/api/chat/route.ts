import { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import axios from "axios";

export async function POST(request: NextRequest) {
    const { messages } = await request.json();

    try {
        const response = await axios.post(
             'https://api.openai.com/v1/chat/completions',
            {
                model: 'gpt-3.5-turbo-1106', // Correct model name
                messages,
                max_tokens: 150,
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${process.env.NEXT_PUBLIC_OPENAI_API_KEY}`,
                },
            }
        );

        return NextResponse.json(response.data);
    } catch (error) {
        console.error('Error with GPT API request:', error);
        return NextResponse.json({ error: 'Error with GPT API request' }, { status: 500 });

    }
    

}