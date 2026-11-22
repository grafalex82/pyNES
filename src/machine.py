"""Route CPU byte access to internal RAM and fixed mapper-0 PRG ROM."""

from apu import APU
from ppu import PPU
from ram import RAM
from rom import ROM


class Machine:
    """Connect memory devices and route accesses in the NES CPU address space.

    Machine is the system's assembly and address-routing component. RAM and ROM own
    their bytes; Machine selects a device and translates a CPU address into an offset
    within that device. CPU uses read_byte(address) and write_byte(address, value)
    for every memory access, including memory-mapped I/O.
    Devices therefore do not need to know where they appear in the CPU address space.

    Construction takes an already parsed NESFile and uses its getters without
    reopening the file. The current configuration supports mapper 0 (fixed NROM
    wiring), submapper 0, no trainer, and exactly 16 KiB or 32 KiB of PRG ROM.
    Other configurations raise NotImplementedError. CHR ROM is connected to the
    PPU's separate video address space, not to this CPU memory interface.

    CPU memory map, with inclusive hexadecimal address ranges:
        $0000-$07FF  Internal RAM: one writable 2048-byte buffer.
        $0800-$1FFF  Three mirrors of the same internal RAM.
        $2000-$3FFF  PPU registers and mirrors; status, video address, and data access.
        $4000        Pulse 1 control; dummy writes, reads unsupported.
        $4004        Pulse 2 control; dummy writes, reads unsupported.
        $4008        Triangle control; dummy writes, reads unsupported.
        $400C        Noise control; dummy writes, reads unsupported.
        $4001-$4003, $4005-$4007, $4009-$400B, $400D-$400F  Other APU registers; not connected yet.
        $4010-$4013  DMC registers; dummy writes and zero reads.
        $4014        Sprite DMA; page transfer without stall, reads unsupported.
        $4015        APU status/control; dummy writes and zero reads.
        $4016        Controller 1; writes ignored and reads return zero.
        $4017        Controller 2 read returns zero; APU frame-counter write ignored.
        $4018-$401F  Normally disabled APU and I/O functionality; not connected yet.
        $4020-$5FFF  Cartridge expansion area; not connected yet.
        $6000-$7FFF  Cartridge RAM when present; not connected yet.
        $8000-$BFFF  First 16 KiB of PRG ROM.
        $C000-$FFFF  Second 16 KiB of PRG ROM, or a mirror of the first for a 16 KiB image.

    RAM uses offset address & 0x07FF, so $0000, $0800, $1000, and $1800 all select
    the same byte. A write through any mirror is immediately visible through every
    alias; no copies are synchronized. Each Machine owns independent RAM, initially
    filled with zeroes for reproducibility rather than to model hardware power-up.

    PRG ROM uses offset (address - 0x8000) & (PRG size - 1). The mask is 0x3FFF for
    a 16 KiB image and 0x7FFF for a 32 KiB image. These fixed mappings require no
    bank-switching state. ROM writes reach the ROM device and propagate its
    PermissionError unchanged, preserving both ROM and RAM. This is a diagnostic
    trap: hardware NROM writes do not change ROM or select banks.

    Reads and writes in $2000-$3FFF are routed to PPU register offsets. PPU status
    reports and clears timed vblank, and PPUDATA reads use a video read buffer.
    OAMDATA reads access object memory. Other PPU reads raise NotImplementedError identifying the register offset.
    Reads and writes at $4010-$4013 and $4015
    route to a dummy APU; writes have no effects and reads return $00. Writes at
    $4017 are also ignored by the APU. Writes to $4014 copy a CPU page into OAM without a stall.
    Writes to $4016 are ignored; controller reads at $4016/$4017 return zero. Other reads
    and writes in $4000-$7FFF raise NotImplementedError identifying the CPU address.

    Addresses are assumed to be valid 16-bit CPU addresses ($0000-$FFFF).
    RAM rejects integer byte values outside 0..255 with ValueError.

    This component provides byte access only. It does not construct a CPU, reset the
    system, execute instructions, or advance timing.
    """

    def __init__(self, cartridge):
        # Other cartridge wiring and trainer placement need their own implementations.
        mapper = cartridge.get_mapper()
        submapper = cartridge.get_submapper()
        if mapper != 0:
            raise NotImplementedError(f"Cartridge mapper {mapper} is not implemented")
        if submapper != 0:
            raise NotImplementedError(f"Mapper 0 submapper {submapper} is not implemented")
        if cartridge.get_trainer():
            raise NotImplementedError("Cartridge trainer placement is not implemented")

        # NROM exposes either one mirrored 16 KiB image or one complete 32 KiB image.
        prg_rom = cartridge.get_prg_rom()
        if len(prg_rom) not in (16384, 32768):
            raise NotImplementedError(f"Mapper 0 PRG ROM size {len(prg_rom)} bytes is not implemented")

        # Devices own their storage; Machine converts CPU addresses to device-relative offsets.
        self._ram = RAM(2048)
        self._rom = ROM(prg_rom)
        chr_rom = cartridge.get_chr_rom()
        self.ppu = PPU(ROM(chr_rom), len(chr_rom), RAM(2048), cartridge.get_mirroring())
        self.apu = APU()
        self._prg_mask = len(prg_rom) - 1


    def read_byte(self, address):
        # Only the low eleven address bits select a physical internal RAM byte.
        if address < 0x2000:
            return self._ram.read_byte(address & 0x07FF)

        # The low three address bits select one of eight mirrored PPU registers.
        if address < 0x4000:
            return self.ppu.read_byte(address & 0x07)

        # Controller reads return a fixed no-input response until controller behavior is implemented.
        if address in (0x4016, 0x4017):
            return 0

        # Route only the selected APU registers, leaving sprite DMA reads unconnected.
        if 0x4010 <= address <= 0x4013 or address == 0x4015:
            return self.apu.read_byte(address - 0x4000)

        # The PRG mask repeats a 16 KiB image and preserves every offset of a 32 KiB image.
        if address >= 0x8000:
            return self._rom.read_byte((address - 0x8000) & self._prg_mask)

        # Unconnected device registers and cartridge RAM must remain visible as missing behavior.
        raise NotImplementedError(f"CPU read at address 0x{address:04X} is not implemented")


    def write_byte(self, address, value):
        # Every RAM alias writes the same physical buffer.
        if address < 0x2000:
            self._ram.write_byte(address & 0x07FF, value)
            return

        # The low three address bits select one of eight mirrored PPU registers.
        if address < 0x4000:
            self.ppu.write_byte(address & 0x07, value)
            return

        # DMA reads through the CPU map and writes through OAMDATA, preserving its address wrapping.
        if address == 0x4014:
            for offset in range(256):
                self.ppu.write_byte(4, self.read_byte((value << 8) | offset))
            return

        # Controller strobing is not implemented; temporarily accept its writes without effects.
        if address == 0x4016:
            return

        # APU writes include the frame counter, while reads at $4017 address controller 2.
        if address in (0x4000, 0x4004, 0x4008, 0x400C) or 0x4010 <= address <= 0x4013 or address in (0x4015, 0x4017):
            self.apu.write_byte(address - 0x4000, value)
            return

        # Delegate ROM writes so the device's diagnostic PermissionError propagates unchanged.
        if address >= 0x8000:
            self._rom.write_byte((address - 0x8000) & self._prg_mask, value)
            return

        # Missing devices must not silently accept writes.
        raise NotImplementedError(f"CPU write at address 0x{address:04X} is not implemented")
