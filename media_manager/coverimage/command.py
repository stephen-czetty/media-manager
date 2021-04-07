import argparse
import base64

from mutagen import File
from mutagen.oggopus import OggOpus
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import Picture
from mutagen.mp4 import MP4, MP4Cover
from PIL import Image

from media_manager.lib.audio import open_audio

def create_parser(subparsers: argparse._SubParsersAction): # pylint:disable=protected-access
    parser = subparsers.add_parser('coverimage', aliases=['cover', 'image'])

    parser.add_argument('audio_file', help='Input audio file', type=str)
    parser.add_argument('image_file', help='Cover image', type=str)
    parser.set_defaults(func=add_image)

_mp4_formats = {
    'JPEG': MP4Cover.FORMAT_JPEG,
    'PNG': MP4Cover.FORMAT_PNG
}

_image_mimes = {
    'JPEG': u'image/jpeg',
    'PNG': u'image/png'
}

def _add_mp4_image(audio: File, image: Image, image_data):
    image_format = _mp4_formats.get(image.format, MP4Cover.FORMAT_JPEG)
    covr = [MP4Cover(image_data, image_format)]

    audio.tags['covr'] = covr
    audio.save()

def _add_ogg_image(audio: File, image: Image, image_data: bytes):
    picture = Picture()
    picture.data = image_data
    picture.type = 3 # Front cover
    picture.desc = u"Cover Art"
    picture.mime = _image_mimes[image.format]
    picture.width = image.width
    picture.height = image.height
    picture.depth = 24
    picture_data = picture.write()
    encoded_data = base64.b64encode(picture_data)

    vcomment_value = encoded_data.decode("ascii")
    audio["metadata_block_picture"] = [vcomment_value]

    audio.save()

_coverimage_methods = {
    OggOpus: _add_ogg_image,
    OggVorbis: _add_ogg_image,
    MP4: _add_mp4_image
}

def add_image(args: argparse.Namespace):
    print(f'Adding an image from {args.image_file} to {args.audio_file}')

    audio = open_audio(args.audio_file)

    image = Image.open(args.image_file)

    with open(args.image_file, "rb") as image_fd:
        data = image_fd.read()
    _coverimage_methods[audio.__class__](audio, image, data)
