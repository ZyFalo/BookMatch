import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")
JWT_SECRET = os.getenv("SECRET_KEY")
JWT_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))