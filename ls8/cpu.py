"""CPU functionality."""

import sys

program_filename = sys.argv[1]

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.PC = 0
        self.SP = 7
        self.FL = 0b00000000
        self.reg[self.SP] = 0xF3
        self.running = False
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP

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
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b100
                #set the Equal E flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b10
                # set the Less-than L flag to 1, otherwise set it to 0.
            else:
                self.FL = 0b1
                # set the Greater-than G flag to 1, otherwise set it to 0.

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

    def handle_HLT(self, operand_a, operand_b):
        self.running = False

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
    
    def handle_CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)

    def handle_ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def handle_POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram[self.reg[self.SP]]

        self.reg[self.SP] += 1

    def handle_PUSH(self, operand_a, operand_b):
        self.reg[self.SP] -= 1

        self.ram[self.reg[self.SP]] = self.reg[operand_a]

    def handle_CALL(self, operand_a, operand_b):
        return_addr = self.PC + 2

        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = return_addr

        reg_num = self.ram[self.PC + 1]
        dest_addr = self.reg[reg_num]

        self.PC = dest_addr

    def handle_RET(self, operand_a, operand_b):
        return_addr = self.ram[self.reg[self.PC + 1]]

        self.PC = return_addr
    
    def handle_JMP(self, operand_a, operand_b):
        return_addr = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

        self.PC = return_addr

    def run(self):
        """Run the CPU."""

        self.running = True

        while self.running:
            IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            inst_len = ((IR & 0b11000000) >> 6) + 1
            sets_pc = (IR & 0b10000) >> 4

            try:
                self.branchtable[IR](operand_a, operand_b)
            except:
                print(f"Invalid instruction {IR}")
                sys.exit()

            if sets_pc != 1:
                self.PC += inst_len
                
cpu = CPU()
cpu.load()
cpu.run()