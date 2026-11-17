# WP2: finite no-wait boundary

## PROVED INPUT

The original `wp1_generalization/inputs/main.tex`, Theorem 1 and Table 1, is the authority for d=3. For the critical mixed compositions, its zero-wait optimum equals 2n only for n≤2; all-AB has an alternating schedule for arbitrary n. The critical-throughput necessary condition for n=qd, a,b≤floor(d/2), is supplied by the Controller as analytic input. No new proof is claimed here.

## CONTROLLER ANALYTIC CONSTRUCTION

For even d=2k, the repeated AB word assigns each operation to worker t mod d; its even residues are A-fixed and odd residues B-fixed. For odd d=2k+1, use the supplied 2d-slot word (AB)^k A (AB)^k B, with t mod d assigning workers. Residue 2k is AB; put A-only workers in even fixed residues and B-only workers in odd fixed residues, filling the rest with AB. FIFO pairs define jobs. These are the Controller’s analytic constructions, not a theorem inferred from computation.

`construct_critical_schedule.py` implements the motif and labels. The independent WP1 verifier checked 8180 schedules, all PASS, spanning d=2,…,25, all critical compositions, and q=1,…,5. `W` is the declared bound; `max_wait_actual` is the realized maximum. This sanity check is not a proof.

## EXACT COMPUTATIONAL RESULT

The inherited unrestricted `full_exact_solver.py` makes each decision with W=0 and T=2n. It allows idle slots, simultaneous operations with different workers, unused workers, and all eligible worker assignments; no failed C1/C3 residue restriction certifies negatives. Every feasible row has a saved witness validated with `verify_witness.py`. Every decided stage-reversed pair is compared, and every positive witness is independently transformed by time/stage reversal and reverified. The complementary independent WP1 implementation is used only for targeted spot checks (`independent_spot_checks.csv`).

| d | Decided / required | Resource-bounded | C4 failures |
|---:|---:|---:|---:|
| 3 | 12 / 12 | 0 | 0 |
| 5 | 63 / 63 | 0 | 7 |
| 7 | 197 / 197 | 0 | 19 |
| 9 | 448 / 450 | 2 | 22 |

Resource-bound cases: d=9, (a,b,c)=(1,1,7), n=34; d=9, (a,b,c)=(2,2,5), n=27.

For d=9, each invocation has the specified 90-second solver limit. Unfinished, timed out or missing cells do not support either feasibility or infeasibility. Complete row-level records and timings are in `c4_exact_map.csv`; `c4_boundary_checks.csv` preserves n_max−1, n_max, and n_max+1 wherever tested.

| d | m | predicted n_max | n_max−1 | n_max | n_max+1 |
|---:|---:|---:|---|---|---|
| 3 | 1 | 2 | 3 FEASIBLE | 3 FEASIBLE | 3 INFEASIBLE |
| 5 | 1 | 9 | 3 FEASIBLE | 3 INFEASIBLE | 3 INFEASIBLE |
| 5 | 2 | 4 | 5 FEASIBLE | 5 FEASIBLE | 5 INFEASIBLE |
| 7 | 1 | 20 | 3 INFEASIBLE | 3 INFEASIBLE | 3 INFEASIBLE |
| 7 | 2 | 13 | 5 FEASIBLE | 5 FEASIBLE | 5 INFEASIBLE |
| 7 | 3 | 6 | 7 FEASIBLE | 7 FEASIBLE | 7 INFEASIBLE |
| 9 | 1 | 35 | 2 INFEASIBLE, 1 UNSOLVED_RESOURCE_BOUND | 3 INFEASIBLE | 3 INFEASIBLE |
| 9 | 2 | 26 | 5 INFEASIBLE | 5 FEASIBLE | 4 INFEASIBLE, 1 UNSOLVED_RESOURCE_BOUND |
| 9 | 3 | 17 | 7 FEASIBLE | 7 FEASIBLE | 7 INFEASIBLE |
| 9 | 4 | 8 | 9 FEASIBLE | 9 FEASIBLE | 9 INFEASIBLE |

Boundary pair outcome by composition:

- d=3: 3 pair agrees.
- d=5: 5 pair agrees, 3 pair fails.
- d=7: 12 pair agrees, 3 pair fails.
- d=9: 20 pair agrees, 3 pair fails, 1 unresolved or not yet tested.

The status counts above are by composition, and missing cells are not represented by a count. The all-AB d=3, n=12 witness is separately verified. Boundary sharpness as a global cutoff requires the entire iff claim, not merely the pair at the predicted boundary.

## COUNTEREXAMPLES

The smallest located failure, ordered by (d,n,a,b,c) in the executed mandatory domain, is d=5, n=6, (a,b,c)=(0,2,3): C4 predicts False, exact feasibility is True. Witness: `witnesses/c4_d5_a0_b2_n6.json`.
All 48 currently located failures, including witnesses for feasible failures and unrestricted negative results, are listed individually in `c4_counterexamples.csv`. C4 is false; enumeration is not a proof of any replacement cutoff.

## OBSERVED PATTERNS

Stage reversal: 0 conflicting decided pairs, 2 unresolved comparisons; all transformed positive witnesses passed validation.
Equal m does not determine feasibility: d=5, m=2, n=6 has both outcomes, e.g. (0,2,3) FEASIBLE; (2,2,1) INFEASIBLE.
Feasibility is nonmonotone in n at exact T=2n: d=5, (a,b,c)=(0,2,3) is infeasible at n=5 and feasible at n=6; 28 adjacent reversals are recorded by the map.

The d=9 map is checked for the same decision patterns; its finite results alone do not identify a new structural mechanism. Nonmonotonicity and dependence on more than max(a,b) already occur at d≤7. No causal or exhaustive mechanism classification is asserted.

## UNPROVED CONJECTURES

No replacement general boundary or composition-invariance assertion is proved here. The supplied critical-throughput analytic construction is distinct from C4; finite computational checks neither prove it nor establish a new theorem. The optional d=11 experiment is not required and is not run.

## Reproduction and scope

From the repository root: `python wp2_no_wait_boundary/run_construction_checks.py`, `python wp2_no_wait_boundary/run_c4.py`, `python wp2_no_wait_boundary/run_independent_checks.py`, and `python wp2_no_wait_boundary/summarize.py`. The map runner resumes from existing rows. WP1 regression was inherited and not rerun wholesale. No manuscript or WP1 output was edited.
