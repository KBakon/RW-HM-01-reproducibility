# RW-HM-01: first exact generalization work package

Executed 2026-11-12. Scope: d=2,...,7, every stage-covering composition, n=d,2d,3d; integer W searched through 2d. Results below are computational evidence unless explicitly identified as authoritative input or an algorithmic correctness justification. No manuscript changes, literature search, publication judgement, or theorem claim were made.

## PROVED INPUT — authority and implemented model

The supplied archive's `main.tex` is the sole authority for the original model and d=3 theorem, specifically Theorem 1 and Table 1. Its SHA-256 is `648d9cc3a28c9bbdb9c09e98d29e8c25b3f18d21d1713e4e7cec4f22ac4ac694`. Byte-identical input copies and hashes are in `inputs/`. `references.bib` and the editorial rejection are background; neither supplies execution instructions or additional model assumptions.

The implementation uses n identical jobs, unit A then unit B operations, separate unary stage machines, nonnegative integer starts, d distinct initially available workers of types A-only/B-only/AB with composition (a,b,c), and a+c>0, b+c>0. Every operation uses one eligible worker. Each worker's consecutive starts differ by at least d. Job waiting satisfies 0 <= B_start-A_start-1 <= W. Workers may remain unused. Different workers may operate the two machines simultaneously. T is the final B completion boundary; fixed-T searches require that boundary exactly.

**The assertion that every T=2n schedule has one operation per slot is false under these assumptions, including for d=3.** This was tested as a hypothesis rather than added as a constraint to the full model. The requested target T=2n is retained throughout the map. It is not assumed to be the generalized optimum: the exact diagnostic d=4, (0,0,4), n=4, W=0 has optimum T=7, after exhaustive rejection of T=5,6. See `diagnostic_optimum.json` and its saved witness. This does not affect the authoritative d=3 theorem.

## EXACT COMPUTATIONAL RESULT — implementations and exactness

`full_exact_solver.py` searches all integer slots up to fixed T with choices empty, A, B, or simultaneous A+B. Its memoized state contains the number of A operations, pending-job ages, and eligibility-grouped worker cooldowns. Every distinct feasible choice of worker type for an available worker is explored; only interchangeable worker labels are merged. It does not assume saturation or C1. Optimization exhaustively tests T from the universal unary-machine/precedence bound n+1 upward; none of the d=3 formula values is supplied to the solver.

`line_rate_solver.py` retains `solve_residue`, an independently implemented exact search over all residue qualification words and bounded-wait A/B words. Because its equivalence fails, its INFEASIBLE result is never used as an unrestricted infeasibility conclusion. The public `solve` first accepts any residue witness as a valid positive construction; otherwise it searches words over empty/A/B/A+B with rolling worker bitmasks and independently implemented coloring transitions. It neither imports nor calls the full solver. This second unrestricted implementation supplies the required trustworthy cross-check after falsification of C3. Its final deterministic branch order is A+B, B, A, empty; no random seeds or solver heuristics are used. One earlier cross-check was interrupted to improve this deterministic order and then resumed; no incomplete check is reported as a decision.

Both formulations exploit identical-job FIFO matching. Correctness justification: if A_i < A_j are matched to B_i > B_j, swapping their B partners preserves positive lag and the common upper lag bound. Repeating removes crossings. Thus matching the earliest outstanding A to the next B loses no feasible schedule. Simultaneous A and B cannot match each other; B must consume a previously outstanding A. This is an algorithmic normalization, not an empirical theorem claim about the generalized optimum.

`verify_witness.py` independently checks operation completeness and uniqueness, job precedence and wait, unary machine capacity, qualification, worker start separation, and exact makespan. It does not use either solver's state representation. An additional explicit labeled-job/labeled-worker brute-force enumerator avoids FIFO and symmetry reductions and agrees on all 264 tiny cells (d=2,...,5, all covered compositions, n=1,2, W=0,1,2, T=2n).

## EXACT COMPUTATIONAL RESULT — regression and verification

- All 240 required cells (five Table 1 representatives, n=1,...,12, W=0,1,2,3) match the authority's optimized makespans exactly.
- All 144 additional cells for the three reversed partners also match: 384/384 total.
- Regression formulas checked: all AB: 2n; two AB plus B: 2n+floor((n-1)/2) at W=0, otherwise 2n; AB+A+B: 2n+floor(2(n-1)/3) at W=0, otherwise 2n; AB+B+B and A+B+B: 3n-1 for every tested W. Each optimum has a saved verified witness; every smaller candidate T from n+1 was rejected by exhaustive search.
- Full versus corrected independent line-rate implementation: 1965/1965 decisions agree. These include every W actually searched for every mandatory row, covering all d<=5 cases and all d=6,7 cases, beyond the selected overlap requested.
- All 1041 saved witnesses pass independent verification and independent stage/time-reversal verification.
- All 312 map rows and all regression cells agree with their independently computed stage-reversed partners.
- Every one of the 64 positive minimum-W boundaries has exact infeasibility at every earlier W, including W-1, and a verified feasible witness at W.
- No final exact instance is unresolved or resource bounded. Each solver call was capped at 60 seconds; the longest recorded independent cross-check took 46.491 seconds. Map row timings aggregate several solver calls and are not individual-instance limits.
- Nine malformed-witness mutations were rejected. Full-model T=2n witnesses were explicitly checked for saturation and x[t+d]=x[t] where a single worker per slot exists; detailed outcomes are in `c1_witness_checks.csv`.

## EXACT COMPUTATIONAL RESULT — Controller candidates

| Candidate | Status | Evidence and scope |
|---|---|---|
| C1 saturation periodicity | COUNTEREXAMPLE | d=3, n=2, W=1, (0,0,3), T=4 is non-saturated. An additional d=3, n=3, W=1 witness has nonperiodic worker occupancy. All tested saturated witnesses pass the conditional periodicity check. |
| C2-even | PASS-ON-TESTED-DOMAIN | All 129 mandatory no-wait decisions for d=2,4,6 and n=d,2d,3d match a<=d/2 and b<=d/2. No assertion is made for other d or all n>=d/2. |
| C2-odd | COUNTEREXAMPLE | d=5, n=5, W=0, (0,1,4) is feasible although c<d. There are 14 contradicting mandatory rows. |
| C3 unrestricted feasibility equals residue-stage-word feasibility | COUNTEREXAMPLE | The same mandatory d=5 case is full-model feasible and residue-model infeasible. 45 mandatory rows have different minimum W. The smaller localized counterexample is d=5, n=4, W=0, (0,2,3). |

The originally requested equality between the full model and the Controller's reduced residue formulation **cannot** be reported as passing: it is mathematically falsified by independently verified feasible schedules. The repaired unrestricted line-rate implementation agrees with the full model on every required overlap. The failed residue formulation is preserved, not silently modified to fit the data.

## EXACT COMPUTATIONAL RESULT — smallest counterexamples

“Smallest” uses order (d,n,W,a,b,c) within the explicitly searched domain, rather than an unspecified order of compositions. The tiny domain is d=2,...,5, n=1,2, W=0,1,2; the localized C3 search scans increasing d<=5, n<=d, W<=2d until its first failure. That search tested 1306 cells before finding the first residue-equivalence failure. The main map supplies the smallest C2-odd failure within its n>=d domain. No global minimality over unbounded integers is claimed.

For the smallest observed C1 saturation failure, all three workers are AB:

| Job | A start | A worker | B start | B worker |
|---|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | 2 |
| 1 | 1 | 1 | 3 | 0 |

Worker 0's starts are three apart; slot 1 has two operations and slot 2 is empty. A single-worker x[1] does not exist. See `witnesses/counterexample_C1_d3_n2_W1.json`. The additional witness `counterexample_C1_worker_periodicity_d3_n3_W1.json` assigns worker 1 at slots 1 and 5 while slot 4 uses worker 2, so even the worker-occupancy sets are not 3-periodic.

For C2-odd and the mandatory C3 failure, d=5, (a,b,c)=(0,1,4), n=5, W=0, T=10:

| Job | A start | A worker | B start | B worker |
|---|---:|---:|---:|---:|
| 0 | 0 | 1 | 1 | 0 |
| 1 | 1 | 2 | 2 | 3 |
| 2 | 4 | 4 | 5 | 1 |
| 3 | 6 | 2 | 7 | 0 |
| 4 | 8 | 3 | 9 | 4 |

Worker 0 is B-only; workers 1,...,4 are AB. All waits are zero and all worker separations are at least five. The saved witness is `witnesses/counterexample_C2_odd_d5_0_1_4_n5_W0.json`. The residue solver exactly rejects W=0; this is a feasibility counterexample, not just a differently shaped feasible witness. The smaller C3 witness at d=5, n=4, (0,2,3), W=0 is in `witnesses/counterexample_C3_smallest_d5_0_2_3_n4_W0.json`.

## EXACT COMPUTATIONAL RESULT — complete minimum-W tables

Each row lists the unrestricted minimum W at n=d,2d,3d and the residue-only minima in the same order. “>L” means no feasible schedule was found by exact exhaustive decisions at any integer W=0,...,L; it does not infer infeasibility for larger W. No workforce compositions are omitted or merged by symmetry.

### d=2

| (a,b,c) | n=2 | n=4 | n=6 | Residue-only minima (same n order) |
|---|---:|---:|---:|---|
| (0,0,2) | 0 | 0 | 0 | 0, 0, 0 |
| (0,1,1) | 0 | 0 | 0 | 0, 0, 0 |
| (1,0,1) | 0 | 0 | 0 | 0, 0, 0 |
| (1,1,0) | 0 | 0 | 0 | 0, 0, 0 |

### d=3

| (a,b,c) | n=3 | n=6 | n=9 | Residue-only minima (same n order) |
|---|---:|---:|---:|---|
| (0,0,3) | 0 | 0 | 0 | 0, 0, 0 |
| (0,1,2) | 1 | 1 | 1 | 1, 1, 1 |
| (0,2,1) | >6 | >6 | >6 | >6, >6, >6 |
| (1,0,2) | 1 | 1 | 1 | 1, 1, 1 |
| (1,1,1) | 1 | 1 | 1 | 1, 1, 1 |
| (1,2,0) | >6 | >6 | >6 | >6, >6, >6 |
| (2,0,1) | >6 | >6 | >6 | >6, >6, >6 |
| (2,1,0) | >6 | >6 | >6 | >6, >6, >6 |

### d=4

| (a,b,c) | n=4 | n=8 | n=12 | Residue-only minima (same n order) |
|---|---:|---:|---:|---|
| (0,0,4) | 0 | 0 | 0 | 0, 0, 0 |
| (0,1,3) | 0 | 0 | 0 | 0, 0, 0 |
| (0,2,2) | 0 | 0 | 0 | 0, 0, 0 |
| (0,3,1) | >8 | >8 | >8 | >8, >8, >8 |
| (1,0,3) | 0 | 0 | 0 | 0, 0, 0 |
| (1,1,2) | 0 | 0 | 0 | 0, 0, 0 |
| (1,2,1) | 0 | 0 | 0 | 0, 0, 0 |
| (1,3,0) | >8 | >8 | >8 | >8, >8, >8 |
| (2,0,2) | 0 | 0 | 0 | 0, 0, 0 |
| (2,1,1) | 0 | 0 | 0 | 0, 0, 0 |
| (2,2,0) | 0 | 0 | 0 | 0, 0, 0 |
| (3,0,1) | >8 | >8 | >8 | >8, >8, >8 |
| (3,1,0) | >8 | >8 | >8 | >8, >8, >8 |

### d=5

| (a,b,c) | n=5 | n=10 | n=15 | Residue-only minima (same n order) |
|---|---:|---:|---:|---|
| (0,0,5) | 0 | 0 | 0 | 0, 0, 0 |
| (0,1,4) | 0 | 1 | 1 | 1, 1, 1 |
| (0,2,3) | 1 | 1 | 2 | 2, 2, 2 |
| (0,3,2) | >10 | >10 | >10 | >10, >10, >10 |
| (0,4,1) | >10 | >10 | >10 | >10, >10, >10 |
| (1,0,4) | 0 | 1 | 1 | 1, 1, 1 |
| (1,1,3) | 0 | 1 | 1 | 1, 1, 1 |
| (1,2,2) | 1 | 1 | 2 | 2, 2, 2 |
| (1,3,1) | >10 | >10 | >10 | >10, >10, >10 |
| (1,4,0) | >10 | >10 | >10 | >10, >10, >10 |
| (2,0,3) | 1 | 1 | 2 | 2, 2, 2 |
| (2,1,2) | 1 | 1 | 2 | 2, 2, 2 |
| (2,2,1) | 1 | 1 | 2 | 2, 2, 2 |
| (2,3,0) | >10 | >10 | >10 | >10, >10, >10 |
| (3,0,2) | >10 | >10 | >10 | >10, >10, >10 |
| (3,1,1) | >10 | >10 | >10 | >10, >10, >10 |
| (3,2,0) | >10 | >10 | >10 | >10, >10, >10 |
| (4,0,1) | >10 | >10 | >10 | >10, >10, >10 |
| (4,1,0) | >10 | >10 | >10 | >10, >10, >10 |

### d=6

| (a,b,c) | n=6 | n=12 | n=18 | Residue-only minima (same n order) |
|---|---:|---:|---:|---|
| (0,0,6) | 0 | 0 | 0 | 0, 0, 0 |
| (0,1,5) | 0 | 0 | 0 | 0, 0, 0 |
| (0,2,4) | 0 | 0 | 0 | 0, 0, 0 |
| (0,3,3) | 0 | 0 | 0 | 0, 0, 0 |
| (0,4,2) | >12 | >12 | >12 | >12, >12, >12 |
| (0,5,1) | >12 | >12 | >12 | >12, >12, >12 |
| (1,0,5) | 0 | 0 | 0 | 0, 0, 0 |
| (1,1,4) | 0 | 0 | 0 | 0, 0, 0 |
| (1,2,3) | 0 | 0 | 0 | 0, 0, 0 |
| (1,3,2) | 0 | 0 | 0 | 0, 0, 0 |
| (1,4,1) | >12 | >12 | >12 | >12, >12, >12 |
| (1,5,0) | >12 | >12 | >12 | >12, >12, >12 |
| (2,0,4) | 0 | 0 | 0 | 0, 0, 0 |
| (2,1,3) | 0 | 0 | 0 | 0, 0, 0 |
| (2,2,2) | 0 | 0 | 0 | 0, 0, 0 |
| (2,3,1) | 0 | 0 | 0 | 0, 0, 0 |
| (2,4,0) | >12 | >12 | >12 | >12, >12, >12 |
| (3,0,3) | 0 | 0 | 0 | 0, 0, 0 |
| (3,1,2) | 0 | 0 | 0 | 0, 0, 0 |
| (3,2,1) | 0 | 0 | 0 | 0, 0, 0 |
| (3,3,0) | 0 | 0 | 0 | 0, 0, 0 |
| (4,0,2) | >12 | >12 | >12 | >12, >12, >12 |
| (4,1,1) | >12 | >12 | >12 | >12, >12, >12 |
| (4,2,0) | >12 | >12 | >12 | >12, >12, >12 |
| (5,0,1) | >12 | >12 | >12 | >12, >12, >12 |
| (5,1,0) | >12 | >12 | >12 | >12, >12, >12 |

### d=7

| (a,b,c) | n=7 | n=14 | n=21 | Residue-only minima (same n order) |
|---|---:|---:|---:|---|
| (0,0,7) | 0 | 0 | 0 | 0, 0, 0 |
| (0,1,6) | 0 | 0 | 1 | 1, 1, 1 |
| (0,2,5) | 0 | 1 | 1 | 1, 1, 1 |
| (0,3,4) | 1 | 1 | 1 | 2, 2, 2 |
| (0,4,3) | >14 | >14 | >14 | >14, >14, >14 |
| (0,5,2) | >14 | >14 | >14 | >14, >14, >14 |
| (0,6,1) | >14 | >14 | >14 | >14, >14, >14 |
| (1,0,6) | 0 | 0 | 1 | 1, 1, 1 |
| (1,1,5) | 0 | 0 | 1 | 1, 1, 1 |
| (1,2,4) | 0 | 1 | 1 | 1, 1, 1 |
| (1,3,3) | 1 | 1 | 1 | 2, 2, 2 |
| (1,4,2) | >14 | >14 | >14 | >14, >14, >14 |
| (1,5,1) | >14 | >14 | >14 | >14, >14, >14 |
| (1,6,0) | >14 | >14 | >14 | >14, >14, >14 |
| (2,0,5) | 0 | 1 | 1 | 1, 1, 1 |
| (2,1,4) | 0 | 1 | 1 | 1, 1, 1 |
| (2,2,3) | 0 | 1 | 1 | 1, 1, 1 |
| (2,3,2) | 1 | 1 | 1 | 2, 2, 2 |
| (2,4,1) | >14 | >14 | >14 | >14, >14, >14 |
| (2,5,0) | >14 | >14 | >14 | >14, >14, >14 |
| (3,0,4) | 1 | 1 | 1 | 2, 2, 2 |
| (3,1,3) | 1 | 1 | 1 | 2, 2, 2 |
| (3,2,2) | 1 | 1 | 1 | 2, 2, 2 |
| (3,3,1) | 1 | 1 | 1 | 2, 2, 2 |
| (3,4,0) | >14 | >14 | >14 | >14, >14, >14 |
| (4,0,3) | >14 | >14 | >14 | >14, >14, >14 |
| (4,1,2) | >14 | >14 | >14 | >14, >14, >14 |
| (4,2,1) | >14 | >14 | >14 | >14, >14, >14 |
| (4,3,0) | >14 | >14 | >14 | >14, >14, >14 |
| (5,0,2) | >14 | >14 | >14 | >14, >14, >14 |
| (5,1,1) | >14 | >14 | >14 | >14, >14, >14 |
| (5,2,0) | >14 | >14 | >14 | >14, >14, >14 |
| (6,0,1) | >14 | >14 | >14 | >14, >14, >14 |
| (6,1,0) | >14 | >14 | >14 | >14, >14, >14 |

## OBSERVED PATTERN — parity, staffing, and finite batches

Across the tested domain, no case with max(a,b)>floor(d/2) reaches T=2n through W=2d. All other compositions do reach the target by W<=2. This describes 174 feasible and 138 bounded-search-infeasible rows; it does not extrapolate to other d, other n, or waiting allowances beyond the searched range.

For even d=2,4,6, every composition with a,b<=d/2 has minimum W=0 at all three batch sizes. Every other composition is infeasible through W=2d. There is no finite-n change among the three mandatory batch sizes for even d.

For odd d, the all-AB composition always has minimum W=0. For the other compositions that meet the observed staffing threshold, the results depend only on m=max(a,b) within this dataset:

| d | m | Minimum W at n=d,2d,3d |
|---|---:|---|
| 3 | 1 | 1,1,1 |
| 5 | 1 | 0,1,1 |
| 5 | 2 | 1,1,2 |
| 7 | 1 | 0,0,1 |
| 7 | 2 | 0,1,1 |
| 7 | 3 | 1,1,1 |

Thus finite-n no-wait exceptions persist beyond n=d: d=7 compositions (0,1,6), (1,0,6), and (1,1,5) are no-wait feasible even at n=2d. They require one waiting slot at n=3d. For d=5 and m=2, the target instead needs W=2 at n=3d. The larger odd recovery distance d=7 does not produce a larger minimum waiting requirement in these batches: its m=3 cases need only W=1. This non-monotone behavior cautions against extrapolating a waiting formula from d=3.

The residue restriction can overstate the necessary waiting flexibility. For example, d=7, (3,3,1), n=21 has unrestricted minimum W=1 and residue-only minimum W=2. The two implementations and independent witnesses retain this distinction explicitly.

## UNPROVED CONJECTURE — analytic targets suggested by the data

One precise replacement worth trying to falsify or prove is: for odd d=2k+1, n=q*d with q>=1, no-wait feasibility at T=2n holds iff c=d or q+max(a,b)<=k. This matches every tested odd-d mandatory row for k=1,2,3 and q=1,2,3. It has not been tested outside that domain and is not a theorem.

Another analytic target is whether, for integer-multiple batches, the staffing threshold max(a,b)<=floor(d/2) characterizes eventual recovery of T=2n with some bounded waiting allowance. The observed bound W<=2 here is only a finite computational result; no universal bound is asserted. Any generalization must allow idle slots and concurrent A+B slots rather than impose C1 or C3.

## Evidence for the Controller

All 384 d=3 regression cells matched the authority, including all 240 required cells. All 312 mandatory map rows were resolved exactly. The unrestricted implementations agreed on every saved cross-formulation decision, and all saved feasible witnesses passed independent verification. C2-even passed all 129 tested rows. C1, C2-odd, and C3 have saved exact counterexamples. The map contains finite-n changes at odd d and no finite-n changes at even d. No tested composition with max(a,b)>floor(d/2) reached T=2n through W=2d.

## Reproduction, files, and technical limits

From the project root, using standard Python 3 (no third-party dependencies):

```text
python wp1_generalization/run_wp1.py regression map
python wp1_generalization/cross_validate.py
python wp1_generalization/audit_exactness.py
python wp1_generalization/finish_report.py
python wp1_generalization/verify_witness.py wp1_generalization/witnesses
```

Experiments checkpoint and resume; to reproduce a fresh run, place the Python files and input copies in a fresh output directory first. `regression_d3.csv`, `line_rate_map.csv`, `exact_checks.jsonl`, `cross_formulation_checks.csv`, `tiny_oracle_checks.csv`, `c1_witness_checks.csv`, `exactness_audit.json`, and `verification_summary.json` retain decisions and verification evidence. `witnesses/` includes every regression optimum, every full-model map minimum, independent cross-check witnesses, residue minima, and named counterexamples. `FILE_SHA256_MANIFEST.json` records delivered artifact hashes.

Not run: optional d=8,9; optional n=4d; broad literature search; generalized makespan optimization beyond the single saturation diagnostic; unbounded waiting searches; formal proof of any new generalization; external proof-assistant or third-party UNSAT-certificate checking. Infeasibility conclusions come from exhaustive finite integer search, not heuristics, numerical MILP tolerances, or a failed residue restriction.

The principal remaining technical risk is ordinary implementation error in exhaustive negative decisions. Independent code paths, the labeled tiny oracle, exact d=3 regression, reversal checks, and witness validation reduce this risk but are not a formal machine-checked proof of the solvers. The Controller's original full-versus-residue equality requirement is scientifically falsified; it is not an unresolved solver disagreement. No required exact case remains resource bounded. All outputs described above were saved under `wp1_generalization/`; the authoritative manuscript and bibliography were not edited.
