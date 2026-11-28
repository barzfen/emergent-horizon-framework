"""Decompose the matched transverse fraction into within-group and mixture shifts."""
import json
import sys

import numpy as np

from electroweak_helicities import fraction


def summarize(path):
    with open(path) as f:
        scan = json.load(f)
    weights = np.zeros((3,2,5))
    for row in scan["rows"]:
        group = int(row["helicities"][0]!=row["helicities"][-1])
        for model,key in enumerate(("massless","custodial","electroweak")):
            weights[model,group] += 2*np.array(row[key])
    denominators = weights.sum(axis=2)
    group_shares = denominators/denominators.sum(axis=1,keepdims=True)
    fractions = weights[:,:,0]/(3*denominators)
    total = np.array([fraction(group.sum(axis=0)) for group in weights])
    np.testing.assert_allclose(total,(group_shares*fractions).sum(axis=1),rtol=1e-13)
    within = ((group_shares[2]+group_shares[0])/2)*(fractions[2]-fractions[0])
    mixture = ((fractions[2]+fractions[0])/2)*(group_shares[2]-group_shares[0])
    np.testing.assert_allclose(sum(within+mixture),total[2]-total[0],atol=1e-15)
    return dict(tilt=scan["tilt"],pair_over_Q=scan["pair_over_Q"],
                mW_over_pair=scan["mW_over_pair"],model_totals=total.tolist(),
                group_fractions=fractions.tolist(),group_denominator_shares=group_shares.tolist(),
                within_group=within.tolist(),mixture=mixture.tolist(),
                total_shift=float(total[2]-total[0]))


if __name__ == "__main__":
    rows = [summarize(path) for path in sys.argv[1:]]
    rows.sort(key=lambda r:(r["tilt"],-r["pair_over_Q"]))
    print(json.dumps(dict(models=["massless","custodial","electroweak"],
                          groups=["equal","opposite"],points=rows),indent=2))
