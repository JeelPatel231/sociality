from pyrogram.types import Message
from pyrogram.filters import create

def text_filter(text: str):
  async def _filter_impl(_,__,msg: Message):
    return msg.text and msg.text == text
  
  return create(_filter_impl)
  