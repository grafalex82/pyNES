"""Verify vblank NMI requests and their delivery through the execution facade."""

from emulator import Emulator


def test_nmi_edges_during_vblank_and_across_frames(make_cpu):
    _, machine = make_cpu()
    ppu = machine.ppu

    # Enabling during an existing vblank raises one request; holding the condition high does not repeat it.
    ppu.advance(27394)
    machine.write_byte(0x2000, 0x80)
    assert ppu.take_nmi() is True
    machine.write_byte(0x2008, 0x80)
    assert ppu.take_nmi() is False

    # A low condition rearms the edge; consuming a request does not depend on the condition staying high.
    machine.write_byte(0x2000, 0x00)
    machine.write_byte(0x2000, 0x80)
    machine.read_byte(0x2002)
    assert ppu.take_nmi() is True
    assert ppu.take_nmi() is False

    # With NMI enabled, each later frame creates another request without status polling.
    ppu.advance(29781)
    assert ppu.take_nmi() is True
    assert ppu.take_nmi() is False
    ppu.advance(29781)
    assert ppu.take_nmi() is True


def test_cpu_enables_nmi_during_vblank_at_instruction_boundary(make_cpu):
    # The STA raises the edge while executing; the facade services it after that instruction.
    prg = bytearray(16380)
    prg[-2:] = (0x0300).to_bytes(2, "little")
    _, machine = make_cpu(prg_program=prg)
    machine.write_byte(0x0000, 0x8D)  # STA $2000
    machine.write_byte(0x0001, 0x00)
    machine.write_byte(0x0002, 0x20)
    emulator = Emulator(machine)
    emulator.cpu.a = 0x80
    machine.ppu.advance(27394)

    # The four-cycle instruction and seven-cycle entry both count against the execution budget.
    emulator.run(1)
    assert emulator.cpu.pc == 0x0300
    assert emulator.cpu.cycles == 11
    assert machine.ppu._frame_cycle == 27405
    assert machine.read_byte(0x01FC) == 0x03


def test_synthetic_nmi_wait_and_following_frame(make_cpu):
    # Point the cartridge's NMI vector at a synthetic RAM handler.
    prg = bytearray(16380)
    prg[-2:] = (0x0300).to_bytes(2, "little")
    _, machine = make_cpu(prg_program=prg)
    program = [0xA5, 0x20, 0xF0, 0xFC, 0xEA]  # LDA $20; BEQ $0000; NOP
    handler = [
        0xE6, 0x20,              # INC $20
        0xA9, 0x3F,              # LDA #$3F
        0x8D, 0x06, 0x20,        # STA $2006
        0xA9, 0x00,              # LDA #$00
        0x8D, 0x06, 0x20,        # STA $2006
        0xA9, 0x21,              # LDA #$21
        0x8D, 0x07, 0x20,        # STA $2007
        0x40,                    # RTI
    ]
    for address, value in enumerate(program):
        machine.write_byte(address, value)
    for address, value in enumerate(handler, 0x0300):
        machine.write_byte(address, value)
    emulator = Emulator(machine)
    machine.ppu.enable_frame_output()
    machine.write_byte(0x2000, 0x80)
    machine.ppu.advance(27392)

    # One completed LDA crosses vblank; entry costs seven cycles and does not execute INC yet.
    emulator.step()
    assert emulator.cpu.pc == 0x0300
    assert emulator.cpu.cycles == 10
    assert machine.ppu._frame_cycle == 27402
    assert machine.read_byte(0x20) == 0
    assert machine.ppu.completed_frame == (1, bytes((102, 102, 102)) * (256 * 240))

    # The handler updates RAM and palette, returns, and the waiting branch eventually falls through.
    for _ in range(20):
        if emulator.cpu.pc == 0x0004:
            break
        emulator.step()
    assert emulator.cpu.pc == 0x0004
    assert machine.read_byte(0x20) == 1
    assert machine.ppu.completed_frame[1][:3] == bytes((102, 102, 102))
    machine.ppu.advance(29781)
    assert machine.ppu.completed_frame[1][:3] == bytes((100, 176, 255))
