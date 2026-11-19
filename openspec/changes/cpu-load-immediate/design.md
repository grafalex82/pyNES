# Design

## Context

CPU.step dispatches through a 256-entry table. Byte and little-endian word fetches already use Machine.

## Goals / Non-Goals

Add only the immediate, absolute, implied, and relative encodings listed in the proposal. Do not generalize
to unrelated instructions, other branch conditions, or additional addressing forms.

## Decisions

Implement the selected opcode handlers using existing fetch and trace helpers rather than a new framework.
LDA/LDX/LDY and TSX set N/Z; STA/STX/STY and TXS preserve flags; DEX/DEY wrap and set N/Z.
Each absolute memory operation goes through Machine exactly once and trace formatting never rereads a device.
Immediate loads, stack transfers, and decrements add two cycles; absolute loads and stores add four.

BPL sign-extends its operand relative to the post-operand PC and wraps at 16 bits. It adds two cycles plus
one when taken and another when a taken branch crosses a page. Replace $A9 in unsupported-opcode tests with
a still-unsupported value such as $02. Maintain existing instruction traces and diagnostic behavior.

Functional execution omits dummy bus accesses, consistent with the current CPU. The user requested grouping
the related instruction families in one change. See https://www.nesdev.org/obelisk-6502-guide/reference.html.

## Risks / Trade-offs

Device reads can have side effects, so additional reads for logging must be tested and avoided. Branches need
page-crossing and 16-bit wrap tests. Verify each family separately as it is implemented.

## Migration Plan

Apply after the PPU package; use synthetic programs for focused tests and bounded runs for local ROM checks.
No ROM is modified. Stop and report the next unsupported behavior without implementing it in this package.
