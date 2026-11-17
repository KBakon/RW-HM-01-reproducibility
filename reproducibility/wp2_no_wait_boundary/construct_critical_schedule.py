"""Controller's critical-throughput schedules; JSON is WP1 verifier compatible."""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'wp1_generalization'))
from verify_witness import verify

def construct(d,a,b,c,q):
    k=d//2
    if d<2 or q<1 or a+b+c!=d or min(a,b,c)<0 or a>k or b>k:
        raise ValueError('invalid critical composition or q')
    types=['AB']*d
    for r in range(0,2*a,2): types[r]='A'
    for r in range(1,2*b,2): types[r]='B'
    motif=('AB'*k) if d%2==0 else ('AB'*k+'A'+'AB'*k+'B')
    word=motif*(2*q if d%2==0 else q)
    pending=[]; ops=[]; j=0
    for t,s in enumerate(word):
        if s=='A':
            pending.append(j); job=j; j+=1
        else: job=pending.pop(0)
        ops.append(dict(job=job,stage=s,start=t,worker=t%d))
    assert not pending and j==q*d
    w=dict(d=d,a=a,b=b,c=c,n=j,W=0 if d%2==0 else 2,T=2*j,worker_types=types,operations=ops)
    verify(w)
    return w

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('d',type=int); p.add_argument('a',type=int); p.add_argument('b',type=int); p.add_argument('c',type=int); p.add_argument('q',type=int); p.add_argument('--output',type=Path)
    x=p.parse_args(); w=construct(x.d,x.a,x.b,x.c,x.q); s=json.dumps(w,indent=2)
    if x.output: x.output.write_text(s+'\n')
    else: print(s)
