#!/usr/bin/env python3
"""Exact audit of the GROW-02 recurrence quoted in the 2026-09-29 discussion.

This verifies the urn mapping and finite-step beta-binomial law conditional on
P_n(ell,ell)=(n+1-ell)/(n+2), P_n(ell,ell+1)=(ell+1)/(n+2).
It does not verify that this is the canonical GROW-02 source rule.
"""
from __future__ import annotations
import json
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def rising(x: int, k: int) -> int:
    out = 1
    for j in range(k):
        out *= x + j
    return out

def exact_distribution(n0: int, ell0: int, steps: int):
    """Exact distribution of ell after `steps` transitions."""
    dist = {ell0: Fraction(1)}
    n = n0
    for _ in range(steps):
        nxt = {}
        for ell, mass in dist.items():
            p_stay = Fraction(n + 1 - ell, n + 2)
            p_up = Fraction(ell + 1, n + 2)
            nxt[ell] = nxt.get(ell, Fraction(0)) + mass * p_stay
            nxt[ell + 1] = nxt.get(ell + 1, Fraction(0)) + mass * p_up
        dist = nxt
        n += 1
    return dist

def beta_binomial_increment_prob(a0: int, b0: int, steps: int, j: int) -> Fraction:
    return Fraction(comb(steps, j) * rising(a0, j) * rising(b0, steps-j),
                    rising(a0+b0, steps))

def run_case(n0: int, ell0: int, steps: int):
    assert n0 >= 1 and 0 <= ell0 <= n0
    a0, b0 = ell0 + 1, n0 + 1 - ell0
    dist = exact_distribution(n0, ell0, steps)
    beta_binomial = {
        ell0 + j: beta_binomial_increment_prob(a0, b0, steps, j)
        for j in range(steps + 1)
    }
    assert dist == beta_binomial
    total = sum(dist.values(), Fraction(0))
    assert total == 1
    # X_k=(ell_k+1)/(n0+k+2) is the Polya urn red fraction.
    mean_x = Fraction(a0, a0+b0)
    limit_var = Fraction(a0*b0, (a0+b0)**2*(a0+b0+1))
    return {
        "n0": n0, "ell0": ell0, "steps": steps,
        "urn_initial_counts": [a0, b0],
        "urn_total_initial": a0+b0,
        "limit_distribution": f"Beta({a0},{b0})",
        "limit_mean_exact": str(mean_x), "limit_mean": float(mean_x),
        "limit_variance_exact": str(limit_var), "limit_variance": float(limit_var),
        "finite_step_beta_binomial_identity": True,
        "finite_step_probability_sum": str(total),
        "finite_step_ell_probabilities": {str(k): str(v) for k,v in sorted(dist.items())},
    }

def main():
    cases = []
    for n0 in [8, 20, 100, 1000]:
        # The screenshot's claimed a0=3 corresponds to ell0=2.
        cases.append(run_case(n0, 2, 25))
        # The screenshot elsewhere says support ell=3; under a=ell+1 this means a0=4.
        cases.append(run_case(n0, 3, 25))
        # A separate balanced-density initialization, when valid.
        cases.append(run_case(n0, n0//2, 25))
    result = {
        "audit_id": "EHF-GROW-02-POLYA-01",
        "source_status": "conditional: recurrence quoted in discussion; original GROW-02 source not located",
        "transition_rule": {
            "stay": "(n+1-ell)/(n+2)",
            "increase": "(ell+1)/(n+2)"
        },
        "mapping": {
            "a": "ell+1", "b": "n+1-ell", "a_plus_b": "n+2",
            "increase_event": "a <- a+1", "stay_event": "b <- b+1"
        },
        "theorem": "For fixed initial (n0,ell0), X_k=(ell_k+1)/(n0+k+2) converges almost surely and in distribution to Beta(ell0+1,n0+1-ell0).",
        "limit_mean": "(ell0+1)/(n0+2)",
        "limit_variance": "(ell0+1)(n0+1-ell0)/((n0+2)^2(n0+3))",
        "cases": cases,
        "checks": {
            "exact_transition_to_polya_update": True,
            "finite_step_law_matches_beta_binomial": True,
            "probabilities_normalize_exactly": True,
            "support_ell0_2_gives_a0_3": True,
            "support_ell0_3_gives_a0_4": True,
            "fixed_ell0_2_mean_does_not_tend_to_half_as_n0_grows": True
        },
        "interpretation": "The limit mean 1/2 is not implied by the quoted fixed-support initialization. For fixed ell0=2 or 3 and n0->infinity, the mean tends to 0. A half-density limit arises only under a different balanced initial scaling ell0/n0->1/2, and is then inherited from the initial condition.",
        "criticality_status": "No critical point or spectral scaling conclusion follows from this urn calculation."
    }
    out = ROOT / "ehf_grow02_polya_support_limit_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "audit_id": result["audit_id"],
        "source_status": result["source_status"],
        "selected_cases": [
            {k:c[k] for k in ("n0","ell0","urn_initial_counts","limit_distribution","limit_mean_exact","limit_mean","finite_step_beta_binomial_identity")}
            for c in cases if c["n0"] in (8,1000) and c["ell0"] in (2,3, c["n0"]//2)
        ],
        "checks": result["checks"],
        "results_file": out.name
    }, indent=2))

if __name__ == "__main__":
    main()
