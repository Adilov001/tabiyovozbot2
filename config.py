from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
