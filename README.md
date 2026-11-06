# bb-distance-lean

Lean proofs of distance bounds for bivariate-bicycle (BB) quantum codes, built
on [QECLean](https://github.com/Stavan-Jain/QECLean). It contains the Gross
`[[144, 12, 12]]` and Bravyi360 `[[360, 12, 24]]` proofs. Each case study keeps
its proof, checked certificates, and deterministic generators together.

## Dependency and build

QECLean is pinned to commit
[`b5a9f13d17b656091bf95024be8ebaf457d2c3a6`](https://github.com/Stavan-Jain/QECLean/commit/b5a9f13d17b656091bf95024be8ebaf457d2c3a6)
in both `lakefile.toml` and `lake-manifest.json`. This is the shared certificate foundations commit
on [QECLean PR #102](https://github.com/Stavan-Jain/QECLean/pull/102), rather than a
moving branch or a released version. Lean is pinned to `v4.30.0-rc2`; all
transitive dependencies are locked in the manifest.

With [elan](https://github.com/leanprover/elan) installed:

```sh
git clone https://github.com/Stavan-Jain/bb-distance-lean.git
cd bb-distance-lean
lake exe cache get
LEAN_NUM_THREADS=1 lake build
lake env lean scripts/AxiomCheck.lean
lake env lean scripts/PublicApi.lean
lake env lean scripts/GrossCheck.lean
LEAN_NUM_THREADS=1 lake build QEC.Stabilizer.Framework.Homological.Certificate
lake env lean scripts/SharedCertificateCheck.lean
```

The certificate build is substantial. Keep `LEAN_NUM_THREADS=1` to limit memory
use. CI also provides swap space. `lake exe cache get` downloads the matching
mathlib artifacts; it does not replace checking the proofs in this repository.
Avoid `lake update` unless deliberately updating the pinned dependencies.

## Public theorems

```lean
import BBDistance.Gross.Distance
import BBDistance.Bravyi360.Distance
import QEC.Stabilizer.Framework.Core.CodeNotation

open scoped Quantum.StabilizerGroup
open Quantum.Stabilizer.Homological.BB.Bravyi360

#check (Quantum.Stabilizer.Homological.BB.grossStabilizerCodeWithDistance : Code[[144, 12, 12]])
#check (stabilizerCodeWithDistance : Code[[360, 12, 24]])
#print axioms distance_lower_bound
#print axioms stabilizerCode_hasDistance24
#print axioms stabilizerCodeWithDistance
```

The declaration namespace is preserved from QECLean; the import root is now
`BBDistance`. The proof policy permits only `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorry`, `native_decide`, or custom axioms.

## Reading the development

- [Gross proof overview](BBDistance/Gross/README.md) explains the single-cover
  distance-doubling proof; [Gross distance](BBDistance/Gross/Distance.lean) exposes
  its unconditional theorem.
- [Bravyi360 distance](BBDistance/Bravyi360/Distance.lean) exposes the exact-distance theorem
  and packaged code.
- [Proof overview](BBDistance/Bravyi360/README.md) explains the two double covers,
  the complete orbit census, and the checks of their lifts.
- [Assembly](BBDistance/Bravyi360/Assembly.lean) joins the lower-bound cases.
- [Certificate library](BBDistance/Certificate.lean) collects the certificate
  machinery used by the concrete proof.
- [Generators](scripts/bravyi360/README.md) describes reproduction and independent
  kernel replay.

QECLean supplies the quantum-code definitions, homological BB framework, binary
mask API, and general cover results. It also owns flat-lift reductions, trimming
redundant checks, dual-witness soundness, and the ordinary and indexed
orbit-census principles.

The packed-arithmetic helpers shared with
[mitten-distance-lean](https://github.com/Stavan-Jain/mitten-distance-lean) now
have one canonical implementation in QECLean. Eight modules under
`BBDistance/Certificate/` preserve their import paths as import-only
compatibility modules. Their declaration namespaces remain unchanged, allowing
both downstream packages to reuse the same API. The larger search and
certificate implementation lives here. New work should reuse QECLean's
definitions and APIs rather than copy them.

## Reproduction and verification

```sh
python3 scripts/check_layout.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/bravyi360/generate.py --verify
python3 scripts/gross/generate.py --verify
```

The Bravyi360 generator reproduces 192 Lean modules from 34 hashed inputs. The
Gross generators reproduce two additional data modules. Their output is
checked by Lean's kernel; Python and the original search are not trusted proof
steps. CI runs these checks, builds every local module, audits axioms, and checks
the public code parameters.

For a fresh source build followed by independent replay of every local safe
declaration, see the [validation instructions](scripts/bravyi360/README.md#validation).
This is a separate, heavier check than loading compiled imports.

Optional Gross blueprint annotations can be checked with
`LEAN_NUM_THREADS=1 lake build BBDistanceBlueprint`. They reuse the general nodes
in QECLean's blueprint.

## Provenance

The initial proof was extracted from QECLean commit
[`88ffe0a`](https://github.com/Stavan-Jain/QECLean/commit/88ffe0a5d166bfb3c63b23228d4beb59f5f53384);
the generators came from qec-lab commit
[`b014c83`](https://github.com/Stavan-Jain/qec-lab/commit/b014c83417f12c9786d95831de919f33e3494370).
[The module map](provenance/module-migration.json) records all 345 moved modules.
Gross was extracted from the later QECLean foundations commit `da172536…`, with
generators from qec-lab commit `aca715a4…`; the same map records these origins.
Proof definitions and bodies were preserved; imports, generated-file banners,
and build tooling were adapted to this repository.

[Original validation evidence](provenance/original-validation/) is preserved
unchanged as historical evidence for the original QECLean layout. Its module
counts and timings are not measurements of this standalone layout.

The later [shared-certificate migration](provenance/shared-certificate-foundations.json)
records which modules became compatibility imports and the single proof adapter
for shift-based list packing. The original extraction records remain intact.

Licensed under [Apache 2.0](LICENSE); see [NOTICE](NOTICE).
