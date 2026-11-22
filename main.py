"""Run a local NES cartridge until an unimplemented behavior is encountered."""

import argparse
import logging
from pathlib import Path
import sys

import pygame

# Resolve components relative to this script, independently of the caller's working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from background_inspection import render_background_inspection
from emulator import Emulator
from frame_display import FrameDisplay
from machine import Machine
from nesfile import NESFile


_CONTROLLER_KEYS = {
    pygame.K_UP: (0, "Up"),
    pygame.K_DOWN: (0, "Down"),
    pygame.K_LEFT: (0, "Left"),
    pygame.K_RIGHT: (0, "Right"),
    pygame.K_RETURN: (0, "Start"),
    pygame.K_RSHIFT: (0, "Select"),
    pygame.K_w: (1, "Up"),
    pygame.K_s: (1, "Down"),
    pygame.K_a: (1, "Left"),
    pygame.K_d: (1, "Right"),
    pygame.K_g: (1, "A"),
    pygame.K_f: (1, "B"),
    pygame.K_t: (1, "Start"),
    pygame.K_r: (1, "Select"),
}
_CONTROLLER_SCANCODES = {
    getattr(pygame, "KSCAN_PERIOD", -1): (0, "A"),
    getattr(pygame, "KSCAN_COMMA", -1): (0, "B"),
}


def _handle_input_event(event, machine):
    """Apply keyboard button changes and report whether F1 was pressed."""
    # Releasing all held buttons prevents stuck input after focus leaves the window.
    if event.type == getattr(pygame, "WINDOWFOCUSLOST", -1):
        for controller in machine.controllers:
            for button in ("A", "B", "Select", "Start", "Up", "Down", "Left", "Right"):
                controller.set_button(button, False)
        return False

    # F1 keeps its inspection toggle independent from controller button state.
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
        return True

    # Resolve punctuation by physical key position, with key symbols as a fallback.
    if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
        return False
    mapping = _CONTROLLER_KEYS.get(event.key)
    scancode = getattr(event, "scancode", None)
    if scancode in _CONTROLLER_SCANCODES:
        mapping = _CONTROLLER_SCANCODES[scancode]
    if mapping is not None:
        player, button = mapping
        machine.controllers[player].set_button(button, event.type == pygame.KEYDOWN)
    return False


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
        inspect_background = False

        # Process events between bounded blocks and present only newly completed frames.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if _handle_input_event(event, machine):
                    inspect_background = not inspect_background
            emulator.run(1000)
            completed_frame = machine.ppu.completed_frame
            if completed_frame is not None and completed_frame[0] != last_frame_number:
                last_frame_number, frame = completed_frame
                if inspect_background:
                    frame = render_background_inspection(machine.ppu.completed_background)
                display.present(frame)
            display.update_fps()
    finally:
        # Release the display on both window close and propagated execution errors.
        pygame.display.quit()


if __name__ == "__main__":
    main()
