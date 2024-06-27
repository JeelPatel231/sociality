from pyrogram.client import Client
from dotenv import dotenv_values
import os

config = {
    **dotenv_values(".development.env"),  # development
    **dotenv_values(".env"),  # production
    **os.environ,  # override loaded values with environment variables
}


class SocialityBot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # cache the username to handle commands
        with self:
            self.me = self.get_me()

    # TODO: override on_message and use try catch
    # for filtering exceptions and responding using bot

app = SocialityBot(
    name="Sociality",
    bot_token=config["BOT_TOKEN"],
    api_id=config["API_ID"],
    api_hash=config["API_HASH"],
    in_memory=True,
)
