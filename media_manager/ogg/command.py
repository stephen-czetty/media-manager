import argparse

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
    cover_image_parser = oggparsers.add_parser('coverimage', aliases=['cover', 'image'])
    cover_image_parser.add_argument('ogg_file', help='Input ogg file', type=str)
    cover_image_parser.add_argument('image_file', help='Cover image', type=str)
    cover_image_parser.set_defaults(func=add_image)

    tag_ogg_parser = oggparsers.add_parser('tag')
    tag_ogg_parser.add_argument('ogg_file', help='Input ogg file', type=str)
    tag_ogg_parser.add_argument('--artist', help='Set artist', type=str)
    tag_ogg_parser.add_argument('--title', help='Set title', type=str)
    tag_ogg_parser.add_argument('--genre', help='Set genre (can be specified multiple times)', type=str, action='append')
    tag_ogg_parser.set_defaults(func=tag_ogg)

    # TODO: Combine this with above and remove the ogg/mp4 portion of the command.
    parser = subparsers.add_parser('mp4')
    mp4parsers = parser.add_subparsers(required=True, help='MP4 help', dest='mp4command')
    cover_image_parser = mp4parsers.add_parser('coverimage', aliases=['cover', 'image'])
    cover_image_parser.add_argument('mp4_file', help='Input mp4 file', type=str)
    cover_image_parser.add_argument('image_file', help='Cover image', type=str)
    cover_image_parser.set_defaults(func=add_mp4_image)

def _open_ogg(file_name):
    return File(file_name, options=[OggOpus, OggVorbis])

def add_image(args: argparse.Namespace):
    print(f'Adding an image from {args.image_file} to {args.ogg_file}')

    audio = _open_ogg(args.ogg_file)
    im = Image.open(args.image_file)
    width, height = im.size
    fmt = im.format

    with open(args.image_file, "rb") as c:
        data = c.read()
    picture = Picture()
    picture.data = data
    picture.type = 3 # Front cover
    picture.desc = u"Cover Art"
    picture.mime = _image_mimes[fmt]
    picture.width = width
    picture.height = height
    picture.depth = 24
    picture_data = picture.write()
    encoded_data = base64.b64encode(picture_data)

    vcomment_value = encoded_data.decode("ascii")
    audio["metadata_block_picture"] = [vcomment_value]

    audio.save()

def tag_ogg(args: argparse.Namespace):
    audio = _open_ogg(args.ogg_file)
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

def add_mp4_image(args: argparse.Namespace):
    audio = MP4(args.mp4_file)
    with open(args.image_file, "rb") as fd:
        image_data = fd.read()

    im = Image.open(args.image_file)
    image_format = _mp4_formats.get(im.format, MP4Cover.FORMAT_JPEG)
    covr = [MP4Cover(image_data, image_format)]

    audio.tags['covr'] = covr
    audio.save()
