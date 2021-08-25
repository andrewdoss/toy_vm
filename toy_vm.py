"""
This module implements a toy VM as an exercise for the Bradfield CS Architecture Course.
"""

class ToyVM:
    def __init__(self, program=None, word_max=(2**16 - 1)):
        if program:
            self.load_program(program)
        else:
            # Default to program with immediate halt
            self.memory = bytearray([0xff]) + bytearray([0] * 19)
        self.regs = [0] * 3
        self.word_max = word_max
        
    def encode_word(self, num):
        """Encodes an int into a little-endian word."""
        return bytearray([num % 256, num // 256])

    def decode_word(self, word):
        """Decodes a litte-endian word into an int."""
        return word[0] + word[1] * 256

    def load_program(self, program):
        """Loads a program into main memory."""
        if len(program) != 20:
            raise ValueError('Program length must be 20 bytes.')
        self.memory = bytearray(program)

    def load_word(self, reg, addr):
        """Load a word from main memory into a register."""
        self.regs[reg] = self.decode_word(self.memory[addr:addr+2])
    
    def store_word(self, reg, addr):
        """Store a word in a register into main memory."""
        self.memory[addr:addr+2] = self.encode_word(self.regs[reg])

    def add(self):
        """Primitive ALU add operation."""
        if self.regs[1] + self.regs[2] > self.word_max:
            raise OverflowError('Add exceeded system word size.')
        else:
            self.regs[1] = self.regs[1] + self.regs[2]

    def sub(self):
        """Primitive ALU subtract operation."""
        if self.regs[1] - self.regs[2] < 0:
            raise ValueError('Invalid inputs for unsigned subtract output.')
        else:
            self.regs[1] = self.regs[1] - self.regs[2]

    def run(self):
        """Executes the specified program."""
        while True:
            # Fetch instruction
            instruction = self.memory[self.regs[0]]

            # Decode and execute instruction
            if instruction == 0x01:
                self.load_word(self.memory[self.regs[0]+1],
                               self.memory[self.regs[0]+2])
            elif instruction == 0x02:
                self.store_word(self.memory[self.regs[0]+1],
                               self.memory[self.regs[0]+2])
            elif instruction == 0x03:
                self.add()
            elif instruction == 0x04:
                self.sub()
            elif instruction == 0xff:
                break
            else:
                raise ValueError(f'Program contains invalid instruction' 
                                 f'{hex(instruction)} at address'
                                 f'{hex(self.regs[0])}.')
            # Increment program counter
            self.regs[0] += 3

        return self

if __name__ == "__main__":
    # Provided addition example: 5281 + 12 = 5293
    test_program_1 = ([0x01, 0x01, 0x10,
                       0x01, 0x02, 0x12,
                       0x03, 0x01, 0x02,
                       0x02, 0x01, 0x0e,
                       0xff,
                       0x00,
                       0x00, 0x00,
                       0xa1, 0x14,
                       0x0c, 0x00], 5293)

    # Construct VM and run
    toy_vm = ToyVM(test_program_1[0]).run()
    assert toy_vm.decode_word(toy_vm.memory[14:16]) == test_program_1[1], 'Test program 1 failed.'

    # Subtraction example: 8746 - 2020 = 6726
    test_program_2 = ([0x01, 0x01, 0x10,
                       0x01, 0x02, 0x12,
                       0x04, 0x01, 0x02,
                       0x02, 0x01, 0x0e,
                       0xff,
                       0x00,
                       0x00, 0x00,
                       0x2a, 0x22,
                       0xe4, 0x07], 6726)

    # Construct VM and run
    toy_vm = ToyVM(test_program_2[0]).run()
    assert toy_vm.decode_word(toy_vm.memory[14:16]) == test_program_2[1], 'Test program 2 failed.'


