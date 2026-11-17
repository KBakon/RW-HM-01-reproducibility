"""Two exact, pure-Python T=2n implementations, independent of full solver.

Enumerates all type words of length d and FIFO bounded-lag stage words.
solve_residue tests the Controller's saturated periodic restriction.
solve uses that construction as a positive fast path and, when it fails,
independently searches slot words over {empty,A,B,A+B} with rolling worker
bitmasks. Thus no residue-model negative is used as an unrestricted negative.
"""
from functools import lru_cache
import time
class ResourceBound(Exception): pass

def type_words(a,b,c,prefix=()):
    if a+b+c==0: yield prefix
    for i,(s,k) in enumerate(zip(('A','B','AB'),(a,b,c))):
        if k:
            counts=[a,b,c]; counts[i]-=1
            yield from type_words(*counts,prefix+(s,))

def solve_residue(d,a,b,c,n,W,seconds=60):
    end=time.monotonic()+seconds; nodes=0
    for types in type_words(a,b,c):
        choices={}
        @lru_cache(None)
        def visit(t,na,pending):
            nonlocal nodes
            nodes+=1
            if nodes%1024==0 and time.monotonic()>end: raise ResourceBound()
            if t==2*n: return na==n and not pending
            if n-na>2*n-t or len(pending)>2*n-t: return False
            for s in ('A','B'):
                if s not in types[t%d]: continue
                if s=='A':
                    if na==n: continue
                    p=pending+(t,)
                else:
                    if not pending or not 1<=t-pending[0]<=W+1: continue
                    p=pending[1:]
                # Store absolute times here (unlike the full solver's ages).
                if p and t+1-p[0]>W+1: continue
                nxt=(t+1,na+(s=='A'),p)
                if visit(*nxt): choices[t,na,pending]=(s,nxt); return True
            return False
        # No age test on absolute start times: handled in transitions instead.
        try: ok=visit(0,0,())
        except ResourceBound: return dict(status='UNSOLVED_RESOURCE_BOUND',nodes=nodes)
        if ok:
            state=(0,0,()); ops=[]; queue=[]; j=0
            while state[0]<2*n:
                t=state[0]; s,nxt=choices[state]
                if s=='A': job=j; queue.append(j); j+=1
                else: job=queue.pop(0)
                ops.append(dict(job=job,stage=s,start=t,worker=t%d)); state=nxt
            return dict(status='FEASIBLE',nodes=nodes,witness=dict(d=d,a=a,b=b,c=c,n=n,W=W,T=2*n,worker_types=list(types),operations=ops))
    return dict(status='INFEASIBLE',nodes=nodes)

def solve(d,a,b,c,n,W,seconds=60):
    """Exact fixed-completion-boundary search without saturation assumption.

    State: absolute unpaired A starts, total A count, and d-1 recent slot
    worker bitsets. Worker labels are renamed within type by their occurrence
    in that history. Simultaneous operations use distinct bits. Every type
    choice for a free worker is explored; other free workers of that same type
    are interchangeable. No import or call to the full solver is made.
    """
    end=time.monotonic()+seconds
    r=solve_residue(d,a,b,c,n,W,seconds)
    if r['status']!='INFEASIBLE': return dict(r,method='residue_positive_fast_path')
    T=2*n; types=('A',)*a+('B',)*b+('AB',)*c
    # Independent optimistic stage supply bound over the whole horizon.
    if n>(a+c)*((T+d-1)//d) or n>(b+c)*((T+d-1)//d):
        return dict(status='INFEASIBLE',nodes=r['nodes'],method='stage_supply_bound')
    groups=[tuple(range(a)),tuple(range(a,a+b)),tuple(range(a+b,d))]
    choices={}; nodes=0
    def normalize(history):
        signatures=[sum(((mask>>u)&1)<<i for i,mask in enumerate(history)) for u in range(d)]
        order=[u for g in groups for u in sorted(g,key=lambda u:(signatures[u],u))]
        return tuple(sum(((mask>>u)&1)<<new for new,u in enumerate(order)) for mask in history),order
    @lru_cache(None)
    def search(t,opened,queue,history):
        nonlocal nodes
        nodes+=1
        if nodes%1024==0 and time.monotonic()>end: raise ResourceBound()
        if t==T: return opened==n and not queue
        closed=opened-len(queue)
        if n-opened>T-t-1 or n-closed>T-t: return False
        if queue and t-queue[0]>W+1: return False
        used=0
        for mask in history: used|=mask
        # A free worker has no occurrence in the last d-1 slots.
        available={s:[] for s in ('A','B','AB')}
        for u,s in enumerate(types):
            if not (used>>u)&1: available[s].append(u)
        for word in ('AB','B','A',''):
            useA='A' in word; useB='B' in word
            if useA and (opened==n or t==T-1): continue
            if useB and (not queue or not 1<=t-queue[0]<=W+1): continue
            if t==T-1 and not useB: continue
            if queue and t-queue[0]==W+1 and not useB: continue
            for typeA in (('A','AB') if useA else ('',)):
                if useA and not available[typeA]: continue
                u=available[typeA][0] if useA else -1
                for typeB in (('B','AB') if useB else ('',)):
                    av=[v for v in available.get(typeB,[]) if v!=u]
                    if useB and not av: continue
                    v=av[0] if useB else -1
                    mask=(1<<u if useA else 0)|(1<<v if useB else 0)
                    h,order=normalize((history+(mask,))[-(d-1):])
                    q=queue[1:] if useB else queue
                    if useA: q=q+(t,)
                    nxt=(t+1,opened+useA,q,h)
                    if search(*nxt):
                        choices[t,opened,queue,history]=(u,v,order,nxt); return True
        return False
    initial=(0,0,(),(0,)*(d-1))
    try: ok=search(*initial)
    except ResourceBound: return dict(status='UNSOLVED_RESOURCE_BOUND',nodes=nodes,method='rolling_mask_word_search')
    if not ok: return dict(status='INFEASIBLE',nodes=nodes,method='rolling_mask_word_search')
    ids=list(range(d)); ops=[]; jobs=[]; j=0; state=initial
    while state[0]<T:
        t=state[0]; u,v,order,nxt=choices[state]
        if v>=0: ops.append(dict(job=jobs.pop(0),stage='B',start=t,worker=ids[v]))
        if u>=0:
            ops.append(dict(job=j,stage='A',start=t,worker=ids[u])); jobs.append(j); j+=1
        ids=[ids[k] for k in order]; state=nxt
    return dict(status='FEASIBLE',nodes=nodes,method='rolling_mask_word_search',witness=dict(d=d,a=a,b=b,c=c,n=n,W=W,T=T,worker_types=list(types),operations=ops))

if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser(); p.add_argument('params',nargs=6,type=int); p.add_argument('--residue-only',action='store_true')
    args=p.parse_args(); print(json.dumps((solve_residue if args.residue_only else solve)(*args.params),indent=2))
