import tempfile
from bot import config
import json
import base64
from gallery_dl.config import load

"""
This file is basically for making gallery-dl config in-memory

so that all the bot's configuration can be handled by .env file consistently
"""

INSTAGRAM_COOKIE_PATH = '/tmp/instagram.cookies.txt'

gallery_dl_conf = {
    "extractor": {
        "instagram": {
          "api": "graphql",
          "cookies": INSTAGRAM_COOKIE_PATH,
        },
        "reddit": {
          "client-id" : config['REDDIT_CLIENT_ID']
        }
    }
}

def setup():
  # instagram cookies txt
  with open(INSTAGRAM_COOKIE_PATH, 'w+b') as instagram_cookie_txt:
    instagram_cookie_txt.write(base64.b64decode(config['INSTAGRAM_COOKIES']))

  # gallery_dl config
  fp = tempfile.NamedTemporaryFile('w+')
  json.dump(gallery_dl_conf, fp)
  fp.seek(0)
  load(files=[fp.name]) # the library is so fucking bad ;__;