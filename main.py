"""Run a local NES cartridge until an unimplemented behavior is encountered."""

import argparse
import logging
from pathlib import Path
import sys

import pygame

# Resolve components relative to this script, independently of the caller's working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from emulator import Emulator
from frame_display import FrameDisplay
from machine import Machine
from nesfile import NESFile


def main():
    # Leave relative cartridge paths relative to the caller's working directory.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", help="path to a valid iNES or NES 2.0 cartridge file")
    parser.add_argument("--debug", action="store_true", help="enable detailed CPU and device logging")
    args = parser.parse_args()

    # Opt in before CPU construction so the startup reset is included in a detailed log.
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.CRITICAL + 1, format="%(message)s")
    cartridge = NESFile(args.rom)
    machine = Machine(cartridge)
    emulator = Emulator(machine)

    # Present the initial PPU state and enable completed-frame capture before execution starts.
    try:
        display = FrameDisplay()
        display.present(machine.ppu.render_frame())
        machine.ppu.enable_frame_output()
        last_frame_number = 0

        # Process events between bounded blocks and present only newly completed frames.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            emulator.run(1000)
            completed_frame = machine.ppu.completed_frame
            if completed_frame is not None and completed_frame[0] != last_frame_number:
                last_frame_number, frame = completed_frame
                display.present(frame)
            display.update_fps()
    finally:
        # Release the display on both window close and propagated execution errors.
        pygame.display.quit()


if __name__ == "__main__":
    main()
