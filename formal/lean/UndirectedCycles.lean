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
  iseqv := {
    refl := by intro x; exact sameTail_refl x
    symm := by intro x y h; exact sameTail_symm h
    trans := by intro x y z h₁ h₂; exact sameTail_trans h₁ h₂
  }

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

/-- Filtering a label absent from a listing does not change it. -/
private theorem forget_absent {α : Type u} [DecidableEq α]
    (xs : List α) (w : α) (hf : w ∉ xs) :
    forget w xs = xs := by
  induction xs with
  | nil => simp [forget]
  | cons x xs ih =>
      have hx : x ≠ w := by
        intro h
        exact hf (by simp [h])
      have ht : w ∉ xs := by
        intro h
        exact hf (List.mem_cons_of_mem _ h)
      simp [forget, hx]
      intro a ha heq
      exact ht (by simpa [heq] using ha)

/-- Deleting the newly inserted label restores the complete original
    listing, for every insertion index including 0 and the end. -/
theorem forget_insertIdx {α : Type u} [DecidableEq α]
    (xs : List α) (w : α) (i : Nat)
    (fresh : w ∉ xs) (hi : i ≤ xs.length) :
    forget w (xs.insertIdx i w) = xs := by
  induction xs generalizing i with
  | nil =>
      cases i with
      | zero => simp [forget]
      | succ i =>
          simp only [List.length_nil] at hi
          omega
  | cons x xs ih =>
      have hx : x ≠ w := by
        intro h
        exact fresh (by simp [h])
      have ht : w ∉ xs := by
        intro h
        exact fresh (List.mem_cons_of_mem _ h)
      cases i with
      | zero =>
          simp [forget, hx]
          intro a ha heq
          exact ht (by simpa [heq] using ha)
      | succ i =>
          have hi' : i ≤ xs.length := by
            simp only [List.length_cons] at hi
            omega
          simpa [forget, hx] using
            congrArg (List.cons x) (ih i ht hi')

/-- Every insertion has the declared predecessor even after taking
    the undirected quotient. -/
theorem delete_after_insertion {α : Type u} [DecidableEq α]
    (xs : List α) (w : α) (i : Nat)
    (fresh : w ∉ xs) (hi : i ≤ xs.length) :
    deleteClass w (classOf (xs.insertIdx i w)) = classOf xs := by
  rw [deleteClass_classOf, forget_insertIdx xs w i fresh hi]

/-- Core EHF-CBB uniqueness result after quotienting orientation:
    two insertion histories yielding the same undirected child
    necessarily have the same undirected parent. Slot indices may be
    different when one history uses the reversed parent orientation. -/
theorem unique_undirected_parent {α : Type u} [DecidableEq α]
    (xs ys : List α) (w : α) (i j : Nat)
    (freshX : w ∉ xs) (freshY : w ∉ ys)
    (hi : i ≤ xs.length) (hj : j ≤ ys.length)
    (hchild : classOf (xs.insertIdx i w) =
      classOf (ys.insertIdx j w)) :
    classOf xs = classOf ys := by
  have h := congrArg (deleteClass w) hchild
  simpa [delete_after_insertion xs w i freshX hi,
    delete_after_insertion ys w j freshY hj] using h

/-- Erasing a known entry and inserting its value at the exact
    position reconstructs the full ordered listing. -/
theorem reinsert_erased_label {α : Type u}
    (zs : List α) (w : α) (i : Nat)
    (h : zs[i]? = some w) :
    (zs.eraseIdx i).insertIdx i w = zs := by
  induction zs generalizing i with
  | nil =>
      cases i <;> simp at h
  | cons x xs ih =>
      cases i with
      | zero =>
          have hx : x = w := by simpa using h
          subst x
          simp
      | succ i =>
          have ht : xs[i]? = some w := by simpa using h
          simpa using congrArg (List.cons x) (ih i ht)

/-- Each occurrence of a vertex admits a concrete position witness. -/
theorem exists_label_index {α : Type u}
    (zs : List α) (w : α) (hw : w ∈ zs) :
    ∃ i : Nat, zs[i]? = some w := by
  induction zs with
  | nil => simp at hw
  | cons x xs ih =>
      rcases List.mem_cons.mp hw with hEq | hTail
      · refine ⟨0, ?_⟩
        simp [hEq]
      · obtain ⟨i, hIdx⟩ := ih hTail
        refine ⟨i + 1, ?_⟩
        simpa using hIdx

/-- Every (root-fixed, oriented) child listing containing w is the
    insertion image of some predecessor listing. The same statement
    therefore holds at the undirected quotient level. This theorem
    does not *by itself* constrain the predecessor to be valid or fresh;
    those facts require the Hamiltonian no-duplicate hypotheses. -/
theorem every_child_is_an_insertion {α : Type u}
    (zs : List α) (w : α) (hw : w ∈ zs) :
    ∃ (parent : List α) (i : Nat),
      classOf zs = classOf (parent.insertIdx i w) := by
  obtain ⟨i, hIdx⟩ := exists_label_index zs w hw
  refine ⟨zs.eraseIdx i, i, ?_⟩
  rw [reinsert_erased_label zs w i hIdx]

#print axioms EHF.Undirected.every_child_is_an_insertion
#print axioms EHF.Undirected.unique_undirected_parent
#print axioms EHF.Undirected.delete_after_insertion
#print axioms EHF.Undirected.classOf_eq_iff
#print axioms EHF.Undirected.deleteClass_classOf
#print axioms EHF.Undirected.delete_reversal_invariant

end EHF.Undirected
