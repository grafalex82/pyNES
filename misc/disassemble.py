"""Write an offline disassembly listing for a mapper-0 cartridge."""

import argparse
from pathlib import Path
import sys

# Resolve component imports from this file so callers can use any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nesfile import NESFile


_OPCODES = {
    0x00: ("BRK", "imp"), 0x01: ("ORA", "ind_x"), 0x05: ("ORA", "zp"), 0x06: ("ASL", "zp"),
    0x08: ("PHP", "imp"), 0x09: ("ORA", "imm"), 0x0A: ("ASL", "acc"), 0x0D: ("ORA", "abs"),
    0x0E: ("ASL", "abs"), 0x10: ("BPL", "rel"), 0x11: ("ORA", "ind_y"), 0x15: ("ORA", "zp_x"),
    0x16: ("ASL", "zp_x"), 0x18: ("CLC", "imp"), 0x19: ("ORA", "abs_y"), 0x1D: ("ORA", "abs_x"),
    0x1E: ("ASL", "abs_x"), 0x20: ("JSR", "abs"), 0x21: ("AND", "ind_x"), 0x24: ("BIT", "zp"),
    0x25: ("AND", "zp"), 0x26: ("ROL", "zp"), 0x28: ("PLP", "imp"), 0x29: ("AND", "imm"),
    0x2A: ("ROL", "acc"), 0x2C: ("BIT", "abs"), 0x2D: ("AND", "abs"), 0x2E: ("ROL", "abs"),
    0x30: ("BMI", "rel"), 0x31: ("AND", "ind_y"), 0x35: ("AND", "zp_x"), 0x36: ("ROL", "zp_x"),
    0x38: ("SEC", "imp"), 0x39: ("AND", "abs_y"), 0x3D: ("AND", "abs_x"), 0x3E: ("ROL", "abs_x"),
    0x40: ("RTI", "imp"), 0x41: ("EOR", "ind_x"), 0x45: ("EOR", "zp"), 0x46: ("LSR", "zp"),
    0x48: ("PHA", "imp"), 0x49: ("EOR", "imm"), 0x4A: ("LSR", "acc"), 0x4C: ("JMP", "abs"),
    0x4D: ("EOR", "abs"), 0x4E: ("LSR", "abs"), 0x50: ("BVC", "rel"), 0x51: ("EOR", "ind_y"),
    0x55: ("EOR", "zp_x"), 0x56: ("LSR", "zp_x"), 0x58: ("CLI", "imp"), 0x59: ("EOR", "abs_y"),
    0x5D: ("EOR", "abs_x"), 0x5E: ("LSR", "abs_x"), 0x60: ("RTS", "imp"), 0x61: ("ADC", "ind_x"),
    0x65: ("ADC", "zp"), 0x66: ("ROR", "zp"), 0x68: ("PLA", "imp"), 0x69: ("ADC", "imm"),
    0x6A: ("ROR", "acc"), 0x6C: ("JMP", "ind"), 0x6D: ("ADC", "abs"), 0x6E: ("ROR", "abs"),
    0x70: ("BVS", "rel"), 0x71: ("ADC", "ind_y"), 0x75: ("ADC", "zp_x"), 0x76: ("ROR", "zp_x"),
    0x78: ("SEI", "imp"), 0x79: ("ADC", "abs_y"), 0x7D: ("ADC", "abs_x"), 0x7E: ("ROR", "abs_x"),
    0x81: ("STA", "ind_x"), 0x84: ("STY", "zp"), 0x85: ("STA", "zp"), 0x86: ("STX", "zp"),
    0x88: ("DEY", "imp"), 0x8A: ("TXA", "imp"), 0x8C: ("STY", "abs"), 0x8D: ("STA", "abs"),
    0x8E: ("STX", "abs"), 0x90: ("BCC", "rel"), 0x91: ("STA", "ind_y"), 0x94: ("STY", "zp_x"),
    0x95: ("STA", "zp_x"), 0x96: ("STX", "zp_y"), 0x98: ("TYA", "imp"), 0x99: ("STA", "abs_y"),
    0x9A: ("TXS", "imp"), 0x9D: ("STA", "abs_x"), 0xA0: ("LDY", "imm"), 0xA1: ("LDA", "ind_x"),
    0xA2: ("LDX", "imm"), 0xA4: ("LDY", "zp"), 0xA5: ("LDA", "zp"), 0xA6: ("LDX", "zp"),
    0xA8: ("TAY", "imp"), 0xA9: ("LDA", "imm"), 0xAA: ("TAX", "imp"), 0xAC: ("LDY", "abs"),
    0xAD: ("LDA", "abs"), 0xAE: ("LDX", "abs"), 0xB0: ("BCS", "rel"), 0xB1: ("LDA", "ind_y"),
    0xB4: ("LDY", "zp_x"), 0xB5: ("LDA", "zp_x"), 0xB6: ("LDX", "zp_y"), 0xB8: ("CLV", "imp"),
    0xB9: ("LDA", "abs_y"), 0xBA: ("TSX", "imp"), 0xBC: ("LDY", "abs_x"), 0xBD: ("LDA", "abs_x"),
    0xBE: ("LDX", "abs_y"), 0xC0: ("CPY", "imm"), 0xC1: ("CMP", "ind_x"), 0xC4: ("CPY", "zp"),
    0xC5: ("CMP", "zp"), 0xC6: ("DEC", "zp"), 0xC8: ("INY", "imp"), 0xC9: ("CMP", "imm"),
    0xCA: ("DEX", "imp"), 0xCC: ("CPY", "abs"), 0xCD: ("CMP", "abs"), 0xCE: ("DEC", "abs"),
    0xD0: ("BNE", "rel"), 0xD1: ("CMP", "ind_y"), 0xD5: ("CMP", "zp_x"), 0xD6: ("DEC", "zp_x"),
    0xD8: ("CLD", "imp"), 0xD9: ("CMP", "abs_y"), 0xDD: ("CMP", "abs_x"), 0xDE: ("DEC", "abs_x"),
    0xE0: ("CPX", "imm"), 0xE1: ("SBC", "ind_x"), 0xE4: ("CPX", "zp"), 0xE5: ("SBC", "zp"),
    0xE6: ("INC", "zp"), 0xE8: ("INX", "imp"), 0xE9: ("SBC", "imm"), 0xEA: ("NOP", "imp"),
    0xEC: ("CPX", "abs"), 0xED: ("SBC", "abs"), 0xEE: ("INC", "abs"), 0xF0: ("BEQ", "rel"),
    0xF1: ("SBC", "ind_y"), 0xF5: ("SBC", "zp_x"), 0xF6: ("INC", "zp_x"), 0xF8: ("SED", "imp"),
    0xF9: ("SBC", "abs_y"), 0xFD: ("SBC", "abs_x"), 0xFE: ("INC", "abs_x"),
}

_ADDRESSING = {
    "imp": (1, ""), "acc": (1, "A"), "imm": (2, "#${:02X}"),
    "zp": (2, "${:02X}"), "zp_x": (2, "${:02X},X"), "zp_y": (2, "${:02X},Y"),
    "abs": (3, "${:04X}"), "abs_x": (3, "${:04X},X"), "abs_y": (3, "${:04X},Y"),
    "ind": (3, "(${:04X})"), "ind_x": (2, "(${:02X},X)"), "ind_y": (2, "(${:02X}),Y"),
    "rel": (2, "${:04X}"),
}

_PPU_REGISTERS = ("PPUCTRL", "PPUMASK", "PPUSTATUS", "OAMADDR", "OAMDATA", "PPUSCROLL", "PPUADDR", "PPUDATA")

_IO_REGISTERS = {
    0x4000: "PULSE1_CTRL", 0x4001: "PULSE1_SWEEP", 0x4002: "PULSE1_TIMER_LO", 0x4003: "PULSE1_TIMER_HI",
    0x4004: "PULSE2_CTRL", 0x4005: "PULSE2_SWEEP", 0x4006: "PULSE2_TIMER_LO", 0x4007: "PULSE2_TIMER_HI",
    0x4008: "TRIANGLE_CTRL", 0x400A: "TRIANGLE_TIMER_LO", 0x400B: "TRIANGLE_TIMER_HI",
    0x400C: "NOISE_CTRL", 0x400E: "NOISE_PERIOD", 0x400F: "NOISE_LENGTH",
    0x4010: "DMC_CTRL", 0x4011: "DMC_OUTPUT", 0x4012: "DMC_ADDRESS", 0x4013: "DMC_LENGTH",
    0x4014: "OAMDMA", 0x4015: "APU_STATUS", 0x4016: "JOY1_STROBE", 0x4017: "JOY2_APU_FRAME",
}


def load_prg_rom(filename):
    """Return the PRG bytes and their selected listing base address."""
    # NESFile separates the PRG section from any preceding trainer and following CHR data.
    cartridge = NESFile(filename)
    mapper = cartridge.get_mapper()
    submapper = cartridge.get_submapper()
    if mapper != 0:
        raise NotImplementedError(f"Cartridge mapper {mapper} is not implemented")
    if submapper != 0:
        raise NotImplementedError(f"Mapper 0 submapper {submapper} is not implemented")

    # A single 16 KiB image is listed at $C000; 32 KiB occupies $8000-$FFFF.
    prg_rom = cartridge.get_prg_rom()
    if len(prg_rom) not in (16384, 32768):
        raise NotImplementedError(f"Mapper 0 PRG ROM size {len(prg_rom)} bytes is not implemented")
    return prg_rom, 0x10000 - len(prg_rom)


def decode_prg(prg_rom, base_address):
    """Yield address, original bytes, mnemonic, and operand for a linear PRG scan."""
    offset = 0
    while offset < len(prg_rom):
        # Undocumented opcodes are data in this listing, not instructions executed by the CPU.
        address = base_address + offset
        opcode = prg_rom[offset]
        instruction = _OPCODES.get(opcode)
        if instruction is None:
            yield address, prg_rom[offset:offset + 1], "db", f"${opcode:02X}"
            offset += 1
            continue

        # An incomplete final instruction leaves every remaining byte visible as data.
        mnemonic, mode = instruction
        size, operand_format = _ADDRESSING[mode]
        if offset + size > len(prg_rom):
            for index in range(offset, len(prg_rom)):
                yield base_address + index, prg_rom[index:index + 1], "db", f"${prg_rom[index]:02X}"
            return

        # Multi-byte operands are little-endian; branches use a signed offset from the next instruction.
        instruction_bytes = prg_rom[offset:offset + size]
        value = int.from_bytes(instruction_bytes[1:], "little")
        if mode == "rel":
            displacement = value if value < 0x80 else value - 0x100
            value = (address + size + displacement) & 0xFFFF
        yield address, instruction_bytes, mnemonic, operand_format.format(value)
        offset += size


def _control_target(instruction_bytes, mnemonic, operand):
    """Return a directly encoded control-flow target, or None for other lines."""
    # Incomplete instructions are data even if their first byte is a branch or jump opcode.
    if mnemonic == "db":
        return None

    # Indirect JMP contains a pointer address, not the destination stored at that pointer.
    mode = _OPCODES[instruction_bytes[0]][1]
    if mode == "rel" or (mode == "abs" and mnemonic in ("JMP", "JSR")):
        return int(operand[1:], 16)
    return None


def _operand_address(instruction_bytes, mnemonic, operand):
    """Return the encoded address or relative branch target, if present."""
    # Data bytes and non-address operands do not identify a CPU address.
    if mnemonic == "db":
        return None
    mode = _OPCODES[instruction_bytes[0]][1]
    if mode == "rel":
        return int(operand[1:], 16)

    # Only the encoded base or branch target is known; indexed effective addresses are not inferred.
    if mode in ("abs", "abs_x", "abs_y", "ind"):
        return int.from_bytes(instruction_bytes[1:], "little")
    return None


def _hardware_symbol(address):
    """Name known CPU-visible registers without changing their encoded addresses."""
    # PPU mirrors need distinct names because their CPU addresses are distinct.
    if 0x2000 <= address < 0x4000:
        name = _PPU_REGISTERS[address & 7]
        return name if address < 0x2008 else f"{name}_{address:04X}"

    # The remaining known registers do not repeat across this address range.
    return _IO_REGISTERS.get(address)


def disassemble_prg(prg_rom, base_address):
    """Return a two-pass listing with direct targets, PRG mirrors, and hardware symbols."""
    # The first scan finds targets, referenced symbols, and boundaries without following control flow.
    targets = set()
    boundaries = set()
    mirrors = set()
    registers = {}
    mirrored_prg = len(prg_rom) == 16384 and base_address == 0xC000
    for address, instruction_bytes, mnemonic, operand in decode_prg(prg_rom, base_address):
        boundaries.add(address)
        target = _control_target(instruction_bytes, mnemonic, operand)
        if target is not None:
            targets.add(target)
        operand_address = _operand_address(instruction_bytes, mnemonic, operand)
        if operand_address is None:
            continue
        name = _hardware_symbol(operand_address)
        if name is not None:
            registers[operand_address] = name
        if mirrored_prg and 0x8000 <= operand_address < 0xC000:
            mirrors.add(operand_address)

    # Register definitions preserve PPU mirror addresses and clarify shared read/write ports.
    lines = []
    for address, name in sorted(registers.items()):
        line = f"{name} EQU ${address:04X}"
        if 0x2008 <= address < 0x4000:
            index = address & 7
            line += f" ; mirror of {_PPU_REGISTERS[index]} (${0x2000 + index:04X})"
        elif address == 0x4015:
            line += " ; read APU status, write channel enables"
        elif address == 0x4016:
            line += " ; read controller 1, write controller strobe"
        elif address == 0x4017:
            line += " ; read controller 2, write APU frame counter"
        lines.append(line)

    # Target labels retain their exact address and identify a hardware symbol when one exists.
    for address in sorted((targets - boundaries) | mirrors):
        value = registers.get(address, f"${address:04X}")
        line = f"L_{address:04X} EQU {value}"
        if address in mirrors:
            line += f" ; mirror of ${address + 0x4000:04X}"
        lines.append(line)
    if lines:
        lines.append("")

    # The second scan places labels and substitutes exact-address symbols without changing operand syntax.
    for address, instruction_bytes, mnemonic, operand in decode_prg(prg_rom, base_address):
        if address in targets:
            lines.append(f"L_{address:04X}:")
        target = _control_target(instruction_bytes, mnemonic, operand)
        if target is not None:
            operand = f"L_{target:04X}"
        else:
            operand_address = _operand_address(instruction_bytes, mnemonic, operand)
            if operand_address in registers:
                operand = operand.replace(f"${operand_address:04X}", registers[operand_address])
            elif operand_address in mirrors:
                operand = operand.replace(f"${operand_address:04X}", f"L_{operand_address:04X}")
        byte_text = " ".join(f"{byte:02X}" for byte in instruction_bytes)
        line = f"${address:04X}: {byte_text:<8}  {mnemonic}"
        if operand:
            line += f" {operand}"
        lines.append(line)
    return "".join(f"{line}\n" for line in lines)


def main():
    # Both paths are relative to the caller's working directory, not the script.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", help="path to a valid mapper-0 iNES or NES 2.0 cartridge file")
    parser.add_argument("output", help="path to the output listing")
    args = parser.parse_args()

    # Different paths, including hard links, can identify the same cartridge.
    source = Path(args.rom)
    output = Path(args.output)
    if source.resolve() == output.resolve() or (output.exists() and source.samefile(output)):
        parser.error("output path must not identify the input cartridge")

    # Finish loading and decoding before opening the destination for writing.
    prg_rom, base_address = load_prg_rom(source)
    listing = disassemble_prg(prg_rom, base_address)
    output.write_text(listing, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
