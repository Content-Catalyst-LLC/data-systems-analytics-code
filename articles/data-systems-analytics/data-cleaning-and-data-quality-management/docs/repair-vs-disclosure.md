# Repair versus disclosure

Not every data defect can be safely repaired.

Repair may be appropriate when:

- authoritative reference data exists
- the correction rule is deterministic
- source semantics are clear
- the impact of repair is auditable

Disclosure may be more appropriate when:

- identity evidence is uncertain
- missingness is nonrandom
- source records conflict without an authoritative source
- imputation would create false precision
- downstream users need to know the limitation
