import argparse

from media_manager.lib.audio import open_audio

# These are documented here: https://mutagen.readthedocs.io/en/latest/api/mp4.html
ARTIST_TAG = '\xa9ART'
TITLE_TAG = '\xa9nam'
GENRE_TAG = '\xa9gen'


def create_parser(subparsers: argparse._SubParsersAction): # pylint:disable=protected-access
    parser = subparsers.add_parser('mp4')

    oggparsers = parser.add_subparsers(required=True, help='MP4 help', dest='mp4command')

    tag_ogg_parser = oggparsers.add_parser('tag')
    tag_ogg_parser.add_argument('mp4_file', help='Input mp4 file', type=str)
    tag_ogg_parser.add_argument('--artist', help='Set artist', type=str)
    tag_ogg_parser.add_argument('--title', help='Set title', type=str)
    tag_ogg_parser.add_argument('--genre', help='Set genre (can be specified multiple times)',
                                type=str, action='append')
    tag_ogg_parser.set_defaults(func=tag_mp4)

def tag_mp4(args: argparse.Namespace):
    audio = open_audio(args.mp4_file)
    if args.artist:
        audio[ARTIST_TAG] = args.artist
    if args.title:
        audio[TITLE_TAG] = args.title
    if args.genre:
        audio[GENRE_TAG] = args.genre[0]
        for next_genre in args.genre[1:]:
            audio.tags.append(('GENRE', next_genre))

    audio.save()
