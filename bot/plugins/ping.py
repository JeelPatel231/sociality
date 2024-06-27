from bot import app
from datetime import datetime
from pyrogram.client import Client
from pyrogram.types import Message
from bot.filters.command_filter import command

@app.on_message(filters=command('ping'))
async def handle_ping(client: Client, msg: Message):
  start = datetime.now()
  ping_mess = await client.send_message(msg.chat.id, "ping test!")
  end = datetime.now()
  duration = (end - start).microseconds / 1000
  await msg.reply_text(f"`Pong!\n{duration}ms`", quote=True)
  await ping_mess.delete()