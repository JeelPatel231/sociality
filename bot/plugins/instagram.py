from bot import app
from pyrogram.client import Client
from gallery_dl.job import DownloadJob
from pyrogram.types.messages_and_media import Message
from bot.filters.regex_filter import create_regex_filter
from bot.lib.gallery_dl_hook import UploadGroupPostProcessor

INSTAGRAM_LINK = r"(?:https?://)?(?:www\.)?instagram\.com"

is_instagram_link = create_regex_filter(INSTAGRAM_LINK)

@app.on_message(filters=is_instagram_link)
async def _(client: Client, msg: Message):
  reply = await msg.reply_text('Handling Instagram Link', quote=True)
  dl_job = DownloadJob(msg.text)
  UploadGroupPostProcessor(dl_job, msg)
  dl_job.run()
