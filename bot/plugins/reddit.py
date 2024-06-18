import re
from bot import app
from pyrogram.client import Client
from gallery_dl.job import DownloadJob
from pyrogram.types.messages_and_media import Message
from bot.filters.regex_filter import create_regex_filter
from bot.lib.gallery_dl_hook import UploadGroupPostProcessor
from bot.filters.regex_filter import create_regex_filter

# Patterns are kanged from gallery_dl

SUBREDDIT_PATTERN = (r"(?:https?://)?(?:\w+\.)?reddit\.com"
               r"(/r/[^/?#]+(?:/([a-z]+))?)/?(?:\?([^#]*))?(?:$|#)")

HOME_PATTERN = (r"(?:https?://)?(?:\w+\.)?reddit\.com"
               r"((?:/([a-z]+))?)/?(?:\?([^#]*))?(?:$|#)")

USER_PATTERN = (r"(?:https?://)?(?:\w+\.)?reddit\.com/u(?:ser)?/"
               r"([^/?#]+(?:/([a-z]+))?)/?(?:\?([^#]*))?$")

SUBMISSION_PATTERN = (r"(?:https?://)?(?:"
            r"(?:\w+\.)?reddit\.com/(?:(?:r|u|user)/[^/?#]+"
            r"/comments|gallery)|redd\.it)/([a-z0-9]+)")

IMAGE_PATTERN = (r"(?:https?://)?((?:i|preview)\.redd\.it|i\.reddituploads\.com)"
               r"/([^/?#]+)(\?[^#]*)?")

REDIRECT_PATTERN = (r"(?:https?://)?(?:"
               r"(?:\w+\.)?reddit\.com/(?:(?:r)/([^/?#]+)))"
               r"/s/([a-zA-Z0-9]{10})")

is_reddit_link = create_regex_filter(SUBREDDIT_PATTERN, HOME_PATTERN, USER_PATTERN, SUBMISSION_PATTERN, IMAGE_PATTERN, REDIRECT_PATTERN)


@app.on_message(filters=is_reddit_link)
async def _(client: Client, msg: Message):
  reply = await msg.reply_text('Handling Reddit Link', quote=True)
  dl_job = DownloadJob(msg.text)
  UploadGroupPostProcessor(dl_job, msg)
  dl_job.run()

