from pyrogram import Client
from dotenv import dotenv_values
import os

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