import os
import asyncio
import mimetypes
from typing import Any
from collections import defaultdict
from pyrogram.types.messages_and_media import Message
from gallery_dl.job import Job
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from gallery_dl.path import PathFormat
from gallery_dl.postprocessor.common import PostProcessor

class UploadGroupPostProcessor(PostProcessor):

    def __init__(self, job: Job, msg: Message, options=None):
      PostProcessor.__init__(self, job)
      self.__msg = msg
      self.__file_paths = []
      ###
      job.hooks = defaultdict(list)
      job.register_hooks({
        "file": (self.file_hook),
      }, options)
      job.hooks["finalize"].append(self.finalize)

    def __map_to_telegram(self, path: str):
      (_type, _encoding) = mimetypes.guess_type(path)
      if _type.startswith('image'):
        return InputMediaPhoto(path)
      
      if _type.startswith('video'):
        return InputMediaVideo(path)

      raise Exception(f'Unhandled Mime Type: {_type} : {_encoding}')
    
    def __clean_files(self, x: Any):
      print(x)
      for i in self.__file_paths:
        os.remove(i)
    
    def file_hook(self, pathfmt: PathFormat):
      self.__file_paths.append(pathfmt.path)

    def finalize(self, pathfmt: PathFormat):
      print(f'finalizing for {self.__msg.text}')
      media_group = list(map(self.__map_to_telegram, self.__file_paths))
      print(f'replying for {self.__msg.text}')
      coroutine = self.__msg.reply_media_group(media=media_group, quote=True)
      fut = asyncio.run_coroutine_threadsafe(coroutine, asyncio.get_running_loop())
      fut.add_done_callback(lambda x: self.__clean_files(x))

