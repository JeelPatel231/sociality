import asyncio
from collections import defaultdict
from gallery_dl.job import Job
from gallery_dl.path import PathFormat
from gallery_dl.postprocessor.common import PostProcessor
from .gallery_dl_config import setup

setup() #this will setup gallery dl config

class UploadGroupPostProcessor(PostProcessor):

    def __init__(self, job: Job, options=None):
      PostProcessor.__init__(self, job)
      self.__job = job
      self.__file_paths = []
      self.__fut = asyncio.get_running_loop().create_future()
      ###
      job.hooks = defaultdict(list)
      job.register_hooks({
        "file": (self.file_hook),
      }, options)
      job.hooks["finalize"].append(self.finalize)

    def file_hook(self, pathfmt: PathFormat):
      self.__file_paths.append(pathfmt.path)

    def finalize(self, pathfmt: PathFormat):
      self.__fut.set_result(self.__file_paths)

    def job_result(self) ->  asyncio.Future[list[str]]:
      self.__job.run()
      return self.__fut