"""Provide execution controls for a connected NES machine."""

from cpu import CPU


class Emulator:
    """Own a CPU connected to the supplied Machine."""

    def __init__(self, machine):
        self._machine = machine
        self._cpu = CPU(machine)


    @property
    def cpu(self):
        """Expose CPU state for inspection."""
        return self._cpu


    def step(self):
        """Execute one instruction on the connected CPU."""
        # Only a completed instruction contributes its nominal cycles to video progress.
        previous_cycles = self._cpu.cycles
        self._cpu.step()
        self._machine.ppu.advance(self._cpu.cycles - previous_cycles)


    def run(self, cycles):
        """Execute whole instructions until the requested cycle budget is reached."""
        # Each call measures its budget from the actual cumulative cycle count.
        target = self._cpu.cycles + cycles

        # Use the shared step boundary so future controls apply to both paths.
        while self._cpu.cycles < target:
            self.step()


    def reset(self):
        """Apply the existing repeated reset to the connected CPU."""
        self._cpu.reset()
