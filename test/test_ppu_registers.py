"""Verify PPU address register effects through CPU address routing."""

import pytest


def test_ppuscroll_and_ppuaddr_share_temporary_address_and_toggle(make_cpu):
    # PPUCTRL supplies nametable bits; a mirrored scroll pair supplies coarse and fine positions.
    _, machine = make_cpu()
    ppu = machine.ppu
    machine.write_byte(0x2000, 0x03)
    machine.write_byte(0x200D, 0x7D)
    machine.write_byte(0x3FFD, 0x5E)
    assert ppu._fine_x == 5
    assert ppu._scroll_address_latch == 0x6D6F
    assert not ppu._awaiting_second_write

    # A status read interrupts a partial pair and the next scroll write starts horizontally.
    machine.write_byte(0x2005, 0xFF)
    machine.read_byte(0x200A)
    machine.write_byte(0x2005, 0x12)
    machine.write_byte(0x2005, 0x34)
    assert ppu._fine_x == 2
    assert ppu._scroll_address_latch & 0x001F == 2
    assert ppu._scroll_address_latch & 0x73E0 == 0x40C0

    # Switching ports within a pair commits the combined temporary address through PPUADDR.
    machine.write_byte(0x2005, 0x2B)
    before = ppu._scroll_address_latch
    machine.write_byte(0x2006, 0xA5)
    assert ppu._vram_address == (before & 0x7F00) | 0xA5
    machine.write_byte(0x2006, 0x21)
    machine.write_byte(0x2005, 0x1B)
    assert not ppu._awaiting_second_write
    assert ppu._scroll_address_latch & 0x73E0 == 0x3060


def test_oam_ports_write_wrap_and_read_without_increment(make_cpu):
    # Writes through mirrored ports advance from $FF through $00 to $01.
    _, machine = make_cpu()
    machine.write_byte(0x200B, 0xFF)
    machine.write_byte(0x2004, 0xA5)
    machine.write_byte(0x3FFC, 0x5A)
    machine.write_byte(0x2004, 0xC3)

    # Selecting each location confirms the bytes and that repeated reads do not advance.
    for address, expected in ((0xFF, 0xA5), (0x00, 0x5A), (0x01, 0xC3)):
        machine.write_byte(0x3FFB, address)
        assert machine.read_byte(0x200C) == expected
        assert machine.read_byte(0x2004) == expected


def test_oam_is_zero_initialized_and_independent_between_machines(make_cpu):
    _, first = make_cpu()
    _, second = make_cpu()
    first.write_byte(0x2004, 0xFF)
    first.write_byte(0x2003, 0)
    assert first.read_byte(0x2004) == 0xFF
    assert second.read_byte(0x2004) == 0


@pytest.mark.parametrize("first_port,second_port", [(0x2006, 0x2006), (0x200E, 0x3FFE), (0x3FFE, 0x2006)])
@pytest.mark.parametrize("high,low,expected", [(0x00, 0x00, 0x0000), (0x21, 0x34, 0x2134),
                                               (0xFF, 0xA5, 0x3FA5)])
def test_ppuaddr_commits_after_two_writes_and_masks_high_bits(make_cpu, first_port, second_port, high, low, expected):
    # Establish an address so the first byte of the next pair cannot be mistaken for a committed address.
    _, machine = make_cpu()
    machine.write_byte(0x2006, 0x12)
    machine.write_byte(0x2006, 0x34)
    assert machine.ppu._vram_address == 0x1234

    # Mirrored ports use the same latch; bits 6 and 7 of the high byte are ignored.
    machine.write_byte(first_port, high)
    assert machine.ppu._vram_address == 0x1234
    machine.write_byte(second_port, low)
    assert machine.ppu._vram_address == expected


@pytest.mark.parametrize("status_port", [0x2002, 0x200A, 0x3FFA])
def test_status_read_restarts_an_interrupted_address_pair(make_cpu, status_port):
    # A completed address survives an interrupted pair and a status read.
    _, machine = make_cpu()
    machine.write_byte(0x2006, 0x20)
    machine.write_byte(0x2006, 0x55)
    machine.write_byte(0x200E, 0x3F)
    assert machine.read_byte(status_port) == 0x00
    assert machine.ppu._vram_address == 0x2055

    # The next write starts a new high/low pair, regardless of which aliases are used.
    machine.write_byte(0x3FFE, 0x12)
    assert machine.ppu._vram_address == 0x2055
    machine.write_byte(0x2006, 0xAB)
    assert machine.ppu._vram_address == 0x12AB
    assert machine.read_byte(status_port) == 0x00


def test_status_write_and_other_register_writes_do_not_reset_the_address_pair(make_cpu):
    _, machine = make_cpu()
    machine.write_byte(0x2006, 0x23)
    machine.write_byte(0x2002, 0xFF)
    machine.write_byte(0x2000, 0x80)
    machine.write_byte(0x2006, 0x45)
    assert machine.ppu._vram_address == 0x2345


def test_ppuaddr_write_latches_are_independent_between_machines(make_cpu):
    # Starting a pair on one PPU must not alter another PPU's address or next-write state.
    _, first = make_cpu()
    _, second = make_cpu()
    first.write_byte(0x2006, 0x21)
    second.write_byte(0x2006, 0x3F)
    second.write_byte(0x2006, 0x20)
    first.write_byte(0x2006, 0x34)
    assert first.ppu._vram_address == 0x2134
    assert second.ppu._vram_address == 0x3F20


@pytest.mark.parametrize("control,step", [(0x00, 1), (0x04, 32), (0xFB, 1), (0xFF, 32)])
def test_ppudata_writes_successive_nametable_bytes(make_cpu, control, step):
    # Mirrored CPU ports select the address, increment mode, and data register.
    _, machine = make_cpu()
    machine.write_byte(0x2008, control)  # PPUCTRL mirror ($2000)
    machine.write_byte(0x200E, 0x20)     # PPUADDR mirror ($2006): high byte
    machine.write_byte(0x3FFE, 0x12)     # PPUADDR mirror ($2006): low byte
    machine.write_byte(0x2007, 0xA5)     # PPUDATA
    machine.write_byte(0x200F, 0x5A)     # PPUDATA mirror ($2007)
    machine.write_byte(0x3FFF, 0xC3)     # PPUDATA mirror ($2007)

    # The first write targets the selected byte; subsequent writes use the requested increment.
    assert machine.ppu.read_vram(0x2012) == 0xA5
    assert machine.ppu.read_vram(0x2012 + step) == 0x5A
    assert machine.ppu.read_vram(0x2012 + 2 * step) == 0xC3
    assert machine.ppu._vram_address == 0x2012 + 3 * step


def test_ppudata_defaults_to_increment_one_and_tracks_control_changes(make_cpu):
    _, machine = make_cpu()
    machine.write_byte(0x2006, 0x20)  # PPUADDR: high byte of $2010
    machine.write_byte(0x2006, 0x10)  # PPUADDR: low byte of $2010
    machine.write_byte(0x2007, 0x11)  # PPUDATA: store at $2010, advance by the default step of 1
    machine.write_byte(0x2000, 0x04)  # PPUCTRL: set bit 2 to select an increment of 32
    machine.write_byte(0x2007, 0x22)  # PPUDATA: store at $2011, then advance to $2031
    machine.write_byte(0x2000, 0x00)  # PPUCTRL: clear bit 2 to select an increment of 1
    machine.write_byte(0x2007, 0x33)  # PPUDATA: store at $2031, then advance to $2032
    assert machine.ppu.read_vram(0x2010) == 0x11
    assert machine.ppu.read_vram(0x2011) == 0x22
    assert machine.ppu.read_vram(0x2031) == 0x33
    assert machine.ppu._vram_address == 0x2032


def test_ppudata_uses_palette_mirrors_and_six_bit_values(make_cpu):
    _, machine = make_cpu()
    machine.write_byte(0x2006, 0x3F)  # PPUADDR: high byte
    machine.write_byte(0x2006, 0x30)  # PPUADDR: low byte
    machine.write_byte(0x2007, 0xE1)  # PPUDATA
    machine.write_byte(0x2007, 0xFF)  # PPUDATA
    assert machine.ppu.read_vram(0x3F00) == 0x21
    assert machine.ppu.read_vram(0x3F11) == 0x3F
    assert machine.ppu._vram_address == 0x3F32


@pytest.mark.parametrize("control,step", [(0x00, 1), (0x04, 32)])
def test_ppudata_wraps_internal_address_and_masks_video_bus(make_cpu, control, step):
    # Start just below the 15-bit boundary; the write is decoded on the 14-bit PPU bus.
    _, machine = make_cpu()
    machine.ppu._vram_address = 0x7FFF
    machine.write_byte(0x2000, control)  # PPUCTRL
    machine.write_byte(0x2007, 0x2A)     # PPUDATA
    assert machine.ppu.read_vram(0x3FFF) == 0x2A
    assert machine.ppu._vram_address == step - 1


def test_ppudata_rejected_chr_write_does_not_advance_address(make_cpu):
    # The synthetic PRG-only cartridge has no supported CHR memory.
    _, machine = make_cpu()
    machine.write_byte(0x2006, 0x00)  # PPUADDR: high byte
    machine.write_byte(0x2006, 0x10)  # PPUADDR: low byte
    with pytest.raises(NotImplementedError, match="CHR RAM"):
        machine.write_byte(0x2007, 0xA5)  # PPUDATA
    assert machine.ppu._vram_address == 0x0010
