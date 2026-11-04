# The Gross [[144, 12, 12]] code

This development proves the exact distance of the Gross bivariate-bicycle code
and packages it as `Code[[144, 12, 12]]`. Its declarations retain the namespace
`Quantum.Stabilizer.Homological.BB`.

The code is a free double cover of a `[[72, 12, 6]]` base. The lower bound
instantiates QECLean's general doubling theorem: a base logical floor, a
weight-twelve witness, a deck homotopy, a safe-sector seam-coset floor, and
admissibility of every light base boundary. The Pauli-level result goes through
QECLean's code-agnostic fold-and-double theorem.

| Read | Purpose |
|---|---|
| [Defs](Defs.lean), [CoverTransfer](CoverTransfer.lean) | Polynomials, complexes, and the double cover |
| [DeckHomotopy](DeckHomotopy.lean), [Witness](Witness.lean) | Deck action on homology and the upper-bound witness |
| [BaseDistance](BaseDistance.lean) | The base distance is six |
| [DangerousSector](DangerousSector.lean), [SafeSector](SafeSector.lean) | Reduction to general sector bounds |
| [SeamBZ](SeamBZ.lean) | Checked seam-coset and light-boundary certificates |
| [LayerInstance](LayerInstance.lean) | Application of the general doubling theorems |
| [StabilizerCode](StabilizerCode.lean), [Distance](Distance.lean) | Canonical stabilizer presentation and exact-distance packaging |

The Brouwer–Zimmermann certificates check 252 light boundaries and two walks
covering 510,414 words. All finite checks run in Lean's kernel. The public
unconditional results are `grossStabilizerCode_hasCodeDistance_12_uncond` and
`grossStabilizerCodeWithDistance`.

```lean
import BBDistance.Gross.Distance
import QEC.Stabilizer.Framework.Core.CodeNotation

open scoped Quantum.StabilizerGroup
open Quantum.Stabilizer.Homological.BB

#check (grossStabilizerCodeWithDistance : Code[[144, 12, 12]])
#print axioms grossStabilizerCode_hasCodeDistance_12_uncond
#print axioms grossStabilizerCodeWithDistance
```

The generated modules are `SeamBZData.lean` and `StabilizerCodeData.lean`.
See the [generator instructions](../../scripts/gross/README.md). The
`scripts/GrossCheck.lean` regression verifies that the capstones continue to use
the general QECLean theorems. Blueprint annotations are preserved in the
optional `BBDistanceBlueprint` library.
