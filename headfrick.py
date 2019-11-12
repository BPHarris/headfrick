"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from platform import platform


class Program:
    """"""

    def __init__(self) -> None:
        """"""
        pass


def get_eof_str() -> str:
    """Return a string representin the platforms EOF input."""
    platform_name = platform().lower()
    eof_str = 'EOF'

    if 'windows' in platform_name:
        eof_str = 'Ctrl+Z then Ctrl+ENTER on a newline'
    if 'macos' in platform_name or 'osx' in platform_name:
        # TODO verify this
        eof_str = 'Ctrl+Z'
    if 'linux' in platform_name or 'unix' in platform_name:
        # TODO verify this
        eof_str = 'Ctrl+Z'
    
    return eof_str


def repl() -> None:
    """Brainfuck REPL."""
    pass


def main() -> None:
    """Entry point."""
    # Configure argument parser
    parser = ArgumentParser(
        description='Interpret a given brainfuck file. If no file is given ' +
            'a REPL is provided.'
    )
    parser.add_argument(
        '-f', '--file',
        type=FileType('r'),
        help='the brainfuck source code file',
        metavar='FILE',
        dest='file'
    )

    args = parser.parse_args()

    # If no file, go to REPL
    if not args.file:
        repl()

    # Otherwise, interpret file
    input_str = args.file.read()
    args.file.close()


if __name__ == '__main__':
    main()
