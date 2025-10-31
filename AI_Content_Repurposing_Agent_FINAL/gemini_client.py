# gemini_client.py
from google import genai
import os

def make_client():
    """
    Create and return a Gemini API client.
    The client reads GEMINI_API_KEY from environment automatically.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    client = genai.Client(api_key=api_key)
    return client

def generate_text(client, prompt, model="gemini-2.0-flash-exp", max_output_tokens=800):
    """
    Simple wrapper to call Gemini generate_content.
    Returns the text response.
    """
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                'max_output_tokens': max_output_tokens,
                'temperature': 0.7,
            }
        )
        return response.text
    except Exception as e:
        print(f"❌ Error generating content: {str(e)}")
        raise