"""Audit saved map and create boundary and reversal files; safe while map grows."""
import csv,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'wp1_generalization'))
from verify_witness import verify
with (root/'c4_exact_map.csv').open(newline='') as f: rows=list(csv.DictReader(f))
fields=rows[0].keys()
with (root/'c4_boundary_checks.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in rows:
        d=int(r['d']); m=int(r['m']); cutoff=d*(d//2-m+1)-1
        if int(r['n']) in (cutoff-1,cutoff,cutoff+1) and int(r['n'])>0: w.writerow(r)
lookup={(int(r['d']),int(r['a']),int(r['b']),int(r['n'])):r for r in rows}
with (root/'stage_reversal_checks.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['d','a','b','n','status','reversed_status','decision_check','witness_check']); w.writeheader()
    for r in rows:
        d,a,b,n=map(int,(r['d'],r['a'],r['b'],r['n'])); other=lookup.get((d,b,a,n)); wc='NOT_APPLICABLE'
        if r['witness_file']:
            x=json.loads((root/r['witness_file']).read_text()); verify(x)
            y=dict(x); y['a'],y['b']=x['b'],x['a']; y['worker_types']=[{'A':'B','B':'A','AB':'AB'}[s] for s in x['worker_types']]; y['operations']=[dict(job=n-1-o['job'],stage={'A':'B','B':'A'}[o['stage']],start=2*n-1-o['start'],worker=o['worker']) for o in x['operations']]
            verify(y); wc='PASS'
        s=r['status']; t=other['status'] if other else 'NOT_YET_TESTED'
        check=('PASS' if s==t and s in ('FEASIBLE','INFEASIBLE') else 'UNRESOLVED' if s=='UNSOLVED_RESOURCE_BOUND' or t in ('UNSOLVED_RESOURCE_BOUND','NOT_YET_TESTED') else 'FAIL')
        w.writerow(dict(d=d,a=a,b=b,n=n,status=s,reversed_status=t,decision_check=check,witness_check=wc))
# Explicit d=3 all-AB schedule beyond C4 range.
n=12; d=3
w=dict(d=d,a=0,b=0,c=d,n=n,W=0,T=2*n,worker_types=['AB']*d,operations=[dict(job=j,stage=s,start=2*j+(s=='B'),worker=(2*j+(s=='B'))%d) for j in range(n) for s in ('A','B')])
verify(w); (root/'witnesses'/'all_AB_d3_n12.json').write_text(json.dumps(w,indent=2)+'\n')
print('Audited',len(rows),'map rows')
