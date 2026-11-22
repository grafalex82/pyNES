"""Model the serial interface of a standard NES controller."""

import logging


logger = logging.getLogger("controller")
_BUTTONS = ("A", "B", "Select", "Start", "Up", "Down", "Left", "Right")


class Controller:
    """Keep current buttons separate from the report captured by the strobe."""

    def __init__(self):
        self._buttons = 0
        self._shift = 0
        self._strobe = False


    def set_button(self, button, pressed):
        """Set one named button without changing an already latched report."""
        # Each button occupies its position in the serial report.
        mask = 1 << _BUTTONS.index(button)
        previous = self._buttons
        self._buttons = (self._buttons | mask) if pressed else (self._buttons & ~mask)

        # Repeated host events do not produce redundant device logs.
        if self._buttons != previous:
            logger.debug("Controller button %s %s", button, "pressed" if pressed else "released")


    def write_strobe(self, value):
        """Capture buttons only on the high-to-low transition of bit 0."""
        # The falling edge captures a stable report for later reads.
        strobe = bool(value & 1)
        if self._strobe and not strobe:
            self._shift = self._buttons

        # Higher bits have no effect on the controller.
        self._strobe = strobe


    def read(self):
        """Return D0, with zero upper bits and ones after the eight-button report."""
        # A high strobe continuously exposes the current A button.
        if self._strobe:
            return self._buttons & 1

        # A low strobe shifts one captured bit out and fills the register with ones.
        value = self._shift & 1
        self._shift = (self._shift >> 1) | 0x80
        return value
