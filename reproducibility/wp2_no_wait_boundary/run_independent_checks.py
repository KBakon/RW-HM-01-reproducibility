import csv,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'wp1_generalization'))
from line_rate_solver import solve
from verify_witness import verify
cases=[(5,0,2,3,6),(5,2,2,1,6),(5,0,1,4,9),(7,0,1,6,20),(7,1,1,5,16)]
with (root/'independent_spot_checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['d','a','b','c','n','status','method','nodes','runtime','witness_verified']);w.writeheader()
 for d,a,b,c,n in cases:
  t=time.monotonic();r=solve(d,a,b,c,n,0,90);w.writerow(dict(d=d,a=a,b=b,c=c,n=n,status=r['status'],method=r.get('method',''),nodes=r['nodes'],runtime=round(time.monotonic()-t,6),witness_verified=verify(r['witness']) if 'witness' in r else 'N/A'))
