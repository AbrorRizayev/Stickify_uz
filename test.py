import os
from dotenv import load_dotenv
load_dotenv('.env')
print("DB CONFIG:", os.getenv("POSTGRES_HOST"), os.getenv("POSTGRES_PORT"))
