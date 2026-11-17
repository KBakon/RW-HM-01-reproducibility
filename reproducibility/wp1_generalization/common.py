"""Shared labeled-worker utilities for the Controller constructions."""
import argparse,json
from pathlib import Path

def roles(d,a,b,c,np,nq,nx):
    if min(a,b,c)<0 or a+b+c!=d or np+nq+nx!=d or a>np or b>nq or c<nx:
        raise ValueError('composition does not fit requested roles')
    types=['A']*a+['B']*b+['AB']*c
    ab=iter(range(a+b,d)); xs=[next(ab) for _ in range(nx)]
    ps=list(range(a))+[next(ab) for _ in range(np-a)]
    qs=list(range(a,a+b))+[next(ab) for _ in range(nq-b)]
    assert len(set(xs+ps+qs))==d
    return types,ps,qs,xs

def witness(d,a,b,c,W,jobs):
    ops=[]
    for j,(ta,ua,tb,ub) in enumerate(jobs):
        ops.extend([dict(job=j,stage='A',start=ta,worker=ua),dict(job=j,stage='B',start=tb,worker=ub)])
    return dict(d=d,a=a,b=b,c=c,n=len(jobs),W=W,T=2*len(jobs),worker_types=['A']*a+['B']*b+['AB']*c,operations=ops)

def reverse(w):
    n=w['n'];T=w['T']; swap={'A':'B','B':'A','AB':'AB'}
    return dict(d=w['d'],a=w['b'],b=w['a'],c=w['c'],n=n,W=w['W'],T=T,worker_types=[swap[s] for s in w['worker_types']],operations=[dict(job=n-1-o['job'],stage=swap[o['stage']],start=T-1-o['start'],worker=o['worker']) for o in w['operations']])

def cli(construct, extra=()):
    p=argparse.ArgumentParser()
    for name in ('d','a','b','c'):p.add_argument(name,type=int)
    for name in extra:p.add_argument(name,type=int)
    p.add_argument('--output',type=Path);x=p.parse_args()
    w=construct(*(getattr(x,name) for name in ('d','a','b','c',*extra)))
    s=json.dumps(w,indent=2)+'\n'
    if x.output:x.output.write_text(s,encoding='utf8')
    else:print(s,end='')
