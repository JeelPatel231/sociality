from bot import config
from librespot.core import Session, CdnManager, PlayableContentFeeder
from librespot.metadata import TrackId
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality
from librespot.audio import CdnFeedHelper, Metadata
from io import BytesIO


class SpotifyDownloader:
    def __init__(self) -> None:
        self.__session = Session.Builder() \
            .user_pass(
                config['SPOTIFY_USERNAME'], 
                config['SPOTIFY_PASSWORD']
            ).create()
        self.__api = self.__session.api()
        self.__cdn = CdnManager(self.__session)
        
    def download_track(self, uri: str) -> BytesIO:
        track_id = TrackId.from_base62(uri)
        # track_id = TrackId.from_uri(uri)
        # 'spotify:track:6BhYxJYdtA581FztYCqERE'
        track = self.__api.get_metadata_4_track(track_id)
        track_selector = VorbisOnlyAudioQuality(AudioQuality.HIGH)
        #
        file: Metadata.AudioFile = track_selector.get_file(track.file)
        url = self.__cdn.get_audio_url(file.file_id)
        loaded_track = CdnFeedHelper.load_track(self.__session, track, file, url , False, None)

        stream = loaded_track.input_stream.stream()

        b_ptr = BytesIO(stream.read(stream.size()))
        b_ptr.name = f"{track.name} - {track.album.name}"
        return b_ptr
