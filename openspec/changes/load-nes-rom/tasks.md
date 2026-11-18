# Tasks

## 1. Minimal test setup

- [x] 1.1 Add pytest requirements and configuration for `src` imports and `test`; verify pytest and configured paths.

## 2. Cartridge file loading

- [x] 2.1 Implement NESFile metadata and section extraction; verify focused tests for valid iNES/NES 2.0 files.
- [x] 2.2 Keep unsupported format features explicit; verify NotImplementedError tests and document parser decisions.
- [x] 2.3 Add a local has_trainer flag and NESFile getters; migrate callers and verify existing tests.
- [x] 2.4 Extract synthetic NES file creation into a pytest fixture; preserve and verify all parsing scenarios.

## 3. Standalone inspection utility

- [x] 3.1 Add `misc/nesinfo.py` with basic parameter output; verify CLI tests for both formats and paths with spaces.
- [x] 3.2 Update usage, current-state notes, and valid-input guidance; verify examples and README naming constraints.

## 4. Integration checks

- [x] 4.1 Run the pytest suite; verify all tests pass without depending on local game ROMs.
- [x] 4.2 Inspect the local ROM; verify expected metadata and unchanged SHA-256.
- [x] 4.3 Validate OpenSpec and edited text formatting; verify strict validation and the 120-character limit.
