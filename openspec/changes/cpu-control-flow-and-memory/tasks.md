# Tasks

After the selected encoding is verified, attempt a relevant local ROM if available, report the next obstacle, and stop.
Resume another task only when it is selected for implementation.

## 1. JMP absolute ($4C)

- [ ] 1.1 Implement the selected encoding; verify the destination, operand wrap, PC, and three cycles with focused
  synthetic pytest cases.
- [ ] 1.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 2. JMP indirect ($6C)

- [ ] 2.1 Implement the selected encoding; verify the destination, page-boundary pointer wrap, and five cycles with
  focused synthetic pytest cases.
- [ ] 2.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 3. JSR absolute ($20)

- [ ] 3.1 Implement the selected encoding; verify the target, return-address bytes, stack and PC wrap, operand
  overlap, and six cycles with focused synthetic pytest cases.
- [ ] 3.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 4. RTS implied ($60)

- [ ] 4.1 Implement the selected encoding; verify the return destination, stack bytes and pointer, PC wrap, and six
  cycles with focused synthetic pytest cases.
- [ ] 4.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 5. STA zero page ($85)

- [ ] 5.1 Implement the selected encoding; verify the value stored at the destination, zero-page endpoints, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 5.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 6. STX zero page ($86)

- [ ] 6.1 Implement the selected encoding; verify the value stored at the destination, zero-page endpoints, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 6.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 7. STY zero page ($84)

- [ ] 7.1 Implement the selected encoding; verify the value stored at the destination, zero-page endpoints, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 7.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 8. LDA zero page ($A5)

- [ ] 8.1 Implement the selected encoding; verify the loaded values and N/Z, zero-page endpoints, PC, and cycles with
  focused synthetic pytest cases.
- [ ] 8.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 9. LDX zero page ($A6)

- [ ] 9.1 Implement the selected encoding; verify the loaded values and N/Z, zero-page endpoints, PC, and cycles with
  focused synthetic pytest cases.
- [ ] 9.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 10. LDY zero page ($A4)

- [ ] 10.1 Implement the selected encoding; verify the loaded values and N/Z, zero-page endpoints, PC, and cycles with
  focused synthetic pytest cases.
- [ ] 10.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 11. STA absolute,X ($9D)

- [ ] 11.1 Implement the selected encoding; verify the value stored at the destination, page crossing and 16-bit wrap,
  PC, and cycles with focused synthetic pytest cases.
- [ ] 11.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 12. STA absolute,Y ($99)

- [ ] 12.1 Implement the selected encoding; verify the value stored at the destination, page crossing and 16-bit wrap,
  PC, and cycles with focused synthetic pytest cases.
- [ ] 12.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 13. LDA absolute,X ($BD)

- [ ] 13.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 13.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 14. LDA absolute,Y ($B9)

- [ ] 14.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 14.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 15. LDX absolute,Y ($BE)

- [ ] 15.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 15.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 16. LDY absolute,X ($BC)

- [ ] 16.1 Implement the selected encoding; verify the loaded values and N/Z, page crossing and 16-bit wrap, PC, and
  cycles with focused synthetic pytest cases.
- [ ] 16.2 Document this encoding and any bus simplification; verify the entry in doc/decisions.md
  states the behavior, rationale, affected ROM scope, and test evidence.

## 17. Integration

- [ ] 17.1 Run the focused and full pytest suites and openspec validate cpu-control-flow-and-memory --strict;
  resolve any failures.
- [ ] 17.2 Update the relevant CPU execution documentation and verify that it describes only implemented behavior.
- [ ] 17.3 If a relevant local ROM can be attempted, run a bounded check and report the next obstacle without
  implementing it; record actual observations only.

## Workflow follow-up

- Review and archive the grouped change after its selected tasks are complete.
