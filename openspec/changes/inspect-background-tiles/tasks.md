# Tasks

## 1. Inspect the stationary background

- [ ] 1.1 Capture immutable nametable, attribute and palette data alongside each completed frame; use synthetic pytest
      cases to verify capture timing, subsequent memory writes, and unchanged emulated state.
- [ ] 1.2 Render the 3 by 7 hexadecimal glyphs and four color swatches from captured data; use focused pytest cases
      for leading zeroes, frame edges, all attribute quadrants, universal backdrop, and disabled background.
- [ ] 1.3 Connect F1 to select the normal or inspection image in the host loop; verify startup default, both toggles,
      continued execution, frame scaling, and independence from `--debug` with synthetic tests.
- [ ] 1.4 Document the key, pixel layout, swatch meaning, stationary-background limits and frame sampling in README.md
      and doc/decisions.md; review those descriptions against the implemented behavior.
- [ ] 1.5 Run the focused PPU, frame display and host-loop pytest tests and report their results.
