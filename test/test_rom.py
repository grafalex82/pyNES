"""Verify ROM reads and rejected writes using synthetic bytes."""

import pytest

from rom import ROM


@pytest.mark.parametrize("data", [b"\xA5", bytes(range(256))])
def test_reads_source_bytes(data):
    rom = ROM(data)
    assert [rom.read_byte(offset) for offset in range(len(data))] == list(data)


@pytest.mark.parametrize("offset, value", [(0, 0xFF), (128, 0x55), (255, 0xFF)])
def test_rejects_writes_without_changing_rom(offset, value):
    # Distinct bytes expose changes anywhere in the image, including its first and last bytes.
    data = bytes(range(256))
    rom = ROM(data)

    # Even writing the byte already present is forbidden and identifies the device offset.
    with pytest.raises(PermissionError, match=f"ROM at offset 0x{offset:04X}"):
        rom.write_byte(offset, value)

    # A rejected write must preserve the entire image, including the target and its neighbors.
    assert [rom.read_byte(index) for index in range(len(data))] == list(data)
