import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    MASTER_DB = os.getenv("MASTER_DB")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_EXPIRES_SECONDS", 3600))
