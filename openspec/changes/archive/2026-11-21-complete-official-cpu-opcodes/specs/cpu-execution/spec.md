# Spec Delta

## ADDED Requirements

### Requirement: Execute INC using absolute addressing

Opcode $EE SHALL decode a little-endian 16-bit operand and use it directly as the destination. Through Machine it SHALL
read the byte, write the original byte, and write (original + 1) modulo 256 to that address. It SHALL set N/Z from the
result, advance PC by three and add six nominal cycles.

#### Scenario: Decode the address in little-endian order

- **WHEN** operand bytes are $34 followed by $02
- **THEN** the destination is $0234, PC advances by three, and six cycles accrue

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $FF
- **THEN** the instruction reads it, writes $FF then $00 to that address, and sets N=0 and Z=1

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $7F
- **THEN** it ends at $80 with N=1 and Z=0

### Requirement: Execute DEC using absolute addressing

Opcode $CE SHALL decode a little-endian 16-bit operand and use it directly as the destination. Through Machine it SHALL
read the byte, write the original byte, and write (original - 1) modulo 256 to that address. It SHALL set N/Z from the
result, advance PC by three and add six nominal cycles.

#### Scenario: Decode the address in little-endian order

- **WHEN** operand bytes are $34 followed by $02
- **THEN** the destination is $0234, PC advances by three, and six cycles accrue

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $00
- **THEN** the instruction reads it, writes $00 then $FF to that address, and sets N=1 and Z=0

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $01
- **THEN** it ends at $00 with N=0 and Z=1

### Requirement: Execute INC using absolute,X addressing

Opcode $FE SHALL decode a little-endian 16-bit operand and use that address plus X modulo 65536 as the destination.
Through Machine it SHALL read the byte, write the original byte, and write (original + 1) modulo 256 to that address. It
SHALL set N/Z from the result, advance PC by three and add seven fixed nominal cycles.

#### Scenario: Index with and without a page crossing

- **WHEN** base=$02FC and X=$01 or $04
- **THEN** the destination is $02FD or $0300; both cost seven cycles and consume three instruction bytes

#### Scenario: Wrap the indexed destination

- **WHEN** base=$FFFF and X=$01
- **THEN** the read and writes access $0000 and the instruction still costs seven cycles

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $FF
- **THEN** the instruction reads it, writes $FF then $00 to that address, and sets N=0 and Z=1

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $7F
- **THEN** it ends at $80 with N=1 and Z=0

### Requirement: Execute DEC using absolute,X addressing

Opcode $DE SHALL decode a little-endian 16-bit operand and use that address plus X modulo 65536 as the destination.
Through Machine it SHALL read the byte, write the original byte, and write (original - 1) modulo 256 to that address. It
SHALL set N/Z from the result, advance PC by three and add seven fixed nominal cycles.

#### Scenario: Index with and without a page crossing

- **WHEN** base=$02FC and X=$01 or $04
- **THEN** the destination is $02FD or $0300; both cost seven cycles and consume three instruction bytes

#### Scenario: Wrap the indexed destination

- **WHEN** base=$FFFF and X=$01
- **THEN** the read and writes access $0000 and the instruction still costs seven cycles

#### Scenario: Write the old byte and then the wrapped result

- **WHEN** the destination initially contains $00
- **THEN** the instruction reads it, writes $00 then $FF to that address, and sets N=1 and Z=0

#### Scenario: Set flags from the resulting byte

- **WHEN** the destination initially contains $01
- **THEN** it ends at $00 with N=0 and Z=1

### Requirement: Execute ORA using indexed-indirect addressing

Opcode $01 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL store A OR operand in A and set N/Z from the result.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $35/$CA or $00/$00
- **THEN** A becomes $FF with N=1, Z=0 or $00 with N=0, Z=1, respectively

### Requirement: Execute AND using indexed-indirect addressing

Opcode $21 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL store A AND operand in A and set N/Z from the result.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $F0/$0F or $FF/$80
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute EOR using indexed-indirect addressing

Opcode $41 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL store A XOR operand in A and set N/Z from the result.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $FF/$FF or $7F/$FF
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute AND using indirect-indexed addressing

Opcode $31 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL store A AND operand in A and set N/Z from the result.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $F0/$0F or $FF/$80
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute ORA using indirect-indexed addressing

Opcode $11 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL store A OR operand in A and set N/Z from the result.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $35/$CA or $00/$00
- **THEN** A becomes $FF with N=1, Z=0 or $00 with N=0, Z=1, respectively

### Requirement: Execute EOR using indirect-indexed addressing

Opcode $51 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL store A XOR operand in A and set N/Z from the result.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** (A, addressed byte) is $FF/$FF or $7F/$FF
- **THEN** A becomes $00 with N=0, Z=1 or $80 with N=1, Z=0, respectively

### Requirement: Execute ADC using indexed-indirect addressing

Opcode $61 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL add A, the operand and incoming C in binary regardless of D, store the low byte in A,
and set N/Z from A, C for carry out, and V for signed overflow.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $7F/$00/1, $FF/$00/1, or $01/$01/0
- **THEN** A/C/V/N/Z become $80/0/1/1/0, $00/1/0/0/1, or $02/0/0/0/0, respectively, with no decimal correction

### Requirement: Execute ADC using indirect-indexed addressing

Opcode $71 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL add A, the operand and incoming C in binary regardless of D, store the low byte in
A, and set N/Z from A, C for carry out, and V for signed overflow.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $7F/$00/1, $FF/$00/1, or $01/$01/0
- **THEN** A/C/V/N/Z become $80/0/1/1/0, $00/1/0/0/1, or $02/0/0/0/0, respectively, with no decimal correction

### Requirement: Execute SBC using indexed-indirect addressing

Opcode $E1 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL subtract the operand and (1 - C) from A in binary regardless of D, store the low byte
in A, and set N/Z from A, C for no unsigned borrow, and V for signed overflow.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $80/$01/1, $00/$00/0, or $42/$42/1
- **THEN** A/C/V/N/Z become $7F/1/1/0/0, $FF/0/0/1/0, or $00/1/0/0/1, respectively, with no decimal correction

### Requirement: Execute SBC using indirect-indexed addressing

Opcode $F1 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL subtract the operand and (1 - C) from A in binary regardless of D, store the low
byte in A, and set N/Z from A, C for no unsigned borrow, and V for signed overflow.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** D is clear or set and A/operand/C are $80/$01/1, $00/$00/0, or $42/$42/1
- **THEN** A/C/V/N/Z become $7F/1/1/0/0, $FF/0/0/1/0, or $00/1/0/0/1, respectively, with no decimal correction

### Requirement: Execute CMP using indexed-indirect addressing

Opcode $C1 SHALL use a one-byte operand. It SHALL add X to the operand modulo 256, then read the little-endian pointer
from that zero-page address and its zero-page successor. It SHALL read the target byte through Machine, advance PC by
two and add six cycles. It SHALL leave A intact and set C if A is at least the operand unsigned, Z if equal, and N from
bit 7 of the wrapped difference.

#### Scenario: Wrap the indexed pointer

- **WHEN** the operand is $F0 and X=$20 with $34/$02 at $10/$11
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Wrap the pointer high-byte read

- **WHEN** the operand is $FC and X=$03 with $34/$02 at $FF/$00
- **THEN** the operand comes from $0234 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** A=$40 and the addressed byte is $41, $40, or $3F
- **THEN** C/Z/N are 0/0/1, 1/1/0, or 1/0/0 respectively and A remains $40.

### Requirement: Execute CMP using indirect-indexed addressing

Opcode $D1 SHALL use a one-byte operand. It SHALL read the little-endian pointer at the operand and its zero-page
successor, then add Y modulo 65536. It SHALL read the target byte through Machine, advance PC by two and add five cycles
plus one on page crossing. It SHALL leave A intact and set C if A is at least the operand unsigned, Z if equal, and N
from bit 7 of the wrapped difference.

#### Scenario: Index without crossing a page

- **WHEN** the pointer is $0230 and Y=$04
- **THEN** the operand comes from $0234 and five cycles accrue

#### Scenario: Wrap the pointer high byte and cross a page

- **WHEN** the operand is $FF, $FF/$00 contain $FF/$02, and Y=$01
- **THEN** the operand comes from $0300 and six cycles accrue

#### Scenario: Wrap the effective address

- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the operand comes from $0000 and six cycles accrue

#### Scenario: Use the addressed byte

- **WHEN** A=$40 and the addressed byte is $41, $40, or $3F
- **THEN** C/Z/N are 0/0/1, 1/1/0, or 1/0/0 respectively and A remains $40.

### Requirement: Execute PHA using implied addressing

Opcode $48 SHALL write A through Machine at $0100 | SP and then decrement SP modulo 256. It SHALL leave the status flags
unchanged, advance PC by one, and add three cycles.

#### Scenario: Save the accumulator at the pre-decrement position

- **WHEN** A=$80 and SP=$FD
- **THEN** $01FD receives $80, SP=$FC, PC advances by one, and three cycles accrue

#### Scenario: Wrap after pushing to the bottom of the stack page

- **WHEN** A=$00 and SP=$00
- **THEN** $0100 receives $00 and SP becomes $FF

### Requirement: Execute PLA using implied addressing

Opcode $68 SHALL increment SP modulo 256, load A from $0100 | SP through Machine, and set N/Z from A. It SHALL advance
PC by one and add four cycles.

#### Scenario: Load a negative value

- **WHEN** SP=$FC and $01FD holds $80
- **THEN** A=$80, N=1, Z=0, SP=$FD, PC advances by one, and four cycles accrue

#### Scenario: Pull zero using a wrapped stack pointer

- **WHEN** SP=$FF and $0100 holds $00
- **THEN** A=$00, N=0, Z=1, and SP becomes $00

### Requirement: Execute PHP using implied addressing

Opcode $08 SHALL write the status byte with bits 5 and 4 set through Machine at $0100 | SP, then decrement SP modulo
256. It SHALL leave the status fields unchanged, advance PC by one, and add three cycles.

#### Scenario: Force B in the saved byte without setting it in the CPU

- **WHEN** PHP executes with P=$A5 and SP=$FD
- **THEN** $01FD receives $B5, P stays $A5, SP=$FC, PC advances by one, and three cycles accrue

#### Scenario: Wrap the stack pointer after pushing

- **WHEN** SP=$00 and P=$7B
- **THEN** $0100 receives $7B and SP becomes $FF

### Requirement: Execute PLP using implied addressing

Opcode $28 SHALL increment SP modulo 256 and read the byte at $0100 | SP through Machine. It SHALL restore N/V/D/I/Z/C
from that byte, ignore bits 5 and 4, and preserve `break_flag`. It SHALL advance PC by one and add four cycles.

#### Scenario: Restore hardware flags on a wrapping pull

- **WHEN** PLP executes with SP=$FF, software B=1, and $CB at $0100
- **THEN** SP=$00, displayed P=$FB, PC advances by one, and four cycles accrue

#### Scenario: Ignore set B and bit 5 in the stack byte

- **WHEN** software B=0 and the pulled byte is $30
- **THEN** all six hardware flags are cleared and displayed P=$20

### Requirement: Execute BRK using implied addressing

Opcode $00 SHALL push the high byte then the low byte of the opcode address plus two, then the pre-instruction status
with bits 5 and 4 set. Each push writes through Machine at $0100 | SP and then decrements SP modulo 256. BRK SHALL set
I, read vector bytes $FFFE then $FFFF through Machine into PC in little-endian order, and add seven cycles. It SHALL
execute even when I is already set and leave the software B field unchanged.

#### Scenario: Save the resume address and old status

- **WHEN** BRK executes at $0234 with SP=$FD, I=0, P=$29, and $34/$C2 in the vector
- **THEN** $01FD/$01FC/$01FB receive $02/$36/$39, SP=$FA, I=1, PC=$C234, and seven cycles accrue

#### Scenario: Wrap the stack with interrupts masked

- **WHEN** BRK executes with SP=$00, I=1, and a known vector
- **THEN** the frame occupies $0100/$01FF/$01FE in push order, SP=$FD, and PC loads the vector

### Requirement: Execute RTI using implied addressing

Opcode $40 SHALL pull status, PC low, then PC high. Each pull increments SP modulo 256 before reading $0100 | SP through
Machine. RTI SHALL restore N/V/D/I/Z/C, ignore stack status bits 5 and 4 and preserve `break_flag`. It SHALL load PC
from the two address bytes without adjustment and add six cycles.

#### Scenario: Resume exactly at the stacked address

- **WHEN** SP=$FA, software B=0, and $BA/$34/$C2 are at $01FB-$01FD
- **THEN** SP=$FD, displayed P=$AA, PC=$C234, and six cycles accrue

#### Scenario: Pull across the end of the stack page

- **WHEN** SP=$FE, software B=1, and $01/$78/$56 are at $01FF/$0100/$0101
- **THEN** SP=$01, displayed P=$31, and PC=$5678
