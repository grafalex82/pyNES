"""Read cartridge file metadata and sections without constructing emulated devices."""

from pathlib import Path


class NESFile:
    """An ordinary iNES or NES 2.0 file exposing metadata and immutable bytes through getters."""

    def __init__(self, filename):
        # The original header remains available for fields that are not decoded yet.
        data = Path(filename).read_bytes()
        self._header = header = data[:16]

        # Both formats share the low eight mapper bits and the low ROM size counts.
        self._mapper = (header[6] >> 4) | (header[7] & 0xF0)
        self._submapper = 0
        prg_count = header[4]
        chr_count = header[5]
        format_marker = header[7] & 0x0C
        if format_marker == 0:
            self._format = "iNES"
        elif format_marker == 0x08:
            self._format = "NES 2.0"
            self._mapper |= (header[8] & 0x0F) << 8
            self._submapper = header[8] >> 4
            prg_extension = header[9] & 0x0F
            chr_extension = header[9] >> 4
            if prg_extension == 0x0F:
                raise NotImplementedError("NES 2.0 PRG-ROM exponent-multiplier size is not implemented")
            if chr_extension == 0x0F:
                raise NotImplementedError("NES 2.0 CHR-ROM exponent-multiplier size is not implemented")
            prg_count |= prg_extension << 8
            chr_count |= chr_extension << 8
        else:
            raise NotImplementedError(f"Cartridge format marker 0x{format_marker:02X} is not implemented")

        # Other console types and extra ROM sections need interpretation beyond ordinary NES cartridge data.
        console_type = header[7] & 0x03
        if console_type:
            raise NotImplementedError(f"{self._format} console type 0x{console_type:02X} is not implemented")
        if format_marker == 0x08 and header[14] & 0x03:
            raise NotImplementedError("NES 2.0 miscellaneous ROM areas are not implemented")

        # These conventional mirroring labels describe header flags, not effective mapper behavior.
        self._battery = bool(header[6] & 0x02)
        if header[6] & 0x08:
            self._mirroring = "four-screen"
        else:
            self._mirroring = "vertical" if header[6] & 0x01 else "horizontal"

        # A trainer precedes PRG; PRG and CHR counts use 16 KiB and 8 KiB units respectively.
        has_trainer = bool(header[6] & 0x04)
        trainer_end = 16 + (512 if has_trainer else 0)
        prg_end = trainer_end + prg_count * 16384
        chr_end = prg_end + chr_count * 8192
        self._trainer = data[16:trainer_end]
        self._prg_rom = data[trainer_end:prg_end]
        self._chr_rom = data[prg_end:chr_end]


    def get_header(self):
        return self._header


    def get_format(self):
        return self._format


    def get_mapper(self):
        return self._mapper


    def get_submapper(self):
        return self._submapper


    def get_trainer(self):
        return self._trainer


    def get_prg_rom(self):
        return self._prg_rom


    def get_chr_rom(self):
        return self._chr_rom


    def get_mirroring(self):
        return self._mirroring


    def get_battery(self):
        return self._battery
