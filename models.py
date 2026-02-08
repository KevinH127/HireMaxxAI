import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

GENAI_LITE = 'gemini-2.5-flash'
GENAI_PRO = 'gemini-2.5-pro'