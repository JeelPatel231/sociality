from dataclasses import dataclass
import base64
import tempfile
import json
from gallery_dl import config as gdl_config


@dataclass
class GalleryDLConfig:
    reddit_client_id: str
    instagram_cookie_b64: str


class GalleryDLAdapter:

    def __create_tempfile_with_contents(self, content:str, delete=True):
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            tmp.write(content)
            return tmp.name
            
    def setup_config(self, config: GalleryDLConfig):
        """
        This is a seperate function and is not inline in constructor 
        for updating the gallery_dl config at runtime.
        """
        instagram_cookie_path = self.__create_tempfile_with_contents(
            base64.b64decode(config.instagram_cookie_b64).decode('utf-8'),
            delete=False
        )
        gallery_dl_conf = {
            "extractor": {
                "instagram": {
                    "api": "graphql",
                    "cookies": instagram_cookie_path,
                },
                "reddit": {"client-id": config.reddit_client_id},
            }
        }
        # gallery_dl config
        with tempfile.NamedTemporaryFile("w+") as _config:
            json.dump(gallery_dl_conf, _config)
            _config.seek(0)
            gdl_config.load(files=[_config.name])  # the library is so fucking bad ;__;

    def __init__(self, config: GalleryDLConfig):
        self.setup_config(config)