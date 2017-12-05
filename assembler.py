"""Ben Weisz 2017 --- University of Toronto"""

from typing import List
import sys

OP_CODES = {'LDA': '0000', 'ADD': '0001', 'SUB': '0010', 'OUT': '1110', 'HLT': '1111', 'SET': ''}

class Assembler_Sap1:
    """SAP1 Assembler."""

    def __init__(self, PROGRAM_PATH: str, OUTPUT_PATH: str) -> None:
        """Initialize the SAP1 Assembler."""
        src = self._load_asm(PROGRAM_PATH)
        ops = self._parse_asm(src)

        with open(OUTPUT_PATH, 'w') as bin_output:
            for op in ops:
                bin_output.write(op + '\n')

    def _parse_asm(self, src: List[str]) -> List[str]:
        """Return the opcodes of <src>."""
        ops = []
        for op in range(16):
            ops.append('0' * 8)

        next_empty = 0

        for line in src:
            tokens = line.split(' ')

            if tokens[0] not in OP_CODES:
                raise NoSuchOperation

            binary = OP_CODES[tokens[0]]
            SET = False

            if tokens[0] == 'LDA':
                dec = self._hex_to_dec(tokens[1][2:])
                binary += self._dec_to_binary(dec, 4)
            elif tokens[0] == 'ADD':
                dec = self._hex_to_dec(tokens[1][2:])
                binary += self._dec_to_binary(dec, 4)
            elif tokens[0] == 'SUB':
                dec = self._hex_to_dec(tokens[1][2:])
                binary += self._dec_to_binary(dec, 4)
            elif tokens[0] == 'OUT':
                binary += '0000'
            elif tokens[0] == 'HLT':
                binary += '0000'
            elif tokens[0] == 'SET':
                adr = self._hex_to_dec(tokens[1][2:])

                dec = self._hex_to_dec(tokens[2][2:])
                data = self._dec_to_binary(dec, 8)

                ops[adr] = data
                SET = True

            if not SET:
                ops[next_empty] = binary
                next_empty += 1

        return ops

    def _load_asm(self, PROGRAM_PATH: str) -> List[str]:
        """Load the assembly code and return
           it as a list of its lines."""
        src = []

        with open(PROGRAM_PATH, 'r') as program_file:
            program_data = []

            for line in program_file.readlines():
                if line != '\n' and line[0] != ';':
                    program_data.append(line)

            for line in range(min(16, len(program_data))):
                src.append(program_data[line].strip())

        return src

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

    def _hex_to_dec(self, hexid: str) -> int:
        """Return the decimal equivalent of <hex>."""
        hex_values = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

        hexid = hexid[::-1]
        dec = 0

        for nibble in range(len(hexid)):
            dec += hex_values[hexid[nibble]] * (16**nibble)

        return dec


class NoSuchOperation:
    """Raised when there is no such operation."""

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Incorrect Arguments.\nPlease Provide:\n\t1. <INPUT_FILE>.txt\n\t2. <OUTPUT_FILE>.txt')
        exit()

    asm = Assembler_Sap1(sys.argv[1], sys.argv[2])
