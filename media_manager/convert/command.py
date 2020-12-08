import argparse

import ffmpeg

def create_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('convert')

    parser.add_argument('input_file', help='Input media file', type=str)
    parser.add_argument('output_file', help='Output media file', type=str)
    parser.add_argument('--overwrite', help='Overwrite output without confirmation', action='store_true')
    #parser.add_argument('--keep-video', help='Keep the video in the output file.', action='store_true')
    parser.set_defaults(func=convert_media)

    return parser

def convert_media(args: argparse.Namespace):
    process = ffmpeg.input(args.input_file).audio.output(args.output_file, acodec='copy', map_chapters=0)
    if args.overwrite:
        process = process.overwrite_output()
    process.run()
