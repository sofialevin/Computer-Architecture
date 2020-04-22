"""CPU functionality."""

import sys

program_filename = sys.argv[1]

class CPU:
    """Main CPU class."""

    HLT = 0b00000001
    LDI = 0b10000010
    PRN = 0b01000111

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.PC = 0

    def ram_read(self, address):

        return self.ram[address]

    def ram_write(self, address, value):

        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(program_filename) as program:
            for instruction in program:
                instruction = instruction.split('#')
                instruction = instruction[0].strip()
                if instruction == '':
                    continue
                    
                self.ram_write(address, int(instruction[:8], 2))
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            IR = self.PC
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            inst_len = ((self.ram_read(IR) & 0b11000000) >> 6) + 1

            if self.ram_read(IR) == self.HLT:
                running = False
                return
            elif self.ram_read(IR) == self.LDI:
                self.register[operand_a] = operand_b
                # self.PC += 3
            elif self.ram_read(IR) == self.PRN:
                print(self.register[operand_a])
                # self.PC += 2
            else:
                running = False
                print(f"Invalid instruction {IR}")

            self.PC += inst_len
                
cpu = CPU()
cpu.load()
cpu.run()