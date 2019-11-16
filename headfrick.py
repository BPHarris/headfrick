"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from platform import platform

# from readchar import readchar

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Memory(list):
    """Class representing a Programs memory, subclass of list."""
    def strech(self, index):
        """Stratch the memory to contain the index."""
        if index >= len(self):
            self += [0] * (index - len(self) + 1)

    def __getitem__(self, index):
        # On access, if cell has not been populated => populate cells upto it
        self.strech(index)

        return super().__getitem__(index)
    
    def __setitem__(self, index, value):
        # On access, if cell has not been populated => populate cells upto it
        self.strech(index)

        return super().__setitem__(index, value)
    
    def __repr__(self) -> str:
        return super().__repr__()[:-1] + ', ... ]'


class Machine:
    """Class representing brainfuck virtual machine."""
    CELL_MIN = 0        # Minimum cell value (inclusive)
    CELL_MAX = 256      # Maximum cell value (exclusive)

    overflow  = lambda v: v if v <  Machine.CELL_MAX else Machine.CELL_MIN
    underflow = lambda v: v if v >= Machine.CELL_MIN else Machine.CELL_MAX

    def __init__(self) -> None:
        """Create pointer and memory of running program."""
        self.pointer = 0
        self.memory = Memory([0])

    def run_program(self, program) -> None:
        """Run the given brainfuck program on this machine."""
        for instruction in instruction:
            self.run_instruction(instruction)

    def run_instruction(self, instruction) -> None:
        """Run the given instruction on the machine."""
        if instruction == '>':
            self.pointer += 1
            self.memory.strech(self.pointer)
        if instruction == '<':
            self.pointer = max(0, self.pointer - 1)

        if instruction == '+':
            self.current(self.current() + 1)
        if instruction == '-':
            self.current(self.current() - 1)

        if instruction == '.':
            print(chr(self.current()))
        if instruction == ',':
            self.current(ord(get_char()))

        if instruction == '[':
            return
        if instruction == ']':
            return
    
    def __jump_forwards(self):
        """Brainfuck jump forwards instruction."""
        pass

    def __jump_backwards(self):
        """Brainfuck jump backwards instruction."""
        pass

    def current(self, value=None):
        """Return the value at the pointer."""
        if value:
            return self.__set_current(value)
        return self.memory[self.pointer]
    
    def __set_current(self, value):
        """Set the value at the pointer."""
        self.memory[self.pointer] = Machine.overflow(Machine.underflow(value))

    def __repr__(self) -> str:
        """Return string representation."""
        return self.memory.__repr__()


def get_char() -> str:
    """Return the first char in the input."""
    return str(input('==> '))[0]


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
        instruction = get_char()

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
