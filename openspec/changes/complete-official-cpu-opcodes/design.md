# Design

## Context

The CPU already has the core byte operations, both indirect addressing modes in `LDA`, and stack accesses in
`JSR` and `RTS`. The [proposal](proposal.md) defines the remaining scope; the [delta](specs/cpu-execution/spec.md)
defines the behavior of each encoding.

## Goals / Non-Goals

**Goals:** Reuse those patterns and add one independently verifiable dispatch entry per implementation step.

**Non-Goals:** Refactor unrelated handlers, model individual bus cycles or DMA, or add hardware interrupt delivery.

## Decisions

- **Absolute `INC` and `DEC`:** Reuse `_modify_absolute` with `_increment_byte` or `_decrement_byte`. Keep both
  writes because mapped devices can observe them. `absolute,X` wraps at 16 bits and costs seven cycles whether or
  not it crosses a page; `absolute` costs six.
- **Indirect operands:** Use `_read_zero_page_word` for the wrapping little-endian pointer. `(zp,X)` adds X before
  reading it and always costs six cycles. `(zp),Y` adds Y after reading it and charges five cycles plus one if the
  effective page changes, including a wrap past `$FFFF`. Route pointer and data reads through Machine.
- **Indirect operations:** Use the existing AND, OR, and XOR expressions and derive N/Z from the result in A.
  Reuse `_add_with_carry` and `_subtract_with_borrow` for binary arithmetic regardless of D; set N/Z from A.
  Reuse `_compare` to update C/Z/N without assigning the subtraction result to A.
- **Stack operations:** Follow `JSR` and `RTS` for write-then-decrement and increment-then-read through Machine,
  wrapping SP within page 1. `PHA` and `PHP` take three cycles; `PLA` and `PLP` take four. `PLA` sets N/Z from A;
  do not use the two-cycle register-transfer finish helper. `PHP` forces `$30` into the saved status byte.
  `PLP` and `RTI` restore the six hardware flags, ignoring bits 5 and 4 and preserving software `break_flag`.
  If using the `p` setter, merge the current software B into the popped byte rather than assigning the byte directly.
- **Software interrupt and return:** `BRK` skips its padding byte, pushes PC+2 (high then low) and pre-instruction
  status with bits 5 and 4 set, sets I without clearing D, and reads the vector through Machine. `RTI` pulls status,
  PC low, then PC high and resumes at the exact saved PC. Build synthetic stack frames independently of `BRK` or a
  running PPU.
- **Tracing:** Reuse the cycle counter and completed trace. Capture fetched bytes without rereading for logging.
  Keep the opcode-only implied trace for `BRK` even though its saved PC accounts for the padding.

## Risks / Trade-offs

- The existing Machine traps ROM writes. Propagate that error instead of making ROM writable or pretending an
  unsuccessful instruction completed.
- The `absolute,X` path omits the provisional indexed read even without a page crossing. Any I/O side effect at that
  provisional address is absent; neither of the two writes is omitted.
- Retain the existing omission of the discarded zero-page read in `(zp,X)` and the provisional page-crossing read in
  `(zp),Y`. The first would read ordinary RAM; the second can skip a mapped-device side effect.
- Omit implied next-byte reads (the padding read for `BRK`) and discarded current-stack reads on pulls. Read side
  effects and bus timing are absent. Setting or restoring I does not add interrupt polling or delivery.
- No ROM patches or cartridge-specific branches. Use synthetic data to verify the instruction in isolation.
