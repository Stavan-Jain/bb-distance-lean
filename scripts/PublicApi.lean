import BBDistance.Gross.Distance
import BBDistance.Bravyi360.Distance
import QEC.Stabilizer.Framework.Core.CodeNotation

open scoped Quantum.StabilizerGroup
open Quantum.Stabilizer.Homological.BB.Bravyi360

#check (stabilizerCodeWithDistance : Code[[360, 12, 24]])
#print axioms distance_lower_bound
#print axioms stabilizerCode_hasDistance24
#print axioms stabilizerCodeWithDistance

#check (Quantum.Stabilizer.Homological.BB.grossStabilizerCodeWithDistance : Code[[144, 12, 12]])
#print axioms Quantum.Stabilizer.Homological.BB.grossStabilizerCode_hasCodeDistance_12_uncond
#print axioms Quantum.Stabilizer.Homological.BB.grossStabilizerCodeWithDistance
