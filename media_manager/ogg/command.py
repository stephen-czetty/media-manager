import argparse

import sys
import base64
from mutagen.oggopus import OggOpus
from mutagen.flac import Picture
from PIL import Image

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
    tag_ogg_parser.set_defaults(func=tag_ogg)

def add_image(args: argparse.Namespace):
    print(f'Adding an image from {args.image_file} to {args.ogg_file}')

    audio = OggOpus(args.ogg_file)
    im = Image.open(args.image_file)
    width, height = im.size
    fmt = im.format
    print(fmt)
    with open(args.image_file, "rb") as c:
        data = c.read()
    picture = Picture()
    picture.data = data
    picture.type = 17
    picture.desc = u"Cover Art"
    picture.mime = u"image/jpeg"
    picture.width = width
    picture.height = height
    picture.depth = 24
    picture_data = picture.write()
    encoded_data = base64.b64encode(picture_data)

    vcomment_value = encoded_data.decode("ascii")
    audio["metadata_block_picture"] = [vcomment_value]

    audio.save()

def tag_ogg(args: argparse.Namespace):
    audio = OggOpus(args.ogg_file)
    if args.artist:
        audio['ARTIST'] = args.artist
    if args.title:
        audio['TITLE'] = args.title

    audio.save()
