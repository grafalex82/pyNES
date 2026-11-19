## ADDED Requirements

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
