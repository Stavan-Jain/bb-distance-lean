"""Emit Gross packaging data from the checked-in data.json.

Only the seven certificate definitions are emitted. The hand-maintained
proofs that consume them are never modified.
"""
import argparse
import json
import os
import sys

from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE.parents[1] / 'BBDistance/Gross/StabilizerCodeData.lean'

def wrap(body: str, width: int = 96, indent: str = "  ") -> str:
    """Greedy-wrap a one-line Lean list literal at ', ' boundaries (<=width)."""
    parts = body.split(", ")
    out, cur = [], ""
    for part in parts:
        cand = part if not cur else cur + ", " + part
        if len(cand) > width and cur:
            out.append(cur + ",")
            cur = indent + part
        else:
            cur = cand
    out.append(cur)
    return "\n".join(out)


d = json.loads((PACKAGE / "data.json").read_text())
def G(ab): return f"(({ab[0]} : ZMod 12), ({ab[1]} : ZMod 6))"
def E(e):  return f"((({e[0]} : ZMod 12), ({e[1]} : ZMod 6)), ({e[2]} : Fin 2))"
def Glist(lst): return "[" + ", ".join(G(x) for x in lst) + "]"
def Elist(lst): return "[" + ", ".join(E(x) for x in lst) + "]"
phiX = '[' + ', '.join(f'({G(pp)}, {E(e)})' for pp, e in d['PhiX']) + ']'
phiZ = '[' + ', '.join(f'({G(pp)}, {E(e)})' for pp, e in d['PhiZ']) + ']'
redP2 = '[' + ', '.join(Glist(b) for b in d['redP2']) + ']'
redCM = '[' + ', '.join(Glist(b) for b in d['redCM']) + ']'
dropSet = Glist(d['dropFaces'])
logX = '[' + ', '.join(Elist(c) for c in d['logX']) + ']'
logZ = '[' + ', '.join(Elist(c) for c in d['logZ']) + ']'

TEMPLATE = '''/-
GENERATED FILE — DO NOT HAND-EDIT (edits WILL be clobbered by regen).
Generator : bb-distance-lean:scripts/gross/gen_packaging.py
Data      : scripts/gross/data.json (candidate binary linear algebra certificates)
Regen     : python3 scripts/gross/generate.py --force
To change this file, change the generator or data and regenerate.
-/
/-
# Gross packaging data (§1 of the `StabilizerCode 144 12` packaging)

The seven offline-validated data defs consumed by
`Gross/StabilizerCode.lean`:
* `dropSet` — 6 faces / 6 vertices dropped to trim 144 generators to 132;
* `redP2` / `redCM` — reduced bases of `ker ∂₂` / `ker cutMap` (6 each),
  satisfying `redP2 j (dropSet i) = [i=j]`;
* `phiX` / `phiZ` — left-inverse "syndrome decoder" certificates;
* `logX` / `logZ` — a symplectic basis of 12 X-cycles + 12 Z-dual-cycles
  with identity `12×12` intersection matrix.
-/

import BBDistance.Gross.Defs

namespace Quantum.Stabilizer.Homological.BB

/-! ## §1  Offline-validated data (see `qec-lab:experiments/bb_lab/phase5/data.json`) -/

/-- The 6 faces / 6 vertices dropped to trim 144 generators down to 132. -/
def dropSet : List GrossGroup :=
  %DROPSET%

/-- Reduced `ker ∂₂` basis (6 face-supports). `∂₂(redP2 j) = 0` and
`(redP2 j)(dropSet i) = [i=j]`. -/
def redP2 : List (List GrossGroup) :=
  %REDP2%

/-- Reduced `ker cutMap` basis (6 vertex-supports). -/
def redCM : List (List GrossGroup) :=
  %REDCM%

/-- Face-independence syndrome decoder: support list of (output-coord, qubit). -/
def phiX : List (GrossGroup × (GrossGroup × Fin 2)) :=
  %PHIX%

/-- Vertex-independence syndrome decoder. -/
def phiZ : List (GrossGroup × (GrossGroup × Fin 2)) :=
  %PHIZ%

/-- 12 X-logical cycle representatives (qubit supports). -/
def logX : List (List (GrossGroup × Fin 2)) :=
  %LOGX%

/-- 12 Z-logical dual-cycle representatives (qubit supports). -/
def logZ : List (List (GrossGroup × Fin 2)) :=
  %LOGZ%

end Quantum.Stabilizer.Homological.BB
'''

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing StabilizerCodeData.lean")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    target = args.out
    if target.exists() and not args.force:
        print(f"refusing to overwrite {target} (pass --force)", file=sys.stderr)
        return 1
    body = TEMPLATE
    for k, v in [("%DROPSET%", dropSet), ("%REDP2%", redP2), ("%REDCM%", redCM),
                 ("%PHIX%", phiX), ("%PHIZ%", phiZ), ("%LOGX%", logX), ("%LOGZ%", logZ)]:
        body = body.replace(k, "  " + wrap(v))
    with target.open("w") as f:
        f.write(body)
    print(f"wrote {target} ({len(body)} chars)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
