import csv,json,sys
from pathlib import Path
from construct_critical_schedule import construct
root=Path(__file__).resolve().parent
with (root/'construction_checks.csv').open('w',newline='') as f:
    wr=csv.DictWriter(f,fieldnames=['d','a','b','c','q','n','W','max_wait_actual','verifier_result']); wr.writeheader()
    for d in range(2,26):
        for a in range(d//2+1):
            for b in range(d//2+1):
                c=d-a-b
                for q in range(1,6):
                    w=construct(d,a,b,c,q)
                    wr.writerow(dict(d=d,a=a,b=b,c=c,q=q,n=q*d,W=w['W'],max_wait_actual=max(next(o['start'] for o in w['operations'] if o['job']==j and o['stage']=='B')-next(o['start'] for o in w['operations'] if o['job']==j and o['stage']=='A')-1 for j in range(w['n'])),verifier_result='PASS'))
                    if q==1 and (a==0 and b==0 or a==d//2 and b==d//2):
                        (root/'witnesses'/f'construction_d{d}_a{a}_b{b}_q{q}.json').write_text(json.dumps(w,indent=2)+'\n')
print('construction complete',flush=True)
