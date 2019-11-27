"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType


class Memory(list):
    """Class representing a Programs memory, subclass of list."""
    def stretch(self, index):
        """Stretch the memory to contain the index, populating empty cells."""
        if index >= len(self):
            self += [0] * (index - len(self) + 1)

    def __getitem__(self, index):
        self.stretch(index)  # On read from cell, stretch memory if needed
        return super().__getitem__(index)
    
    def __setitem__(self, index, value):
        self.stretch(index)  # On write to cell, stretch memory if needed
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
        for instruction in program:
            self.run_instruction(instruction)

    def run_instruction(self, instruction) -> None:
        """Run the given instruction on the machine."""
        if instruction == 'p':
            return

        if instruction == '>':
            self.pointer += 1
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
        # On print, stretch memory to show pointer movement
        self.memory.stretch(self.pointer)

        return str(self.memory) + '\n ' + self.pointer * '   ' + '^'


def get_char() -> str:
    """Return the first char in the input, takes no input to be a newline."""
    return (str(input('==> ')) + '\n')[0]


def repl(machine: Machine) -> None:
    """Brainfuck REPL."""
    REPL_COMMANDS = set(['q', 'p', 'r'])

    while True:
        instruction = str(input('==> '))

        if all([i in Machine.INSTRUCTION_SET | set('p') for i in instruction]):
            machine.run_program(instruction)
        if any(i not in Machine.INSTRUCTION_SET | REPL_COMMANDS for i in instruction):
            print('Invalid instruction.')
            continue

        if instruction == 'q':          # q : quit repl
            break
        if instruction.endswith('p'):   # p : print machine state
            print(machine)
        if instruction == 'r':          # r : reset machine
            machine = Machine()
    
    return None


def main() -> None:
    """Parse arguments; run REPL if no file, otherwise exec file."""
    parser = ArgumentParser(
        description='Interpret a brainfuck file. If no file is given, run the REPL.'
    )
    parser.add_argument(
        'file', nargs='?', type=FileType('r'), help='the brainfuck source code file'
    )
    parser.add_argument(
        '-d', '--dump', default=False, action='store_const', const=True,
        help='print the machine state on exit?'
    )

    args = parser.parse_args()

    machine = Machine()

    if not args.file:
        repl(machine)
    else:
        machine.run_program(args.file.read())
        args.file.close()

    if args.dump:
        print(machine)
    
    return None


if __name__ == '__main__':
    main()
