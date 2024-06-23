import mimetypes
import os
from bot import app
from pyrogram.client import Client
from gallery_dl.job import DownloadJob
from pyrogram.types.messages_and_media import Message
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument
from bot.filters.regex_filter import create_regex_filter
from bot.lib.gallery_dl_hook import UploadGroupPostProcessor

INSTAGRAM_LINK = r"(?:https?://)?(?:www\.)?instagram\.com"

is_instagram_link = create_regex_filter(INSTAGRAM_LINK)


def mimetype_to_telegram(path: str):
  (_type, _encoding) = mimetypes.guess_type(path)
  if _type is None:
    raise Exception(f'Mime Type cannot be guessed for path: {path}')

  if _type.startswith('image'):
    return InputMediaPhoto(path)
  
  if _type.startswith('video'):
    return InputMediaVideo(path)
    
  raise Exception(f'Unhandled Mime Type: {_type} : {_encoding}')

@app.on_message(filters=is_instagram_link)
async def _(client: Client, msg: Message):
  handling_reply = await msg.reply_text('Handling Instagram Link', quote=True) 
  hook_job = UploadGroupPostProcessor(DownloadJob(msg.text))
  downloaded_files = await hook_job.job_result()
  
  # files have been downloaded, send the files
  input_media = list(map(mimetype_to_telegram, downloaded_files))
  await msg.reply_media_group(media=input_media, quote=True)
  await handling_reply.delete()

  # clean up the files from filesystem
  for file in downloaded_files:
    os.remove(file)
