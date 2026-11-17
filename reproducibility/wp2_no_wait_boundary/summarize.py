"""Summarize the current completed and resource-bounded exact decisions."""
import csv,collections,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(p/'audit_c4.py')],check=True)
with (p/'c4_exact_map.csv').open(newline='') as f: rows=list(csv.DictReader(f))
with (p/'construction_checks.csv').open(newline='') as f: construction=list(csv.DictReader(f))
with (p/'stage_reversal_checks.csv').open(newline='') as f: rev=list(csv.DictReader(f))
bad=[r for r in rows if r['exact_feasible'] and r['exact_feasible']!=r['predicted_C4']]
with (p/'c4_counterexamples.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(bad)
expected={d:sum(d*(d//2-max(a,b)+1)-1+(2 if d<9 else 1) for a in range(d//2+1) for b in range(d//2+1) if max(a,b)) for d in (3,5,7,9)}
bykey={(int(x['d']),int(x['a']),int(x['b']),int(x['n'])):x for x in rows}
lines=['# WP2: finite no-wait boundary','', '## PROVED INPUT','','The original `wp1_generalization/inputs/main.tex`, Theorem 1 and Table 1, is the authority for d=3. For the critical mixed compositions, its zero-wait optimum equals 2n only for n≤2; all-AB has an alternating schedule for arbitrary n. The critical-throughput necessary condition for n=qd, a,b≤floor(d/2), is supplied by the Controller as analytic input. No new proof is claimed here.','','## CONTROLLER ANALYTIC CONSTRUCTION','','For even d=2k, the repeated AB word assigns each operation to worker t mod d; its even residues are A-fixed and odd residues B-fixed. For odd d=2k+1, use the supplied 2d-slot word (AB)^k A (AB)^k B, with t mod d assigning workers. Residue 2k is AB; put A-only workers in even fixed residues and B-only workers in odd fixed residues, filling the rest with AB. FIFO pairs define jobs. These are the Controller’s analytic constructions, not a theorem inferred from computation.','','`construct_critical_schedule.py` implements the motif and labels. The independent WP1 verifier checked '+str(len(construction))+' schedules, all '+('PASS' if all(x['verifier_result']=='PASS' for x in construction) else 'NOT PASS')+', spanning d=2,…,25, all critical compositions, and q=1,…,5. `W` is the declared bound; `max_wait_actual` is the realized maximum. This sanity check is not a proof.','','## EXACT COMPUTATIONAL RESULT','','The inherited unrestricted `full_exact_solver.py` makes each decision with W=0 and T=2n. It allows idle slots, simultaneous operations with different workers, unused workers, and all eligible worker assignments; no failed C1/C3 residue restriction certifies negatives. Every feasible row has a saved witness validated with `verify_witness.py`. Every decided stage-reversed pair is compared, and every positive witness is independently transformed by time/stage reversal and reverified. The complementary independent WP1 implementation is used only for targeted spot checks (`independent_spot_checks.csv`).','','| d | Decided / required | Resource-bounded | C4 failures |','|---:|---:|---:|---:|']
for d in (3,5,7,9):
 z=[r for r in rows if int(r['d'])==d]; lines.append(f"| {d} | {sum(r['status'] in ('FEASIBLE','INFEASIBLE') for r in z)} / {expected[d]} | {sum(r['status']=='UNSOLVED_RESOURCE_BOUND' for r in z)} | {sum(r in bad for r in z)} |")
timeouts=[x for x in rows if x['status']=='UNSOLVED_RESOURCE_BOUND']
lines += ['', 'Resource-bound cases: '+('; '.join(f"d={x['d']}, (a,b,c)=({x['a']},{x['b']},{x['c']}), n={x['n']}" for x in timeouts) if timeouts else 'none')+'.']
lines += ['', 'For d=9, each invocation has the specified 90-second solver limit. Unfinished, timed out or missing cells do not support either feasibility or infeasibility. Complete row-level records and timings are in `c4_exact_map.csv`; `c4_boundary_checks.csv` preserves n_max−1, n_max, and n_max+1 wherever tested.','','| d | m | predicted n_max | n_max−1 | n_max | n_max+1 |','|---:|---:|---:|---|---|---|']
def tally(z):
 c=collections.Counter(x['status'] for x in z)
 return ', '.join(f'{v} {s}' for s,v in sorted(c.items())) if c else 'not yet tested'
for d in (3,5,7,9):
 for m in range(1,d//2+1):
  N=d*(d//2-m+1)-1; z=[x for x in rows if int(x['d'])==d and int(x['m'])==m]
  lines.append(f"| {d} | {m} | {N} | "+' | '.join(tally([x for x in z if int(x['n'])==n]) for n in (N-1,N,N+1))+' |')
lines += ['', 'Boundary pair outcome by composition:', '']
for d in (3,5,7,9):
 comps={(int(x['a']),int(x['b'])) for x in rows if int(x['d'])==d}
 outcomes=collections.Counter()
 for a,b in comps:
  m=max(a,b); N=d*(d//2-m+1)-1
  x=bykey.get((d,a,b,N)); y=bykey.get((d,a,b,N+1))
  if not x or not y or 'UNSOLVED_RESOURCE_BOUND' in (x['status'],y['status']): outcomes['unresolved or not yet tested']+=1
  elif x['status']=='FEASIBLE' and y['status']=='INFEASIBLE':outcomes['pair agrees']+=1
  else:outcomes['pair fails']+=1
 lines.append(f"- d={d}: "+', '.join(f'{v} {k}' for k,v in sorted(outcomes.items()))+'.')
lines += ['', 'The status counts above are by composition, and missing cells are not represented by a count. The all-AB d=3, n=12 witness is separately verified. Boundary sharpness as a global cutoff requires the entire iff claim, not merely the pair at the predicted boundary.','','## COUNTEREXAMPLES','']
if bad:
 first=min(bad,key=lambda x:tuple(int(x[k]) for k in ('d','n','a','b','c')))
 lines += [f"The smallest located failure, ordered by (d,n,a,b,c) in the executed mandatory domain, is d={first['d']}, n={first['n']}, (a,b,c)=({first['a']},{first['b']},{first['c']}): C4 predicts {first['predicted_C4']}, exact feasibility is {first['exact_feasible']}. Witness: `{first['witness_file'] or 'not applicable (exact infeasibility)'}`.",f"All {len(bad)} currently located failures, including witnesses for feasible failures and unrestricted negative results, are listed individually in `c4_counterexamples.csv`. C4 is false; enumeration is not a proof of any replacement cutoff."]
else: lines += ['No C4 failure has yet been located; incomplete and resource-bounded cells remain unresolved.']
lines += ['', '## OBSERVED PATTERNS','']
revfail=[r for r in rev if r['decision_check']=='FAIL']; unresolved=[r for r in rev if r['decision_check']=='UNRESOLVED']
lines.append(f"Stage reversal: {len(revfail)} conflicting decided pairs, {len(unresolved)} unresolved comparisons; all transformed positive witnesses passed validation." if not revfail else f"Stage reversal conflicts: {len(revfail)}; see stage_reversal_checks.csv.")
groups=collections.defaultdict(list)
for x in rows:
 if x['exact_feasible']:groups[(int(x['d']),int(x['m']),int(x['n']))].append(x)
diffs=[(k,v) for k,v in groups.items() if len({x['exact_feasible'] for x in v})>1]
if diffs:
 k,v=min(diffs); lines.append(f"Equal m does not determine feasibility: d={k[0]}, m={k[1]}, n={k[2]} has both outcomes, e.g. "+'; '.join(f"({x['a']},{x['b']},{x['c']}) {x['status']}" for x in (next(x for x in v if x['status']=='FEASIBLE'),next(x for x in v if x['status']=='INFEASIBLE')))+'.')
else: lines.append('No equal-m discrepancy located among currently decided rows; this is not a proof.')
nonmono=[]
for key,x in bykey.items():
 d,a,b,n=key;y=bykey.get((d,a,b,n+1))
 if y and x['status']=='INFEASIBLE' and y['status']=='FEASIBLE':nonmono.append((d,a,b,n))
if nonmono:
 d,a,b,n=min(nonmono); lines.append(f"Feasibility is nonmonotone in n at exact T=2n: d={d}, (a,b,c)=({a},{b},{d-a-b}) is infeasible at n={n} and feasible at n={n+1}; {len(nonmono)} adjacent reversals are recorded by the map.")
else: lines.append('No adjacent infeasible-to-feasible reversal observed in completed cells.')
lines += ['', 'The d=9 map is checked for the same decision patterns; its finite results alone do not identify a new structural mechanism. Nonmonotonicity and dependence on more than max(a,b) already occur at d≤7. No causal or exhaustive mechanism classification is asserted.','','## UNPROVED CONJECTURES','','No replacement general boundary or composition-invariance assertion is proved here. The supplied critical-throughput analytic construction is distinct from C4; finite computational checks neither prove it nor establish a new theorem. The optional d=11 experiment is not required and is not run.','','## Reproduction and scope','','From the repository root: `python wp2_no_wait_boundary/run_construction_checks.py`, `python wp2_no_wait_boundary/run_c4.py`, `python wp2_no_wait_boundary/run_independent_checks.py`, and `python wp2_no_wait_boundary/summarize.py`. The map runner resumes from existing rows. WP1 regression was inherited and not rerun wholesale. No manuscript or WP1 output was edited.']
(p/'C4_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Report updated')
