import argparse

import io
import sys
import base64
from mutagen import File
from mutagen.oggopus import OggOpus
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import Picture
from mutagen.mp4 import MP4, MP4Cover
from PIL import Image

_image_mimes = {
    'JPEG': u'image/jpeg',
    'PNG': u'image/png'
}

def create_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('ogg')

    oggparsers = parser.add_subparsers(required=True, help='Ogg/vorbis help', dest='oggcommand')

    tag_ogg_parser = oggparsers.add_parser('tag')
    tag_ogg_parser.add_argument('ogg_file', help='Input ogg file', type=str)
    tag_ogg_parser.add_argument('--artist', help='Set artist', type=str)
    tag_ogg_parser.add_argument('--title', help='Set title', type=str)
    tag_ogg_parser.add_argument('--genre', help='Set genre (can be specified multiple times)', type=str, action='append')
    tag_ogg_parser.set_defaults(func=tag_ogg)

    cover_image_parser = subparsers.add_parser('coverimage', aliases=['cover', 'image'])
    cover_image_parser.add_argument('audio_file', help='Input audio file', type=str)
    cover_image_parser.add_argument('image_file', help='Cover image', type=str)
    cover_image_parser.set_defaults(func=add_image)

def _open_audio(file_name):
    return File(file_name, options=[OggOpus, OggVorbis, MP4])
    
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

def tag_ogg(args: argparse.Namespace):
    audio = _open_audio(args.ogg_file)
    if args.artist:
        audio['ARTIST'] = args.artist
    if args.title:
        audio['TITLE'] = args.title
    if args.genre:
        audio['GENRE'] = args.genre[0]
        for next_genre in args.genre[1:]:
            audio.tags.append(('GENRE', next_genre))

    audio.save()

_mp4_formats = {
    'JPEG': MP4Cover.FORMAT_JPEG,
    'PNG': MP4Cover.FORMAT_PNG
}

def _add_mp4_image(audio: File, image: Image, image_data):
    image_format = _mp4_formats.get(image.format, MP4Cover.FORMAT_JPEG)
    covr = [MP4Cover(image_data, image_format)]

    audio.tags['covr'] = covr
    audio.save()

_coverimage_methods = {
    OggOpus: _add_ogg_image,
    OggVorbis: _add_ogg_image,
    MP4: _add_mp4_image
}

def add_image(args: argparse.Namespace):
    print(f'Adding an image from {args.image_file} to {args.audio_file}')

    audio = _open_audio(args.audio_file)

    im = Image.open(args.image_file)

    with open(args.image_file, "rb") as c:
        data = c.read()
    _coverimage_methods[audio.__class__](audio, im, data)
