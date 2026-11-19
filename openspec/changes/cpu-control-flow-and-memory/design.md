# Design

## Context

CPU.step dispatches opcodes, reads instruction bytes through Machine, accumulates nominal instruction cycles, and
logs completed instructions using captured bytes. The first 23 encodings in this change have been implemented; the
immediate logical operations and indirect indexed stores are planned. Each encoding remains an individual learning step.

## Goals / Non-Goals

Implement the encodings specified in the delta while keeping Machine responsible for every memory request. Do not
introduce a general instruction framework or implement unrelated CPU, peripheral, or interrupt behavior.

## Decisions

- JMP absolute uses the little-endian operand directly. JMP indirect reads the target through Machine and wraps its
  pointer's high-byte read within the same page, including at $FFFF, matching the original CPU behavior.
- JSR fetches the low operand, saves the last operand address on stack high byte first, then fetches the high operand.
  Preserving this order handles an operand that aliases stack RAM. RTS pulls low then high and increments the
  restored address. SP wraps within the stack page; PC wraps at 16 bits.
- Zero-page operands are zero-extended. Indexed absolute addresses add X or Y modulo 65536. Loads update N and Z;
  stores write the selected register. Loads add a cycle on page crossing; indexed stores always take five cycles.
- Accumulator shifts move the outgoing bit into C; rotates additionally insert the old C at the opposite end. Each
  sets N and Z from the resulting byte. Immediate comparisons set C for an unsigned register value greater than or
  equal to the operand, Z for equality, and N from bit 7 of the eight-bit difference without storing that difference.
- Immediate logical operations combine the fetched operand with A and set N and Z from the resulting byte.
- Indexed-indirect stores add X to the zero-page operand modulo 256 before reading the little-endian pointer; the
  pointer's high-byte address also wraps within zero page. Indirect-indexed stores read that zero-page pointer first,
  with the same high-byte wrap, and add Y to the resulting address modulo 65536. Both use Machine for all accesses.
- Indexed-indirect stores omit the hardware's discarded read at the original zero-page operand address, where RAM reads
  have no side effects in this emulator. Indirect-indexed stores omit the provisional indexed read even when no page is
  crossed, potentially suppressing device read side effects. Both omissions preserve the functional bus model, apply to
  all ROMs, and patch none.
- Immediate logical operations need no omitted dummy access. Trace the fetched operand without additional reads.
- Accumulator shifts and rotates omit the hardware's discarded read at the next instruction address, as with existing
  implied instructions. Immediate comparisons need no omitted dummy access. The omission can suppress device read side
  effects for every ROM using these accumulator encodings; no ROM is patched.
- Preserve existing instruction trace behavior using fetched bytes and without extra reads. As requested, focused
  instruction tests check direct effects and do not test logging, PC wrap, or unrelated registers and flags. Place
  each opcode or operand byte on a separate setup line.
- Follow the existing functional bus model: indexed stores and page-crossing indexed loads omit provisional reads;
  JSR omits its internal dummy read; RTS omits its opcode-adjacent, stack-page, and final return-address dummy reads.
  Their device-visible read side effects are therefore not modeled. Plain JMP and zero-page encodings need no omitted
  dummy access in this model. These simplifications apply to every ROM using the affected encodings; no ROM is patched.
- After an individual encoding is selected and verified, report the next observed obstacle and stop. The grouped plan
  does not authorize automatically implementing the next encoding.

See the [NESdev instruction reference](https://www.nesdev.org/wiki/Instruction_reference),
[6502 bus-cycle reference](https://www.nesdev.org/6502_cpu.txt), and
[Mesen CPU reference](https://github.com/SourMesen/Mesen2/blob/master/Core/NES/NesCpu.h).

## Risks / Trade-offs

The indirect JMP page boundary and JSR stack aliasing change the actual destination if implemented with ordinary
word fetching. Test their direct results. Memory-mapped reads can have side effects, so logging must not reread devices.
