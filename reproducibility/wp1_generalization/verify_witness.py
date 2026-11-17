"""Independent, dependency-free schedule validation. Run on JSON paths or directories."""
import json
from pathlib import Path
import sys

def verify(w):
    d,n,W,T = (w[k] for k in ('d','n','W','T'))
    types=w['worker_types']; ops=w['operations']
    assert len(types)==d and len(ops)==2*n
    assert [types.count(s) for s in ('A','B','AB')]==[w[k] for k in ('a','b','c')]
    jobs={}; machines={}; workers={}
    for o in ops:
        j,s,t,u=(o[k] for k in ('job','stage','start','worker'))
        assert isinstance(t,int) and 0<=t<T and 0<=u<d and 0<=j<n
        assert s in ('A','B') and s in types[u]
        assert (j,s) not in jobs and (s,t) not in machines
        jobs[j,s]=t; machines[s,t]=j
        workers.setdefault(u,[]).append(t)
    for j in range(n):
        assert (j,'A') in jobs and (j,'B') in jobs
        assert 0<=jobs[j,'B']-jobs[j,'A']-1<=W
    for ts in workers.values():
        ts.sort(); assert all(y-x>=d for x,y in zip(ts,ts[1:]))
    assert max(o['start']+1 for o in ops)==T
    assert max(o['start']+1 for o in ops if o['stage']=='B')==T
    return True

def c1(w):
    slots=[[] for _ in range(w['T'])]
    for o in w['operations']: slots[o['start']].append(o['worker'])
    if any(len(s)!=1 for s in slots): return 'COUNTEREXAMPLE_NON_SATURATED'
    x=[s[0] for s in slots]
    return 'PASS' if all(x[t]==x[t+w['d']] for t in range(len(x)-w['d'])) else 'COUNTEREXAMPLE_NON_PERIODIC'

if __name__=='__main__':
    paths=[]
    for arg in sys.argv[1:]:
        p=Path(arg); paths.extend(p.rglob('*.json') if p.is_dir() else [p])
    for p in paths: verify(json.loads(p.read_text()))
    print(f'Verified {len(paths)} witnesses')
