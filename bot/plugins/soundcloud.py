
from bot import app
from pyrogram.client import Client
from pyrogram.types import Message
from bot.filters.regex_filter import create_regex_filter
from bot.lib.gallery_dl_tgbot import download_with_gallerydl


SOUNDCLOUD_TRACK_LINK = r"^(https?:\/\/)?soundcloud\.com\/(\w+)\/([\w-]+)$"

soundcloud_link = create_regex_filter(SOUNDCLOUD_TRACK_LINK)

@app.on_message(filters=soundcloud_link)
async def _(client: Client, msg: Message):
  handling_reply = await msg.reply_text('Handling SoundCloud Link', quote=True)

  # prefix with ytdl to tell gallery_dl to use ytdl
  # figure out a way to make a copy of this object 
  # and edit that instead of the original object
  msg.text = f"ytdl:{msg.text}"
  await download_with_gallerydl(msg)

  await handling_reply.delete()