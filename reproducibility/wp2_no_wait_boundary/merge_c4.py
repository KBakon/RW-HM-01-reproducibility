"""Merge durable independent shards into a sorted, deduplicated exact map."""
import csv
from pathlib import Path
p=Path(__file__).resolve().parent; main=p/'c4_exact_map.csv'; rows={};fields=None
for f in [main]+sorted(p.glob('c4_shard_*.csv')):
 if not f.exists():continue
 with f.open(newline='') as stream:
  reader=csv.DictReader(stream);fields=reader.fieldnames
  for row in reader:
   key=tuple(int(row[k]) for k in ('d','a','b','n'))
   if key in rows and rows[key]!=row:raise ValueError(f'conflicting duplicate {key}')
   rows[key]=row
with main.open('w',newline='') as stream:
 writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(rows[k] for k in sorted(rows))
print('merged',len(rows),'rows')
