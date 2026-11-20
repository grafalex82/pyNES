# Tasks

After the selected encoding is verified, attempt a relevant local ROM if available, report the next obstacle, and stop.
Resume another task only when it is selected for implementation.

## 1. JMP absolute ($4C)

- [x] 1.1 Implement the selected encoding; verify the destination and three cycles with a focused synthetic pytest case.
- [x] 1.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 2. JMP indirect ($6C)

- [x] 2.1 Implement the selected encoding; verify the destination, page-boundary pointer wrap, and five cycles with
  focused synthetic pytest cases.
- [x] 2.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 3. JSR absolute ($20)

- [x] 3.1 Implement the selected encoding; verify the target, return-address bytes, stack wrap, operand overlap, and
  six cycles with focused synthetic pytest cases.
- [x] 3.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 4. RTS implied ($60)

- [x] 4.1 Implement the selected encoding; verify the return destination, stack bytes and pointer, and six
  cycles with focused synthetic pytest cases.
- [x] 4.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 5. STA zero page ($85)

- [x] 5.1 Implement the selected encoding; verify the value stored at the destination, zero-page endpoints, PC, and
  cycles with focused synthetic pytest cases.
- [x] 5.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 6. STX zero page ($86)

- [x] 6.1 Implement the selected encoding; verify the value stored at the destination, zero-page endpoints, PC, and
  cycles with focused synthetic pytest cases.
- [x] 6.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 7. STY zero page ($84)

- [x] 7.1 Implement the selected encoding; verify the value stored at the destination, zero-page endpoints, PC, and
  cycles with focused synthetic pytest cases.
- [x] 7.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 8. LDA zero page ($A5)

- [x] 8.1 Implement the selected encoding; verify the loaded values and N/Z, zero-page endpoints, PC, and cycles with
  focused synthetic pytest cases.
- [x] 8.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 9. LDX zero page ($A6)

- [x] 9.1 Implement the selected encoding; verify the loaded values and N/Z, zero-page endpoints, PC, and cycles with
  focused synthetic pytest cases.
- [x] 9.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 10. LDY zero page ($A4)

- [x] 10.1 Implement the selected encoding; verify the loaded values and N/Z, zero-page endpoints, PC, and cycles with
  focused synthetic pytest cases.
- [x] 10.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 11. STA absolute,X ($9D)

- [x] 11.1 Implement the selected encoding; verify the value stored at the destination, page crossing and 16-bit wrap,
  PC, and cycles with focused synthetic pytest cases.
- [x] 11.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 12. STA absolute,Y ($99)

- [x] 12.1 Implement the selected encoding; verify the value stored at the destination, page crossing and 16-bit wrap,
  PC, and cycles with focused synthetic pytest cases.
- [x] 12.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 13. LDA absolute,X ($BD)

- [x] 13.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [x] 13.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 14. LDA absolute,Y ($B9)

- [x] 14.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [x] 14.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 15. LDX absolute,Y ($BE)

- [x] 15.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [x] 15.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 16. LDY absolute,X ($BC)

- [x] 16.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [x] 16.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 17. ASL accumulator ($0A)

- [x] 17.1 Implement the selected encoding; verify A, C/N/Z, PC, and cycles with focused synthetic pytest cases.
- [x] 17.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 18. LSR accumulator ($4A)

- [x] 18.1 Implement the selected encoding; verify A, C/N/Z, PC, and cycles with focused synthetic pytest cases.
- [x] 18.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 19. ROL accumulator ($2A)

- [x] 19.1 Implement the selected encoding; verify both incoming carry values, A, C/N/Z, PC, and cycles with focused
  synthetic pytest cases.
- [x] 19.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 20. ROR accumulator ($6A)

- [x] 20.1 Implement the selected encoding; verify both incoming carry values, A, C/N/Z, PC, and cycles with focused
  synthetic pytest cases.
- [x] 20.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 21. CMP immediate ($C9)

- [x] 21.1 Implement the selected encoding; verify equal, lower, and greater values, C/N/Z, PC, and cycles with
  focused synthetic pytest cases.
- [x] 21.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 22. CPX immediate ($E0)

- [x] 22.1 Implement the selected encoding; verify equal, lower, and greater values, C/N/Z, PC, and cycles with
  focused synthetic pytest cases.
- [x] 22.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 23. CPY immediate ($C0)

- [x] 23.1 Implement the selected encoding; verify equal, lower, and greater values, C/N/Z, PC, and cycles with
  focused synthetic pytest cases.
- [x] 23.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 24. AND immediate ($29)

- [x] 24.1 Implement the selected encoding; verify A, N/Z, PC, and cycles with focused synthetic pytest cases.
- [x] 24.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 25. ORA immediate ($09)

- [x] 25.1 Implement the selected encoding; verify A, N/Z, PC, and cycles with focused synthetic pytest cases.
- [x] 25.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 26. EOR immediate ($49)

- [x] 26.1 Implement the selected encoding; verify A, N/Z, PC, and cycles with focused synthetic pytest cases.
- [x] 26.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 27. STA indexed-indirect ($81)

- [x] 27.1 Implement the selected encoding; verify the written value, indexed zero-page and pointer-byte wrapping, PC,
  and cycles with focused synthetic pytest cases.
- [x] 27.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 28. STA indirect-indexed ($91)

- [x] 28.1 Implement the selected encoding; verify the written value, pointer-byte wrapping, page crossing, effective
  address wrapping, PC, and cycles with focused synthetic pytest cases.
- [x] 28.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 29. LDA indexed-indirect ($A1)

- [x] 29.1 Implement the selected encoding; verify the loaded value, N/Z, indexed zero-page and pointer-byte wrapping,
  PC, and cycles with focused synthetic pytest cases.
- [x] 29.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 30. LDA indirect-indexed ($B1)

- [x] 30.1 Implement the selected encoding; verify the loaded value, N/Z, pointer-byte wrapping, page crossing,
  effective address wrapping, PC, and cycles with focused synthetic pytest cases.
- [x] 30.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 31. ADC immediate ($69)

- [x] 31.1 Implement the selected encoding; verify A, C/V/N/Z, both incoming carries, signed overflow, binary arithmetic
  with D clear and set, PC, and cycles with focused synthetic pytest cases.
- [x] 31.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 32. SBC immediate ($E9)

- [x] 32.1 Implement the selected encoding; verify A, C/V/N/Z, both incoming carries, borrow, signed overflow, binary
  arithmetic with D clear and set, PC, and cycles with focused synthetic pytest cases.
- [x] 32.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 33. ADC zero page ($65)

- [x] 33.1 Implement the selected encoding; verify A, C/V/N/Z, incoming carry, D, zero-page endpoints, PC, and cycles
  with focused synthetic pytest cases.
- [x] 33.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 34. SBC zero page ($E5)

- [x] 34.1 Implement the selected encoding; verify A, C/V/N/Z, incoming borrow, D, zero-page endpoints, PC, and cycles
  with focused synthetic pytest cases.
- [x] 34.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 35. ASL zero page ($06)

- [x] 35.1 Implement the selected encoding; verify the memory result, original and final writes, C/N/Z, zero-page
  endpoints, PC, and cycles with focused synthetic pytest cases.
- [x] 35.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 36. LSR zero page ($46)

- [x] 36.1 Implement the selected encoding; verify the memory result, original and final writes, C/N/Z, zero-page
  endpoints, PC, and cycles with focused synthetic pytest cases.
- [x] 36.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 37. ROL zero page ($26)

- [x] 37.1 Implement the selected encoding; verify the memory result, original and final writes, both incoming carries,
  C/N/Z, zero-page endpoints, PC, and cycles with focused synthetic pytest cases.
- [x] 37.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 38. ROR zero page ($66)

- [x] 38.1 Implement the selected encoding; verify the memory result, original and final writes, both incoming carries,
  C/N/Z, zero-page endpoints, PC, and cycles with focused synthetic pytest cases.
- [x] 38.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 39. AND zero page ($25)

- [x] 39.1 Implement the selected encoding; verify A, N/Z, zero-page endpoints, PC, and cycles with focused synthetic
  pytest cases.
- [x] 39.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 40. ORA zero page ($05)

- [x] 40.1 Implement the selected encoding; verify A, N/Z, zero-page endpoints, PC, and cycles with focused synthetic
  pytest cases.
- [x] 40.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 41. EOR zero page ($45)

- [x] 41.1 Implement the selected encoding; verify A, N/Z, zero-page endpoints, PC, and cycles with focused synthetic
  pytest cases.
- [x] 41.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 42. STA zero page,X ($95)

- [ ] 42.1 Implement the selected encoding; verify the stored value, indexed zero-page wrapping, PC, and cycles with
  focused synthetic pytest cases.
- [ ] 42.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 43. STX zero page,Y ($96)

- [ ] 43.1 Implement the selected encoding; verify the stored value, indexed zero-page wrapping, PC, and cycles with
  focused synthetic pytest cases.
- [ ] 43.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 44. STY zero page,X ($94)

- [ ] 44.1 Implement the selected encoding; verify the stored value, indexed zero-page wrapping, PC, and cycles with
  focused synthetic pytest cases.
- [ ] 44.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 45. LDA zero page,X ($B5)

- [ ] 45.1 Implement the selected encoding; verify the loaded value, N/Z, indexed zero-page wrapping, PC, and cycles
  with focused synthetic pytest cases.
- [ ] 45.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 46. LDX zero page,Y ($B6)

- [ ] 46.1 Implement the selected encoding; verify the loaded value, N/Z, indexed zero-page wrapping, PC, and cycles
  with focused synthetic pytest cases.
- [ ] 46.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 47. LDY zero page,X ($B4)

- [ ] 47.1 Implement the selected encoding; verify the loaded value, N/Z, indexed zero-page wrapping, PC, and cycles
  with focused synthetic pytest cases.
- [ ] 47.2 Review bus behavior and document any new hardware departure in doc/decisions.md, if applicable.

## 48. Integration

- [ ] 48.1 Run the focused and full pytest suites and openspec validate cpu-control-flow-and-memory --strict;
  resolve any failures.
- [ ] 48.2 Review documentation for hardware departures and their rationale without listing instruction support.
- [ ] 48.3 If a relevant local ROM can be attempted, run a bounded check and report the next obstacle without
  implementing it; record actual observations only.

## Workflow follow-up

- Review and archive the grouped change after its selected tasks are complete.
