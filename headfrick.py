"""headfrick.py - A simple brainfuck interpreter."""

from argparse import ArgumentParser, FileType


class Memory(list):
    """
    Class representing a Machine's memory, subclass of list. Memory is lazy
    and arbitrary length.
    """

    def stretch(self, index):
        """Stretch the memory to contain the index, populating empty cells."""
        if index >= len(self):
            self += [0] * (index - len(self) + 1)

    def __getitem__(self, index: int) -> int:
        # On read from cell, stretch memory if needed
        self.stretch(index)

        return super().__getitem__(index)

    def __setitem__(self, index: int, value: int) -> int:
        # On write to cell, stretch memory if needed
        self.stretch(index)

        return super().__setitem__(index, value)

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + ', ... ]'


class Machine:
    """Class representing brainfuck/headfrick virtual machine."""
    CELL_MIN = 0        # Minimum cell value
    CELL_MAX = 255      # Maximum cell value

    INSTRUCTION_SET = set(['>', '<', '+', '-', '.', ',', '[', ']'])

    def __init__(self) -> None:
        """Create pointer and memory."""
        self.pointer = 0
        self.memory = Memory([0])

    def run_program(self, program: str) -> None:
        """Run the given brainfuck program on this machine."""
        instruction_pointer = 0

        while instruction_pointer < len(program):
            instruction = program[instruction_pointer]

            if instruction == '>':
                self.pointer += 1
            if instruction == '<':
                self.pointer = max(0, self.pointer - 1)

            if instruction == '+':
                self.set_current(self.memory[self.pointer] + 1)
            if instruction == '-':
                self.set_current(self.memory[self.pointer] - 1)

            if instruction == '.':
                print(chr(self.memory[self.pointer]))
            if instruction == ',':
                self.set_current(ord(get_char()))
            
            if instruction == '[':
                # Read to closing-]
                stack = list('[')
                internal_instructions = str()
                closing_instruction = instruction_pointer

                while stack:
                    instruction_pointer += 1

                    if program[instruction_pointer] == '[':
                        stack.append('[')
                    if program[instruction_pointer] == ']':
                        stack.pop()
                        closing_instruction = instruction_pointer
                    
                    internal_instructions += program[instruction_pointer]
                
                # Remove closing-]
                internal_instructions = internal_instructions[:-1]

                while self.memory[self.pointer] != Machine.CELL_MIN:
                    self.run_program(internal_instructions)

                instruction_pointer = closing_instruction
            if instruction == ']':
                raise SyntaxError("Invalid instruction '{}'.".format(instruction))

            # Increment instruction pointer
            instruction_pointer += 1

    def set_current(self, value: int) -> None:
        """Set the value at the current pointer location."""
        self.memory[self.pointer] = value % (Machine.CELL_MAX + 1)

    def __repr__(self) -> str:
        """Return string representation."""
        # On print, stretch memory to show pointer movement
        self.memory.stretch(self.pointer)

        # TODO: Fix tracking when numbers > 1 digit
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
