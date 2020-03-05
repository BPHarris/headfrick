"""headfrick.py -- A simple brainfuck interpreter.

Interpret a brainfuck file. If no file is given, run the REPL.

Usage:  headfrick.py [[-d] FILE | -h | -v]

-h, --help      show this message
-d, --dump      print the machine state on exit
-v, --version   display the interpreter version

"""

from typing import Dict
from docopt import docopt
from os.path import isfile


__version__ = '0.1.1a'


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
        # TODO Add option for printing in binary
        # TODO Print first three, currently pointed to +/- 1, and last three
        return '[' + ', '.join(f'{i:03}' for i in self) + ']'


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
        self.memory.stretch(self.pointer)   # stretch to show pointer movement
        return str(self.memory) + '\n ' + self.pointer * '     ' + '^'


def get_char() -> str:
    """Return the first char in the input, takes no input to be a newline."""
    return (str(input('==> ')) + '\n')[0]


def repl(machine: Machine) -> Machine:
    """Brainfuck REPL."""
    REPL_COMMANDS = set(['q', 'p', 'r'])

    while True:
        instruction = str(input('==> '))

        if all(i in Machine.INSTRUCTION_SET | set('p') for i in instruction):
            machine.run_program(instruction)
        if any(i not in Machine.INSTRUCTION_SET | REPL_COMMANDS for i in instruction):
            print('Invalid instruction.')
            continue

        if 'p' in instruction[:-1]:
            print('Print command only valid at the end of an instruction.')
            continue

        if instruction == 'q':          # q : quit repl
            break
        if instruction.endswith('p'):   # p : print machine state
            print(machine)
        if instruction == 'r':          # r : reset machine
            machine = Machine()
    
    return machine


def main(args: Dict) -> None:
    """Interpreter entry point."""
    machine = Machine()

    if args['--version']:
        print(f'headfrick.py: version {__version__}')
        quit()

    if not args['FILE']:
        print(repl(machine))
        quit()

    if not isfile(args['FILE']):
        print(f'headfrick.py: {args["FILE"]} does not exist')
        quit()

    with open(args['FILE']) as file:
        machine.run_program(file.read())

    if args['--dump']:
        print(machine)


if __name__ == '__main__':
    main(docopt(__doc__))
