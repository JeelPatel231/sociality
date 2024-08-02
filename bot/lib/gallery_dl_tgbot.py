from pyrogram.client import Client
from pyrogram.types import Message
from .gallery_dl_hook import UploadGroupPostProcessor
from gallery_dl.job import DownloadJob
import mimetypes
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
import os

def mimetype_to_telegram(path: str):
  (_type, _encoding) = mimetypes.guess_type(path)
  if _type is None:
    raise Exception(f'Mime Type cannot be guessed for path: {path}')

  if _type.startswith('image'):
    return InputMediaPhoto(path)
  
  if _type.startswith('video'):
    return InputMediaVideo(path)
  
  if _type.startswith('audio'):
    return InputMediaAudio(path)
    
  raise Exception(f'Unhandled Mime Type: {_type} : {_encoding}')

async def download_with_gallerydl(msg: Message):
  hook_job = UploadGroupPostProcessor(DownloadJob(msg.text))
  downloaded_files = await hook_job.job_result()
  
  # files have been downloaded, send the files
  input_media = list(map(mimetype_to_telegram, downloaded_files))
  await msg.reply_media_group(media=input_media, quote=True)

  # clean up the files from filesystem
  for file in downloaded_files:
    os.remove(file)