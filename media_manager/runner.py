import argparse
from typing import List

from .ogg import command

def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help='Increase verbosity', action='count', default=0)

    subparsers = parser.add_subparsers(required=True, help='Subcommands', dest='subcommand')
    command.create_parser(subparsers)

    return parser

def main():
    parser = _create_parser()

    args = parser.parse_args()
    args.func(args)
