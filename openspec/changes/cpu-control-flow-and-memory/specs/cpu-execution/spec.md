## ADDED Requirements

### Requirement: Execute AND with an immediate operand

Opcode $29 SHALL combine A with the next byte using bitwise AND, store the result in A, and set N and Z from that
byte. It SHALL advance PC by two and add two nominal cycles, preserving other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$F0 and AND #$0F executes
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Set the negative flag
- **WHEN** A=$FF and AND #$80 executes
- **THEN** A=$80, N=1, and Z=0

### Requirement: Execute ORA with an immediate operand

Opcode $09 SHALL combine A with the next byte using bitwise OR, store the result in A, and set N and Z from that
byte. It SHALL advance PC by two and add two nominal cycles, preserving other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$00 and ORA #$00 executes
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Combine distinct bits
- **WHEN** A=$10 and ORA #$80 executes
- **THEN** A=$90, N=1, and Z=0

### Requirement: Execute EOR with an immediate operand

Opcode $49 SHALL combine A with the next byte using bitwise exclusive OR, store the result in A, and set N and Z from
that byte. It SHALL advance PC by two and add two nominal cycles, preserving other registers and flags.

#### Scenario: Produce zero
- **WHEN** A=$FF and EOR #$FF executes
- **THEN** A=$00, N=0, and Z=1

#### Scenario: Toggle matching bits
- **WHEN** A=$0F and EOR #$8F executes
- **THEN** A=$80, N=1, and Z=0

### Requirement: Execute STA using indexed-indirect addressing

Opcode $81 SHALL add X to its one-byte operand modulo 256, read the little-endian target pointer from that zero-page
address and the following zero-page address modulo 256, and write A through Machine to the target. It SHALL advance
PC by two, add six nominal cycles, and preserve other registers and flags.

#### Scenario: Wrap the indexed pointer address
- **WHEN** the operand is $F0, X=$20, and $10/$11 contain $34/$12
- **THEN** the write targets $1234 through Machine

#### Scenario: Wrap the pointer's high-byte address
- **WHEN** the operand is $FC, X=$03, and $FF/$00 contain $34/$12
- **THEN** the write targets $1234 through Machine

### Requirement: Execute STA using indirect-indexed addressing

Opcode $91 SHALL read a little-endian target pointer from the one-byte operand's zero-page address and the following
zero-page address modulo 256, add Y to the pointer modulo 65536, and write A through Machine to the result. It SHALL
advance PC by two, add six nominal cycles regardless of page crossing, and preserve other registers and flags.

#### Scenario: Wrap the pointer and cross a page
- **WHEN** the operand is $FF, $FF/$00 contain $FF/$12, and Y=$01
- **THEN** the write targets $1300 through Machine

#### Scenario: Wrap the effective address
- **WHEN** the pointer is $FFFF and Y=$01
- **THEN** the write targets $0000 through Machine

#### Scenario: Index without crossing a page
- **WHEN** the pointer is $1230 and Y=$04
- **THEN** the write targets $1234 through Machine and adds six nominal cycles

### Requirement: Execute ASL on the accumulator

Opcode $0A SHALL shift A left by one bit, set C from the old bit 7, insert zero into bit 0, and set N and Z from the
eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Shift out the high bit
- **WHEN** A=$80 and ASL executes
- **THEN** A=$00, C=1, Z=1, and N=0

#### Scenario: Set the negative flag
- **WHEN** A=$40 and ASL executes
- **THEN** A=$80, C=0, Z=0, and N=1

### Requirement: Execute LSR on the accumulator

Opcode $4A SHALL shift A right by one bit, set C from the old bit 0, insert zero into bit 7, and set N and Z from the
eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Shift out the low bit
- **WHEN** A=$01 and LSR executes
- **THEN** A=$00, C=1, Z=1, and N=0

#### Scenario: Shift the high bit
- **WHEN** A=$80 and LSR executes
- **THEN** A=$40, C=0, Z=0, and N=0

### Requirement: Execute ROL on the accumulator

Opcode $2A SHALL shift A left by one bit, set C from the old bit 7, insert the old C into bit 0, and set N and Z from
the eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Rotate through a set carry
- **WHEN** A=$80, C=1, and ROL executes
- **THEN** A=$01, C=1, Z=0, and N=0

#### Scenario: Rotate with a clear carry
- **WHEN** A=$40, C=0, and ROL executes
- **THEN** A=$80, C=0, Z=0, and N=1

### Requirement: Execute ROR on the accumulator

Opcode $6A SHALL shift A right by one bit, set C from the old bit 0, insert the old C into bit 7, and set N and Z from
the eight-bit result. It SHALL advance PC by one and add two nominal cycles, preserving the other registers and flags.

#### Scenario: Rotate through a set carry
- **WHEN** A=$01, C=1, and ROR executes
- **THEN** A=$80, C=1, Z=0, and N=1

#### Scenario: Rotate with a clear carry
- **WHEN** A=$02, C=0, and ROR executes
- **THEN** A=$01, C=0, Z=0, and N=0

### Requirement: Execute CMP with an immediate operand

Opcode $C9 SHALL compare A with the next byte, set C if A is unsigned greater than or equal to the operand, set Z on
equality, and set N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add two nominal cycles,
preserving all registers other than PC and flags other than N/Z/C.

#### Scenario: Compare equal values
- **WHEN** A=$42 and CMP #$42 executes
- **THEN** C=1, Z=1, and N=0

#### Scenario: Compare unequal values
- **WHEN** A=$00 with operand $01, or A=$80 with operand $01, is compared
- **THEN** N/Z/C are respectively 1/0/0 and 0/0/1

### Requirement: Execute CPX with an immediate operand

Opcode $E0 SHALL compare X with the next byte, set C if X is unsigned greater than or equal to the operand, set Z on
equality, and set N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add two nominal cycles,
preserving all registers other than PC and flags other than N/Z/C.

#### Scenario: Compare equal values
- **WHEN** X=$42 and CPX #$42 executes
- **THEN** C=1, Z=1, and N=0

#### Scenario: Compare unequal values
- **WHEN** X=$00 with operand $01, or X=$80 with operand $01, is compared
- **THEN** N/Z/C are respectively 1/0/0 and 0/0/1

### Requirement: Execute CPY with an immediate operand

Opcode $C0 SHALL compare Y with the next byte, set C if Y is unsigned greater than or equal to the operand, set Z on
equality, and set N from bit 7 of the eight-bit difference. It SHALL advance PC by two and add two nominal cycles,
preserving all registers other than PC and flags other than N/Z/C.

#### Scenario: Compare equal values
- **WHEN** Y=$42 and CPY #$42 executes
- **THEN** C=1, Z=1, and N=0

#### Scenario: Compare unequal values
- **WHEN** Y=$00 with operand $01, or Y=$80 with operand $01, is compared
- **THEN** N/Z/C are respectively 1/0/0 and 0/0/1

### Requirement: Execute JMP using absolute addressing

Opcode $4C SHALL load PC from its little-endian two-byte operand and add three cycles. All other registers, flags, and
memory SHALL remain unchanged.

#### Scenario: Jump to an asymmetric address
- **WHEN** $4C $34 $12 executes at $0000
- **THEN** PC becomes $1234, cycles increase by three

#### Scenario: Wrap an operand fetch
- **WHEN** opcode and operand bytes straddle $FFFF and $0000 in synthetic connected memory
- **THEN** operand fetch wraps at 16 bits and PC becomes the decoded target

### Requirement: Execute JMP using indirect addressing

Opcode $6C SHALL read a little-endian pointer from its operand and load PC from the two pointed-to bytes. The
high-byte read SHALL wrap within the pointer page. It SHALL add five cycles, preserve all other CPU registers and
flags, and perform no memory writes.

#### Scenario: Resolve a pointer
- **WHEN** JMP ($1234) reads $78 at $1234 and $56 at $1235 through connected memory
- **THEN** PC becomes $5678, five cycles accrue

#### Scenario: Emulate page-boundary behavior
- **WHEN** JMP ($12FF) reads $78 at $12FF and $56 at $1200
- **THEN** PC becomes $5678 and the high byte is not read from $1300

### Requirement: Execute JSR using absolute addressing

Opcode $20 SHALL call the little-endian absolute target, pushing the address of its last operand byte high byte first
to $0100+SP, decrementing SP modulo 256 after each write. It SHALL add six cycles and preserve A/X/Y and all flags.

#### Scenario: Push the return address and call
- **WHEN** JSR $1234 at $8000 executes with SP=$FD
- **THEN** $80 is written to $01FD, $02 to $01FC, SP becomes $FB, PC becomes $1234, and six cycles accrue

#### Scenario: Wrap the stack pointer
- **WHEN** JSR executes with SP=$00
- **THEN** its high and low return bytes are written to $0100 and $01FF in that order and SP becomes $FE

#### Scenario: Fetch the high operand after stack writes
- **WHEN** the high operand aliases a stack destination in connected RAM
- **THEN** the high target byte is read after both writes

### Requirement: Execute RTS using implied addressing

Opcode $60 SHALL increment SP and read the low return byte at $0100+SP, then increment SP and read its high byte. It
SHALL set PC to that word plus one modulo 65536, add six cycles, and preserve A/X/Y, flags, and memory.

#### Scenario: Return using stack bytes
- **WHEN** RTS executes with SP=$FB, $02 at $01FC, and $80 at $01FD
- **THEN** SP becomes $FD, PC becomes $8003, and six cycles accrue

#### Scenario: Wrap stack and return address
- **WHEN** SP=$FE and $FF is stored at both $01FF and $0100
- **THEN** RTS reads low then high through connected memory, leaves SP=$00, and sets PC=$0000

### Requirement: Execute STA using zero page addressing

Opcode $85 SHALL use the zero-extended one-byte operand to write A to memory and preserve all flags. It SHALL advance
PC by two bytes modulo 65536, add three cycles, and preserve all registers other than PC.

#### Scenario: Access the selected address
- **WHEN** STA zero page ($85) executes and the operand is $FF
- **THEN** it writes to $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

### Requirement: Execute STX using zero page addressing

Opcode $86 SHALL use the zero-extended one-byte operand to write X to memory and preserve all flags. It SHALL advance
PC by two bytes modulo 65536, add three cycles, and preserve all registers other than PC.

#### Scenario: Access the selected address
- **WHEN** STX zero page ($86) executes and the operand is $FF
- **THEN** it writes to $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

### Requirement: Execute STY using zero page addressing

Opcode $84 SHALL use the zero-extended one-byte operand to write Y to memory and preserve all flags. It SHALL advance
PC by two bytes modulo 65536, add three cycles, and preserve all registers other than PC.

#### Scenario: Access the selected address
- **WHEN** STY zero page ($84) executes and the operand is $FF
- **THEN** it writes to $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

### Requirement: Execute LDA using zero page addressing

Opcode $A5 SHALL use the zero-extended one-byte operand to read the byte into A, set N from bit 7, and set Z exactly
when the byte is zero. It SHALL advance PC by two bytes modulo 65536, add three cycles, and preserve all registers
other than A and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDA zero page ($A5) executes and the operand is $FF
- **THEN** it reads from $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDX using zero page addressing

Opcode $A6 SHALL use the zero-extended one-byte operand to read the byte into X, set N from bit 7, and set Z exactly
when the byte is zero. It SHALL advance PC by two bytes modulo 65536, add three cycles, and preserve all registers
other than X and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDX zero page ($A6) executes and the operand is $FF
- **THEN** it reads from $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** X holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDY using zero page addressing

Opcode $A4 SHALL use the zero-extended one-byte operand to read the byte into Y, set N from bit 7, and set Z exactly
when the byte is zero. It SHALL advance PC by two bytes modulo 65536, add three cycles, and preserve all registers
other than Y and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDY zero page ($A4) executes and the operand is $FF
- **THEN** it reads from $00FF through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Address zero page endpoints
- **WHEN** the operand is $00 or $FF
- **THEN** the effective address is $0000 or $00FF respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** Y holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute STA using absolute,X addressing

Opcode $9D SHALL use the little-endian operand plus X modulo 65536 to write A to memory and preserve all flags. It
SHALL advance PC by three bytes modulo 65536, add five cycles regardless of page crossing, and preserve all registers
other than PC.

#### Scenario: Access the selected address
- **WHEN** STA absolute,X ($9D) executes and the operand is $00FF and X=$01
- **THEN** it writes to $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and X=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five cycles in both cases

### Requirement: Execute STA using absolute,Y addressing

Opcode $99 SHALL use the little-endian operand plus Y modulo 65536 to write A to memory and preserve all flags. It
SHALL advance PC by three bytes modulo 65536, add five cycles regardless of page crossing, and preserve all registers
other than PC.

#### Scenario: Access the selected address
- **WHEN** STA absolute,Y ($99) executes and the operand is $00FF and Y=$01
- **THEN** it writes to $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and Y=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five cycles in both cases

### Requirement: Execute LDA using absolute,X addressing

Opcode $BD SHALL use the little-endian operand plus X modulo 65536 to read the byte into A, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than A and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDA absolute,X ($BD) executes and the operand is $00FF and X=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and X=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDA using absolute,Y addressing

Opcode $B9 SHALL use the little-endian operand plus Y modulo 65536 to read the byte into A, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than A and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDA absolute,Y ($B9) executes and the operand is $00FF and Y=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and Y=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** A holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDX using absolute,Y addressing

Opcode $BE SHALL use the little-endian operand plus Y modulo 65536 to read the byte into X, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than X and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDX absolute,Y ($BE) executes and the operand is $00FF and Y=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and Y=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** X holds the value, N equals bit 7 and Z is set only for $00

### Requirement: Execute LDY using absolute,X addressing

Opcode $BC SHALL use the little-endian operand plus X modulo 65536 to read the byte into Y, set N from bit 7, and set
Z exactly when the byte is zero. It SHALL advance PC by three bytes modulo 65536, add four cycles plus one on a page
crossing, and preserve all registers other than Y and PC, and flags other than N/Z.

#### Scenario: Access the selected address
- **WHEN** LDY absolute,X ($BC) executes and the operand is $00FF and X=$01
- **THEN** it reads from $0100 through connected memory
- **AND** PC and cycles follow the specified effects

#### Scenario: Wrap the effective address
- **WHEN** the operand is $FFFF and X=$01
- **THEN** the effective address is $0000

#### Scenario: Page crossing and nominal cycles
- **WHEN** the index crosses and does not cross a page
- **THEN** the instruction adds five and four cycles respectively

#### Scenario: Set N and Z from the loaded byte
- **WHEN** addressed memory provides $00, $7F, $80, or $FF
- **THEN** Y holds the value, N equals bit 7 and Z is set only for $00
