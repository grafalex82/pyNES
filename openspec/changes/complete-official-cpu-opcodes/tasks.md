# Tasks

Implement and check off only one opcode per step. Use `make_cpu` in `test/test_cpu.py`. Follow the existing test names:
use the mnemonic or instruction family, the addressing mode where relevant, and the behavior under test. In shared
parameterized tests, label rows by mnemonic beside their hexadecimal opcodes, as in the existing logic tests.
Write each instruction byte on its own line. Verify direct effects including PC and nominal cycles. Record the reason
and visible effects of each inherited or new approximation in `doc/decisions.md` as it is introduced; a shared entry
can cover multiple encodings when the same decision applies.

## 1. Memory increment and decrement

For each case check the destination, N/Z, and the two ordered writes (original, then modified). Record the visible
two-write sequence and the omitted indexed provisional read.

- [x] 1.1 Implement `INC absolute ($EE)` in `src/cpu.py`. Verify little-endian addressing, `$FF` to `$00`,
  the negative-result case, and six cycles.
  Run `python -m pytest test/test_cpu.py -k test_absolute_increment_and_decrement`.
- [x] 1.2 Implement `DEC absolute ($CE)` in `src/cpu.py`. Verify little-endian addressing, `$00` to `$FF`,
  the zero-result case, and six cycles.
  Run `python -m pytest test/test_cpu.py -k test_absolute_increment_and_decrement`.
- [x] 1.3 Implement `INC absolute,X ($FE)` in `src/cpu.py`. Verify crossing, noncrossing, and wrapped destinations,
  `$FF` to `$00`, the negative-result case, and fixed seven cycles.
  Run `python -m pytest test/test_cpu.py -k test_indexed_absolute_increment_and_decrement`.
- [x] 1.4 Implement `DEC absolute,X ($DE)` in `src/cpu.py`. Verify crossing, noncrossing, and wrapped destinations,
  `$00` to `$FF`, the zero-result case, and fixed seven cycles.
  Run `python -m pytest test/test_cpu.py -k test_indexed_absolute_increment_and_decrement`.

## 2. Indirect bitwise operations

For all indirect encodings, cover pointer high-byte wrapping at `$FF`. For `(zp,X)`, cover X addition with and
without zero-page wrap and fixed six cycles. For `(zp),Y`, cover crossing, noncrossing, and wrapped effective
addresses with the corresponding five or six cycles. Record the omitted zero-page or provisional indexed reads.

- [x] 2.1 Implement `AND (zp,X) ($21)` and verify addressing and zero/negative AND results in A and N/Z.
  Run `python -m pytest test/test_cpu.py -k test_indexed_indirect_logic_updates_accumulator_and_nz`.
- [x] 2.2 Implement `ORA (zp,X) ($01)` and verify addressing and zero/negative OR results in A and N/Z.
  Run `python -m pytest test/test_cpu.py -k test_indexed_indirect_logic_updates_accumulator_and_nz`.
- [x] 2.3 Implement `EOR (zp,X) ($41)` and verify addressing and zero/negative XOR results in A and N/Z.
  Run `python -m pytest test/test_cpu.py -k test_indexed_indirect_logic_updates_accumulator_and_nz`.
- [x] 2.4 Implement `AND (zp),Y ($31)` and verify addressing and zero/negative AND results in A and N/Z.
  Run `python -m pytest test/test_cpu.py -k test_indirect_indexed_logic_updates_accumulator_and_nz`.
- [x] 2.5 Implement `ORA (zp),Y ($11)` and verify addressing and zero/negative OR results in A and N/Z.
  Run `python -m pytest test/test_cpu.py -k test_indirect_indexed_logic_updates_accumulator_and_nz`.
- [x] 2.6 Implement `EOR (zp),Y ($51)` and verify addressing and zero/negative XOR results in A and N/Z.
  Run `python -m pytest test/test_cpu.py -k test_indirect_indexed_logic_updates_accumulator_and_nz`.

## 3. Indirect arithmetic and compare

Use the same addressing and timing cases as section 2. For `ADC` and `SBC`, verify A and C/V/N/Z with D clear and
set, both incoming C values, carry or borrow, and signed overflow. For `CMP`, verify C/Z/N for less than, equal,
and greater than, including a wrapped negative difference; A is not assigned a subtraction result.

- [x] 3.1 Implement `ADC (zp,X) ($61)` and verify indirect addressing and binary addition.
  Run `python -m pytest test/test_cpu.py -k test_adc_indexed_indirect`.
- [x] 3.2 Implement `ADC (zp),Y ($71)` and verify indirect addressing and binary addition.
  Run `python -m pytest test/test_cpu.py -k test_adc_indirect_indexed`.
- [x] 3.3 Implement `SBC (zp,X) ($E1)` and verify indirect addressing and binary subtraction.
  Run `python -m pytest test/test_cpu.py -k test_sbc_indexed_indirect`.
- [x] 3.4 Implement `SBC (zp),Y ($F1)` and verify indirect addressing and binary subtraction.
  Run `python -m pytest test/test_cpu.py -k test_sbc_indirect_indexed`.
- [x] 3.5 Implement `CMP (zp,X) ($C1)` and verify indirect addressing and comparison flags.
  Run `python -m pytest test/test_cpu.py -k test_cmp_indexed_indirect_updates_cnz`.
- [x] 3.6 Implement `CMP (zp),Y ($D1)` and verify indirect addressing and comparison flags.
  Run `python -m pytest test/test_cpu.py -k test_cmp_indirect_indexed_updates_cnz`.

## 4. Single-byte stack operations

Check stack position, SP wrap, and one-byte PC advance for each. Seed pull tests directly through Machine. Record
the omitted reads and explain why saved B differs from the software inspection field.

- [ ] 4.1 Implement `PHA ($48)`; verify the pushed accumulator and three cycles.
  Run `python -m pytest test/test_cpu.py -k test_pha_pushes_accumulator`.
- [ ] 4.2 Implement `PLA ($68)`; verify negative and zero results in A/N/Z and four cycles.
  Run `python -m pytest test/test_cpu.py -k test_pla_pulls_accumulator_and_updates_nz`.
- [ ] 4.3 Implement `PHP ($08)`; verify the pushed status for both software B values and three cycles.
  Run `python -m pytest test/test_cpu.py -k test_php_pushes_status`.
- [ ] 4.4 Implement `PLP ($28)`; verify the six restored flags, both mismatches between saved and current B,
  and four cycles. Run `python -m pytest test/test_cpu.py -k test_plp_restores_status`.

## 5. Software interrupt and return

- [ ] 5.1 Implement `BRK ($00)`; verify the frame order, SP wrap, saved PC and status, setting I, execution with I set,
  vector PC, and seven cycles. Record the omitted padding read.
  Run `python -m pytest test/test_cpu.py -k test_brk_pushes_interrupt_frame_and_loads_vector`.
- [ ] 5.2 Implement `RTI ($40)`; verify flags and both saved/current B mismatches, pull order, SP wrap, exact saved PC,
  and six cycles. Record the omitted reads.
  Run `python -m pytest test/test_cpu.py -k test_rti_restores_status_and_program_counter`.

## Workflow follow-up

- Start with `$EE`. After each game-driven step, record the next observed obstacle and stop before implementing it.
  The sections group coverage and do not dictate the order after `$EE`.
- After all 22 opcode steps are complete, run `python -m pytest test/test_cpu.py` and confirm that all 151 official
  encodings have dispatch entries before archiving.
