/-
GENERATED FILE — DO NOT HAND-EDIT
Generator: bb-distance-lean:scripts/bravyi360/generate.py
Emitter, relative to generator directory:
  emitters/generate_affine_search.py
Data and SHA-256 hashes: audit_manifest.json
Regenerate:
  python3 scripts/bravyi360/generate.py --force
-/

import BBDistance.Certificate.SearchCertificate
import BBDistance.Bravyi360.Adjoints

noncomputable section

set_option maxRecDepth 1000000
namespace Quantum.Stabilizer.Homological.F2Mask.AffineSearchData
open PackedDigits BB.Bravyi360 BB.Bravyi360.FiberData

set_option maxHeartbeats 0 in
-- Elaborating this packed certificate can exceed the default heartbeat budget.
/-- The top transpose fits in all256-bit search lanes. -/
theorem topTranspose_bounded : ∀ p ∈ topETransposeColumns, p.1 < 256 ∧ p.2 < 2^256 := by decide +kernel

set_option maxHeartbeats 0 in
-- Elaborating this packed certificate can exceed the default heartbeat budget.
/-- The bottom transpose fits in all256-bit search lanes. -/
theorem bottomTranspose_bounded : ∀ p ∈ bottomETransposeColumns, p.1 < 256 ∧ p.2 < 2^256 := by decide +kernel

end Quantum.Stabilizer.Homological.F2Mask.AffineSearchData
