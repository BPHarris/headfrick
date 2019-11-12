"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from platform import platform


class Memory(list):
    """Class representing a Programs memory, subclass of list."""
    def __getitem__(self, index):
        # On access, if cell has not been populated => populate cells upto it
        if index >= len(self):
            self += [0] * index - len(self) + 1

        return super().__getitem__(index)


class Program:
    """Class representing a program in execution."""
    CELL_MIN = 0        # Minimum cell value (inclusive)
    CELL_MAX = 256      # Maximum cell value (exclusive)

    overflow  = lambda value: value if value < CELL_MAX else CELL_MIN
    underflow = lambda value: value if value > CELL_MIN else CELL_MAX

    def __init__(self) -> None:
        """Create pointer and memory of running program."""
        self.pointer = 0
        self.memory = list()

    def run(self, instructions) -> None:
        """Run the brainfuck program."""
        for instruction in instruction:
            self.run_instruction(instruction)

    def run_instruction(self, instruction) -> None:
        """Run the given instruction on the program."""
        if instruction == '>':
            self.__increment_pointer()
        if instruction == '<':
            self.__decrement_pointer()
        if instruction == '+':
            self.__increment_cell()
        if instruction == '-':
            self.__decrement_cell()
        if instruction == '.':
            self.__output_cell()
        if instruction == ',':
            self.__input_cell()
        if instruction == '[':
            self.__jump_forwards()
        if instruction == ']':
            self.__jump_backwards()

    def __increment_pointer():
        """Brainfuck increment pointer instruction."""
        self.pointer += 1

    def __decrement_pointer():
        """Brainfuck decrement pointer instruction."""
        self.pointer = max(0, self.pointer - 1)

    def __increment_cell():
        """Brainfuck increment cell instruction."""
        self.memory[self.pointer] = overflow(self.memory[self.pointer] + 1)

    def __decrement_cell():
        """Brainfuck decrement cell instruction."""
        self.memory[self.pointer] = underflow(self.memory[self.pointer] - 1)

    def __output_cell():
        """Brainfuck output cell instruction, output current cell as ASCII."""
        print(chr(self.memory[self.pointer]))

    def __input_cell():
        """Brainfuck input cell instruction, read input into current cell."""
        self.memory[self.pointer] = ord(stdin.read(1))

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
