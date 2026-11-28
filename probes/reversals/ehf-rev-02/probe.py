"""EHF-REV-02: exact two-reversal algebra audit. Requires sympy."""
import sympy as s

I = s.eye(4)
P = s.zeros(4)
Q = s.zeros(4)
for i in range(4):
    P[i ^ 2, i] = 1
    Q[i ^ 1, i] = -1 if i & 2 else 1

assert P*P == I and Q*Q == I and P*Q + Q*P == s.zeros(4)
basis = [I, P, Q, P*Q]
assert s.Matrix.hstack(*(m.reshape(16, 1) for m in basis)).rank() == 4

# X commuting with P and Q: linear equations in 16 indeterminates.
x = s.symbols("x0:16")
X = s.Matrix(4, 4, x)
equations = list(X*P-P*X) + list(X*Q-Q*X)
coeff, _ = s.linear_eq_to_matrix(equations, x)
assert 16 - coeff.rank() == 4
assert P.eigenvals() == {-1: 2, 1: 2}
assert Q.eigenvals() == {-1: 2, 1: 2}
print("PASS: algebra rank 4, commutant dimension 4, P/Q eigenvalues ±1 each twice.")
print("Complex generated algebra: M2(C); 4D representation: two equivalent 2D copies.")
print("No canonical three inequivalent sectors or SU(3) 1:2:3 norm law.")
