import Init

/-!
EHF-LEAN-03 — rooted undirected cyclic listings up to reversal.

To remove cyclic-rotation redundancy, a single distinguished old vertex
is held at the first position of each cycle listing. All remaining
vertices are recorded as a tail. Reversing that tail changes the
orientation but not the unoriented cycle.

The quotient below identifies a tail with its reversal. This is the
reflection component of the dihedral symmetry, after the first vertex
is fixed by normalization. Neither an underlying-graph adjacency
constraint nor an ordering/cardinality theorem is asserted here.
-/

namespace EHF.Undirected

universe u

/-- Two root-fixed listings of the same undirected cyclic ordering
    differ by either identity or reversal of the tail. -/
def sameTail {α : Type u} (xs ys : List α) : Prop :=
  xs = ys ∨ xs = ys.reverse

theorem sameTail_refl {α : Type u} (xs : List α) :
    sameTail xs xs := Or.inl rfl

theorem sameTail_symm {α : Type u} {xs ys : List α}
    (h : sameTail xs ys) : sameTail ys xs := by
  rcases h with he | he
  · exact Or.inl he.symm
  · right
    rw [he]
    simp

theorem sameTail_trans {α : Type u} {xs ys zs : List α}
    (h₁ : sameTail xs ys) (h₂ : sameTail ys zs) :
    sameTail xs zs := by
  rcases h₁ with h₁ | h₁
  · rcases h₂ with h₂ | h₂
    · exact Or.inl (h₁.trans h₂)
    · exact Or.inr (h₁.trans h₂)
  · rcases h₂ with h₂ | h₂
    · exact Or.inr (by simpa [h₂] using h₁)
    · left
      calc
        xs = ys.reverse := h₁
        _ = (zs.reverse).reverse := by rw [h₂]
        _ = zs := by simp

/-- The reversal equivalence relation, explicitly specified to avoid
    conflicts with other list equivalence structures. -/
def reversalSetoid (α : Type u) : Setoid (List α) where
  r := sameTail
  iseqv := ⟨(fun x => sameTail_refl x),
    (fun _ _ h => sameTail_symm h),
    (fun _ _ _ h₁ h₂ => sameTail_trans h₁ h₂)⟩

/-- An unoriented cyclic listing with a distinguished fixed root, encoded
    by the non-root tail up to its reversal. Valid cycles are those whose
    tail lists contain every non-root label exactly once and have length
    at least two. -/
def UndirectedTail (α : Type u) : Type u :=
  Quotient (reversalSetoid α)

/-- Convert a concrete oriented tail to an undirected equivalence class. -/
def classOf {α : Type u} (xs : List α) : UndirectedTail α :=
  Quotient.mk (reversalSetoid α) xs

/-- Reversing the orientation of a root-fixed cyclic listing does not
    change its underlying undirected cycle. -/
theorem classOf_reverse {α : Type u} (xs : List α) :
    classOf xs = classOf xs.reverse :=
  Quotient.sound (Or.inr (by simp))

/-- Exact quotient equality: no further equivalence beyond identity
    and reversal is silently introduced. -/
theorem classOf_eq_iff {α : Type u} (xs ys : List α) :
    classOf xs = classOf ys ↔ sameTail xs ys := by
  constructor
  · exact Quotient.exact
  · intro h
    exact Quotient.sound h

/-- Remove every occurrence of a newly introduced label. In the EHF
    Hamiltonian-cycle use case the label occurs exactly once. -/
def forget {α : Type u} [DecidableEq α] (w : α) (xs : List α) :
    List α :=
  xs.filter (fun x => decide (x ≠ w))

/-- Forgetting a label commutes with reversing the direction. -/
theorem forget_reverse {α : Type u} [DecidableEq α] (w : α)
    (xs : List α) :
    forget w xs.reverse = (forget w xs).reverse := by
  simp [forget]

/-- Deletion is well-defined on undirected cycle classes: an arbitrary
    orientation choice cannot affect the class of the predecessor. -/
def deleteClass {α : Type u} [DecidableEq α] (w : α) :
    UndirectedTail α → UndirectedTail α :=
  Quotient.lift
    (fun xs => classOf (forget w xs))
    (by
      intro xs ys h
      apply Quotient.sound
      rcases h with he | he
      · exact Or.inl (congrArg (forget w) he)
      · exact Or.inr (by rw [he, forget_reverse]))

/-- On a concrete representative, quotient deletion agrees with
    deleting the label from the oriented listing. -/
theorem deleteClass_classOf {α : Type u} [DecidableEq α]
    (w : α) (xs : List α) :
    deleteClass w (classOf xs) = classOf (forget w xs) := rfl

/-- A reversal of the child cannot change its undirected predecessor. -/
theorem delete_reversal_invariant {α : Type u} [DecidableEq α]
    (w : α) (xs : List α) :
    deleteClass w (classOf xs) =
      deleteClass w (classOf xs.reverse) := by
  rw [← classOf_reverse xs]

#print axioms EHF.Undirected.classOf_eq_iff
#print axioms EHF.Undirected.deleteClass_classOf
#print axioms EHF.Undirected.delete_reversal_invariant

end EHF.Undirected
