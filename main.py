"""Run a local NES cartridge until an unimplemented behavior is encountered."""

import argparse
import logging
from pathlib import Path
import sys

# Resolve components relative to this script, independently of the caller's working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from emulator import Emulator
from machine import Machine
from nesfile import NESFile


def main():
    # Leave relative cartridge paths relative to the caller's working directory.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", help="path to a valid iNES or NES 2.0 cartridge file")
    args = parser.parse_args()

    # Configure logging before CPU construction so the startup reset is visible.
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    cartridge = NESFile(args.rom)
    machine = Machine(cartridge)
    emulator = Emulator(machine)

    # Each block returns at an instruction boundary without resetting the machine.
    while True:
        emulator.run(1000)


if __name__ == "__main__":
    main()
