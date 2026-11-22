"""Verify the console entry point using a synthetic cartridge."""

from pathlib import Path
import importlib.util
import subprocess
import sys

import pygame
import pytest

import frame_display


SCRIPT = Path(__file__).resolve().parents[1] / "main.py"


@pytest.fixture(autouse=True)
def dummy_display(monkeypatch):
    # A dummy window lets both direct and subprocess checks run without a desktop.
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    pygame.display.quit()
    yield
    pygame.display.quit()


@pytest.fixture
def main_module():
    spec = importlib.util.spec_from_file_location("pynes_main", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def make_cartridge(tmp_path):
    def create_cartridge(program):
        # A fixed PRG bank starts the synthetic program at $8000.
        header = b"NES\x1a" + bytes([1, 0]) + bytes(10)
        prg = bytearray(16384)
        prg[:len(program)] = program
        prg[-4:-2] = b"\x00\x80"
        path = tmp_path / "synthetic.nes"
        path.write_bytes(header + prg)
        return path

    return create_cartridge


def test_help_without_cartridge(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], cwd=tmp_path, capture_output=True, text=True, timeout=10,
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "rom" in result.stdout
    assert "--debug" in result.stdout
    assert result.stderr == ""


def test_help_does_not_initialize_display(main_module, monkeypatch, capsys):
    # Argument parsing exits before the display initializer can be called.
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), "--help"])
    monkeypatch.setattr(pygame.display, "init", lambda: pytest.fail("Help must not initialize the display"))
    with pytest.raises(SystemExit) as error:
        main_module.main()
    assert error.value.code == 0
    assert "usage:" in capsys.readouterr().out
    assert not pygame.display.get_init()


def test_synthetic_cartridge_updates_the_existing_window(main_module, make_cartridge, monkeypatch):
    # The program writes a first color, waits for vblank without NMI, then writes a second color.
    program = bytes([
        0xA9,  # LDA #$00: Leave PPUCTRL NMI disabled.
        0x00,
        0x8D,  # STA $2000: Apply PPUCTRL.
        0x00,
        0x20,
        0xA9,  # LDA #$3F: Load the high byte of palette address $3F00.
        0x3F,
        0x8D,  # STA $2006: Write the high byte through PPUADDR.
        0x06,
        0x20,
        0xA9,  # LDA #$00: Load the low byte of palette address $3F00.
        0x00,
        0x8D,  # STA $2006: Select the backdrop address.
        0x06,
        0x20,
        0xA9,  # LDA #$01: Load the first backdrop color.
        0x01,
        0x8D,  # STA $2007: Write the first backdrop color.
        0x07,
        0x20,
        0xAD,  # LDA $2002: Wait until PPUSTATUS reports vblank.
        0x02,
        0x20,
        0x10,  # BPL $8014: Keep polling while bit 7 is clear.
        0xFB,
        0xA9,  # LDA #$3F: Reload the high byte of palette address $3F00.
        0x3F,
        0x8D,  # STA $2006: Write the high byte through PPUADDR.
        0x06,
        0x20,
        0xA9,  # LDA #$00: Reload the low byte of palette address $3F00.
        0x00,
        0x8D,  # STA $2006: Select the backdrop address again.
        0x06,
        0x20,
        0xA9,  # LDA #$21: Load the second backdrop color.
        0x21,
        0x8D,  # STA $2007: Write the second backdrop color.
        0x07,
        0x20,
        0x4C,  # JMP $8028: Wait for the host to display the next frame.
        0x28,
        0x80,
    ])
    cartridge = make_cartridge(program)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(cartridge)])
    presentations = []
    observed_between_vblanks = []
    original_present = main_module.FrameDisplay.present
    original_run = main_module.Emulator.run

    def record_present(display, frame):
        original_present(display, frame)
        surface = pygame.display.get_surface()
        presentations.append((surface, surface.get_at((0, 0))[:3], surface.get_at((767, 719))[:3]))

    def run_block(emulator, cycles):
        # The initial frame and window must exist before the first instruction.
        if emulator.cpu.cycles == 0:
            assert emulator.cpu.pc == 0x8000
            assert pygame.display.get_surface().get_size() == (768, 720)
            assert len(presentations) == 1
        if emulator.cpu.cycles > 100000:
            pytest.fail("The second vblank did not arrive within the expected budget")
        original_run(emulator, cycles)
        ppu = emulator._machine.ppu
        assert not ppu._nmi_enabled
        if ppu.completed_frame and ppu.completed_frame[0] == 1 and len(presentations) == 2:
            if ppu.read_vram(0x3F00) == 0x21:
                assert pygame.display.get_surface().get_at((0, 0))[:3] == (0, 42, 136)
                observed_between_vblanks.append(True)
        if ppu.completed_frame and ppu.completed_frame[0] == 2:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    # The real CPU, PPU, and window run until the second completed frame is presented.
    monkeypatch.setattr(main_module.FrameDisplay, "present", record_present)
    monkeypatch.setattr(main_module.Emulator, "run", run_block)
    main_module.main()
    assert observed_between_vblanks
    assert len(presentations) == 3
    assert presentations[0][0] is presentations[1][0] is presentations[2][0]
    assert presentations[0][1:] == ((102, 102, 102), (102, 102, 102))
    assert presentations[1][1:] == ((0, 42, 136), (0, 42, 136))
    assert presentations[2][1:] == ((100, 176, 255), (100, 176, 255))
    assert not pygame.display.get_init()


def test_close_event_before_first_block_releases_display(main_module, make_cartridge, monkeypatch):
    cartridge = make_cartridge(bytes([0xEA]))
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(cartridge)])
    original_present = main_module.FrameDisplay.present

    def close_after_initial_frame(display, frame):
        original_present(display, frame)
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    # A close event stops execution before the first CPU block.
    monkeypatch.setattr(main_module.FrameDisplay, "present", close_after_initial_frame)
    monkeypatch.setattr(main_module.Emulator, "run", lambda *args: pytest.fail("CPU must not run after close"))
    main_module.main()
    assert not pygame.display.get_init()


def test_synthetic_cartridge_presents_nametable_tile(main_module, tmp_path, monkeypatch):
    # The program writes a tile and palette through CPU registers, then waits for the first completed frame.
    program = bytes([
        0xA9, 0x20, 0x8D, 0x06, 0x20, 0xA9, 0x00, 0x8D, 0x06, 0x20,
        0xA9, 0x01, 0x8D, 0x07, 0x20,
        0xA9, 0x3F, 0x8D, 0x06, 0x20, 0xA9, 0x01, 0x8D, 0x06, 0x20,
        0xA9, 0x21, 0x8D, 0x07, 0x20,
        0xA9, 0x08, 0x8D, 0x01, 0x20, 0x4C, 0x23, 0x80,
    ])
    prg = bytearray(16384)
    prg[:len(program)] = program
    prg[-4:-2] = b"\x00\x80"
    chr_rom = bytearray(8192)
    chr_rom[16] = 0x80
    cartridge = tmp_path / "tile.nes"
    cartridge.write_bytes(b"NES\x1a" + bytes([1, 1]) + bytes(10) + prg + chr_rom)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(cartridge)])
    original_present = main_module.FrameDisplay.present
    presentations = []

    def record_present(display, frame):
        original_present(display, frame)
        surface = pygame.display.get_surface()
        presentations.append((surface.get_at((0, 0))[:3], surface.get_at((3, 0))[:3]))
        if len(presentations) == 2:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    # The startup window displays the tile at scale 3 after vblank captures the changed nametable.
    monkeypatch.setattr(main_module.FrameDisplay, "present", record_present)
    main_module.main()
    assert presentations == [((102, 102, 102), (102, 102, 102)), ((100, 176, 255), (102, 102, 102))]
    assert not pygame.display.get_init()


@pytest.mark.parametrize("options", [[], ["--debug"]])
def test_f1_toggles_inspection_on_completed_frames(main_module, make_cartridge, monkeypatch, options):
    # A looping synthetic program keeps the CPU running with the background layer disabled.
    cartridge = make_cartridge(bytes([0x4C, 0x00, 0x80]))
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), *options, str(cartridge)])
    original_present = main_module.FrameDisplay.present
    original_run = main_module.Emulator.run
    presentations = []
    cycles_at_presentation = []
    current_cycles = [0]

    def run_block(emulator, cycles):
        original_run(emulator, cycles)
        current_cycles[0] = emulator.cpu.cycles
        if current_cycles[0] > 90000:
            pytest.fail("The two completed frames did not arrive")

    def record_present(display, frame):
        # Record pixels after real scaling in the original display surface.
        original_present(display, frame)
        surface = pygame.display.get_surface()
        samples = [surface.get_at(point)[:3] for point in ((0, 0), (2, 2), (3, 3), (5, 5), (0, 21), (5, 23))]
        presentations.append((surface, samples))
        cycles_at_presentation.append(current_cycles[0])

        # Two complete presses switch on and then off; key releases do not toggle the mode.
        if len(presentations) < 3:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F1))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_F1))
        else:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    # The inspection view appears at the next frame and normal output returns at the following frame.
    monkeypatch.setattr(main_module.Emulator, "run", run_block)
    monkeypatch.setattr(main_module.FrameDisplay, "present", record_present)
    main_module.main()
    gray = (102, 102, 102)
    white = (255, 255, 255)
    black = (0, 0, 0)
    assert [samples for _, samples in presentations] == [
        [gray] * 6,
        [white, white, black, black, gray, gray],
        [gray] * 6,
    ]
    assert presentations[0][0] is presentations[1][0] is presentations[2][0]
    assert 0 == cycles_at_presentation[0] < cycles_at_presentation[1] < cycles_at_presentation[2]


def test_fps_title_tracks_slow_frames_between_cpu_blocks(main_module, make_cartridge, monkeypatch):
    # Advance wall-clock time between PPU frames, starting with the initial preview at time zero.
    cartridge = make_cartridge(bytes([0xEA]))
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(cartridge)])
    now = [0.0]
    monkeypatch.setattr(frame_display, "monotonic", lambda: now[0])

    def run_block(emulator, cycles):
        if now[0] == 6:
            assert pygame.display.get_caption()[0] == "pyNES - 0.2 FPS"
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return
        now[0] += 1
        if now[0] == 5:
            emulator._machine.ppu.advance(27394)

    # The host keeps the measurement through empty blocks and updates after the completed frame.
    monkeypatch.setattr(main_module.Emulator, "run", run_block)
    main_module.main()
    assert not pygame.display.get_init()


def test_execution_error_releases_display_and_propagates(main_module, make_cartridge, monkeypatch):
    cartridge = make_cartridge(bytes([0x02]))
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(cartridge)])
    with pytest.raises(NotImplementedError, match="CPU opcode 0x02 at address 0x8000"):
        main_module.main()
    assert not pygame.display.get_init()


@pytest.mark.parametrize("options, logging_enabled", [([], False), (["--debug"], True)])
def test_cli_logging_is_opt_in(make_cartridge, options, logging_enabled):
    # SEI and CLD complete before an unsupported opcode ends both runs with a traceback.
    cartridge = make_cartridge(bytes([0x78, 0xD8, 0x02]))
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *options, str(cartridge)], capture_output=True, text=True, timeout=10,
    )

    # The flag controls reset and instruction logs, while the execution error remains visible in both modes.
    assert result.returncode != 0
    assert "NotImplementedError: CPU opcode 0x02 at address 0x8002" in result.stderr
    assert ("Reset completed:" in result.stderr) is logging_enabled
    assert ("8000   78" in result.stderr) is logging_enabled
    assert ("CYC=2" in result.stderr) is logging_enabled
    assert ("CYC=4" in result.stderr) is logging_enabled


def test_display_initialization_error_releases_display(main_module, make_cartridge, monkeypatch):
    cartridge = make_cartridge(bytes([0xEA]))
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(cartridge)])

    def fail_set_mode(size):
        raise RuntimeError("display initialization failed")

    # Even a failure after display.init() must release the partially initialized subsystem.
    monkeypatch.setattr(pygame.display, "set_mode", fail_set_mode)
    with pytest.raises(RuntimeError, match="display initialization failed"):
        main_module.main()
    assert not pygame.display.get_init()


def test_runs_relative_cartridge_path_from_another_directory(tmp_path):
    # A mapper-0 program executes SEI before the unsupported instruction at $8001.
    header = b"NES\x1a" + bytes([1, 0]) + bytes(10)
    prg = bytearray(16384)
    prg[:2] = bytes([0x78, 0x02])
    prg[0x3FFC:0x3FFE] = bytes([0x00, 0x80])
    cartridge = tmp_path / "cartridge with spaces.nes"
    cartridge.write_bytes(header + prg)

    # Run the absolute script path with a relative ROM path outside the repository.
    result = subprocess.run(
        [sys.executable, str(SCRIPT), cartridge.name], cwd=tmp_path, capture_output=True, text=True, timeout=10,
    )

    # The ordinary traceback identifies the next unsupported opcode and its address.
    assert result.returncode != 0
    assert "NotImplementedError" in result.stderr
    assert "0x02" in result.stderr
    assert "0x8001" in result.stderr


def test_continues_after_first_cycle_block(tmp_path):
    # The first 500 NOPs fill one block; the next NOP precedes $02 at $81F5.
    header = b"NES\x1a" + bytes([1, 0]) + bytes(10)
    prg = bytearray(16384)
    prg[:502] = bytes([0xEA]) * 501 + bytes([0x02])
    prg[0x3FFC:0x3FFE] = bytes([0x00, 0x80])
    cartridge = tmp_path / "cartridge.nes"
    cartridge.write_bytes(header + prg)

    # Bound the subprocess so a loop that fails to reach the next instruction cannot hang the suite.
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(cartridge)], capture_output=True, text=True, timeout=10,
    )

    # The diagnostic proves execution passed the first block and reached the intended instruction.
    assert result.returncode != 0
    assert "NotImplementedError: CPU opcode 0x02 at address 0x81F5 is not implemented" in result.stderr
