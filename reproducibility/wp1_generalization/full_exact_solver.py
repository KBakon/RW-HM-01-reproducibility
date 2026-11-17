"""Unrestricted exact integer-slot DFS/DP; no saturation or periodicity assumption.

Workers of equal eligibility are canonicalized by cooldown. Pending A starts
are matched FIFO: uncrossing two matched pairs preserves both positive lag and
the common upper lag bound. Jobs are otherwise identical, so this loses none.
Both machines may operate in a slot, with distinct workers. Idle slots allowed.
Fixed T means exact final B completion T. Only exhaustive failure is INFEASIBLE.
"""
from functools import lru_cache
import time
import json
import argparse

class ResourceBound(Exception): pass

def solve(d,a,b,c,n,W,T,seconds=60):
    assert d==a+b+c and d>=2 and n>=1 and W>=0 and a+c>0 and b+c>0
    types=['A']*a+['B']*b+['AB']*c
    groups=[list(range(a)),list(range(a,a+b)),list(range(a+b,d))]
    deadline=time.monotonic()+seconds; nodes=0; choices={}
    def canon(cd):
        return tuple(v for g in groups for v in sorted(cd[i] for i in g))
    @lru_cache(None)
    def dfs(t,na,pending,cd):
        nonlocal nodes
        nodes+=1
        if nodes%1024==0 and time.monotonic()>deadline: raise ResourceBound()
        nb=na-len(pending); rem=T-t
        if t==T: return na==n and not pending
        if n-na>rem-1 or n-nb>rem: return False
        if pending and pending[0]>W+1: return False
        # Optimistic eligible-worker capacities for remaining A/B assignments.
        for stage,needed in [('A',n-na),('B',n-nb)]:
            cap=sum(max(0,1+(rem-1-cd[i])//d) for i in range(d) if stage in types[i])
            if cap<needed: return False
        canA=na<n and t<T-1
        canB=bool(pending)
        forcedB=bool(pending) and pending[0]==W+1
        # Pair first, then single A/B, then idle. No new-A/same-slot-B pair.
        for doA,doB in [(1,1),(1,0),(0,1),(0,0)]:
            if doA and not canA or doB and not canB or forcedB and not doB: continue
            if t==T-1 and not doB: continue
            avA=[i for i in range(d) if cd[i]==0 and 'A' in types[i]] if doA else [-1]
            seenA=set()
            for u in avA:
                if u>=0 and types[u] in seenA: continue
                if u>=0: seenA.add(types[u])
                avB=[i for i in range(d) if cd[i]==0 and 'B' in types[i] and i!=u] if doB else [-1]
                seenB=set()
                for v in avB:
                    if v>=0 and types[v] in seenB: continue
                    if v>=0: seenB.add(types[v])
                    newcd=[max(0,z-1) for z in cd]
                    for i in (u,v):
                        if i>=0: newcd[i]=d-1
                    p=pending[1:] if doB else pending
                    if doA: p=p+(0,)
                    p=tuple(age+1 for age in p)
                    nxt=(t+1,na+doA,p,canon(newcd))
                    if dfs(*nxt):
                        choices[t,na,pending,cd]=(u,v,nxt)
                        return True
        return False
    initial=(0,0,(),(0,)*d)
    try: feasible=dfs(*initial)
    except ResourceBound: return {'status':'UNSOLVED_RESOURCE_BOUND','nodes':nodes}
    if not feasible: return {'status':'INFEASIBLE','nodes':nodes}
    # Replay canonical workers while retaining permanent worker identities.
    state=initial; actual=[(0,i) for i in range(d)]; ops=[]; queue=[]; job=0
    while state[0]<T:
        t=state[0]; u,v,nxt=choices[state]
        ids=[z[1] for z in actual]
        if v>=0:
            j=queue.pop(0); ops.append(dict(job=j,stage='B',start=t,worker=ids[v]))
        if u>=0:
            ops.append(dict(job=job,stage='A',start=t,worker=ids[u])); queue.append(job); job+=1
        updated=[(d-1 if i in (u,v) else max(0,z[0]-1),z[1]) for i,z in enumerate(actual)]
        actual=[z for g in groups for z in sorted([updated[i] for i in g])]
        state=nxt
    witness=dict(d=d,a=a,b=b,c=c,n=n,W=W,T=T,worker_types=types,operations=ops)
    return dict(status='FEASIBLE',witness=witness,nodes=nodes)

def optimize(d,a,b,c,n,W,seconds=60):
    start=time.monotonic(); checks=[]
    for T in range(n+1,2*d*n+1):
        left=seconds-(time.monotonic()-start)
        if left<=0: return dict(status='UNSOLVED_RESOURCE_BOUND',checks=checks)
        r=solve(d,a,b,c,n,W,T,left); checks.append((T,r['status']))
        if r['status']!='INFEASIBLE': return dict(r,checks=checks)
    raise AssertionError('serial construction upper bound failed')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('params',nargs=6,type=int,metavar='d_a_b_c_n_W'); p.add_argument('--T',type=int)
    args=p.parse_args(); print(json.dumps(solve(*args.params,args.T) if args.T else optimize(*args.params),indent=2))
