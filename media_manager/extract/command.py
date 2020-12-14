import argparse
from pathlib import PurePath

import ffmpeg

def create_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('extract')

    parser.add_argument('input_file', help='Input media file', type=str)
    parser.add_argument('output_file', help='Output media file', type=str, default=None)
    parser.add_argument('--overwrite', help='Overwrite output without confirmation', action='store_true')
    #parser.add_argument('--keep-video', help='Keep the video in the output file.', action='store_true')
    parser.set_defaults(func=convert_media)

    return parser

def _determine_audio_type(file_name):
    return 'ogg'

def _create_output_filename(input_file_name, audio_type):
    path = PurePath(input_file_name)
    return str(path.stem) + f'.{audio_type}'

def convert_media(args: argparse.Namespace):
    audio_type = _determine_audio_type(args.input_file)
    output_file = args.output_file or _create_output_filename(args.input_file, audio_type)
    process = ffmpeg.input(args.input_file).audio.output(output_file, acodec='copy', map_chapters=0)
    if args.overwrite:
        process = process.overwrite_output()
    process.run()
