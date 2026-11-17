"""T1: even-d alternating role schedule for arbitrary n."""
from common import roles,witness,cli

def construct(d,a,b,c,n):
    if d<2 or d%2 or n<1:raise ValueError('d must be even >=2, n >=1')
    k=d//2;_,p,q,_=roles(d,a,b,c,k,k,0)
    return witness(d,a,b,c,0,[(2*j,p[j%k],2*j+1,q[j%k]) for j in range(n)])
if __name__=='__main__':cli(construct,('n',))
