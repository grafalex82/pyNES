# Design

## Context

Machine currently handles both controller reads and the $4016 write as fixed stubs. The pygame event loop already
handles F1 and window close between 1000-cycle emulation blocks. See the proposal and delta specs for scope.

## Goals / Non-Goals

**Goals:** Keep the standard controller's software-visible serial behavior independent of the host input mechanism.

**Non-Goals:** Model electrical signaling, bus history, DMC read interference, other devices, or physical gamepads.

## Decisions

- Add a small controller module with separate current button state and latched serial state per controller. Machine
  owns two instances, broadcasts $4016 strobe writes, and routes reads independently. This follows device boundaries
  and permits synthetic tests without pygame; embedding button state directly in Machine would conflate responsibilities.
- While strobe is high, expose the current A state; on its falling edge latch the current eight buttons. Low-strobe
  reads consume one bit and fill the shift register with ones. Repeated low writes do not restart a report. This
  models the standard controller's parallel-to-serial behavior without modeling electrical timing. See
  [NESdev standard controller](https://www.nesdev.org/wiki/Standard_controller).
- The pygame loop updates current state on key-down and key-up and clears both controllers on focus loss. It retains
  F1 handling. Bind the comma and period key positions (the unshifted US-layout keys marked < and >) without requiring
  Shift; use physical scancodes where available so the agreed positions remain usable across keyboard layouts.
  Polling only once per frame could miss short presses, so events are processed between existing execution blocks.
- Return only D0 and zero bits 1-7. Hardware leaves some bits open bus or uses them for expansion devices, so this is
  a software-visible approximation and can affect programs that depend on those bits. Document it and its reason in
  the decision record. No game patches are planned.
- Log button-state changes using a component logger; avoid logging repeated events that do not change state. Opposing
  directions are passed through as pressed: no extra host-side policy is imposed.

## Risks / Trade-offs

- [Keyboard rollover may prevent some simultaneous inputs] → Document the limitation; it depends on the host keyboard.
- [Host input is sampled between bounded blocks rather than at an exact emulated cycle] → Keep the existing block
  scheduling and document this functional approximation; exact input timing is outside the current scope.
- [Fixed zero upper bus bits can affect software] → Test the explicit response and revisit only when an observed need
  justifies modeling the bus.
