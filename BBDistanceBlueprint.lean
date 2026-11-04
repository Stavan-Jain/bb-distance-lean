import Architect
import QECBlueprint
import BBDistance.Gross

/-! Blueprint annotations for the Gross distance proof; general nodes come from QECLean. -/

attribute [blueprint "thm:base-distance"
  (title := /-- The $[[72,12,6]]$ base has chain distance six -/)
  (statement := /-- Every nonzero class in the homology of the base
    bivariate-bicycle complex is represented only by chains of weight at least
    six, and six is attained. -/)
  (proof := /-- The lower bound is \cref{thm:small-cycle-floor} together with
    the check that no weight-six cycle is a boundary; the witness realises the
    bound. -/)]
  Quantum.Stabilizer.Homological.BB.base_chain_distance_eq_6

attribute [blueprint "thm:gross-logical-weight"
  (title := /-- Every gross logical has weight at least six -/)
  (statement := /-- Pulled back along the cover of \cref{def:x-double-cover},
    the base floor gives a weight-six lower bound for every nontrivial logical
    operator of the gross code. -/)
  (proof := /-- Pushing a gross chain down to the base is a chain map, so it
    sends cycles to cycles and boundaries to boundaries, and it cannot increase
    weight. If the pushed-down chain is a nonzero class, \cref{thm:base-distance}
    applies directly. -/)]
  Quantum.Stabilizer.Homological.BB.gross_logical_weight_ge_6

attribute [blueprint "thm:gross-sector-dichotomy"
  (title := /-- Safe and dangerous sectors -/)
  (statement := /-- Every nontrivial gross logical operator falls into one of
    two sectors, and in each the weight is at least twelve: the *safe* sector,
    where the two sheets of the cover contribute independently, and the
    *dangerous* sector, where they do not and a finer argument is needed. -/)
  (proof := /-- In the safe sector the class survives to each sheet separately,
    so \cref{thm:gross-logical-weight} applies twice and the weights add to at
    least $6 + 6 = 12$. The dangerous sector is where the deck transformation
    acts trivially on homology; there the hexagon and direction-pair bounds
    take over, classifying the light stabilizers and confining the remaining
    classes to Smith cosets whose floor is again twelve. -/)]
  Quantum.Stabilizer.Homological.BB.gross_pauli_distance_eq_12_of_two_sectors

attribute [blueprint "def:gross-stabilizer-code"
  (title := /-- The gross code as a stabilizer code -/)
  (statement := /-- IBM's gross code presented as a \cref{def:stabilizer-code}
    with $n = 144$ and $k = 12$. -/)]
  Quantum.Stabilizer.Homological.BB.grossStabilizerCode

attribute [blueprint "thm:gross-distance"
  (title := /-- The gross code has distance exactly twelve -/)
  (statement := /-- The gross code (\cref{def:gross-stabilizer-code}) has
    distance exactly $12$, unconditionally. -/)
  (proof := /-- The lower bound is \cref{thm:gross-sector-dichotomy}, moved from
    chains to Pauli weights by \cref{thm:chain-weight-transfer}. A weight-twelve
    logical operator is exhibited explicitly, making the distance exact rather
    than a bound. Every finite check in the argument is discharged in the
    kernel, so the theorem depends on exactly the three standard axioms. -/)]
  Quantum.Stabilizer.Homological.BB.grossStabilizerCode_hasCodeDistance_12_uncond

attribute [blueprint "def:gross-code-with-distance"
  (title := /-- The gross code, packaged -/)
  (statement := /-- The $[[144,12,12]]$ gross code as an inhabitant of
    \cref{def:code-with-distance} — the headline result of this
    development. -/)]
  Quantum.Stabilizer.Homological.BB.grossStabilizerCodeWithDistance
