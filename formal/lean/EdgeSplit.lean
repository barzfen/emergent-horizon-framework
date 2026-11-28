/-!
EHF / CBB-BIN — a first formally checkable invariant.

A Boolean label is assigned to each vertex. An edge's comparison bit is
the XOR of the labels of its endpoints. When an existing edge (u,v) is
replaced by (u,w) and (w,v), XOR-composing the two new edge bits gives
the original bit, independently of the new vertex's label.

This is a local identity, not a theorem that all EHF growth operations
preserve every global property of a Hamiltonian cycle.
-/

namespace EHF.BinaryGrowth

/-- Comparison bit of two Boolean vertex labels. -/
def edgeBit (u v : Bool) : Bool := Bool.xor u v

/-- Subdividing an edge preserves its XOR comparison after composition. -/
theorem split_preserves_edgeBit (u w v : Bool) :
    Bool.xor (edgeBit u w) (edgeBit w v) = edgeBit u v := by
  cases u <;> cases w <;> cases v <;> rfl

#print axioms EHF.BinaryGrowth.split_preserves_edgeBit

end EHF.BinaryGrowth
