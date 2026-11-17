"""T4: repeated odd stage motif; even case delegates to T1."""
from common import roles,witness,cli
from construct_t1_even import construct as even
from collections import deque

def construct(d,a,b,c,q):
    if d<2 or q<1:raise ValueError('d >=2 and q >=1 required')
    if d%2==0:return even(d,a,b,c,q*d)
    k=d//2;_,p,r,x=roles(d,a,b,c,k,k,1)
    residue=[None]*d
    for i in range(k):residue[2*i]=p[i];residue[2*i+1]=r[i]
    residue[2*k]=x[0]
    motif='AB'*k+'A'+'AB'*k+'B';pending=deque();jobs=[]
    for t,s in enumerate(motif*q):
        u=residue[t%d]
        if s=='A':pending.append((t,u))
        else:
            ta,ua=pending.popleft();jobs.append((ta,ua,t,u))
        if (t+1)%(2*d)==0:assert not pending, 'motif does not close'
    return witness(d,a,b,c,2,jobs)
if __name__=='__main__':cli(construct,('q',))
