from bot import app
from pyrogram.client import Client
from pyrogram.types.messages_and_media import Message
from bot.filters.regex_filter import create_regex_filter
from bot.lib.gallery_dl_tgbot import download_with_gallerydl

INSTAGRAM_LINK = r"(?:https?://)?(?:www\.)?instagram\.com"

is_instagram_link = create_regex_filter(INSTAGRAM_LINK)




@app.on_message(filters=is_instagram_link)
async def _(client: Client, msg: Message):
  handling_reply = await msg.reply_text('Handling Instagram Link', quote=True) 
  
  await download_with_gallerydl(msg)

  await handling_reply.delete()
  