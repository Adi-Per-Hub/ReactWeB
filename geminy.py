import os
from dotenv import load_dotenv # Import the function to load .env file
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# The genai client will now automatically pick up GEMINI_API_KEY
# if it's correctly set in your .env file
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)
print(response.text)