import argparse
from typing import List

from .convert import command as convert_command
from .ogg import command as ogg_command


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help='Increase verbosity', action='count', default=0)

    subparsers = parser.add_subparsers(required=True, help='Subcommands', dest='subcommand')
    convert_command.create_parser(subparsers)
    ogg_command.create_parser(subparsers)

    return parser

def main():
    parser = _create_parser()

    args = parser.parse_args()
    args.func(args)
