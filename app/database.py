from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variable
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Database and collection
db = client["students_db"]
students_collection = db["students"]
