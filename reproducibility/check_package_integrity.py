"""Read-only SHA-256 integrity check; no scientific campaign."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'manifests/SHA256SUMS.json').read_text(encoding='utf-8'))['files']
for n,h in m.items():
    p=(root/n).resolve()
    assert p.is_relative_to(root.resolve()),n
    assert hashlib.sha256(p.read_bytes()).hexdigest()==h,n
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert actual==set(m)|{'manifests/SHA256SUMS.json'}
print('PASS:',len(m),'file hashes')
