import os
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram import Bot
from pymongo import MongoClient

load_dotenv()

TOKEN = str(os.environ.get("TOKEN", None))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 1214585391))
API_KEY = str(os.environ.get("API_KEY"))
DB_URL = str(os.environ.get("DB_URL"))

bot = Bot(TOKEN)
db_client = MongoClient(DB_URL)
updater = Updater(TOKEN)
dispatcher = updater.dispatcher