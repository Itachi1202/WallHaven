import os
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram import Bot

load_dotenv()

TOKEN = str(os.environ.get("TOKEN", None))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 1214585391))
API_KEY = str(os.environ.get("API_KEY"))

bot = Bot(TOKEN)
updater = Updater(TOKEN)
dispatcher = updater.dispatcher