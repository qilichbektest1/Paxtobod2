import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
DATABASE_PATH = "taxi_bot.db"

# Admin user ID (o'zingizning user ID'ingiz)
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))

# Taxi drivers group where orders will be sent
TAXI_GROUP_ID = int(os.getenv("TAXI_GROUP_ID", "0"))

# Bot name
BOT_NAME = "🚕 Toshkent-Paxtobod Taxi Bot"
