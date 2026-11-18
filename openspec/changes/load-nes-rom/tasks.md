# Tasks

## 1. Minimal test setup

- [ ] 1.1 Add pytest requirements and configuration for `src` imports and `test`; verify pytest and configured paths.

## 2. Cartridge file loading

- [ ] 2.1 Implement NESFile metadata and section extraction; verify focused tests for valid iNES/NES 2.0 files.
- [ ] 2.2 Keep unsupported format features explicit; verify NotImplementedError tests and document parser decisions.

## 3. Standalone inspection utility

- [ ] 3.1 Add `misc/nesinfo.py` with basic parameter output; verify CLI tests for both formats and paths with spaces.
- [ ] 3.2 Update usage, current-state notes, and valid-input guidance; verify examples and README naming constraints.

## 4. Integration checks

- [ ] 4.1 Run the pytest suite; verify all tests pass without depending on local game ROMs.
- [ ] 4.2 Inspect the local ROM; verify expected metadata and unchanged SHA-256.
- [ ] 4.3 Validate OpenSpec and edited text formatting; verify strict validation and the 120-character limit.
