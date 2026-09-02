import gzip
import hashlib
import json
import pathlib
import sys
import urllib.request

FAMS = [
    "PF00071",
    "PF00017",
    "PF00018",
    "PF07714",
    "PF00063",
    "PF01576",
    "PF02736",
    "PF00782",
    "PF00069",
    "PF00102",
    "PF00856",
    "PF01753",
    "PF00349",
    "PF03727",
    "PF00078",
    "PF06815",
    "PF06817",
    "PF00075",
    "PF00998",
    "PF00004",
    "PF02359",
    "PF02933",
    "PF17862",
    "PF02786",
    "PF02787",
    "PF25596",
    "PF02142",
]
KIND = sys.argv[1] if len(sys.argv) > 1 else "seed"
ONLY = sys.argv[2:] or FAMS
OUT = pathlib.Path("aln")
OUT.mkdir(exist_ok=True)
rec = {}
for fam in ONLY:
    dest = OUT / f"{fam}.{KIND}.sto.gz"
    if not dest.exists() or dest.stat().st_size == 0:
        url = f"https://www.ebi.ac.uk/interpro/wwwapi/entry/pfam/{fam}/?annotation=alignment:{KIND}"
        req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=600) as r:
            ver = r.headers.get("InterPro-Version")
            dest.write_bytes(r.read())
    else:
        ver = None
    raw = dest.read_bytes()
    try:
        text = gzip.decompress(raw).decode("utf-8", "replace")
    except Exception:
        text = raw.decode("utf-8", "replace")
    rows = [ln for ln in text.splitlines() if ln and not ln.startswith(("#", "//"))]
    rec[fam] = {
        "bytes_gz": len(raw),
        "rows": len(rows),
        "sha256_gz": hashlib.sha256(raw).hexdigest(),
        "interpro_version": ver,
    }
    print(
        f"{fam:9s} {KIND:5s} rows={len(rows):7d} gz={len(raw) / 1e6:8.2f} MB ver={ver}", flush=True
    )
pathlib.Path(f"aln-{KIND}-index.json").write_text(json.dumps(rec, indent=1))
