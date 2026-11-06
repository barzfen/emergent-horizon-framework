"""Matrix-element-weighted angular contrast on a restricted hard slice."""
import json
import numpy as np
from angular_ensemble import grid
from six_soft import gram, moments


def hard_nodes(n):
    # Solid-angle measure on a patch in the incoming-pair rest frame.
    nodes, weights = np.polynomial.legendre.leggauss(n)
    u_max = np.cos(np.radians(65))
    for u,wu in zip(u_max*nodes,weights):
        radius = np.sqrt(1-u*u)
        for phi,wp in zip(np.radians(67.5+22.5*nodes),weights):
            yield (u,radius*np.sin(phi),radius*np.cos(phi)),wu*wp


def calculate(n,soft_n,grams):
    directions,moment = grid(20,40,soft_n)
    openings = (.008,.004,.002,.001)
    sums = np.zeros((4,3))
    for beam,w in hard_nodes(n):
        for i,t in enumerate(openings):
            row,hard_weight = moments(beam,t,grams,directions,moment,True)["all"]
            # The hard weight is t² times the full tree squared amplitude.
            # Its common factor t² cancels across events at each opening.
            sums[i] += w*hard_weight*np.array([1,row[0],row[1]])
    mean,quad = (sums[:,i]/sums[:,0] for i in (1,2))
    contrast = quad/mean
    values = np.column_stack((mean,quad,contrast))
    diffs = np.diff(-values,axis=0)/np.array([3*t*t/4 for t in openings[:-1]])[:,None]
    estimates = (4*diffs[1:]-diffs[:-1])/3
    np.testing.assert_allclose(estimates[0],estimates[1],rtol=.003,atol=.02)
    return estimates[1]


if __name__ == "__main__":
    grams = gram()
    report={}
    for n,soft_n in ((3,24),(5,48),(7,48)):
        report[str(n)] = calculate(n,soft_n,grams).tolist()
        print(n,report[str(n)],flush=True)
    np.testing.assert_allclose(report["5"],report["7"],rtol=.005,atol=.02)
    print(json.dumps({"columns":["mean_K","mean_K_cos2phi","quadratic_normalized_moment"],
                      "hard_grid_to_coefficients":report},indent=2))
