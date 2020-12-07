import argparse

def create_parser(subparsers: argparse._SubParsersAction):
    parser = subparsers.add_parser('ogg')

    oggparsers = parser.add_subparsers(required=True, help='Ogg/vorbis help', dest='oggcommand')
    cover_image_parser = oggparsers.add_parser('coverimage', aliases=['cover', 'image'])
    cover_image_parser.add_argument('ogg_file', help='Input ogg file', type=argparse.FileType('r+b'))
    cover_image_parser.add_argument('image_file', help='Cover image', type=argparse.FileType('rb'))
    cover_image_parser.set_defaults(func=add_image)

def add_image(args: argparse.Namespace):
    print(f'Adding an image from {args.image_file.name} to {args.ogg_file.name}')
