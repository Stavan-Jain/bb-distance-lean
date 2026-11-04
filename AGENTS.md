# bb-distance-lean

This repository contains concrete bivariate-bicycle distance formalizations,
their certificate checkers, and deterministic generators. General QEC theory
lives in the pinned QECLean dependency.

- Preserve proofs verbatim when moving them, adapting only imports and names.
- Every new theorem and lemma needs a `/-- ... -/` docstring.
- Never use `sorry`, `native_decide`, or custom axioms in committed code.
  Accepted dependencies are `propext`, `Classical.choice`, and `Quot.sound`;
  declarations needing fewer axioms are also allowed.
- Verify with `lake env lean scripts/AxiomCheck.lean` and `#print axioms`.
- Reuse QECLean and mathlib APIs. Promote new abstractions to QECLean only
  when they have a clear, general mathematical interface.
- Never hand-edit a file carrying `GENERATED FILE — DO NOT HAND-EDIT`.
  Change its emitter or input under `scripts/bravyi360/` or `scripts/gross/`, regenerate, and
  run the corresponding `generate.py --verify`.
- Keep imports acyclic and cover every local module from `BBDistance.lean`.
  Run `python3 scripts/check_layout.py` after moving or adding modules.
- Use `LEAN_NUM_THREADS=1` for full builds; run only one build in this
  checkout at a time. Heavy certificate checking can take tens of minutes.
- The toolchain, QECLean commit, and transitive dependency lockfile are pinned.
  Do not run `lake update`, fetch a new mathlib cache, or rebuild large parts
  of mathlib without the user's authorization. Reuse matching cached
  dependencies when available.
- Keep historical timing evidence in `provenance/original-validation/`
  unchanged. It measures the original development, not the extracted tree.
