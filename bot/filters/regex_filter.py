from pyrogram.filters import create
from pyrogram.types import Message
import re

def create_regex_filter(*patterns: str):
  async def regex_filter(_, __, m: Message):
    compiled = map(re.compile, patterns)
    return m.text and any(map(lambda x: bool(x.match(m.text)), compiled))
  
  return create(regex_filter)