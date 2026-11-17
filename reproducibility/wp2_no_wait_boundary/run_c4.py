"""Resume-safe unrestricted exact decisions, partitioned by composition."""
import csv,json,sys,time
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'wp1_generalization'))
from full_exact_solver import solve
from verify_witness import verify
fields=['d','k','a','b','c','m','n','predicted_C4','exact_feasible','witness_file','runtime','status','notes']
part=int(sys.argv[1]) if len(sys.argv)>1 else 0
parts=int(sys.argv[2]) if len(sys.argv)>2 else 1
p=root/(f'c4_shard_{part}.csv' if parts>1 else 'c4_exact_map.csv')
seen=set()
for existing in {root/'c4_exact_map.csv',p}:
 if existing.exists():
  with existing.open(newline='') as f:
   for r in csv.DictReader(f): seen.add(tuple(int(r[x]) for x in ('d','a','b','n')))
with p.open('a',newline='') as f:
 out=csv.DictWriter(f,fieldnames=fields)
 if not f.tell():out.writeheader();f.flush()
 for d in (3,5,7,9):
  k=d//2
  for a in range(k+1):
   for b in range(k+1):
    if (a*(k+1)+b)%parts!=part:continue
    m=max(a,b)
    if not m:continue
    c=d-a-b; cutoff=d*(k-m+1)-1
    for n in range(1,cutoff+(2 if d<9 else 1)+1):
     if (d,a,b,n) in seen:continue
     start=time.monotonic();result=solve(d,a,b,c,n,0,2*n,90 if d==9 else 86400);status=result['status'];path=''
     if status=='FEASIBLE':
      w=result['witness'];verify(w);path=f'witnesses/c4_d{d}_a{a}_b{b}_n{n}.json';(root/path).write_text(json.dumps(w,indent=2)+'\n')
     row=dict(d=d,k=k,a=a,b=b,c=c,m=m,n=n,predicted_C4=str(n//d+m<=k),exact_feasible={'FEASIBLE':'True','INFEASIBLE':'False','UNSOLVED_RESOURCE_BOUND':''}[status],witness_file=path,runtime=f'{time.monotonic()-start:.6f}',status=status,notes=f"full_exact_solver; nodes={result['nodes']}")
     out.writerow(row);f.flush();print(d,a,b,n,status,row['runtime'],flush=True)
