# apu-registers Specification

## Purpose

Provide a minimal CPU-visible audio register boundary for incremental NES execution without audio output.

## Requirements

### Requirement: Accept selected audio register writes

CPU writes of any byte to $4000-$4013, $4015 and $4017 SHALL succeed without audio effects, DMC reads, DMC DMA,
or audio IRQs. This is a deliberate dummy behavior, not an implementation of audio playback.

#### Scenario: Write selected registers

- **WHEN** a byte is written to any address in $4000-$4013, $4015 or $4017
- **THEN** the write succeeds without generating audio, reading DMC samples, or triggering an audio interrupt

#### Scenario: Write DMC control flags

- **WHEN** a byte enabling DMC looping and IRQs is written to $4010
- **THEN** the write succeeds without starting DMC playback or asserting an audio interrupt

#### Scenario: Enable DMC in the dummy control register

- **WHEN** a byte with bit 4 set is written to $4015
- **THEN** the write succeeds without starting DMC playback or asserting an audio interrupt

### Requirement: Return deterministic dummy audio reads

CPU reads of $4000-$4013 and $4015 SHALL return $00 regardless of earlier writes or reads. The $4015 result reports
all channel activity and interrupt flags as clear; this is an approximation, not hardware status emulation.

#### Scenario: Read selected registers

- **WHEN** any address in $4000-$4013 or $4015 is read before or after writes
- **THEN** it returns $00 on every read

#### Scenario: Read status after enabling DMC

- **WHEN** $10 is written to $4015 and $4015 is subsequently read more than once
- **THEN** each status read returns $00, including a clear DMC-active bit
