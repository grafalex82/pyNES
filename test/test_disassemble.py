"""Verify offline PRG loading using synthetic mapper-0 cartridges."""

import pytest

from misc.disassemble import decode_prg, load_prg_rom


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
