"""Build the per-residue jsd_conservation column for one arm, from pinned Pfam alignments.

Route, with no aligner in the loop: Pfam full alignments carry our own UniProt entry as a
row, declared by a `#=GS <name> AC <accession>` line. That row's gap pattern is an exact
residue-to-column map, so no profile alignment and no HMM is needed. Residues outside every
Pfam envelope, and residues that fall in an insert column, read null.
"""

from __future__ import annotations

import gzip
import hashlib
import pathlib

import jsd as J
import numpy as np

ALN = pathlib.Path(__file__).resolve().parent / "aln"


def stream_match_matrix(path: pathlib.Path, want_acc: str):
    """Return (M, mask, our_row_index, n_rows, sha256) reading only the match columns."""
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    names, gs = [], {}
    mask = None
    keep: list[np.ndarray] = []
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("//"):
                continue
            if line.startswith("#=GS "):
                p = line.split(None, 3)
                if len(p) >= 4 and p[2] == "AC":
                    gs[p[1]] = p[3].strip().split(".")[0]
                continue
            if line.startswith("#"):
                continue
            name, _, seq = line.partition(" ")
            seq = seq.strip()
            if not seq:
                continue
            arr = np.frombuffer(seq.encode("ascii", "replace"), dtype=np.uint8)
            if mask is None:
                mask = ~(((arr >= ord("a")) & (arr <= ord("z"))) | (arr == ord(".")))
            if arr.shape[0] != mask.shape[0]:
                continue  # wrapped or malformed row; Pfam full is unwrapped
            names.append(name)
            keep.append(J._LUT[arr[mask]])
    M = np.vstack(keep)
    ours = [i for i, n in enumerate(names) if gs.get(n) == want_acc]
    return M, mask, (ours[0] if ours else None), names, gs, sha


def residue_scores(fam: str, acc: str, kind: str = "full"):
    """UniProt residue number -> JSD, for the family's own row of this accession."""
    path = ALN / f"{fam}.{kind}.sto.gz"
    if not path.exists():
        return None, {"family": fam, "status": "alignment-missing"}
    M, mask, ours, names, gs, sha = stream_match_matrix(path, acc)
    meta = {
        "family": fam,
        "kind": kind,
        "rows": int(M.shape[0]),
        "match_columns": int(M.shape[1]),
        "sha256_gz": sha,
        "alignment_width": int(mask.shape[0]),
    }
    if ours is None:
        meta["status"] = "accession-absent"
        return None, meta
    name = names[ours]
    beg = int(name.rsplit("/", 1)[1].split("-")[0])
    meta["status"] = "ok"
    meta["row"] = name
    w = J.henikoff(M)
    s = J.jsd(M, w)
    # walk our own row: every non-gap match column is one UniProt residue, from `beg`.
    # a residue also occupies insert columns; those carry no shared column and read null.
    raw = None
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith(name + " "):
                raw = line.rstrip("\n").partition(" ")[2].strip()
                break
    arr = np.frombuffer(raw.encode("ascii", "replace"), dtype=np.uint8)
    out, pos, mcol = {}, beg, 0
    for i in range(arr.shape[0]):
        c = chr(arr[i])
        if mask[i]:  # match column
            if c != "-":
                out[pos] = float(s[mcol])
                pos += 1
            mcol += 1
        else:  # insert column
            if c != ".":
                pos += 1  # residue exists, no shared column
    meta["residues_scored"] = len(out)
    meta["uniprot_span"] = [beg, pos - 1]
    return out, meta
