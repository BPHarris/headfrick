"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from platform import platform


class Program:
    """"""

    def __init__(self) -> None:
        """Create pointer and memory of running program."""
        self.pointer = 0
        self.memory = list()

    def run(self, instructions) -> None:
        """Run the brainfuck program."""
        pass

    def __increment_pointer():
        """Brainfuck increment pointer instruction."""
        pass

    def __decrement_pointer():
        """Brainfuck decrement pointer instruction."""
        pass

    def __increment_cell():
        """Brainfuck increment cell instruction."""
        pass

    def __decrement_cell():
        """Brainfuck decrement cell instruction."""
        pass

    def __output_cell():
        """Brainfuck output cell instruction, output current cell as ASCII."""
        pass

    def __input_cell():
        """Brainfuck input cell instruction, read input into current cell."""
        pass

    def __jump_forwards():
        """Brainfuck jump forwards intruction."""
        pass

    def __jump_backwards():
        """Brainfuck jump forwards intruction."""
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

    if not args.file:
        repl()

    instructions = args.file.read()
    args.file.close()

    Program().run(instructions)


if __name__ == '__main__':
    main()
