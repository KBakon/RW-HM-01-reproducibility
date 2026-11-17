# RW-HM-01 — Evidence provenance correction: representative witness count

**Date:** 2026-11-13  
**Scope:** non-scientific provenance correction only  
**Affected field:** `saved_representatives`  
**Historical value:** `121`  
**Corrected downstream value:** `120`

## Decision

The historical value `121` is a documentation-count error. For P3.7 and all downstream reproducibility text, the authoritative count of representative witness **paths recorded by the WP3 campaign** is **120**.

This correction does not modify any theorem, model assumption, construction, proof, feasibility result, validation-domain count, or P2 Scientific Identity Lock. It does not require P4 reopening. Original authority files are preserved byte-for-byte as historical records; this file supersedes them **only for the single `saved_representatives` provenance field**.

## Evidence

1. Frozen runner `run_construction_validation.py` SHA-256: `8541938c79f59881293bede35d093b41581234e35c7392633e91d3bb821339a3`.
2. Frozen campaign CSV SHA-256: `d88c3f164984a72129feeac26f25e0b56d555f81250d985ad2232fdc04418bbc`. It is byte-identical to the original `theorem_witness_verification.csv` preserved from the WP3 campaign.
3. The runner's explicit save predicate selects exactly **120** representative rows, with no duplicate filenames:
   - T1: **44**
   - T2: **20**
   - T3: **8**
   - T4: **48**
   - total: **120**
4. The frozen CSV contains exactly **120** nonempty `witness_file` rows and **120** distinct witness paths.
5. The deterministically reconstructed expected inventory in `reproducibility/wp3_structural_theorems/representative_witness_inventory_expected.csv` contains 120 rows and its filename set matches the CSV's nonempty `witness_file` set exactly. Inventory SHA-256: `943cf6a91fd27d270da659abb54054bc6dd37893bb33a68f1bdc4ed28506cac5`.
6. No preserved WP3 artifact inspected identifies a 121st representative filename or a separate representative-witness inventory. The original construction log records the theorem-case totals and no failures, but no additional representative.

## What remains valid

The following frozen campaign records are unaffected:

- T1 validated schedules: **19,856**
- T2 validated schedules: **6,180**
- T3 validated schedules: **98**
- T4 validated schedules: **52,960**
- total original schedules: **79,094**, all recorded PASS
- separately relabeled schedules: **79,094**, all recorded PASS
- inherited comparison summary: **581 AGREE / 0 CONFLICT / 607 NOT_AVAILABLE**

These are computational corroboration, not proof. T1-T4 remain established analytically in the manuscript/proof authority.

## CLI-verification wording

The historical WP3 prose states that 121 representatives were separately passed through the verifier command-line interface. The preserved package does not contain a CLI witness inventory/log that independently substantiates that separate statement. Therefore downstream manuscript text must **not** repeat that claim as independently verified. It may state instead:

> The campaign CSV records 120 representative witness paths. The corresponding campaign rows have `verifier_result=PASS` and `relabel_result=PASS`; the complete 79,094 original and 79,094 relabeled validation records are preserved in the campaign CSV.

## Downstream authority rule

For `saved_representatives` only, use this precedence:

`EVIDENCE_PROVENANCE_CORRECTION_2026-11-13.md/json` -> historical WP3 summary/note -> P2 handoff's historical count.

No other authority precedence changes.
