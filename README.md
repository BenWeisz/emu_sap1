# SAP1 Emulator and Assembler

---

***Requirements***
---
- Python 3

***About SAP1***
---
The __SAP1__ is the first CPU outlined in __Albert Paul Malvino__ and __Jerald A. Brown's__ book __***Digital Computer Electronic***__.
Simple in its design, the __SAP1__ has 5 operation types with 1 extra being added to the SAP1 assembly language to assign values. 

| Operation Type     | SAP Assembly  | OP Code    |
|:------------------:|:-------------:|:----------:|
| __Load__ value from 0x\<adr> to register A | LDA 0x\<adr>  | 0000\<adr> |
| __Add__ value from 0x\<adr> to register A | ADD 0x\<adr>  | 0001\<adr> |
| __Subtract__ value at 0x\<adr> from register A | SUB 0x\<adr>  | 0010\<adr> |
| __Output__ the value in register A | OUT | 1110XXXX |
| __Halt__ the program | HLT | 1111XXXX |
| __Set__ the value of 0x\<adr> to 0x\<val> __(Assembler Only)__ | SET 0x\<adr> 0x\<val> | N/A |

__***Note***__: 
1. \<adr> is a 4-bit word with no prefix (either in hexidecimal or binary).
2. Use '; \<comment>'.

__***Specs***__:
- 16 bytes of memory
- 1 loadable register 
- Decimal output

***Usage***
---
1. __Write__ your assmebly code in a text file.
2. __Save__ the text file as \<INPUT_FILE>.txt
3. __Choose__ an output file name, in general: \<OUTPUT_FILE>.txt
4. __Run__ the following code in CMD, Terminal or any equivalent:
<br/></br>
  ```py assembler.py <INPUT_FILE>.txt <OUTPUT_FILE>.txt```
<br/></br>
5. __Run__ the following to run your program:
<br/></br>
  ```py emu.py <OUTPUT_FILE>.txt```
