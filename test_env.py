import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

API_KEY = os.getenv("OPENAI_API_KEY")

print(f"API Key: {API_KEY}")  # API 키 출력 (테스트용)
