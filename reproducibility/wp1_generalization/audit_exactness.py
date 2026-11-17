"""Tiny labeled-job/labeled-worker exhaustive oracle and counterexample search."""
import itertools,json,csv
from pathlib import Path
from full_exact_solver import solve as full
from line_rate_solver import solve,solve_residue
from verify_witness import verify,c1
ROOT=Path(__file__).resolve().parent

def compositions(d):
    for a in range(d+1):
        for b in range(d-a+1):
            c=d-a-b
            if a+c and b+c: yield a,b,c

def brute(d,a,b,c,n,W,T):
    """Enumerate explicit per-job start pairs, then every labeled coloring.
    No queue matching, residue assumption, cooldown canonicalization, or
    search code from either principal formulation is used.
    """
    types=['A']*a+['B']*b+['AB']*c
    for aa in itertools.combinations(range(T-1),n):
        for bb in itertools.product(*(range(t+1,min(T,t+W+2)) for t in aa)):
            if len(set(bb))!=n or max(bb)!=T-1: continue
            ops=sorted([(aa[j],'A',j) for j in range(n)]+[(bb[j],'B',j) for j in range(n)])
            last=[-d]*d
            def color(i):
                if i==len(ops): return True
                t,s,j=ops[i]
                for u in range(d):
                    if s in types[u] and t-last[u]>=d:
                        old=last[u]; last[u]=t
                        if color(i+1): return True
                        last[u]=old
                return False
            if color(0): return True
    return False

def main():
    rows=[]
    for d in range(2,6):
        for a,b,c in compositions(d):
            for n in (1,2):
                for W in (0,1,2):
                    T=2*n; oracle=brute(d,a,b,c,n,W,T)
                    f=full(d,a,b,c,n,W,T); s=solve(d,a,b,c,n,W)
                    assert (f['status']=='FEASIBLE')==oracle==(s['status']=='FEASIBLE')
                    for r in (f,s):
                        if 'witness' in r: verify(r['witness'])
                    rows.append(dict(d=d,a=a,b=b,c=c,n=n,W=W,T=T,oracle_feasible=oracle,full_status=f['status'],line_status=s['status']))
    with (ROOT/'tiny_oracle_checks.csv').open('w',newline='') as out:
        wr=csv.DictWriter(out,fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    # Smallest residue-equivalence failure under (d,n,W,a,b,c), n<=d.
    searched=0; smallest=None
    for d in range(2,6):
        for n in range(1,d+1):
            for W in range(2*d+1):
                for a,b,c in compositions(d):
                    searched+=1; r=solve_residue(d,a,b,c,n,W); f=full(d,a,b,c,n,W,2*n)
                    assert r['status']!='UNSOLVED_RESOURCE_BOUND' and f['status']!='UNSOLVED_RESOURCE_BOUND'
                    if r['status']!=f['status']:
                        verify(f['witness']); name=f'witnesses/counterexample_C3_smallest_d{d}_{a}_{b}_{c}_n{n}_W{W}.json'
                        (ROOT/name).write_text(json.dumps(f['witness'],indent=2))
                        smallest=dict(d=d,a=a,b=b,c=c,n=n,W=W,full_status=f['status'],residue_status=r['status'],witness_file=name); break
                if smallest: break
            if smallest: break
        if smallest: break
    # C1: explicit worker occupancy is not periodic, as well as non-saturated.
    w=dict(d=3,a=0,b=0,c=3,n=3,W=1,T=6,worker_types=['AB']*3,operations=[
        dict(job=0,stage='A',start=0,worker=0),dict(job=0,stage='B',start=1,worker=1),
        dict(job=1,stage='A',start=1,worker=2),dict(job=1,stage='B',start=3,worker=0),
        dict(job=2,stage='A',start=4,worker=2),dict(job=2,stage='B',start=5,worker=1)])
    verify(w); (ROOT/'witnesses/counterexample_C1_worker_periodicity_d3_n3_W1.json').write_text(json.dumps(w,indent=2))
    # Smallest C1 failure in the tiny domain, ordered by d,n,W,a,b,c.
    c1small=None
    for row in sorted(rows,key=lambda r:tuple(r[k] for k in ('d','n','W','a','b','c'))):
        f=full(*(row[k] for k in ('d','a','b','c','n','W','T')))
        if 'witness' in f and c1(f['witness'])!='PASS':
            c1small={k:row[k] for k in ('d','a','b','c','n','W','T')}; break
    summary=dict(tiny_oracle_cells=len(rows),tiny_oracle_mismatches=0,c3_smallest_search_order=['d','n','W','a','b','c'],c3_cells_before_first_failure=searched,c3_smallest=smallest,c1_smallest_in_tiny_domain=c1small)
    (ROOT/'exactness_audit.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
