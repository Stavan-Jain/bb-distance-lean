import BBDistance.Certificate
import QEC.Stabilizer.Framework.Homological.Certificate

/-!
Check that BB certificate modules and the shared QECLean certificate API can
be imported together. The BB compatibility modules must reuse the canonical
declarations, including the shift-based list-packing specification used by
both the BB and mitten developments. No concrete case study is imported.
-/

#check PackedDigits.packList_eq_ofDigits
#check PackedDigits.packList_eq_packF
#check PackedDigits.popcount32_packF
#check PackedDigits.popcount128_packF
#check PackedDigits.binary_reconstruction_list_sound

#print axioms PackedDigits.packList_eq_ofDigits
#print axioms PackedDigits.binary_reconstruction_list_sound
