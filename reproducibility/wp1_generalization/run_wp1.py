"""Reproduce mandatory experiments. Results checkpointed after every instance."""
import csv, hashlib, json, time, zipfile
from pathlib import Path
from full_exact_solver import solve as full, optimize
from line_rate_solver import solve_residue as reduced
from verify_witness import verify,c1

ROOT=Path(__file__).resolve().parent
WIT=ROOT/'witnesses'; WIT.mkdir(exist_ok=True)

def save(w,name):
    verify(w); p=WIT/(name+'.json'); p.write_text(json.dumps(w,indent=2)); return str(p.relative_to(ROOT))

def append(path,row):
    exists=path.exists()
    with path.open('a',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(row));
        if not exists: wr.writeheader()
        wr.writerow(row)

def evidence(row):
    with (ROOT/'exact_checks.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')

def formula(a,b,c,n,W):
    if c==3: return 2*n
    if c==2: return 2*n+((n-1)//2 if W==0 else 0)
    if (a,b,c)==(1,1,1): return 2*n+(2*(n-1)//3 if W==0 else 0)
    return 3*n-1

def regression():
    path=ROOT/'regression_d3.csv'
    done=set()
    if path.exists():
        done={(int(r['a']),int(r['b']),int(r['c']),int(r['n']),int(r['W'])) for r in csv.DictReader(path.open())}
    # Five authority representatives plus all three stage-reversed partners.
    for a,b,c in [(0,0,3),(0,1,2),(1,1,1),(0,2,1),(1,2,0),(1,0,2),(2,0,1),(2,1,0)]:
        for n in range(1,13):
            for W in range(4):
                if (a,b,c,n,W) in done: continue
                start=time.monotonic(); r=optimize(3,a,b,c,n,W)
                expected=formula(a,b,c,n,W)
                T=r.get('witness',{}).get('T'); wf=''
                if 'witness' in r: wf=save(r['witness'],f'reg_d3_{a}_{b}_{c}_n{n}_W{W}')
                row=dict(d=3,a=a,b=b,c=c,n=n,W=W,expected_T=expected,optimized_T=T,status=r['status'],matches=T==expected,witness_file=wf,seconds=round(time.monotonic()-start,6))
                append(path,row); evidence(dict(kind='regression',**row,checks=r.get('checks')))
                if T!=expected: raise RuntimeError('HANDOFF BLOCKED: regression failure '+str(row))
        print('REGRESSION',a,b,c,flush=True)

def run_map():
    path=ROOT/'line_rate_map.csv'; done=set()
    if path.exists(): done={(int(r['d']),int(r['a']),int(r['b']),int(r['c']),int(r['n'])) for r in csv.DictReader(path.open())}
    for d in range(2,8):
        for a in range(d+1):
            for b in range(d-a+1):
                c=d-a-b
                if a+c==0 or b+c==0: continue
                for n in (d,2*d,3*d):
                    if (d,a,b,c,n) in done: continue
                    start=time.monotonic(); found=None; full_status=None; red_min=None; wf=''; c1s=[]; issues=[]; unknown=False
                    for W in range(2*d+1):
                        r=reduced(d,a,b,c,n,W)
                        f=full(d,a,b,c,n,W,2*n)
                        for label,result in [('residue',r),('full',f)]:
                            name=''
                            if 'witness' in result:
                                name=save(result['witness'],f'map_{label}_d{d}_{a}_{b}_{c}_n{n}_W{W}')
                                if label=='full': c1s.append(c1(result['witness'])); wf=name
                            evidence(dict(kind='map',solver=label,d=d,a=a,b=b,c=c,n=n,W=W,status=result['status'],nodes=result.get('nodes'),witness_file=name))
                        if r['status']=='FEASIBLE' and red_min is None: red_min=W
                        if r['status']!=f['status']:
                            issues.append(f"W={W}:full={f['status']},reduced={r['status']}")
                            print('DISAGREEMENT',d,a,b,c,n,W,f['status'],r['status'],flush=True)
                        if f['status']=='UNSOLVED_RESOURCE_BOUND': unknown=True
                        if f['status']=='FEASIBLE': found=W; full_status='FEASIBLE'; break
                    if full_status is None: full_status='UNSOLVED_RESOURCE_BOUND' if unknown else 'NO_LINE_RATE_THROUGH_2d'
                    # W=0 is always evaluated above.
                    no_wait = found==0
                    predicted=(a<=d//2 and b<=d//2) if d%2==0 else c==d
                    c2s='PASS-ON-TESTED-DOMAIN' if no_wait==predicted else 'COUNTEREXAMPLE'
                    row=dict(d=d,a=a,b=b,c=c,n=n,min_W_tested=found if found is not None else '',line_rate_feasible_at_min_W=full_status,witness_file=wf,c1_status='COUNTEREXAMPLE' if any(s!='PASS' for s in c1s) else ('PASS-ON-TESTED-DOMAIN' if c1s else 'NO_FEASIBLE_WITNESS'),c2_status=c2s,notes='; '.join(issues+(['earlier W unresolved'] if unknown else [])+(['none found through W='+str(2*d)] if found is None else [])),reduced_min_W=red_min if red_min is not None else '',seconds=round(time.monotonic()-start,6))
                    append(path,row)
                    print('MAP',d,a,b,c,n,'minW',found,full_status,round(time.monotonic()-start,2),flush=True)

if __name__=='__main__':
    import sys
    if 'regression' in sys.argv: regression()
    if 'map' in sys.argv: run_map()
