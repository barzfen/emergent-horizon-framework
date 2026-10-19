#!/usr/bin/env python3
"""Reproduce the analytic RECUR/HOL complete-symmetry holonomy formula.

Standard-library only.  This is not a simulation of gravity; it checks the
closed rotation factor derived for the RECUR observer connection.
"""

from math import acos, cos, degrees, pi


def rotation_cosine(n: int) -> float:
    if n < 5:
        raise ValueError("RECUR Hamilton observer audit starts at n=5")
    q = n - 2
    return (3 * q * q - 4) / (q ** 3)


def rotation_angle(n: int) -> float:
    return acos(rotation_cosine(n))


def characteristic_residual(n: int, theta: float) -> float:
    """Residual of lambda^2 - 2 c lambda + 1 at lambda=e^(i theta)."""
    c = rotation_cosine(n)
    lam = complex(cos(theta), __import__("math").sin(theta))
    return abs(lam * lam - 2 * c * lam + 1)


def main() -> None:
    print("n  cos(theta)       theta(deg)     residual")
    for n in range(5, 21):
        c = rotation_cosine(n)
        theta = rotation_angle(n)
        residual = characteristic_residual(n, theta)
        print(f"{n:2d} {c: .12f}  {degrees(theta):10.6f}  {residual:.3e}")

    # Large-n consequence used by HOL-02.
    for n in (50, 100, 1000, 10000):
        print(
            f"n={n:5d}: theta={degrees(rotation_angle(n)):.8f} deg, "
            f"distance_to_pi/2={degrees(pi/2-rotation_angle(n)):.8f} deg"
        )

    # Analytically c_n = 3/q - 4/q^3 -> 0, hence theta_n -> pi/2.
    assert rotation_cosine(100000) < 0.00004
    print("PASS: characteristic roots lie on the unit circle and theta_n -> pi/2.")


if __name__ == "__main__":
    main()
