"""Prepare mapper-0 program ROM bytes for an offline disassembly."""

from pathlib import Path
import sys

# Resolve component imports from this file so callers can use any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nesfile import NESFile


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
