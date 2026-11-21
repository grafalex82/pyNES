"""Verify PPU address register effects through CPU address routing."""

import pytest


def test_ppuctrl_settings_start_cleared(make_cpu):
    _, machine = make_cpu()
    ppu = machine.ppu
    assert not any((ppu._base_nametable_x, ppu._base_nametable_y, ppu._increment_32,
                    ppu._sprite_pattern_table_high, ppu._background_pattern_table_high,
                    ppu._sprite_height_16, ppu._ext_output_enabled, ppu._nmi_enabled))
    assert ppu.last_writes[0] is None


@pytest.mark.parametrize("value,expected", [
    (0x00, (False, False, False, False, False, False, False, False)),
    (0x01, (True, False, False, False, False, False, False, False)),
    (0x02, (False, True, False, False, False, False, False, False)),
    (0x04, (False, False, True, False, False, False, False, False)),
    (0x08, (False, False, False, True, False, False, False, False)),
    (0x10, (False, False, False, False, True, False, False, False)),
    (0x20, (False, False, False, False, False, True, False, False)),
    (0x40, (False, False, False, False, False, False, True, False)),
    (0x80, (False, False, False, False, False, False, False, True)),
    (0xA5, (True, False, True, False, False, True, False, True)),
    (0xFF, (True, True, True, True, True, True, True, True)),
])
def test_ppuctrl_updates_all_named_settings(make_cpu, value, expected):
    # Start with all bits set so each write must also clear settings absent from the new value.
    _, machine = make_cpu()
    machine.write_byte(0x2000, 0xFF)
    machine.write_byte(0x3FF8, value)

    # Mirrored PPUCTRL writes decode each independent setting into a boolean.
    ppu = machine.ppu
    assert (ppu._base_nametable_x, ppu._base_nametable_y, ppu._increment_32,
            ppu._sprite_pattern_table_high, ppu._background_pattern_table_high,
            ppu._sprite_height_16, ppu._ext_output_enabled, ppu._nmi_enabled) == expected
    assert ppu.last_writes[0] == value


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
    assert machine.ppu.last_writes[6] == low


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
    assert machine.ppu.last_writes[2] == 0xFF


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
