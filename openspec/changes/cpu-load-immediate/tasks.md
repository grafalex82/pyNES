# Tasks

## 1. Immediate loads

- [ ] 1.1 Implement $A9/$A2/$A0; test boundary values, N/Z, unrelated flags, PC wrap, and two cycles.
- [ ] 1.2 Verify trace bytes without extra reads; replace unsupported $A9 examples and document the instructions.

## 2. Absolute stores

- [ ] 2.1 Implement $8D/$8E/$8C; test destination, values, flags, little-endian addressing, PC, and four cycles.
- [ ] 2.2 Test trace bytes and ROM or unconnected-write errors; document the behavior and omitted dummy reads.

## 3. Stack transfer

- [ ] 3.1 Implement $9A; test SP boundaries, preserved X and flags, PC, cycles, and trace; document the behavior.

## 4. Absolute loads

- [ ] 4.1 Implement $AD/$AE/$AC; test values, little-endian addresses, N/Z, unrelated state, PC wrap, and cycles.
- [ ] 4.2 Verify one routed device read, no reread for logging, and trace bytes; document the behavior.

## 5. Relative branch

- [ ] 5.1 Implement $10; test signed displacement, both paths, PC wrap, page crossing, flags, and cycles.
- [ ] 5.2 Verify trace bytes and a bounded synthetic PPU polling program; document omitted dummy reads.

## 6. Index decrements

- [ ] 6.1 Implement $CA/$88; test wrap, N/Z, other flags, PC, cycles, and trace; document the behavior.

## 7. Integration

- [ ] 7.1 Update CPU documentation and the decision record for all selected instructions and bus approximations.
- [ ] 7.2 Run focused and full pytest suites and validate this change in strict mode.
- [ ] 7.3 Run applicable local ROMs with a bounded cycle budget and report the next obstacle without implementing it.

## Workflow follow-up

- Review and archive this change after the implementation and verification are complete.
