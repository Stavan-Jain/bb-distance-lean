import QEC.Stabilizer.Framework.Homological.BZCertificate
import Mathlib.LinearAlgebra.Pi

namespace Quantum.Stabilizer.Homological.F2Mask

variable {ι κ : Type} {n m : Nat} (e : ι ≃ Fin n) (f : κ ≃ Fin m)

/--
A certified XOR reconstruction is a linear map between binary chain spaces.
-/
def reconLinear (w : List (Nat × Nat)) : (ι → ZMod 2) →ₗ[ZMod 2] (κ → ZMod 2) where
  toFun c := chainOfMask f (reconX w (maskOf e c))
  map_add' a b := by rw [maskOf_add, reconX_xor, chainOfMask_xor]
  map_smul' a c := by
    rcases (by decide : ∀ z : ZMod 2, z = 0 ∨ z = 1) a with rfl | rfl
    · simp [maskOf_zero, reconX_zero, chainOfMask_zero]
    · simp

/--
Reading back a binary reconstruction gives the original bounded XOR result.
-/
theorem maskOf_reconLinear (w : List (Nat × Nat)) (c : ι → ZMod 2)
    (h : ∀ p ∈ w, p.2 < 2 ^ m) :
    maskOf f (reconLinear e f w c) = reconX w (maskOf e c) := by
  exact maskOf_chainOfMask f (reconX_lt w _ m h)

end Quantum.Stabilizer.Homological.F2Mask

namespace Quantum.Stabilizer.Homological

open scoped BigOperators

/--
A linear map on a finite binary coordinate space is determined by point
masses.
-/
theorem linearMap_eq_of_single {ι M : Type} [Fintype ι] [DecidableEq ι]
    [AddCommMonoid M] [Module (ZMod 2) M]
    (T U : (ι → ZMod 2) →ₗ[ZMod 2] M)
    (h : ∀ i, T (Pi.single i 1) = U (Pi.single i 1)) : T = U := by
  apply LinearMap.pi_ext
  intro i z
  rcases (by decide : ∀ a : ZMod 2, a = 0 ∨ a = 1) z with rfl | rfl
  · simp
  · exact h i

/--
A left inverse checked on point masses proves injectivity of a binary linear
map.
-/
theorem injective_of_decoder_single {ι M : Type} [Fintype ι] [DecidableEq ι]
    [AddCommMonoid M] [Module (ZMod 2) M]
    (T : (ι → ZMod 2) →ₗ[ZMod 2] M)
    (D : M →ₗ[ZMod 2] (ι → ZMod 2))
    (h : ∀ i, D (T (Pi.single i 1)) = Pi.single i 1) : Function.Injective T := by
  have hd : D.comp T = LinearMap.id := linearMap_eq_of_single _ _ h
  intro a b hab
  have h := congrArg D hab
  have hda := LinearMap.congr_fun hd a
  have hdb := LinearMap.congr_fun hd b
  simpa using hda.symm.trans (h.trans hdb)

end Quantum.Stabilizer.Homological
