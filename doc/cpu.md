# CPU register state

[`CPU`](../src/cpu.py) provides register and status properties. Construct it as `CPU(machine)` after connecting
memory with [`Machine`](memory.md). CPU uses that Machine reference to read its initial reset vector.
The component stores state, converts status bytes, and performs functional startup without instruction execution.

## Register properties

| Property | Private storage | Width | Valid values |
| --- | --- | --- | --- |
| `a` | `_a` | 8 bits | `$00..$FF` |
| `x` | `_x` | 8 bits | `$00..$FF` |
| `y` | `_y` | 8 bits | `$00..$FF` |
| `sp` | `_sp` | 8 bits | `$00..$FF` |
| `pc` | `_pc` | 16 bits | `$0000..$FFFF` |
| `p` | Computed from booleans | 8 bits | `$00..$FF` input; bit 5 always reads as 1 |

All properties support reading and assignment. Register setters use ordinary `assert` statements to check the ranges
in the table before changing state. An out-of-range value raises `AssertionError`, leaving the previous state intact.
These assertions are omitted when Python runs with `-O`. Callers supply integer register values and boolean flags.
Assigning `a`, `x`, `y`, `sp`, or `pc` changes only that stored value, without truncation, instruction execution,
or status-flag updates.

## Initial CPU state

Construction sets A/X/Y/SP/PC to zero and all seven status booleans to `False`, then calls `reset()` once.
Reset subtracts 3 from SP modulo 256, making the initial SP `$FD`, and sets I. The resulting initial state is
A=X=Y=`$00`, SP=`$FD`, N=V=B=D=Z=C=0, I=1, and displayed P=`$24`.

Reset reads `$FFFC` followed by `$FFFD` through Machine and combines `low | (high << 8)` into PC.
For example, bytes `$34 $12` produce PC=`$1234`. It performs no opcode fetch, target validation, or memory writes.
RAM initialized before CPU construction, including the stack page, remains unchanged.

This functional model omits dummy bus reads and timing. The deterministic initial profile and these omissions are
recorded in [the decision record](decisions.md#functional-cpu-startup-2026-11-18).
Repeated-reset verification and reset debug logging remain pending in the
[reset-cpu change](../openspec/changes/reset-cpu/tasks.md).

## Seven booleans and the status byte

The six hardware flags and software B field each have their own private boolean and read/write property.
There is no stored or cached packed P byte, and no variable for the unused bit 5.

```text
bit   7 6 5 4 3 2 1 0
      N V 1 B D I Z C
```

| Bit | Field | Property | Private boolean | Mask |
| --- | --- | --- | --- | --- |
| 7 | Negative (N) | `negative` | `_negative` | `$80` |
| 6 | Overflow (V) | `overflow` | `_overflow` | `$40` |
| 5 | Constant 1 | None | None | `$20` |
| 4 | Software break field (B) | `break_flag` | `_break_flag` | `$10` |
| 3 | Decimal (D) | `decimal` | `_decimal` | `$08` |
| 2 | Interrupt disable (I) | `interrupt_disable` | `_interrupt_disable` | `$04` |
| 1 | Zero (Z) | `zero` | `_zero` | `$02` |
| 0 | Carry (C) | `carry` | `_carry` | `$01` |

Reading `p` shifts each current boolean to its bit position and combines the results with `$20` using bitwise OR.
A `True` boolean contributes a set bit; a `False` boolean contributes zero. Changes to an individual flag therefore
appear immediately in the next read of `p`, without synchronizing another stored register.

Assigning `p` unpacks each masked bit using `bool(value & mask)`. Every assignment replaces all seven booleans,
including clearing flags whose input bits are zero. Input bit 5 is ignored. Consequently, assigning `$00` reads back
as `$20`, assigning `$10` reads back as `$30`, and assigning `$FF` sets all seven fields and reads back as `$FF`.

For an already constructed `cpu`, property access looks like this:

```python
cpu.a = 0x12
cpu.pc = 0xABCD
cpu.p = 0x00
cpu.break_flag = True
assert cpu.p == 0x30

cpu.p = 0x85
assert cpu.negative is True
assert cpu.interrupt_disable is True
assert cpu.carry is True
assert cpu.break_flag is False
assert cpu.p == 0xA5
```

## Why B is a software field

Hardware has six stored status flags. B is a transient signal used when saving status: PHP/BRK save bit 4 as 1,
while IRQ/NMI save it as 0. PLP/RTI do not restore a physical B latch. See the
[NESdev status reference](https://www.nesdev.org/wiki/Status_flags#The_B_flag).

pyNES deliberately stores B for convenient inspection and byte conversion through `break_flag`. It starts false
and has no independent execution or interrupt effect. This convention and its rationale are recorded in
[the decision record](decisions.md#stored-b-for-status-inspection-2026-11-18).
Future stack instructions and interrupts will define their hardware behavior separately from this inspection field.

## Verification

Two parameterized tests in [`test/test_cpu.py`](../test/test_cpu.py) check packing and unpacking with individual
flag bits, all-set/clear bytes, B, and ignored input bit 5. Unpacking starts from all fields set, so zero bits must
clear previous values. One shared parameterized test checks accepted endpoints and rejected out-of-range values
for each register. All CPU tests use real NESFile, Machine, and CPU instances through the `make_cpu` factory fixture.
Its iNES header helper names PRG/CHR bank counts and mapper explicitly. By default the reset vector points to `$0000`
in RAM. The factory returns `(cpu, machine)`, so tests can set registers and write their own data or future instruction
bytes through `machine.write_byte`. RAM starts filled with zeros; the factory does not preload test data.
The `cpu` fixture takes `prg_size` and `start_address`; tests override them with `pytest.mark.parametrize`.

Two startup cases cover 16 KiB and 32 KiB PRG layouts. They check only initial registers and flags, including the
little-endian PC from the reset vector. Reads and writes are not mocked. Instruction execution remains unimplemented.

Run them from the repository root with `python -m pytest test/test_cpu.py`.
