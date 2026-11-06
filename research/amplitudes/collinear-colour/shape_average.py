"""Fixed-mass Dalitz-patch integration of the six-gluon soft contrast."""
import json
import sys
import numpy as np
from angular_ensemble import grid
from six_soft import gram, moments, ETA
from weighted_angles import hard_nodes

PATCH = ((.46,.54),(.625,17/24))
OPENINGS = (.008,.004,.002,.001)


def hard_event(x,y,beam,rho):
    # Units Q=1. The massive cluster recoils against two massless spectators.
    energy, other = x/2,y/2
    last = 1-energy-other
    parent = np.sqrt(energy**2-rho**2)
    cosine = (last**2-parent**2-other**2)/(2*parent*other)
    assert abs(cosine)<1
    px,pz = other*cosine,other*np.sqrt(1-cosine**2)
    beams = [(-.5,*(-sign*.5*np.array(beam))) for sign in (1,-1)]
    p=np.array([(energy/2,parent/2,0,rho/2),*beams,
                (other,px,0,pz),(last,-parent-px,0,-pz),
                (energy/2,parent/2,0,-rho/2)])
    assert np.max(np.abs(p.sum(axis=0)))<1e-12
    assert np.max(np.abs(np.sum(p*p*ETA,axis=1)))<1e-12
    assert abs(np.sum((p[0]+p[-1])**2*ETA)-rho**2)<1e-12
    return p


def integrate(shape_n,beam_n,soft_n,grams):
    nodes,weights=np.polynomial.legendre.leggauss(shape_n)
    def along(limits):
        a,b=limits
        return list(zip((a+b)/2+(b-a)/2*nodes,weights))
    directions,moment=grid(20,40,soft_n)
    sums=np.zeros((4,3))
    minimum_gap=180.
    for x,wx in along(PATCH[0]):
        for y,wy in along(PATCH[1]):
            for beam,wb in hard_nodes(beam_n):
                for j,rho in enumerate(OPENINGS):
                    p=hard_event(x,y,beam,rho)
                    separation=np.degrees(np.arccos(np.clip((p[:,1:]/p[:,:1])@directions.T,-1,1))).min()
                    minimum_gap=min(minimum_gap,float(separation))
                    row,weight=moments(beam,rho,grams,directions,moment,True,p)["all"]
                    sums[j]+=wx*wy*wb*weight*np.array([1,row[0],row[1]])
    mean,m2=(sums[:,i]/sums[:,0] for i in (1,2))
    table=np.column_stack((mean,m2,m2/mean))
    diff=-np.diff(table,axis=0)/np.array([3*t*t/4 for t in OPENINGS[:-1]])[:,None]
    ext=(4*diff[1:]-diff[:-1])/3
    np.testing.assert_allclose(ext[0],ext[1],rtol=.003,atol=.02)
    return {"coefficients":ext[1].tolist(),"minimum_sampled_separation_degrees":minimum_gap}


if __name__=="__main__":
    grams=gram()
    if sys.argv[1:] == ["--centre"]:
        PATCH=((.5,.5),(2/3,2/3))
        print(json.dumps(integrate(1,5,36,grams),indent=2))
        raise SystemExit
    cases={}
    for g in ((2,3,20),(3,4,28),(4,5,36)):
        cases[str(g)]=integrate(*g,grams)
        print(g,cases[str(g)],flush=True)
    np.testing.assert_allclose(cases["(3, 4, 28)"]["coefficients"],
                               cases["(4, 5, 36)"]["coefficients"],rtol=.007,atol=.02)
    print(json.dumps({"patch":PATCH,"columns":["mean_K","mean_K_cos2phi","normalized_contrast_K"],
                      "grids":cases},indent=2))
