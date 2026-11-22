# Tasks

## 1. Silent APU register boundary

- [x] 1.1 Extend APU access and Machine routing; verify all selected addresses and repeated reads after writes with
      focused pytest cases, including unused $4009/$400D and direct unsupported APU offsets.
- [x] 1.2 Verify CPU execution and neighboring DMA, controller, and unsupported address behavior with synthetic tests;
      run the relevant pytest tests.
- [x] 1.3 Document the register map, hardware differences, fixed status, and consequences in the current documentation
      and decision record; review them against the implemented behavior.
- [x] 1.4 Attempt the previously observed game with a bounded run, record the ROM identity and next obstacle, and stop
      without implementing that obstacle.
