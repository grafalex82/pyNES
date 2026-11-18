"""Verify RAM byte access and value-range errors using valid offsets."""

import pytest

from ram import RAM


@pytest.mark.parametrize("size", [1, 16, 2048])
def test_initializes_ram_with_zeroes(size):
    ram = RAM(size)
    assert [ram.read_byte(offset) for offset in range(size)] == [0] * size


def test_reads_and_overwrites_all_byte_values():
    # Distinct contents expose accidental aliasing between device offsets.
    ram = RAM(256)
    for offset in range(256):
        ram.write_byte(offset, offset)
    assert [ram.read_byte(offset) for offset in range(256)] == list(range(256))

    # Overwriting every location also verifies that writing zero replaces a previous nonzero byte.
    for offset in range(256):
        ram.write_byte(offset, 255 - offset)
    assert [ram.read_byte(offset) for offset in range(256)] == list(reversed(range(256)))


@pytest.mark.parametrize("value", [-1, 256])
def test_rejects_out_of_range_values_without_changing_ram(value):
    # Existing data makes a rejected write distinguishable from storing or truncating the value.
    ram = RAM(3)
    ram.write_byte(0, 0x12)
    ram.write_byte(1, 0x34)
    ram.write_byte(2, 0x56)

    # Both sides of the byte range must report the value and the accepted range.
    with pytest.raises(ValueError, match=rf"{value}.*0\.\.255"):
        ram.write_byte(1, value)

    # Rejection preserves both the target byte and its neighbors.
    assert [ram.read_byte(offset) for offset in range(3)] == [0x12, 0x34, 0x56]


def test_boundary_writes_leave_other_bytes_unchanged():
    # The first and last physical bytes must store different values independently.
    ram = RAM(2048)
    ram.write_byte(0, 0x12)
    ram.write_byte(2047, 0xAB)

    # Checking every byte includes both neighbors and the untouched middle of the buffer.
    assert [ram.read_byte(offset) for offset in range(2048)] == [0x12] + [0] * 2046 + [0xAB]


def test_ram_instances_have_independent_storage():
    # Creating another RAM must neither inherit nor clear existing contents.
    first = RAM(16)
    first.write_byte(0, 0x12)
    first.write_byte(15, 0xAB)
    second = RAM(16)
    assert [second.read_byte(offset) for offset in range(16)] == [0] * 16
    assert [first.read_byte(offset) for offset in range(16)] == [0x12] + [0] * 14 + [0xAB]

    # Writes in the second buffer must leave the first buffer intact.
    second.write_byte(0, 0x34)
    second.write_byte(15, 0xCD)
    assert [second.read_byte(offset) for offset in range(16)] == [0x34] + [0] * 14 + [0xCD]
    assert [first.read_byte(offset) for offset in range(16)] == [0x12] + [0] * 14 + [0xAB]
