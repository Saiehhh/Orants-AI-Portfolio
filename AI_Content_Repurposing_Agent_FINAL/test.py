from google import genai
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure it's in your .env file as GEMINI_API_KEY=your_key_here")

# Configure the client
client = genai.Client(api_key=api_key)

# Use the correct model name
prompt = "Write a 2-line motivational quote about AI learning."

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=prompt
)

print("\n✅ Gemini API Connected Successfully!\n")
print("AI Output:\n", response.text)