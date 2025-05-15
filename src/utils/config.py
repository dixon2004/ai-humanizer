from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Google Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
