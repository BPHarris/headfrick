"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from platform import platform

# from readchar import readchar

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Memory(list):
    """Class representing a Programs memory, subclass of list."""
    def __getitem__(self, index):
        # On access, if cell has not been populated => populate cells upto it
        if index >= len(self):
            self += [0] * index - len(self) + 1

        return super().__getitem__(index)


class Machine:
    """Class representing brainfuck virtual machine."""
    CELL_MIN = 0        # Minimum cell value (inclusive)
    CELL_MAX = 256      # Maximum cell value (exclusive)

    overflow  = lambda value: value if value < CELL_MAX else CELL_MIN
    underflow = lambda value: value if value > CELL_MIN else CELL_MAX

    def __init__(self) -> None:
        """Create pointer and memory of running program."""
        self.pointer = 0
        self.memory = list()

    def run_program(self, program) -> None:
        """Run the given brainfuck program on this machine."""
        for instruction in instruction:
            self.run_instruction(instruction)

    def run_instruction(self, instruction) -> None:
        """Run the given instruction on the machine."""
        if instruction == '>':
            self.pointer += 1
        if instruction == '<':
            self.pointer = max(0, self.pointer - 1)

        if instruction == '+':
            self.memory[self.pointer] = overflow(self.memory[self.pointer] + 1)
        if instruction == '-':
            self.memory[self.pointer] = underflow(self.memory[self.pointer] - 1)

        if instruction == '.':
            print(chr(self.memory[self.pointer]))
        if instruction == ',':
            self.memory[self.pointer] = ord(stdin.read(1))

        if instruction == '[':
            return
        if instruction == ']':
            return
    
    def __repr__(self):
        """Return string representation."""
        return self.memory.__repr__()


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


def repl() -> int:
    """Brainfuck REPL."""
    machine = Machine()
    instruction = 'initial'

    while instruction:
        instruction = str(input('==> '))[0]

        if instruction == 'q':
            break
        if instruction == 'p':
            print(machine)
            continue
        if instruction == 'r':
            machine = Machine()
            continue

        if instruction not in ('>', '<', '+', '-', '.', ',', '[', ']'):
            print('Invalid instruction.')
            continue
        machine.run_instruction(instruction)
    
    return EXIT_SUCCESS


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
        exit(repl())

    instructions = args.file.read()
    args.file.close()

    Machine().run_program(instructions)


if __name__ == '__main__':
    main()
