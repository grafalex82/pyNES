"""Verify approximate PPU vblank timing with synthetic execution."""

import pytest

from emulator import Emulator


def test_vblank_boundaries_and_status_reads_do_not_shift_the_phase(make_cpu):
    # Reads before vblank do not advance time or cause the flag to alternate.
    _, machine = make_cpu()
    machine.ppu.advance(27393)
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS
    assert machine.read_byte(0x200A) == 0x00  # PPUSTATUS mirror
    assert machine.ppu._frame_cycle == 27393

    # At the boundary, the first status read reports and clears vblank without changing phase.
    machine.ppu.advance(1)
    machine.write_byte(0x2006, 0x20)  # PPUADDR: start an incomplete address pair
    assert machine.read_byte(0x3FFA) == 0x80  # PPUSTATUS mirror
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS
    machine.write_byte(0x2006, 0x3F)  # PPUADDR: start a new pair after the status read
    machine.write_byte(0x2006, 0x00)  # PPUADDR: complete address $3F00
    assert machine.ppu._vram_address == 0x3F00
    machine.ppu.advance(100)
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS remains clear during the same vblank
    assert machine.ppu._frame_cycle == 27494

    # A later frame sets the flag again at its own boundary, independent of the earlier reads.
    machine.ppu.advance(29781 - 27494 + 27393)
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS: one cycle before vblank
    machine.ppu.advance(1)
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS: next vblank


def test_unread_vblank_is_cleared_at_prerender_boundary(make_cpu):
    _, machine = make_cpu()
    machine.ppu.advance(29666)
    assert machine.ppu._vblank is True
    machine.ppu.advance(1)
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS: cleared at cycle 29667


def test_large_advance_crosses_multiple_frames_without_polling(make_cpu):
    # Cross several complete frames and stop one cycle before a later vblank starts.
    _, machine = make_cpu()
    machine.ppu.advance(29781 * 4 + 27393)
    assert machine.ppu._frame_cycle == 27393
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS

    # Vblank recurs even without polling and a large advance still processes all boundaries.
    machine.ppu.advance(1)
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS
    machine.ppu.advance(29781 * 3)
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS: another frame's vblank


def test_emulator_advances_only_for_completed_instructions(make_cpu):
    # NOP, LDA immediate, and STA zero page take two, two, and three nominal cycles.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)  # NOP
    machine.write_byte(0x0001, 0xA9)  # LDA #$5A
    machine.write_byte(0x0002, 0x5A)
    machine.write_byte(0x0003, 0x85)  # STA $20
    machine.write_byte(0x0004, 0x20)
    machine.write_byte(0x0005, 0x02)  # Unsupported opcode
    emulator = Emulator(machine)
    emulator.step()
    emulator.step()
    emulator.step()
    assert emulator.cpu.cycles == 7
    assert machine.ppu._frame_cycle == 7
    assert machine.read_byte(0x0020) == 0x5A

    # Zero-budget runs, failed instructions, and CPU reset do not advance or reconstruct the PPU.
    emulator.run(0)
    with pytest.raises(NotImplementedError, match="opcode 0x02"):
        emulator.step()
    assert machine.ppu._frame_cycle == 7
    emulator.reset()
    assert machine.ppu._frame_cycle == 7


def test_zero_budget_and_cpu_reset_preserve_an_active_vblank(make_cpu):
    _, machine = make_cpu()
    emulator = Emulator(machine)
    machine.ppu.advance(27394)
    emulator.run(0)
    emulator.reset()
    assert machine.ppu._frame_cycle == 27394
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS: vblank survives both operations


def test_cpu_status_read_occurs_before_completed_instruction_advances_video(make_cpu):
    # The four-cycle LDA reaches vblank only after it has read the previous status through Machine.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xAD)  # LDA $2002
    machine.write_byte(0x0001, 0x02)
    machine.write_byte(0x0002, 0x20)
    emulator = Emulator(machine)
    machine.ppu.advance(27390)
    emulator.step()
    assert emulator.cpu.a == 0x00
    assert emulator.cpu.cycles == 4
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS: vblank began at the instruction boundary


def test_vblank_recurs_during_bounded_execution_without_nmi(make_cpu):
    # A two-instruction loop lets a real CPU advance PPU timing through multiple frames.
    _, machine = make_cpu()
    machine.write_byte(0x0000, 0xEA)  # NOP
    machine.write_byte(0x0001, 0x4C)  # JMP $0000
    machine.write_byte(0x0002, 0x00)
    machine.write_byte(0x0003, 0x00)
    emulator = Emulator(machine)

    # The requested budget may finish after a boundary, but vblank is still visible without NMI enabled.
    emulator.run(27393)
    assert emulator.cpu.cycles == 27395
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS
    emulator.run(1)
    assert machine.read_byte(0x2002) == 0x00  # PPUSTATUS remains clear in this vblank
    emulator.run(29781)
    assert machine.read_byte(0x2002) == 0x80  # PPUSTATUS: next frame
