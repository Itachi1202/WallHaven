import os
from pymongo import MongoClient
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram import Bot

load_dotenv()

DB_URL = str(os.environ.get("DB_URL"))
TOKEN = str(os.environ.get("TOKEN", None))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 1214585391))
API_KEY = str(os.environ.get("API_KEY"))

db_client = MongoClient(DB_URL)
bot = Bot(TOKEN)
updater = Updater(TOKEN)
dispatcher = updater.dispatcher