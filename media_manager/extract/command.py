import argparse
from pathlib import Path

import ffmpeg

from media_manager.lib.exceptions import MediaManagerError

def create_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('extract')

    parser.add_argument('input_file', help='Input media file', type=str)
    parser.add_argument('output_file', help='Output media file', type=str, nargs='?')
    parser.add_argument('--overwrite', help='Overwrite output without confirmation', action='store_true')
    #parser.add_argument('--keep-video', help='Keep the video in the output file.', action='store_true')
    parser.set_defaults(func=convert_media)

    return parser

CODECS = {
    'aac': 'mp4',
    'opus': 'ogg'
}

def _determine_output_container(file_name):
    file_data = ffmpeg.probe(file_name)
    for stream in file_data.get('streams', []):
        if stream.get('codec_type') == 'audio':
            return CODECS.get(stream.get('codec_name'), 'ogg')
    raise MediaManagerError('No audio stream found')

def _create_output_filename(input_file_name, audio_type):
    path = Path(input_file_name).resolve()
    return str(path.parent / path.stem) + f'.{audio_type}'

def convert_media(args: argparse.Namespace):
    container_type = _determine_output_container(args.input_file)
    output_file = args.output_file or _create_output_filename(args.input_file, container_type)
    process = ffmpeg.input(args.input_file).audio.output(output_file, acodec='copy', map_chapters=0)
    if args.overwrite:
        process = process.overwrite_output()
    try:
        process.run()
    except ffmpeg.Error:
        # The underlying ffmpeg already writes its error to
        # stderr, so this exception just creates noise.
        pass
