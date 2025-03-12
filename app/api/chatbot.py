import os
import openai
import dotenv

# Load environment variables
dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_completion(prompt, model_engine="gpt-3.5-turbo"):
    """
    Get a chat completion response from OpenAI's API.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error in chat_completion: {e}")
        return "Sorry, I don't understand."

def get_embeddings(text, model_engine="text-embedding-ada-002"):
    """
    Get embeddings for a given text using OpenAI's API.
    """
    try:
        response = openai.Embedding.create(
            input=text,
            model=model_engine,
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"Error in get_embeddings: {e}")
        return None