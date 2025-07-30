from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Access database and collection
db = client[DB_NAME]
users_collection = db["users"]

async def create_db():
    try:
        await db.command("ping")
        print("✅ MongoDB connected successfully.")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
