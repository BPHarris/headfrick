"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from platform import platform

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Memory(list):
    """Class representing a Programs memory, subclass of list."""
    def strech(self, index):
        """Stretch the memory to contain the index, populating empty cells."""
        if index >= len(self):
            self += [0] * (index - len(self) + 1)

    def __getitem__(self, index):
        self.strech(index)  # On read from cell, strech memory if needed
        return super().__getitem__(index)
    
    def __setitem__(self, index, value):
        self.strech(index)  # On write to cell, strech memory if needed
        return super().__setitem__(index, value)
    
    def __repr__(self) -> str:
        return super().__repr__()[:-1] + ', ... ]'


class Machine:
    """Class representing brainfuck virtual machine."""
    CELL_MIN = 0        # Minimum cell value
    CELL_MAX = 255      # Maximum cell value

    INSTRUCTION_SET = set(['>', '<', '+', '-', '.', ',', '[', ']'])

    # TODO Fix issue where cell or 1 can't be decremented
    overflow  = lambda v: v if v <= Machine.CELL_MAX else Machine.CELL_MIN
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
    return (str(input('==> ')) + '\n')[0]


def repl() -> int:
    """Brainfuck REPL."""
    machine = Machine()
    instruction = 'initial'
    REPL_COMMANDS = set(['q', 'p', 'r'])

    while instruction:
        instruction = get_char()

        if instruction in Machine.INSTRUCTION_SET:
            machine.run_instruction(instruction)
        if instruction not in Machine.INSTRUCTION_SET | REPL_COMMANDS:
            print('Invalid instruction.')

        if instruction == 'q':      # q : quit repl
            break
        if instruction == 'p':      # p : print machine state
            print(machine)
        if instruction == 'r':      # r : reset machine
            machine = Machine()
    
    return EXIT_SUCCESS


def main() -> None:
    """Parse arguments; run REPL if no file, otherwise exec file."""
    parser = ArgumentParser(
        description='Interpret a brainfuck file. If no file is given, run the REPL.'
    )
    parser.add_argument(
        'file', nargs='?', type=FileType('r'), help='the brainfuck source code file'
    )

    args = parser.parse_args()

    if not args.file:
        exit(repl())

    Machine().run_program(args.file.read())
    args.file.close()


if __name__ == '__main__':
    main()
