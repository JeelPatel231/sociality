from pyrogram import Client
from dotenv import dotenv_values
from gallery_dl.config import load
import os

load(files=['gallery-dl.conf']) # load gallery-dl config from current directory explicitly

config = {
  **dotenv_values('.development.env'), # development
  **dotenv_values('.env'), # production
  **os.environ,  # override loaded values with environment variables
}

app = Client(
    name="Sociality",
    bot_token=config["BOT_TOKEN"],
    api_id=config["API_ID"],
    api_hash=config["API_HASH"],
)