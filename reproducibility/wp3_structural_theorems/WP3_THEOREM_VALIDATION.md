# WP3 structural theorem validation

## CONTROLLER ANALYTIC THEOREMS

T1–T4 are the Controller-supplied analytic statements and constructions, pending independent scientific proof audit. The checks below validate their implementation and compare their consequences with inherited exact decisions; they do not prove the theorems. The model is unchanged from WP1/WP2, including distinct workers, unary machines, nonnegative integer starts, simultaneous A and B starts on different machines, and unused workers.

- **T1:** for even d=2k and a,b≤k, the supplied role construction gives W=0, T=2n for every n≥1. At n=d, that staffing condition is also necessary under any W.
- **T2:** for odd d=2k+1, n=d, the critical staffing condition a,b≤k is necessary and sufficient for T=2d under some W. Within it, W_min=0 exactly when a,b≤k−1; otherwise W_min=1.
- **T3:** for odd d=2k+1≥5 and (a,b,c)=(0,k,k+1), n=d is infeasible at W=0, while the supplied n=d+1 schedule is feasible at T=2n. The time/stage-reversed statement holds for (k,0,k+1).
- **T4:** for n=qd, q≥1, the critical staffing condition is necessary for T=2n under any W; it is sufficient with W=0 for even d and W≤2 for odd d.

## PROOF OBLIGATIONS

These are the supplied arguments and the explicit index checks relevant to a subsequent independent proof audit; the computational checks are not a substitute for that audit.

**Shared capacity and role allocation.** In slots 0,…,2qd−1, an individual worker has at most 2q starts separated by d. All 2qd operations therefore require every worker to attain this capacity. A-stage capacity is at most (d−b)2q and B-stage capacity at most (d−a)2q, giving b,a≤floor(d/2). For n=d this applies to T1 and T2, and for any q to T4. It counts starts, not occupied time slots: it does not assume one operation per slot. For a critical even composition, assigning all a A-only workers to k P roles and all b B-only workers to k Q roles leaves exactly enough AB workers to fill the rest. In the odd W=1/T4 construction c=d−a−b≥1 permits a distinct AB X, and the remaining AB workers fill the unused P/Q roles. In T2 W=0, a,b≤k−1 implies c≥3, allowing distinct X,Y,Z and the remaining P/Q slots.

**T1.** The A and B machines start at the distinct integers 2j and 2j+1 for j=0,…,n−1; the final B completes at 2n. Each P_i or Q_i recurs every k jobs, hence exactly 2k=d slots later. The role sets are disjoint. The case k=1 gives one P and one Q, including n=1; n need not be a multiple of d and roles can be unused.

**T2 necessity, W=0.** With n=d and T=2d, there are 2d operations; each of the d workers starts exactly twice and exactly once in each d-slot half. This does not imply the individual slots are saturated. Let p count first-half A starts and x indicate an A at d−1. No B can start at zero, and no-wait yields p−x first-half B operations, so 2p−x=d=2k+1; consequently x=1, p=k+1. The halves contain (A,B) counts (k+1,k) and (k,k+1). If b=k, all k first-half B operations use B-only workers, and all k B-only workers must also serve B in the second half. Thus exactly one second-half B is AB-served. The B at d must use an AB worker whose first start was at 0: no B-only first start can be at 0, and separation requires any first start for the worker at d to be ≤0. The worker at A time d−1 must next start at 2d−1, the only possible second-half time allowed by recovery; that operation can only be B. These two AB workers are distinct, yielding the supplied contradiction. Thus b≤k−1; time/stage reversal gives a≤k−1. Time reversal swaps stages and maps t to 2d−1−t; if needed, a uniform shift restores exact final completion and leaves separation and waits unchanged. This argument applies at k=1 as well.

**T2 W=0 indices.** The supplied A-start ranges are 0,…,k−1; the singleton d−1=2k; d+1,…,d+k−1; and 2d−2=4k. They are disjoint, have k+1+max(k−1,0)+1=2k+1 starts, and the B starts are their one-slot shifts. At k=1 the middle range is empty and the A starts are 0,2,4. P_i has separation d; Q_i has separation d+1; X and Z have separation d; Y's separation is 2d−2−k=3k≥d, with equality at k=1. The final B starts at 2d−1. All X,Y,Z are distinct AB roles.

**T2 W=1 indices.** First-stage A starts are 0,…,k−1, d−1, d,…,d+k−2, and 2d−3; the middle range is empty for k=1 and all displayed starts are distinct. B starts are 1,…,k, d+1, d+2,…,d+k, and 2d−1, also distinct. There are k+1+(k−1)+1=d jobs. Every first-block wait is zero; the other displayed A-to-B differences are two, hence W=1. The ordinary P and Q reuses are d apart; the last P reuse is 3k≥d; X is reused exactly d slots later. For k=1 the jobs start (A,B) at (0,1), (2,4), (3,5). The B start at 2d−1 fixes T=2d.

**T3 indices and reversal.** Blocks A–E contain k+1+(k−1)+1+1=2k+2=d+1 jobs, and the final B starts at 2d+1, giving T=2(d+1). The A starts are 0,…,k−1; d−1; d+1,…,d+k−1; 2d−1; 2d. Their B starts are all exactly one later and distinct. At time 2d, the D-job B and E-job A are simultaneous on different machines and use different workers. For 1≤j≤k−1, C_j's two A starts differ by d; C_0 starts at 0,d,2d; C_k starts at d−1,2d−1; C_1's final B at 2d+1 is d after its second A at d+1. For B_i with i≤k−2, the two starts differ by d+1; B_{k−1} starts at k and 2d, separated by 3k+2≥d. The lower boundary k=2 ensures C_1 exists, the j=1,…,k−1 block contains one job, and C_1's three starts remain d-separated. The k=1 formula is not asserted. Stage/time reversal swaps A-only and B-only types, preserves separations and waits, preserves distinct-machine simultaneous starts, and is explicitly verified for both families.

**T4 motif and boundaries.** For odd d=2k+1, slots 0,…,2k−1 have alternating A/B and residue 2k is A; the second d-slot half repeats the alternating k fixed A and k fixed B residues, while residue 2k is B. The word contains d A and d B operations, every prefix has enough A operations for FIFO matching, and its queue is empty at each 2d-slot boundary. Thus no job crosses a motif boundary. FIFO A-to-B differences are at most three, so W≤2; at k=1 the maximum is two. A given residue is always assigned the same worker and successive uses are exactly d apart, including across motif boundaries. The final motif ends in B, giving T=2qd. For even d, T4 delegates to T1. The construction uses no residue restriction to draw a negative scheduling conclusion.

## CONSTRUCTION VALIDATION

The script `run_construction_validation.py` generated and independently passed WP1's `verify_witness.py` on every required case. It also rechecked each case after reversing the worker-label permutation and worker-type list; this explicitly tests invariance to those labels. The CSV has one row per original case and records both results, the declared W, actual maximum wait, and representative witness paths. The distinct n values are deduplicated when d=2 makes 1=d−1.

| Construction | Validated original schedules | Scope |
|---|---:|---|
| T1 | 19,856 | Every even d=2,…,40, each critical composition, requested n values |
| T2 W=0 | 2,870 | Every odd d=3,…,41, a,b≤k−1 |
| T2 W=1 | 3,310 | Every odd d=3,…,41, a,b≤k |
| T3 | 98 | Every odd d=5,…,101, both asymmetric families |
| T4 | 52,960 | Every d=2,…,41, every critical composition, q=1,…,8 |
| Total | 79,094 | Plus 79,094 separately verified relabelings |

All 79,094 original and 79,094 relabeled verification results were PASS. The runner asserts motif closure at every boundary and the verifier checks operation counts, job precedence/wait, machine capacity, worker eligibility, recovery and exact makespan. There are 121 saved representative JSON witnesses, all separately passed through the verifier's command-line interface. The CSV and constructors reproduce the unsaved individual cases. No failed construction was encountered.

## INHERITED EXACT CONSISTENCY

`check_inherited_consistency.py` reads the stored maps only. There are **581 AGREE, 0 CONFLICT, and 607 NOT_AVAILABLE** comparison rows. The comparisons include:

| Comparison | AGREE | NOT_AVAILABLE |
|---|---:|---:|
| T1 no-wait against WP1 | 87 | 75 |
| T2 W=0 against WP2 | 50 | 72 |
| T2 W=1 and minimum-W comparisons against WP1 | 122 | 122 |
| T3 at n=d and d+1 against WP2 | 10 | 2 |
| T4 bounded-wait consequence against WP1 | 312 | 336 |

Unavailable rows represent cases outside the saved campaigns, including WP2's exclusion of all-AB, WP1's non-stage-covering or larger-d compositions, and T3 at d=9,n=10. They are not feasibility conclusions. For noncritical compositions, WP1's `NO_LINE_RATE_THROUGH_2d` supports the listed finite-W comparisons only; the all-W necessity is the separate Controller analytic result. WP2's two d=9 resource-bound cells were neither rerun nor treated as decisions. No WP1 or WP2 exact campaign was rerun.

## ANY COUNTEREXAMPLE

No construction failure or conflict with an available inherited exact decision was found. WP2 had previously falsified C4; its full counterexample list remains in `wp2_no_wait_boundary/c4_counterexamples.csv`. A lack of observed construction failures is not a proof of T1–T4.

## REMAINING UNPROVED QUESTIONS

T1–T4 await independent scientific proof audit. The checks do not resolve the general odd-d, arbitrary-n no-wait feasibility classification, or the exact minimum wait for arbitrary multiples qd beyond the stated one-cycle result. They do not resolve the two WP2 resource-bound cells. No replacement for C4, literature assessment, manuscript change, or publication decision is made here.

Reproduce from the repository root with `python wp3_structural_theorems/run_construction_validation.py` and `python wp3_structural_theorems/check_inherited_consistency.py`. The standalone constructors accept command-line arguments and can emit verifier-compatible JSON.
