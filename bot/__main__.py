from pyrogram.types import BotCommand
from pyrogram.sync import idle
from bot import app
from .plugins import *

async def main():
    #start the client first
    await app.start()
    print("APP IS RUNNING")
    
    await app.set_bot_commands([
        BotCommand('ping', 'To check latency and also if bot is alive or dead.')
    ])

    # keep running
    await idle()

if __name__ == "__main__":
    app.run(main())