import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPEN_ROUTER_KEY')

GENAI_PRO = 'openai/gpt-oss-120b:free'
