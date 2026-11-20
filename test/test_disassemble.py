"""Verify offline PRG loading using synthetic mapper-0 cartridges."""

import pytest

from misc.disassemble import decode_prg, disassemble_prg, load_prg_rom


@pytest.fixture
def make_cartridge_file(tmp_path):
    def create_file(header, prg_rom, *, trainer=b"", chr_rom=b"\xE7" * 8192):
        filename = tmp_path / "cartridge.nes"
        filename.write_bytes(header + trainer + prg_rom + chr_rom)
        return filename

    return create_file


@pytest.mark.parametrize("format_marker", [0x00, 0x08], ids=["ines", "nes20"])
@pytest.mark.parametrize("prg_size, base_address", [(16384, 0xC000), (32768, 0x8000)])
@pytest.mark.parametrize("has_trainer", [False, True], ids=["no-trainer", "trainer"])
def test_loads_prg_in_file_order(make_cartridge_file, format_marker, prg_size, base_address, has_trainer):
    # Different sections and PRG halves expose incorrect offsets or accidental mirroring.
    header = b"NES\x1a" + bytes([prg_size // 16384, 1, 0x04 if has_trainer else 0, format_marker]) + bytes(8)
    trainer = b"\x35" * 512 if has_trainer else b""
    prg_rom = bytes(range(256)) * 64
    if prg_size == 32768:
        prg_rom += bytes(reversed(range(256))) * 64
    filename = make_cartridge_file(header, prg_rom, trainer=trainer)
    original = filename.read_bytes()

    # Loading uses the physical PRG bytes once and selects the corresponding CPU listing window.
    loaded_prg, base = load_prg_rom(filename)
    assert loaded_prg == prg_rom
    assert base == base_address
    assert filename.read_bytes() == original


@pytest.mark.parametrize(
    "flags6, flags7, byte8, prg_banks, message",
    [
        (0x10, 0x00, 0x00, 1, "Cartridge mapper 1"),
        (0x00, 0x10, 0x00, 1, "Cartridge mapper 16"),
        (0x00, 0x08, 0x01, 1, "Cartridge mapper 256"),
        (0x00, 0x08, 0x20, 1, "Mapper 0 submapper 2"),
        (0x00, 0x00, 0x00, 0, "Mapper 0 PRG ROM size 0 bytes"),
        (0x00, 0x00, 0x00, 3, "Mapper 0 PRG ROM size 49152 bytes"),
    ],
)
def test_rejects_unsupported_layouts(make_cartridge_file, flags6, flags7, byte8, prg_banks, message):
    # Distinct header fields exercise each part of the parsed mapper and the supported PRG sizes.
    header = b"NES\x1a" + bytes([prg_banks, 1, flags6, flags7, byte8]) + bytes(7)
    filename = make_cartridge_file(header, bytes(prg_banks * 16384))

    # A parsed but unsupported configuration must identify the missing mapping.
    with pytest.raises(NotImplementedError, match=message):
        load_prg_rom(filename)


# The cases group the official encodings by their expected operand spelling, independently of the decoder table.
_OFFICIAL_CASES = [
    (b"", "", (
        "00:BRK 08:PHP 18:CLC 28:PLP 38:SEC 40:RTI 48:PHA 58:CLI 60:RTS 68:PLA 78:SEI "
        "88:DEY 8A:TXA 98:TYA 9A:TXS A8:TAY AA:TAX B8:CLV BA:TSX C8:INY CA:DEX D8:CLD "
        "E8:INX EA:NOP F8:SED"
    )),
    (b"", "A", "0A:ASL 2A:ROL 4A:LSR 6A:ROR"),
    (b"\x34", "#$34", "09:ORA 29:AND 49:EOR 69:ADC A0:LDY A2:LDX A9:LDA C0:CPY C9:CMP E0:CPX E9:SBC"),
    (b"\x34", "$34", (
        "05:ORA 06:ASL 24:BIT 25:AND 26:ROL 45:EOR 46:LSR 65:ADC 66:ROR 84:STY 85:STA "
        "86:STX A4:LDY A5:LDA A6:LDX C4:CPY C5:CMP C6:DEC E4:CPX E5:SBC E6:INC"
    )),
    (b"\x34", "$34,X", (
        "15:ORA 16:ASL 35:AND 36:ROL 55:EOR 56:LSR 75:ADC 76:ROR 94:STY 95:STA "
        "B4:LDY B5:LDA D5:CMP D6:DEC F5:SBC F6:INC"
    )),
    (b"\x34", "$34,Y", "96:STX B6:LDX"),
    (b"\x34\x12", "$1234", (
        "0D:ORA 0E:ASL 20:JSR 2C:BIT 2D:AND 2E:ROL 4C:JMP 4D:EOR 4E:LSR 6D:ADC 6E:ROR "
        "8C:STY 8D:STA 8E:STX AC:LDY AD:LDA AE:LDX CC:CPY CD:CMP CE:DEC EC:CPX ED:SBC EE:INC"
    )),
    (b"\x34\x12", "$1234,X", (
        "1D:ORA 1E:ASL 3D:AND 3E:ROL 5D:EOR 5E:LSR 7D:ADC 7E:ROR "
        "9D:STA BC:LDY BD:LDA DD:CMP DE:DEC FD:SBC FE:INC"
    )),
    (b"\x34\x12", "$1234,Y", "19:ORA 39:AND 59:EOR 79:ADC 99:STA B9:LDA BE:LDX D9:CMP F9:SBC"),
    (b"\x34\x12", "($1234)", "6C:JMP"),
    (b"\x34", "($34,X)", "01:ORA 21:AND 41:EOR 61:ADC 81:STA A1:LDA C1:CMP E1:SBC"),
    (b"\x34", "($34),Y", "11:ORA 31:AND 51:EOR 71:ADC 91:STA B1:LDA D1:CMP F1:SBC"),
    (b"\x7F", "$C081", "10:BPL 30:BMI 50:BVC 70:BVS 90:BCC B0:BCS D0:BNE F0:BEQ"),
]

_OFFICIAL_ENCODINGS = [
    (int(entry[:2], 16), operand_bytes, entry[3:], expected_operand)
    for operand_bytes, expected_operand, entries in _OFFICIAL_CASES
    for entry in entries.split()
]


@pytest.mark.parametrize(
    "opcode, operand_bytes, mnemonic, expected_operand",
    [pytest.param(*case, id=f"{case[2]}-{case[0]:02X}") for case in _OFFICIAL_ENCODINGS],
)
def test_decodes_official_instructions(opcode, operand_bytes, mnemonic, expected_operand):
    program = bytes([opcode]) + operand_bytes
    assert list(decode_prg(program, 0xC000)) == [(0xC000, program, mnemonic, expected_operand)]


@pytest.mark.parametrize(
    "opcode",
    sorted(set(range(256)) - {case[0] for case in _OFFICIAL_ENCODINGS}),
    ids=lambda opcode: f"{opcode:02X}",
)
def test_unofficial_opcode_is_data_and_scanning_continues(opcode):
    program = bytes([opcode, 0xEA])
    assert list(decode_prg(program, 0x8000)) == [
        (0x8000, bytes([opcode]), "db", f"${opcode:02X}"),
        (0x8001, b"\xEA", "NOP", ""),
    ]


@pytest.mark.parametrize("program", [b"\xA9", b"\x4C", b"\x4C\xEA"])
def test_incomplete_final_instruction_preserves_each_byte_as_data(program):
    assert list(decode_prg(program, 0xC000)) == [
        (0xC000 + offset, bytes([value]), "db", f"${value:02X}") for offset, value in enumerate(program)
    ]


@pytest.mark.parametrize(
    "address, displacement, target",
    [(0xC010, 0x00, "$C012"), (0xC010, 0x7F, "$C091"), (0xC010, 0x80, "$BF92"),
     (0xC010, 0xFF, "$C011"), (0xFFFE, 0x02, "$0002")],
)
def test_relative_operands_use_signed_displacement(address, displacement, target):
    program = bytes([0xD0, displacement])
    assert list(decode_prg(program, address)) == [(address, program, "BNE", target)]


def test_decodes_consecutive_instructions_with_their_addresses():
    program = b"\xA9\x80\x85\x10\xEA\x6C\x34\x12\x02"
    assert list(decode_prg(program, 0x8000)) == [
        (0x8000, b"\xA9\x80", "LDA", "#$80"),
        (0x8002, b"\x85\x10", "STA", "$10"),
        (0x8004, b"\xEA", "NOP", ""),
        (0x8005, b"\x6C\x34\x12", "JMP", "($1234)"),
        (0x8008, b"\x02", "db", "$02"),
    ]


def test_decodes_loaded_prg_without_trainer_or_chr(make_cartridge_file):
    # Distinct surrounding sections expose a scan that starts before or ends after PRG.
    header = b"NES\x1a" + bytes([1, 1, 0x04, 0x00]) + bytes(8)
    prg_rom = b"\xA9\x80\x85\x10" + b"\xEA" * (16384 - 4)
    filename = make_cartridge_file(header, prg_rom, trainer=b"\x35" * 512)
    loaded_prg, base_address = load_prg_rom(filename)

    # The complete scan preserves the PRG byte sequence and its selected CPU addresses.
    decoded = list(decode_prg(loaded_prg, base_address))
    assert decoded[:2] == [(0xC000, b"\xA9\x80", "LDA", "#$80"), (0xC002, b"\x85\x10", "STA", "$10")]
    assert decoded[-1] == (0xFFFF, b"\xEA", "NOP", "")
    assert b"".join(instruction_bytes for _, instruction_bytes, _, _ in decoded) == prg_rom


def test_listing_reuses_forward_target_and_defines_backward_target():
    program = b"\xD0\x04\xF0\x02\x30\xFA\xEA"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "L_C000:",
        "$C000: D0 04    BNE L_C006",
        "$C002: F0 02    BEQ L_C006",
        "$C004: 30 FA    BMI L_C000",
        "L_C006:",
        "$C006: EA       NOP",
    ]


@pytest.mark.parametrize(
    "opcode, mnemonic",
    [(0x10, "BPL"), (0x30, "BMI"), (0x50, "BVC"), (0x70, "BVS"),
     (0x90, "BCC"), (0xB0, "BCS"), (0xD0, "BNE"), (0xF0, "BEQ")],
)
def test_listing_labels_each_relative_branch(opcode, mnemonic):
    program = bytes([0xEA, opcode, 0xFD])
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "L_C000:",
        "$C000: EA       NOP",
        f"$C001: {opcode:02X} FD    {mnemonic} L_C000",
    ]


def test_listing_labels_direct_jumps_but_keeps_indirect_pointer():
    program = b"\x20\x09\xC0\x4C\x09\xC0\x6C\x09\xC0\xEA"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "$C000: 20 09 C0 JSR L_C009",
        "$C003: 4C 09 C0 JMP L_C009",
        "$C006: 6C 09 C0 JMP ($C009)",
        "L_C009:",
        "$C009: EA       NOP",
    ]


def test_listing_does_not_infer_indirect_jump_or_data_targets():
    program = b"\x6C\x00\xC0\xAD\x00\xC0"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "$C000: 6C 00 C0 JMP ($C000)",
        "$C003: AD 00 C0 LDA $C000",
    ]


def test_listing_uses_equ_for_targets_outside_or_inside_an_instruction():
    program = b"\x4C\x04\xC0\xA9\x42\x20\x00\x20\x4C\x0B\xC0"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "PPUCTRL EQU $2000",
        "L_2000 EQU PPUCTRL",
        "L_C004 EQU $C004",
        "L_C00B EQU $C00B",
        "",
        "$C000: 4C 04 C0 JMP L_C004",
        "$C003: A9 42    LDA #$42",
        "$C005: 20 00 20 JSR L_2000",
        "$C008: 4C 0B C0 JMP L_C00B",
    ]


def test_listing_uses_equ_for_relative_target_outside_prg():
    assert disassemble_prg(b"\xD0\xFB", 0xC000).splitlines() == [
        "L_BFFD EQU $BFFD",
        "",
        "$C000: D0 FB    BNE L_BFFD",
    ]


def test_listing_can_label_data_without_inventing_targets_for_incomplete_instructions():
    program = b"\x4C\x03\xC0\x02\x4C\xD0"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "$C000: 4C 03 C0 JMP L_C003",
        "L_C003:",
        "$C003: 02       db $02",
        "$C004: 4C       db $4C",
        "$C005: D0       db $D0",
    ]


def _assert_listing_covers_prg(lines, prg_rom, base_address):
    # Consecutive addresses and reconstructed bytes establish that no PRG byte is repeated or lost.
    entries = [(int(line[1:5], 16), bytes.fromhex(line[7:15])) for line in lines if line.startswith("$")]
    assert entries[0][0] == base_address
    assert all(next_address == address + len(data) for (address, data), (next_address, _) in zip(entries, entries[1:]))
    assert entries[-1][0] + len(entries[-1][1]) == 0x10000
    assert b"".join(data for _, data in entries) == prg_rom


def test_16k_listing_uses_exact_mirror_aliases_for_control_and_data(make_cartridge_file):
    # Lower and upper windows can name the same byte while retaining different CPU addresses.
    program = (
        b"\x4C\x00\x80\x20\xFF\xBF\xAD\x00\x80\xAD\x01\x80\xBD\xFF\xBF\xB9\x00\x80"
        b"\x6C\xFF\xBF\xA9\x80\xAD\xFF\x7F\xBD\xFF\x7F\xB9\x00\xC0\xAD\x00\xC0\x4C\x00\xC0"
    )
    prg_rom = program + b"\xEA" * (16384 - len(program) - 2) + b"\x4C\x80"
    header = b"NES\x1a" + bytes([1, 1, 0, 0]) + bytes(8)
    filename = make_cartridge_file(header, prg_rom)

    # The same alias is reused by different instructions and still denotes the lower address.
    loaded_prg, base_address = load_prg_rom(filename)
    lines = disassemble_prg(loaded_prg, base_address).splitlines()
    assert lines[:18] == [
        "L_8000 EQU $8000 ; mirror of $C000",
        "L_8001 EQU $8001 ; mirror of $C001",
        "L_BFFF EQU $BFFF ; mirror of $FFFF",
        "",
        "L_C000:",
        "$C000: 4C 00 80 JMP L_8000",
        "$C003: 20 FF BF JSR L_BFFF",
        "$C006: AD 00 80 LDA L_8000",
        "$C009: AD 01 80 LDA L_8001",
        "$C00C: BD FF BF LDA L_BFFF,X",
        "$C00F: B9 00 80 LDA L_8000,Y",
        "$C012: 6C FF BF JMP (L_BFFF)",
        "$C015: A9 80    LDA #$80",
        "$C017: AD FF 7F LDA $7FFF",
        "$C01A: BD FF 7F LDA $7FFF,X",
        "$C01D: B9 00 C0 LDA $C000,Y",
        "$C020: AD 00 C0 LDA $C000",
        "$C023: 4C 00 C0 JMP L_C000",
    ]
    assert lines[-2:] == ["$FFFE: 4C       db $4C", "$FFFF: 80       db $80"]
    _assert_listing_covers_prg(lines, prg_rom, 0xC000)


def test_16k_listing_labels_relative_branch_to_mirror():
    prg_rom = b"\xD0\xFD" + b"\xEA" * (16384 - 2)
    lines = disassemble_prg(prg_rom, 0xC000).splitlines()
    assert lines[:3] == [
        "L_BFFF EQU $BFFF ; mirror of $FFFF",
        "",
        "$C000: D0 FD    BNE L_BFFF",
    ]


def test_32k_listing_does_not_treat_lower_prg_as_a_mirror(make_cartridge_file):
    # The two 16 KiB windows are distinct in a 32 KiB cartridge.
    program = b"\x4C\x00\x80\xAD\x00\x80\x6C\xFF\xBF\x4C\xFF\xBF"
    prg_rom = program + b"\xEA" * (32768 - len(program))
    header = b"NES\x1a" + bytes([2, 1, 0, 0]) + bytes(8)
    filename = make_cartridge_file(header, prg_rom)

    # Direct targets use line labels, while data and indirect operands remain numeric.
    loaded_prg, base_address = load_prg_rom(filename)
    lines = disassemble_prg(loaded_prg, base_address).splitlines()
    assert lines[:5] == [
        "L_8000:",
        "$8000: 4C 00 80 JMP L_8000",
        "$8003: AD 00 80 LDA $8000",
        "$8006: 6C FF BF JMP ($BFFF)",
        "$8009: 4C FF BF JMP L_BFFF",
    ]
    assert "L_BFFF:" in lines
    assert not any("mirror of" in line for line in lines)
    _assert_listing_covers_prg(lines, prg_rom, 0x8000)


@pytest.mark.parametrize(
    "address, symbol",
    [
        (0x2000, "PPUCTRL"), (0x2001, "PPUMASK"), (0x2002, "PPUSTATUS"), (0x2003, "OAMADDR"),
        (0x2004, "OAMDATA"), (0x2005, "PPUSCROLL"), (0x2006, "PPUADDR"), (0x2007, "PPUDATA"),
        (0x4000, "PULSE1_CTRL"), (0x4001, "PULSE1_SWEEP"), (0x4002, "PULSE1_TIMER_LO"),
        (0x4003, "PULSE1_TIMER_HI"), (0x4004, "PULSE2_CTRL"), (0x4005, "PULSE2_SWEEP"),
        (0x4006, "PULSE2_TIMER_LO"), (0x4007, "PULSE2_TIMER_HI"), (0x4008, "TRIANGLE_CTRL"),
        (0x400A, "TRIANGLE_TIMER_LO"), (0x400B, "TRIANGLE_TIMER_HI"), (0x400C, "NOISE_CTRL"),
        (0x400E, "NOISE_PERIOD"), (0x400F, "NOISE_LENGTH"), (0x4010, "DMC_CTRL"), (0x4011, "DMC_OUTPUT"),
        (0x4012, "DMC_ADDRESS"), (0x4013, "DMC_LENGTH"), (0x4014, "OAMDMA"), (0x4015, "APU_STATUS"),
        (0x4016, "JOY1_STROBE"), (0x4017, "JOY2_APU_FRAME"),
    ],
)
def test_listing_names_each_hardware_register(address, symbol):
    program = bytes([0xAD, address & 0xFF, address >> 8])
    lines = disassemble_prg(program, 0xC000).splitlines()
    assert len(lines) == 3
    assert lines[0].startswith(f"{symbol} EQU ${address:04X}")
    assert lines[1] == ""
    assert lines[2] == f"$C000: AD {address & 0xFF:02X} {address >> 8:02X} LDA {symbol}"


@pytest.mark.parametrize(
    "base, symbol",
    [(0x2000, "PPUCTRL"), (0x2001, "PPUMASK"), (0x2002, "PPUSTATUS"), (0x2003, "OAMADDR"),
     (0x2004, "OAMDATA"), (0x2005, "PPUSCROLL"), (0x2006, "PPUADDR"), (0x2007, "PPUDATA")],
)
def test_listing_preserves_each_ppu_mirror_address(base, symbol):
    # Every mirror retains its own address while naming the repeated register.
    for address in range(base + 8, 0x4000, 8):
        program = bytes([0xAD, address & 0xFF, address >> 8])
        lines = disassemble_prg(program, 0xC000).splitlines()
        alias = f"{symbol}_{address:04X}"
        assert lines[0] == f"{alias} EQU ${address:04X} ; mirror of {symbol} (${base:04X})"
        assert lines[2] == f"$C000: AD {address & 0xFF:02X} {address >> 8:02X} LDA {alias}"


def test_listing_preserves_ppu_mirrors_and_indexed_bases():
    program = b"\xBD\x00\x20\xB9\x08\x20\xAD\x08\x20\xAD\xFF\x3F"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "PPUCTRL EQU $2000",
        "PPUCTRL_2008 EQU $2008 ; mirror of PPUCTRL ($2000)",
        "PPUDATA_3FFF EQU $3FFF ; mirror of PPUDATA ($2007)",
        "",
        "$C000: BD 00 20 LDA PPUCTRL,X",
        "$C003: B9 08 20 LDA PPUCTRL_2008,Y",
        "$C006: AD 08 20 LDA PPUCTRL_2008",
        "$C009: AD FF 3F LDA PPUDATA_3FFF",
    ]


def test_listing_identifies_shared_controller_and_apu_addresses():
    program = (
        b"\xAD\x17\x40\x8D\x17\x40\xEE\x17\x40\xBD\x17\x40\x6C\x17\x40\x4C\x17\x40"
        b"\xAD\x16\x40\x8D\x16\x40\xAD\x15\x40\x8D\x15\x40"
    )
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "APU_STATUS EQU $4015 ; read APU status, write channel enables",
        "JOY1_STROBE EQU $4016 ; read controller 1, write controller strobe",
        "JOY2_APU_FRAME EQU $4017 ; read controller 2, write APU frame counter",
        "L_4017 EQU JOY2_APU_FRAME",
        "",
        "$C000: AD 17 40 LDA JOY2_APU_FRAME",
        "$C003: 8D 17 40 STA JOY2_APU_FRAME",
        "$C006: EE 17 40 INC JOY2_APU_FRAME",
        "$C009: BD 17 40 LDA JOY2_APU_FRAME,X",
        "$C00C: 6C 17 40 JMP (JOY2_APU_FRAME)",
        "$C00F: 4C 17 40 JMP L_4017",
        "$C012: AD 16 40 LDA JOY1_STROBE",
        "$C015: 8D 16 40 STA JOY1_STROBE",
        "$C018: AD 15 40 LDA APU_STATUS",
        "$C01B: 8D 15 40 STA APU_STATUS",
    ]


def test_listing_links_hardware_control_targets_to_register_symbols():
    program = b"\x20\x08\x20\x4C\x00\x20\x6C\x08\x20"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "PPUCTRL EQU $2000",
        "PPUCTRL_2008 EQU $2008 ; mirror of PPUCTRL ($2000)",
        "L_2000 EQU PPUCTRL",
        "L_2008 EQU PPUCTRL_2008",
        "",
        "$C000: 20 08 20 JSR L_2008",
        "$C003: 4C 00 20 JMP L_2000",
        "$C006: 6C 08 20 JMP (PPUCTRL_2008)",
    ]


def test_listing_links_hardware_relative_target_to_register_symbol():
    assert disassemble_prg(b"\xD0\xFB", 0x401A).splitlines() == [
        "JOY2_APU_FRAME EQU $4017 ; read controller 2, write APU frame counter",
        "L_4017 EQU JOY2_APU_FRAME",
        "",
        "$401A: D0 FB    BNE L_4017",
    ]


def test_listing_does_not_symbolize_immediates_unknown_registers_or_inferred_indexed_addresses():
    program = b"\xA9\x17\xA5\x17\xAD\x09\x40\xAD\x0D\x40\xAD\x18\x40\xBD\xFF\x1F"
    assert disassemble_prg(program, 0xC000).splitlines() == [
        "$C000: A9 17    LDA #$17",
        "$C002: A5 17    LDA $17",
        "$C004: AD 09 40 LDA $4009",
        "$C007: AD 0D 40 LDA $400D",
        "$C00A: AD 18 40 LDA $4018",
        "$C00D: BD FF 1F LDA $1FFF,X",
    ]


def test_listing_combines_hardware_symbols_with_prg_mirror_aliases():
    # Hardware and PRG mirrors coexist without changing their distinct CPU addresses.
    program = b"\x20\x00\x80\xAD\x08\x20\xAD\x00\x80"
    prg_rom = program + b"\xEA" * (16384 - len(program))
    lines = disassemble_prg(prg_rom, 0xC000).splitlines()
    assert lines[:6] == [
        "PPUCTRL_2008 EQU $2008 ; mirror of PPUCTRL ($2000)",
        "L_8000 EQU $8000 ; mirror of $C000",
        "",
        "$C000: 20 00 80 JSR L_8000",
        "$C003: AD 08 20 LDA PPUCTRL_2008",
        "$C006: AD 00 80 LDA L_8000",
    ]
    _assert_listing_covers_prg(lines, prg_rom, 0xC000)
