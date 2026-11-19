# Tasks

## 1. Immediate loads

- [x] 1.1 Implement $A9/$A2/$A0; test boundary values, N/Z, PC advancement, and two cycles.
- [x] 1.2 Replace unsupported $A9 examples.

## 2. Absolute stores

- [x] 2.1 Implement $8D/$8E/$8C; test destination, values, flags, little-endian addressing, PC, and four cycles.
- [x] 2.2 Test ROM or unconnected-write errors; document any omitted dummy reads.

## 3. Stack transfer

- [x] 3.1 Implement $9A/$BA; test transferred values, flags, PC, and cycles.
- [x] 3.2 Implement TXA/TYA/TAX/TAY; test transferred values, N/Z, PC, and cycles.

## 4. Absolute loads

- [x] 4.1 Implement $AD/$AE/$AC; test values, little-endian addresses, N/Z, PC advancement, and cycles.
- [x] 4.2 Verify one routed device read.

## 5. Relative branches

- [x] 5.1 Implement BEQ/BNE/BPL/BMI/BCC/BCS/BVC/BVS; test both paths, signed offsets, page crossing, and cycles.
- [x] 5.2 Document omitted branch dummy reads.

## 6. Index decrements

- [ ] 6.1 Implement $CA/$88; test wrap, N/Z, other flags, PC, and cycles.

## 7. Integration

- [ ] 7.1 Update CPU documentation and the decision record for all selected instructions and bus approximations.
- [ ] 7.2 Run focused and full pytest suites and validate this change in strict mode.
- [ ] 7.3 Run applicable local ROMs with a bounded cycle budget and report the next obstacle without implementing it.

## Workflow follow-up

- Review and archive this change after the implementation and verification are complete.
