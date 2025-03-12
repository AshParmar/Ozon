import os
import dotenv
import google.generativeai as genai
from typing import Optional, List

# Load environment variables
dotenv.load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

def chat_completion(prompt: str) -> Optional[str]:
    """
    Get a chat completion response from Gemini API.

    Args:
        prompt (str): The user's input prompt.

    Returns:
        Optional[str]: The generated response from the model, or None if an error occurs.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error in chat_completion: {e}")
        return None

def get_embeddings(text: str) -> Optional[List[float]]:
    """
    Get embeddings for a given text using Gemini API.
    
    (Note: Gemini API does not currently provide embeddings like OpenAI’s API, 
    so this function is a placeholder.)

    Args:
        text (str): The text to get embeddings for.

    Returns:
        Optional[List[float]]: Placeholder return value, since embeddings are unavailable.
    """
    print("Warning: Gemini API does not currently support text embeddings.")
    return None

# Example usage
if __name__== "_main_":
    prompt = "What is the capital of France?"
    response = chat_completion(prompt)
    if response:
        print(f"Chat Completion: {response}")

    text = "This is a sample text for embeddings."
    embeddings = get_embeddings(text)
    if embeddings:
        print(f"Embeddings: {embeddings}")