/- Verify that Gross uses the generic QECLean doubling and certificate APIs. -/
import BBDistance.Gross.Distance

open Quantum Quantum.Stabilizer.Homological Quantum.Stabilizer.Homological.BB

open Lean in
run_cmd do
  let env ← getEnv
  let required := #[
    ``SmallCycleData.cycle_weight_ge_6,
    ``XDoubleCoverData.deckTrivial_of_bezout,
    ``XDoubleCoverData.dangerous_bound_of_single_shape,
    ``XDoubleCoverData.dangerous_bound_of_pair_shape]
  -- The chain-level capstone runs the generic sector dichotomy and safe-floor reduction.
  let chainRoute := #[``XDoubleCoverData.safeFloor_of_seamCosetFloor,
    ``XDoubleCoverData.chainWeight_ge_double_of_sectors]
  -- Both certificate inputs must come from the generic Brouwer–Zimmermann layer.
  let bz := #[``XDoubleCoverData.SeamBZCertificate.seamCosetFloor,
    ``XDoubleCoverData.SeamBZCertificate.boundary_census,
    ``F2Mask.bz_ok_of_xorSpan, ``F2Mask.kernel_eq_sum_of_peel]
  -- The unconditional Pauli-level capstones go through the code-agnostic
  -- fold-and-double theorem in its sector form, with the generic admissible
  -- dispatch as the dangerous floor and the seam-coset floor as the safe one.
  let foldDouble := #[``XDoubleCoverData.isLeast_logicalWeight_two_mul_of_foldDouble,
    ``Quantum.Stabilizer.FoldDouble.isLeast_logicalWeight_two_mul_of_floors_sector,
    ``XDoubleCoverData.condition_F_of_seamCosetFloor,
    ``XDoubleCoverData.dangerousFloorNZ_of_admissible]
  -- ... and therefore no longer through Gross's own case split over the census.
  let perInstance := #[``dangerous_sector_of_classification]
  let targets := #[
    (``gross_chain_distance_eq_12,
      #[``XDoubleCoverData.chain_distance_eq_double_of_admissible,
        ``XDoubleCoverData.chain_distance_eq_double,
        ``XDoubleCoverData.dangerousFloorNZ_of_admissible] ++ chainRoute ++ bz, perInstance),
    (``gross_pauli_distance_eq_12, foldDouble ++ bz, perInstance),
    (``grossStabilizerCode_hasCodeDistance_12_uncond,
      #[``gross_pauli_distance_eq_12, ``StabilizerGroup.hasCodeDistance_of_isLeast]
        ++ foldDouble ++ bz, perInstance),
    (``grossStabilizerCodeWithDistance,
      #[``gross_pauli_distance_eq_12, ``StabilizerGroup.hasCodeDistance_of_isLeast]
        ++ foldDouble ++ bz, perInstance),
    (``grossStabilizerCode_hasCodeDistance_12,
      #[``XDoubleCoverData.pauli_distance_eq_double,
        ``StabilizerGroup.hasCodeDistance_of_isLeast,
        ``XDoubleCoverData.SeamBZCertificate.boundary_census], #[])]
  for (root, endpoints, forbidden) in targets do
    let mut pending := #[root]
    let mut visited : NameSet := {}
    while !pending.isEmpty do
      let name := pending.back!
      pending := pending.pop
      if visited.contains name then continue
      visited := visited.insert name
      if let some info := env.find? name then
        if let some value := info.value? (allowOpaque := true) then
          pending := pending ++ value.getUsedConstants.filter (fun n =>
            n.toString.startsWith "Quantum." || n.toString.startsWith "_private.QEC." || n.toString.startsWith "_private.BBDistance.")
    for dependency in required ++ endpoints do
      unless visited.contains dependency do
        throwError "{root} no longer uses the generic theorem {dependency}"
    for dependency in forbidden do
      if visited.contains dependency then
        throwError "{root} uses the per-instance assembly {dependency}"
  logInfo "Gross generic proof dependencies OK (including BZ and fold-and-double)"
