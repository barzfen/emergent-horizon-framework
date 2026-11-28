import Init

/-!
EHF-LEAN-02 — all-slot growth of a complete-graph Hamiltonian cycle.

A Hamiltonian cycle is represented by a *directed, rooted listing* of
the vertices of a finite vertex set, visited exactly once and with at
least three vertices. Consecutive entries are joined, including the
closing edge from the last vertex back to the first.

The ambient graph is complete: all these edges are admissible.
Rotations, reversal, and constraints of more general graphs are not
quotiented or modelled here.

For every edge slot (including the closing edge), inserting a fresh
vertex yields a Hamiltonian cycle on the enlarged set. Erasing
the inserted vertex *at that slot* restores the original listing.
-/

namespace EHF.CycleGrowth

universe u

/-- A cyclic vertex listing that visits precisely the declared finite
    vertex labels once. The first entry fixes the cyclic rotation. -/
structure HamiltonianCycle (α : Type u) (labels : List α) where
  vertices : List α
  nodup : vertices.Nodup
  covers : ∀ x : α, x ∈ vertices ↔ x ∈ labels
  atLeastThree : 3 ≤ vertices.length

/-- A fresh vertex inserted into an in-range position cannot introduce
    a repeated vertex. -/
private theorem nodup_insertIdx_fresh {α : Type u}
    (xs : List α) (w : α) (i : Nat)
    (h : xs.Nodup) (hfresh : w ∉ xs) (hi : i ≤ xs.length) :
    (xs.insertIdx i w).Nodup := by
  induction xs generalizing i with
  | nil =>
      cases i with
      | zero => simp
      | succ i =>
          simp only [List.length_nil] at hi
          omega
  | cons x xs ih =>
      cases i with
      | zero =>
          simpa using (List.nodup_cons.mpr ⟨hfresh, h⟩ :
            (w :: x :: xs).Nodup)
      | succ i =>
          have hd : x ∉ xs := (List.nodup_cons.mp h).1
          have ht : xs.Nodup := (List.nodup_cons.mp h).2
          have hf : w ∉ xs := by
            intro hw
            exact hfresh (List.mem_cons_of_mem _ hw)
          have hb : i ≤ xs.length := by
            simp only [List.length_cons] at hi
            omega
          have hne : x ≠ w := by
            intro heq
            apply hfresh
            simp [heq]
          have hx : x ∉ xs.insertIdx i w := by
            intro hm
            rcases (List.mem_insertIdx hb).mp hm with hEq | hMem
            · exact hne hEq
            · exact hd hMem
          have htail : (xs.insertIdx i w).Nodup :=
            ih i ht hf hb
          simpa using (List.nodup_cons.mpr ⟨hx, htail⟩ :
            (x :: xs.insertIdx i w).Nodup)

/-- Slots are the n directed edges in a cyclic listing of n vertices:
    index 0 denotes the edge leaving the first vertex, while n-1
    denotes the closing edge returning to the first vertex. -/
def insertAfter {α : Type u} {labels : List α}
    (c : HamiltonianCycle α labels) (w : α)
    (fresh : w ∉ labels)
    (slot : Fin c.vertices.length) :
    HamiltonianCycle α (w :: labels) := by
  have hi : slot.val + 1 ≤ c.vertices.length := by omega
  have hw : w ∉ c.vertices := by
    intro h
    exact fresh ((c.covers w).mp h)
  refine {
    vertices := c.vertices.insertIdx (slot.val + 1) w
    nodup := nodup_insertIdx_fresh c.vertices w (slot.val + 1)
      c.nodup hw hi
    covers := ?_
    atLeastThree := ?_
  }
  · intro x
    constructor
    · intro hm
      rcases (List.mem_insertIdx hi).mp hm with hEq | hOld
      · simp [hEq]
      · exact List.mem_cons_of_mem _ ((c.covers x).mp hOld)
    · intro hm
      rcases (List.mem_cons).mp hm with hEq | hOld
      · exact (List.mem_insertIdx hi).mpr (Or.inl hEq)
      · exact (List.mem_insertIdx hi).mpr
          (Or.inr ((c.covers x).mpr hOld))
  · rw [List.length_insertIdx_of_le_length hi w]
    have hmin : 3 ≤ c.vertices.length := c.atLeastThree
    omega

/-- Growth adds exactly one vertex for every permitted edge slot. -/
theorem insertion_length {α : Type u} {labels : List α}
    (c : HamiltonianCycle α labels) (w : α)
    (fresh : w ∉ labels) (slot : Fin c.vertices.length) :
    (insertAfter c w fresh slot).vertices.length = c.vertices.length + 1 := by
  unfold insertAfter
  simp [List.length_insertIdx_of_le_length (show slot.val + 1 ≤ c.vertices.length by omega) w]

/-- Deleting the inserted vertex from the chosen slot gives the parent,
    including for the closing-edge slot. -/
theorem delete_inserted {α : Type u} {labels : List α}
    (c : HamiltonianCycle α labels) (w : α)
    (fresh : w ∉ labels) (slot : Fin c.vertices.length) :
    (insertAfter c w fresh slot).vertices.eraseIdx (slot.val + 1) =
      c.vertices := by
  unfold insertAfter
  exact List.eraseIdx_insertIdx_self w

/-- The child contains precisely the original vertex labels and w. -/
theorem insertion_membership {α : Type u} {labels : List α}
    (c : HamiltonianCycle α labels) (w : α)
    (fresh : w ∉ labels) (slot : Fin c.vertices.length) (x : α) :
    x ∈ (insertAfter c w fresh slot).vertices ↔
      x = w ∨ x ∈ c.vertices := by
  have hi : slot.val + 1 ≤ c.vertices.length := by omega
  change x ∈ c.vertices.insertIdx (slot.val + 1) w ↔ _
  exact List.mem_insertIdx hi

/-- A fixed parent and a fresh vertex give different child listings
    when inserted after different edges. Thus all n slots are distinct
    at the level of rooted directed cyclic listings. -/
theorem distinct_slots {α : Type u} {labels : List α}
    (c : HamiltonianCycle α labels) (w : α)
    (fresh : w ∉ labels)
    (p q : Fin c.vertices.length)
    (heq : (insertAfter c w fresh p).vertices =
      (insertAfter c w fresh q).vertices) : p = q := by
  have hp : p.val + 1 ≤ c.vertices.length := by omega
  have hq : q.val + 1 ≤ c.vertices.length := by omega
  have hw : w ∉ c.vertices := by
    intro hm
    exact fresh ((c.covers w).mp hm)
  have hn : (c.vertices.insertIdx (p.val + 1) w).Nodup :=
    nodup_insertIdx_fresh c.vertices w (p.val + 1) c.nodup hw hp
  have hlen : p.val + 1 <
      (c.vertices.insertIdx (p.val + 1) w).length := by
    rw [List.length_insertIdx_of_le_length hp w]
    omega
  have hP : (c.vertices.insertIdx (p.val + 1) w)[p.val + 1]? =
      some w := by
    simpa [hp] using
      (List.getElem?_insertIdx_self (l := c.vertices)
        (i := p.val + 1) (x := w))
  have hQ' : (c.vertices.insertIdx (q.val + 1) w)[q.val + 1]? =
      some w := by
    simpa [hq] using
      (List.getElem?_insertIdx_self (l := c.vertices)
        (i := q.val + 1) (x := w))
  change c.vertices.insertIdx (p.val + 1) w =
    c.vertices.insertIdx (q.val + 1) w at heq
  have hQ : (c.vertices.insertIdx (p.val + 1) w)[q.val + 1]? =
      some w := by
    rw [heq]
    exact hQ'
  have hIdx : p.val + 1 = q.val + 1 :=
    (List.Nodup.getElem?_inj hlen hn).mp (hP.trans hQ.symm)
  apply Fin.ext
  omega

/-- A generated child determines the exact insertion index and
    the exact ordered parent listing even if two proposed parents have
    different declared universes. This establishes non-overlap of the
    generated child listings across parents and slots. -/
theorem unique_ancestry {α : Type u} {leftLabels rightLabels : List α}
    (parentA : HamiltonianCycle α leftLabels)
    (parentB : HamiltonianCycle α rightLabels)
    (w : α) (freshA : w ∉ leftLabels) (freshB : w ∉ rightLabels)
    (p : Fin parentA.vertices.length)
    (q : Fin parentB.vertices.length)
    (heq : (insertAfter parentA w freshA p).vertices =
      (insertAfter parentB w freshB q).vertices) :
    p.val = q.val ∧ parentA.vertices = parentB.vertices := by
  have hp : p.val + 1 ≤ parentA.vertices.length := by omega
  have hq : q.val + 1 ≤ parentB.vertices.length := by omega
  have hn : (parentA.vertices.insertIdx (p.val + 1) w).Nodup :=
    (insertAfter parentA w freshA p).nodup
  have hlen : p.val + 1 <
      (parentA.vertices.insertIdx (p.val + 1) w).length := by
    rw [List.length_insertIdx_of_le_length hp w]
    omega
  have hP : (parentA.vertices.insertIdx (p.val + 1) w)[p.val + 1]? =
      some w := by
    simpa [hp] using
      (List.getElem?_insertIdx_self (l := parentA.vertices)
        (i := p.val + 1) (x := w))
  have hQ' : (parentB.vertices.insertIdx (q.val + 1) w)[q.val + 1]? =
      some w := by
    simpa [hq] using
      (List.getElem?_insertIdx_self (l := parentB.vertices)
        (i := q.val + 1) (x := w))
  have hlist : parentA.vertices.insertIdx (p.val + 1) w =
      parentB.vertices.insertIdx (q.val + 1) w := heq
  have hQ : (parentA.vertices.insertIdx (p.val + 1) w)[q.val + 1]? =
      some w := by
    rw [hlist]
    exact hQ'
  have hIndex : p.val + 1 = q.val + 1 :=
    (List.Nodup.getElem?_inj hlen hn).mp (hP.trans hQ.symm)
  have hSlot : p.val = q.val := by omega
  constructor
  · exact hSlot
  · have hDel :=
      congrArg (fun xs : List α => xs.eraseIdx (p.val + 1)) hlist
    simpa [hIndex] using hDel

#print axioms EHF.CycleGrowth.unique_ancestry
#print axioms EHF.CycleGrowth.distinct_slots
#print axioms EHF.CycleGrowth.delete_inserted
#print axioms EHF.CycleGrowth.insertion_length
#print axioms EHF.CycleGrowth.insertion_membership

end EHF.CycleGrowth
