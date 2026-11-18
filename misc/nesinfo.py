"""Print cartridge file metadata without starting emulation."""

import argparse
from pathlib import Path
import sys

# Resolve component imports from this file so callers can use any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nesfile import NESFile


def main():
    # A positional path keeps inspection separate from future emulator startup options.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", help="path to a valid iNES or NES 2.0 cartridge file")
    args = parser.parse_args()

    # Sizes describe extracted file sections; flags do not configure emulated devices.
    cartridge = NESFile(args.rom)
    print(f"Format: {cartridge.get_format()}")
    print(f"Mapper: {cartridge.get_mapper()}")
    print(f"Submapper: {cartridge.get_submapper()}")
    print(f"PRG ROM: {len(cartridge.get_prg_rom())} bytes")
    print(f"CHR ROM: {len(cartridge.get_chr_rom())} bytes")
    print(f"Trainer: {len(cartridge.get_trainer())} bytes")
    print(f"Mirroring (header): {cartridge.get_mirroring()}")
    print(f"Nonvolatile memory (header): {'yes' if cartridge.get_battery() else 'no'}")


if __name__ == "__main__":
    main()
