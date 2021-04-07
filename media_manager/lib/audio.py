from mutagen import File
from mutagen.oggopus import OggOpus
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4

def open_audio(file_name: str) -> File:
    return File(file_name, options=[OggOpus, OggVorbis, MP4])
