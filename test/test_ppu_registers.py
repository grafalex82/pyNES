"""Verify PPU address register effects through CPU address routing."""

import pytest


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
    assert machine.read_byte(status_port) == 0x80


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
