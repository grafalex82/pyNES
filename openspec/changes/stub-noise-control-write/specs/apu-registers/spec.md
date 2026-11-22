# APU Register Delta

## MODIFIED Requirements

### Requirement: Accept selected audio register writes

CPU writes of any byte to $4000, $4004, $4008, $400C, $4010-$4013 and $4015 SHALL succeed without audio effects,
DMC reads,
DMC DMA, or audio IRQs. This is a deliberate dummy behavior, not an implementation of audio playback.

#### Scenario: Write selected registers

- **WHEN** a byte is written to any of $4000, $4004, $4008, $400C, $4010, $4011, $4012, $4013, and $4015
- **THEN** the write succeeds without generating audio, reading DMC samples, or triggering an audio interrupt

#### Scenario: Write DMC control flags

- **WHEN** a byte enabling DMC looping and IRQs is written to $4010
- **THEN** the write succeeds without starting DMC playback or asserting an audio interrupt

#### Scenario: Enable DMC in the dummy control register

- **WHEN** a byte with bit 4 set is written to $4015
- **THEN** the write succeeds without starting DMC playback or asserting an audio interrupt
