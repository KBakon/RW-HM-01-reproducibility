# Reproducibility material: reusable skilled-worker scheduling

This public GitHub repository hosts the reproducibility package associated with the manuscript. The Zenodo archival record and DOI remain pending the first archived GitHub release. Original code: MIT. Original research data/documentation: CC BY 4.0. See ../LICENSE_SCOPE.md and the public license notices at archive root. Repository: https://github.com/KBakon/RW-HM-01-reproducibility. A Zenodo DOI does not yet exist and is pending the first archived GitHub release.

## Layout and evidence

Keep the three sibling directories together. WP1 supplies exact solvers, the independent verifier, common.py, and T1–T4 constructors. WP2 contains its complete source, exact maps and original witnesses. WP3 contains the frozen construction runner, consistency checker, original records, correction and exactly 120 original representative JSON files. MODEL_SPECIFICATION.md defines the formal scheduling model. Python uses the standard library only; see environment/PYTHON_ENVIRONMENT.md.

Historical reports describe their original campaigns; their references to original upstream input bundles do not imply those private bundles are included here. WP1 inputs/ is deliberately excluded: private manuscript inputs and unrelated correspondence are unnecessary to the runtime. The historical WP1 finish_report.py report assembler requires that omitted private input inventory and is excluded; all solver/verifier/constructor and campaign runtime dependencies are included. Console logs are excluded, including one containing personal machine paths. No scientific source or data file has been sanitized or edited.

## Limited checks (safe on a fresh extraction)

From this directory:
```
python wp1_generalization/verify_witness.py wp3_structural_theorems/witnesses
```
This checks exactly the 120 saved WP3 representatives. Package integrity can be checked against manifests/SHA256SUMS.json using the standard-library helper below:
```
python check_package_integrity.py
```
The checksum manifest excludes only itself.

## Future campaign reproduction — disposable copies only

These commands are provided for future users; they were NOT executed during this package assembly. The original scripts write checkpoints, maps or witnesses. Preserve this frozen archive and run in a separate writable copy. Create/retain each work package's witnesses/ directory first.
```
python wp3_structural_theorems/run_construction_validation.py
python wp3_structural_theorems/check_inherited_consistency.py
python wp1_generalization/run_wp1.py regression map
python wp2_no_wait_boundary/run_c4.py
```
The construction runner writes theorem_witness_verification.csv; the same original campaign CSV is also preserved under wp3_theorem_witness_verification.csv. WP1 run_wp1.py is resume/checkpoint based; existing result maps may cause it to skip completed cells. WP2 run_c4.py has the same checkpoint behavior; a future independent from-scratch campaign must use a disposable copy without its generated output maps/witnesses, retaining source and required sibling libraries. Exact solver scripts may report resource-bound cells; unavailability is not infeasibility. Historical numeric results are provided as evidence, not a promise of identical runtimes or search completion on another machine.

## Corrected representative inventory

The historical validation_summary.json retains saved_representatives: 121. The unchanged EVIDENCE_PROVENANCE_CORRECTION_2026-11-13.md/json supersedes that field only. The deterministic inventory and campaign CSV specify 120 paths: T1=44, T2=20, T3=8, T4=48. All 120 original files are included without renaming or regeneration. The original 79,094 and relabeled 79,094 PASS records and inherited 581 AGREE / 0 CONFLICT / 607 NOT_AVAILABLE totals are unchanged. NOT_AVAILABLE means no usable inherited decision. Computation is corroboration; analytic proofs establish the theorems and are not replaced by these checks.

This repository contains no manuscript PDF/source or figures. The manuscript and its declarations were not edited. The selected public route is GitHub + Zenodo. The manuscript will receive the actual repository DOI and Data Availability Statement only after the Zenodo record is created and a separate author-approved manuscript update is performed.
