"""Independent formulation checks, corrected residue minima, and symmetry QA."""
import csv,json,time
from pathlib import Path
from line_rate_solver import solve,solve_residue
from verify_witness import verify,c1
ROOT=Path(__file__).resolve().parent

def main():
    checks=[json.loads(s) for s in (ROOT/'exact_checks.jsonl').read_text().splitlines()]
    full=[r for r in checks if r['kind']=='map' and r['solver']=='full']
    path=ROOT/'cross_formulation_checks.csv'; done={}
    if path.exists():
        done={(int(r['d']),int(r['a']),int(r['b']),int(r['c']),int(r['n']),int(r['W'])):r for r in csv.DictReader(path.open())}
    for r in full:
        key=tuple(r[k] for k in ('d','a','b','c','n','W'))
        if key in done: continue
        start=time.monotonic(); s=solve(*key)
        name=''
        if 'witness' in s:
            verify(s['witness']); name='witnesses/cross_line_d%d_%d_%d_%d_n%d_W%d.json'%key
            (ROOT/name).write_text(json.dumps(s['witness'],indent=2))
        row={k:r[k] for k in ('d','a','b','c','n','W')}
        row.update(full_status=r['status'],independent_line_status=s['status'],agreement=r['status']==s['status'],method=s.get('method'),nodes=s.get('nodes'),seconds=round(time.monotonic()-start,6),witness_file=name)
        with path.open('a',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(row))
            if not done: writer.writeheader()
            writer.writerow(row)
        done[key]=row
        if s['status']!=r['status']: print('CROSS FAILURE',key,row,flush=True)
        if key[-1]==0: print('CROSS',key,round(time.monotonic()-start,3),flush=True)
    # Complete independent residue minima, even when unrestricted minimum is earlier.
    path=ROOT/'line_rate_map.csv'; rows=list(csv.DictReader(path.open()))
    for row in rows:
        d,a,b,c,n=[int(row[k]) for k in ('d','a','b','c','n')]
        rm=None; statuses=[]
        for W in range(2*d+1):
            r=solve_residue(d,a,b,c,n,W); statuses.append(r['status'])
            if r['status']=='FEASIBLE':
                rm=W; verify(r['witness'])
                name=f'witnesses/residue_min_d{d}_{a}_{b}_{c}_n{n}_W{W}.json'
                (ROOT/name).write_text(json.dumps(r['witness'],indent=2)); break
        row['residue_min_W']=rm if rm is not None else ''
        row.pop('reduced_min_W',None)
        row['c3_status']='COUNTEREXAMPLE' if row['min_W_tested']!='' and (rm is None or int(row['min_W_tested'])<rm) else 'PASS-ON-TESTED-DOMAIN'
        keys=[k for k in done if k[:5]==(d,a,b,c,n)]
        row['full_vs_independent_line_status']='AGREE' if all(str(done[k]['agreement'])=='True' for k in keys) else 'FAIL_OR_RESOURCE_BOUND'
        row['notes']=row['notes'].replace('reduced=','residue=')
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    by={(r['d'],r['a'],r['b'],r['c'],r['n']):r for r in rows}
    for r in rows:
        reverse=by[r['d'],r['b'],r['a'],r['c'],r['n']]
        assert r['min_W_tested']==reverse['min_W_tested'] and r['residue_min_W']==reverse['residue_min_W']
    for p in (ROOT/'witnesses').glob('*.json'): verify(json.loads(p.read_text()))
    print('ALL CROSS CHECKS',len(done),'SYMMETRY ROWS',len(rows),flush=True)

if __name__=='__main__': main()
