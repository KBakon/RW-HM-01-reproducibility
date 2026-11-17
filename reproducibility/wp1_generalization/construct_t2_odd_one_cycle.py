"""T2: the supplied odd one-cycle W=0 and W=1 constructions."""
from common import roles,witness,cli

def construct(d,a,b,c,W):
    if d<3 or d%2!=1 or W not in (0,1):raise ValueError('d must be odd >=3, W must be 0 or 1')
    k=d//2
    if W==0:
        _,p,q,x=roles(d,a,b,c,k-1,k-1,3);X,Y,Z=x
        A={0:X,d-1:Z,2*d-2:Y};B={d:X,k:Y,2*d-1:Z}
        for i in range(1,k):
            A[i]=p[i-1];A[d+i]=p[i-1];B[i]=q[i-1];B[d+i+1]=q[i-1]
        jobs=[(t,A[t],t+1,B[t+1]) for t in sorted(A)]
    else:
        _,p,q,x=roles(d,a,b,c,k,k,1);X=x[0]
        jobs=[(i,p[i],i+1,q[i]) for i in range(k)]
        jobs.append((d-1,X,d+1,q[0]))
        jobs.extend((d+i,p[i],d+i+2,q[i+1]) for i in range(k-1))
        jobs.append((2*d-3,p[k-1],2*d-1,X))
    return witness(d,a,b,c,W,jobs)
if __name__=='__main__':cli(construct,('W',))
