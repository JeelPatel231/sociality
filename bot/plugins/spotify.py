from bot.filters.regex_filter import create_regex_filter
from bot.lib.librespot import SpotifyDownloader
import re
from bot import app
from pyrogram.client import Client
from pyrogram.types.messages_and_media import Message

downloader = SpotifyDownloader()

SPOTIFY_TRACK_LINK = r"(https?:\/\/)?open\.spotify\.com\/track\/(\w+)"

spotify_link = create_regex_filter(SPOTIFY_TRACK_LINK)

@app.on_message(filters=spotify_link)
async def _(client: Client, msg: Message):
  await msg.reply_text('Handling Spotify Link', quote=True)
  matches = re.match(SPOTIFY_TRACK_LINK, msg.text)
  base62_track_uri = matches.group(2)
  song_bytes = downloader.download_track(base62_track_uri)
  await msg.reply_audio(song_bytes, quote=True)