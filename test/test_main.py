"""Verify the console entry point using a synthetic cartridge."""

from pathlib import Path
import subprocess
import sys


SCRIPT = Path(__file__).resolve().parents[1] / "main.py"


def test_help_without_cartridge(tmp_path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], cwd=tmp_path, capture_output=True, text=True, timeout=10,
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "rom" in result.stdout
    assert result.stderr == ""


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
