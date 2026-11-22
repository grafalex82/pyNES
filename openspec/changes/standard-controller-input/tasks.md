# Tasks

## 1. Standard controller input

- [ ] 1.1 Implement independent standard controller button and serial states, connect both ports through Machine, and
  replace stub tests with focused pytest coverage of strobing, latching, read order, independent ports, excess reads,
  upper bits, and the preserved $4017 APU write.
- [ ] 1.2 Connect the agreed keyboard mapping and focus-loss handling to the existing event loop, and use focused
  pygame event tests to verify both players, simultaneous buttons, key releases, focus loss, and existing F1 behavior.
- [ ] 1.3 Document current controller support and keyboard controls in README and relevant guides; record the bus-bit
  and host-input timing approximations with rationale in the decision record, and review them against the behavior.
- [ ] 1.4 Run relevant pytest tests and a supported local game if available; report the result and next observed
  obstacle without implementing it.
