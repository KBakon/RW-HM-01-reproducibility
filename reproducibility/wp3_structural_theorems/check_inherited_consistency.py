"""Compare theorem consequences with saved WP1/WP2 exact rows only."""
import csv
from pathlib import Path
p=Path(__file__).resolve().parent;root=p.parent
with (root/'wp1_generalization/line_rate_map.csv').open(newline='') as f:wp1={(int(x['d']),int(x['a']),int(x['b']),int(x['n'])):x for x in csv.DictReader(f)}
with (root/'wp2_no_wait_boundary/c4_exact_map.csv').open(newline='') as f:wp2={(int(x['d']),int(x['a']),int(x['b']),int(x['n'])):x for x in csv.DictReader(f)}
fields=['theorem','comparison','d','a','b','c','n','W','prediction','inherited_result','result','source','notes']
rows=[]
def add(theorem,comp,d,a,b,n,W,pred,obs,source,note=''):
 status='NOT_AVAILABLE' if obs is None else 'AGREE' if pred==obs else 'CONFLICT'
 rows.append(dict(theorem=theorem,comparison=comp,d=d,a=a,b=b,c=d-a-b,n=n,W=W,prediction=pred,inherited_result=obs if obs is not None else '',result=status,source=source,notes=note))
def wp2decision(d,a,b,n):
 r=wp2.get((d,a,b,n))
 if not r or r['status']=='UNSOLVED_RESOURCE_BOUND':return None
 return r['status']=='FEASIBLE'
def wp1wait(d,a,b,n,W):
 r=wp1.get((d,a,b,n))
 if not r:return None
 if r['line_rate_feasible_at_min_W']=='FEASIBLE':return int(r['min_W_tested'])<=W
 if r['line_rate_feasible_at_min_W']=='NO_LINE_RATE_THROUGH_2d' and W<=2*d:return False
 raise ValueError(r)
for d in (2,4,6,8):
 k=d//2
 for a in range(k+1):
  for b in range(k+1):
   for q in (1,2,3):
    add('T1','even_no_wait',d,a,b,q*d,0,True,wp1wait(d,a,b,q*d,0),'wp1_generalization/line_rate_map.csv','T1 sufficiency only; d=8 is outside WP1 coverage.')
for d in (3,5,7,9):
 k=d//2
 for a in range(d+1):
  for b in range(d-a+1):
   crit=a<=k and b<=k
   add('T2','W0',d,a,b,d,0,crit and a<k and b<k,wp2decision(d,a,b,d),'wp2_no_wait_boundary/c4_exact_map.csv','WP2 excludes all-AB and noncritical compositions.')
   add('T2','W1',d,a,b,d,1,crit,wp1wait(d,a,b,d,1),'wp1_generalization/line_rate_map.csv','Tests W=1; no-line-through-2d does not establish infeasibility for every W.')
   r=wp1.get((d,a,b,d)); expected='0' if crit and a<k and b<k else '1' if crit else '>1'
   actual=None if not r else r['min_W_tested'] if r['line_rate_feasible_at_min_W']=='FEASIBLE' and crit else '>1' if not wp1wait(d,a,b,d,1) else str(r['min_W_tested'])
   add('T2','minimum_W_or_exceeds_1',d,a,b,d,'0,1',expected,actual,'wp1_generalization/line_rate_map.csv','Noncritical comparison is only W_min >1, not the supplied all-W necessity.')
for d in (5,7,9):
 k=d//2
 for a,b in ((0,k),(k,0)):
  for n in (d,d+1):add('T3','infeasible_then_feasible',d,a,b,n,0,n==d+1,wp2decision(d,a,b,n),'wp2_no_wait_boundary/c4_exact_map.csv','WP2 d=9 did not include n=d+1 for m=k.')
for d in range(2,10):
 k=d//2
 for a in range(d+1):
  for b in range(d-a+1):
   for q in (1,2,3):
    W=0 if d%2==0 else 2;crit=a<=k and b<=k
    add('T4','critical_throughput',d,a,b,q*d,W,crit,wp1wait(d,a,b,q*d,W),'wp1_generalization/line_rate_map.csv','For noncritical compositions this only checks infeasibility through the stated W bound; all-W necessity is analytic.')
with (p/'inherited_exact_consistency.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
from collections import Counter
print('Consistency',Counter(x['result'] for x in rows))
for theory in ('T1','T2','T3','T4'):print(theory,Counter(x['result'] for x in rows if x['theorem']==theory))
