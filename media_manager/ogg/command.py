import argparse

from media_manager.lib.audio import open_audio


def create_parser(subparsers: argparse._SubParsersAction): # pylint:disable=protected-access
    parser = subparsers.add_parser('ogg')

    oggparsers = parser.add_subparsers(required=True, help='Ogg/vorbis help', dest='oggcommand')

    tag_ogg_parser = oggparsers.add_parser('tag')
    tag_ogg_parser.add_argument('ogg_file', help='Input ogg file', type=str)
    tag_ogg_parser.add_argument('--artist', help='Set artist', type=str)
    tag_ogg_parser.add_argument('--title', help='Set title', type=str)
    tag_ogg_parser.add_argument('--genre', help='Set genre (can be specified multiple times)',
                                type=str, action='append')
    tag_ogg_parser.set_defaults(func=tag_ogg)

def tag_ogg(args: argparse.Namespace):
    audio = open_audio(args.ogg_file)
    if args.artist:
        audio['ARTIST'] = args.artist
    if args.title:
        audio['TITLE'] = args.title
    if args.genre:
        audio['GENRE'] = args.genre[0]
        for next_genre in args.genre[1:]:
            audio.tags.append(('GENRE', next_genre))

    audio.save()
