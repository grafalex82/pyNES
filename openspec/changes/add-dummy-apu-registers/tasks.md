# Tasks

## 1. Dummy audio register boundary

- [ ] 1.1 Add a separate stateless APU component and route $4010-$4013 and $4015 through Machine. Verify with focused
  synthetic pytest cases that writes of representative byte values succeed and repeated reads return $00, including
  after enabling DMC and writing $4010 control flags; check that writes do not initiate sample reads, DMA, or IRQs.
- [ ] 1.2 Update the existing unconnected-access cases and verify that reads and writes at $400F, $4014, and $4016
  still raise address-specific `NotImplementedError`, while existing PPU, RAM, and ROM routing remains unchanged.
- [ ] 1.3 Document the supported addresses and hardware departures in `README.md`, `doc/memory.md`,
  `doc/development.md`, and `doc/decisions.md`; verify the status, open-bus, DMA, and no-audio limitations are explicit.

## 2. Integration checks

- [ ] 2.1 Run the relevant pytest cases, including a small synthetic CPU program exercising selected audio accesses,
  and record the results without requiring local ROMs.
- [ ] 2.2 If the identified local Battle City and Super Mario Bros. ROMs are available, verify their recorded identities
  and perform bounded execution checks; report the first subsequent obstacle or budget exhaustion and confirm the
  ROMs are unchanged. If unavailable, report that limitation. Do not implement the next obstacle.
