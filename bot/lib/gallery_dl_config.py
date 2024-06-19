import tempfile
from bot import config
import json
from gallery_dl.config import load

"""
This file is basically for making gallery-dl config in-memory

so that all the bot's configuration can be handled by .env file consistently
"""

gallery_dl_conf = {
    "extractor": {
        "instagram": {
          "api": "graphql"
        },
        "reddit": {
          "client-id" : config['REDDIT_CLIENT_ID']
        }
    }
}

def setup():
  fp = tempfile.NamedTemporaryFile('w+')
  print(fp.name)
  json.dump(gallery_dl_conf, fp)
  fp.seek(0)
  load(files=[fp.name]) # the library is so fucking bad ;__;