# Annotated game disassembly

Game disassembly is deferred at the user's request. When it resumes, identify each source ROM before assigning fixed
addresses or interpreting routines.

For each listing, record the ROM filename, SHA-256, revision when known, mapper, and relevant bank layout. Distinguish
CPU addresses from file offsets and bank-relative locations. Include instruction bytes so observations can be checked
against the original file.

Use labels and English comments to explain what a routine computes, its inputs and outputs, important RAM variables,
device accesses, and its role in the game. Mark uncertain interpretations as hypotheses. Separate executable code
from data rather than assuming a linear sweep has identified every instruction correctly.

Expand listings as game execution reveals new routines. Explain algorithms in adjacent Markdown when assembly
comments alone are insufficient. Record patched bytes separately and cross-reference doc/decisions.md.
