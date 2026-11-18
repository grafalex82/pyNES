"""Store read-only memory independently of cartridge files and CPU address routing."""


class ROM:
    """Read-only memory with byte access and PermissionError on writes.
    Byte offsets start at zero; CPU address routing and mirroring belong to Machine.
    """

    def __init__(self, data):
        self._rom = bytes(data)


    def read_byte(self, offset):
        return self._rom[offset]


    def write_byte(self, offset, value):
        # PermissionError is a diagnostic trap; a hardware NROM write does not alter ROM or select banks.
        raise PermissionError(f"Cannot write ROM at offset 0x{offset:04X}")
