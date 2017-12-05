"""Ben Weisz 2017 --- University of Toronto

   Emulator For SAP1 As Described By Malvino and Brown 1977."""

from typing import List
import sys

class Emu_Sap1:
    """Sap1 Emulator.

    === OP CODES ===
    LDA - 0000
    ADD - 0001
    SUB - 0010
    OUT - 1110
    HLT - 1111
    """

    # === Private Attributes ===
    # memory: The memory of the Sap1.
    # cycle_state: 6-bit word representing
    #              current cycle state.
    # program_counter: 4-bit word representing
    #                  the current program address in focus.
    # memory_address_register: 4-bit word representing the
    #                          memory address register.
    # instruction_register: 8-bit word representing the
    #                       instruction register.
    # a_register: 8-bit word representing the accumulator.
    # b_register: 8-bit word representing the b register.

    # === Representation Invariants ===
    # len(memory) == 16
    # 0 <= len(program_data) <= 16

    cycle_state: str

    memory: List[str]
    program_counter: str
    memory_address_register: str
    instruction_register: str
    a_register: str
    b_register: str

    def __init__(self, PROGRAM_PATH: str) -> None:
        """Initialize the Emu_Sap1."""

        # Memory Setup
        self.memory = []
        self._memory_clr()

        self._memory_load(PROGRAM_PATH)

        # Control Sequencer Setup
        self.cycle_state = '000001'

        # Program Counter Setup
        self.program_counter = '0000'

        # Memory Address Register Setup
        self.memory_address_register = '0000'

        # Instruction Register Setup
        self.instruction_register = '00000000'

        # Working Registers Setup
        self.a_register = '00000000'
        self.b_register = '00000000'

    def run(self) -> None:
        """Run Emu_Sap1 with the current memory."""

        HLT_FLAG = False

        while True:
            for cycle in range(6):
                if self.cycle_state == '000001':
                    # Address State
                    self.memory_address_register = self.program_counter

                elif self.cycle_state == '000010':
                    # Increment State
                    old_address = self._bin_to_dec(self.program_counter)

                    if old_address != 15:
                        self.program_counter = self._dec_to_binary(old_address + 1, 4)
                    else:
                        self.program_counter = self._dec_to_binary(0, 4)

                elif self.cycle_state == '000100':
                    # Fetch State
                    op = self._memory_fetch_by_address(self.memory_address_register)
                    self.instruction_register = op

                elif self.cycle_state == '001000':
                    # OP Exection State 1
                    if self.instruction_register[:4] == '0000':
                        # LDA
                        self.memory_address_register = self.instruction_register[4:]
                    elif self.instruction_register[:4] == '0001':
                        self.memory_address_register = self.instruction_register[4:]
                    elif self.instruction_register[:4] == '0010':
                        self.memory_address_register = self.instruction_register[4:]
                    elif self.instruction_register[:4] == '1110':
                        self._display(self.a_register)
                    elif self.instruction_register[:4] == '1111':
                        HLT_FLAG = True
                        break

                elif self.cycle_state == '010000':
                    # OP Execution State 2
                    if self.instruction_register[:4] == '0000':
                        value = self._memory_fetch_by_address(self.memory_address_register)
                        self.a_register = value
                    elif self.instruction_register[:4] == '0001':
                        value = self._memory_fetch_by_address(self.memory_address_register)
                        self.b_register = value
                    elif self.instruction_register[:4] == '0010':
                        value = self._memory_fetch_by_address(self.memory_address_register)
                        self.b_register = value
                    elif self.instruction_register[:4] == '1110':
                        pass

                elif self.cycle_state == '100000':
                    # Op Execution State 3
                    if self.instruction_register[:4] == '0000':
                        pass
                    elif self.instruction_register[:4] == '0001':
                        sum_word = self._alu(self.a_register, self.b_register, False)
                        self.a_register = sum_word
                    elif self.instruction_register[:4] == '0010':
                        sum_word = self._alu(self.a_register, self.b_register, True)
                        self.a_register = sum_word
                    elif self.instruction_register[:4] == '1110':
                        pass

                self._increment_cycle_state()

            if HLT_FLAG:
                break

        self._master_reset()

    def _display(self, word: str) -> None:
        """Display the <word> in decimal."""
        if word[0] == '1':
            print('-', end='')
            word = self._alu(word, '00000001', True)
            word = self._not_word(word)

        print(self._bin_to_dec(word), end='')

    def _alu(self, a: str, b: str, sub: bool) -> str:
        """Add <a> and <b>."""

        carry = 1 if sub else 0
        sum_reversed = ''

        if sub:
            b = self._not_word(b)

        for i in range(8):
            bit = 7 - i

            ones_count = []
            ones_count.extend([a[bit], b[bit], str(carry)])

            if ones_count.count('1') == 2 or ones_count.count('1') == 3:
                carry = 1
            else:
                carry = 0

            sum_reversed += str(ones_count.count('1') % 2)

        return sum_reversed[::-1]

    def _not_word(self, word: str) -> str:
        """NOT the binary word <word>."""
        out_word = ''
        for bit in range(len(word)):
            if word[bit] == '0':
                out_word += '1'
            else:
                out_word += '0'

        return out_word

    def _increment_cycle_state(self) -> None:
        """Increment the cycle state."""

        state = 0
        for t in range(6):
            if self.cycle_state[t] == '1':
                state = t

        if state != 0:
            state -= 1
            new_cycle = ('0' * state) + '1' + ('0' * (5 - state))

            self.cycle_state = new_cycle
        else:
            self.cycle_state = ('0' * 5) + '1'

    def _master_reset(self) -> None:
        """Reset the Emu_Sap1 to its original state.

        Note: Sap1 did not have the ability to modify
              its own program data, and thus it does not
              need to be reset."""

        # Control Sequencer Reset
        self.cycle_state = '000001'

        # Program Counter Reset
        self.program_counter = '0000'

        # Memory Address Register Reset
        self.memory_address_register = '0000'

        # Instruction Register Reset
        self.instruction_register = '00000000'

        # Working Registers Reset
        self.a_register = '00000000'
        self.b_register = '00000000'

    def _memory_fetch_by_address(self, address: str) -> str:
        """Fetch the 8-bit word which is
           stored at <address> in memory."""

        return self.memory[self._bin_to_dec(address)]

    def _memory_load(self, PROGRAM_PATH: str) -> None:
        """Load the Emu_Sap1 memory with the
           program data in <PROGRAM_PATH>"""
        with open(PROGRAM_PATH, 'r') as program_file:
            program_data = program_file.readlines()

            for op in range(min(16, len(program_data))):
                self.memory[op] = program_data[op].strip()

    def _memory_clr(self) -> None:
        """Clear the memory of the Emu_Sap1."""
        self.memory.clear()

        for adr in range(16):
            self.memory.append('00000000')

    def _bin_to_dec(self, bin: str) -> int:
        """Return the decimal represntation of <bin>."""
        bin = bin[::-1]
        dec = 0

        for bit in range(len(bin)):
            dec += int(bin[bit]) * 2**(bit)

        return dec

    def _dec_to_binary(self, dec: int, zeros: int) -> str:
        """Return the binary equivalent of the given
           decimal number with <zeros> zfill."""

        bit_list = []
        binary = ''

        while dec != 0:
            bit_list.append(dec % 2)
            dec = dec // 2

        for bit in bit_list[::-1]:
            binary += str(bit)

        return binary.zfill(zeros)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Incorrect Arguments.\nPlease Provide:\n\t1. <INPUT_FILE>.txt')
        exit()

    emu = Emu_Sap1(sys.argv[1])
    emu.run()
