import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is missing from the .env file.")

model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)