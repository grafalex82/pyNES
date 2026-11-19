"""Shared synthetic CPU and cartridge fixtures."""

import pytest

from cpu import CPU
from machine import Machine
from nesfile import NESFile


PRG_ROM_BANK_SIZE = 16384


def make_ines_header(*, prg_rom_banks, chr_rom_banks=0, mapper=0):
    """Build an ordinary iNES header with horizontal mirroring and no trainer or battery."""
    # Bytes 4/5 count PRG/CHR banks; bytes 6/7 hold the low/high mapper nibbles.
    header = bytearray(16)
    header[:4] = b"NES\x1a"
    header[4] = prg_rom_banks
    header[5] = chr_rom_banks
    header[6] = (mapper & 0x0F) << 4
    header[7] = mapper & 0xF0
    return bytes(header)


@pytest.fixture
def make_cpu(tmp_path):
    # Tests can select the memory layout and entry point while using real memory operations.
    def create_cpu(*, prg_size=PRG_ROM_BANK_SIZE, start_address=0x0000, prg_program=b""):
        # Place PRG code at the mapped entry and install the reset vector in the last bank.
        prg = bytearray(prg_size)
        prg_offset = (start_address - 0x8000) & (prg_size - 1)
        prg[prg_offset:prg_offset + len(prg_program)] = prg_program
        prg[-4:-2] = start_address.to_bytes(2, "little")

        # Connect the cartridge before CPU construction reads its reset vector.
        header = make_ines_header(prg_rom_banks=prg_size // PRG_ROM_BANK_SIZE, chr_rom_banks=0, mapper=0)
        filename = tmp_path / "cpu.nes"
        filename.write_bytes(header + prg)
        machine = Machine(NESFile(filename))
        return CPU(machine), machine

    # Both components remain available for test-specific registers, data, and instruction bytes in RAM.
    return create_cpu


@pytest.fixture
def prg_size():
    return PRG_ROM_BANK_SIZE


@pytest.fixture
def start_address():
    return 0x0000


@pytest.fixture
def cpu(make_cpu, prg_size, start_address):
    cpu, _ = make_cpu(prg_size=prg_size, start_address=start_address)
    return cpu


