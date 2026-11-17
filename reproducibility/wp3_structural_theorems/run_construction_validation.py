"""Exhaustively validate the supplied constructions, not schedule feasibility."""
import csv,json,sys,traceback
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'wp1_generalization'))
from verify_witness import verify
from construct_t1_even import construct as t1
from construct_t2_odd_one_cycle import construct as t2
from construct_t3_nonmonotone import construct as t3
from construct_t4_multiple_d import construct as t4
fields=['theorem','variant','d','a','b','c','n','q','W','max_wait_actual','verifier_result','relabel_result','witness_file','diagnostic']

def tasks():
 for d in range(2,41,2):
  k=d//2
  for a in range(k+1):
   for b in range(k+1):
    for n in sorted({1,d-1,d,d+1,2*d,5*d}):yield ('T1','even',d,a,b,n,None,lambda d=d,a=a,b=b,n=n:t1(d,a,b,d-a-b,n))
 for d in range(3,42,2):
  k=d//2
  for a in range(k+1):
   for b in range(k+1):
    for W in ([0,1] if a<k and b<k else [1]):yield ('T2',f'W{W}',d,a,b,d,None,lambda d=d,a=a,b=b,W=W:t2(d,a,b,d-a-b,W))
 for d in range(5,102,2):
  k=d//2
  for reverse in (False,True):yield ('T3','reversed' if reverse else 'forward',d,k if reverse else 0,0 if reverse else k,d+1,None,lambda d=d,reverse=reverse:t3(d,reverse))
 for d in range(2,42):
  k=d//2
  for a in range(k+1):
   for b in range(k+1):
    for q in range(1,9):yield ('T4','odd' if d%2 else 'even',d,a,b,q*d,q,lambda d=d,a=a,b=b,q=q:t4(d,a,b,d-a-b,q))

def permuted(w):
 d=w['d']; out=dict(w);out['worker_types']=list(reversed(w['worker_types']));out['operations']=[dict(o,worker=d-1-o['worker']) for o in w['operations']];return out

def maxwait(w):
 A={o['job']:o['start'] for o in w['operations'] if o['stage']=='A'}
 return max(o['start']-A[o['job']]-1 for o in w['operations'] if o['stage']=='B')

failed=set();counts={};path=root/'theorem_witness_verification.csv'
with path.open('w',newline='',encoding='utf8') as f:
 out=csv.DictWriter(f,fieldnames=fields);out.writeheader()
 for theorem,variant,d,a,b,n,q,build in tasks():
  if theorem in failed:continue
  c=d-a-b;w=None;name='';detail='';status='PASS';label='PASS'
  try:
   w=build(); assert (w['d'],w['a'],w['b'],w['c'],w['n'],w['T'])==(d,a,b,c,n,2*n)
   verify(w);verify(permuted(w)); actual=maxwait(w)
   if d in (2,3,5,7,40,41,101) and a in (0,d//2) and b in (0,d//2) and (q is None or q in (1,8)):
    name=f'witnesses/{theorem}_{variant}_d{d}_a{a}_b{b}_n{n}'+(f'_q{q}' if q else '')+'.json';(root/name).write_text(json.dumps(w,indent=2)+'\n')
  except Exception:
   failed.add(theorem);status='FAIL';label='NOT_COMPLETED';actual='';detail=traceback.format_exc();name=f'witnesses/FAILED_{theorem}_{variant}_d{d}_a{a}_b{b}_n{n}.json'
   (root/name).write_text(json.dumps({'witness':w,'diagnostic':detail},indent=2)+'\n')
   print('FAIL',theorem,d,a,b,n,detail,flush=True)
  out.writerow(dict(theorem=theorem,variant=variant,d=d,a=a,b=b,c=c,n=n,q=q or '',W=w['W'] if w else '',max_wait_actual=actual,verifier_result=status,relabel_result=label,witness_file=name,diagnostic=detail))
  counts[theorem]=counts.get(theorem,0)+1
  if counts[theorem]%5000==0:f.flush();print(theorem,counts[theorem],flush=True)
print('COUNTS',counts,'FAILED',sorted(failed),flush=True)
