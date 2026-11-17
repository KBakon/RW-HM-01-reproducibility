"""T3: n=d+1 construction and time/stage-reversed family."""
from common import witness,reverse
import argparse,json
from pathlib import Path

def construct(d,reversed_stages=False):
    if d<5 or d%2!=1:raise ValueError('d must be odd >=5')
    k=d//2;b=list(range(k));c=list(range(k,d))
    jobs=[(j,c[j],j+1,b[j]) for j in range(k)]
    jobs.append((d-1,c[k],d,c[0]))
    jobs.extend((d+j,c[j],d+j+1,b[j-1]) for j in range(1,k))
    jobs.append((2*d-1,c[k],2*d,b[k-1]))
    jobs.append((2*d,c[0],2*d+1,c[1]))
    w=witness(d,0,k,k+1,0,jobs)
    return reverse(w) if reversed_stages else w
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('d',type=int);p.add_argument('--reverse',action='store_true');p.add_argument('--output',type=Path);x=p.parse_args();s=json.dumps(construct(x.d,x.reverse),indent=2)+'\n'
    if x.output:x.output.write_text(s,encoding='utf8')
    else:print(s,end='')
