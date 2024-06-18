from pyrogram import idle
from bot import app
from .plugins import *

def main():
    #start the client first
    app.start()
    print("APP IS RUNNING")

    # keep running
    idle()

if __name__ == "__main__":
    main()