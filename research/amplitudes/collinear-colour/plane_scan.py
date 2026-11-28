"""Rotate the opening plane while keeping the hard recoil and beam cuts fixed."""
import json
import numpy as np
from angular_ensemble import grid
from six_soft import gram, moments, ETA
from shape_average import PATCH, OPENINGS, hard_event
from weighted_angles import hard_nodes


def scan(angle, shape_n, beam_n, soft_n, grams):
    angle = np.radians(angle)
    cosine, sine = np.cos(angle), np.sin(angle)
    directions, moment = grid(20,40,soft_n)
    y,z = directions[:,1].copy(),directions[:,2].copy()
    directions[:,1] = cosine*y+sine*z
    directions[:,2] = -sine*y+cosine*z
    nodes,weights = np.polynomial.legendre.leggauss(shape_n)
    def along(limits):
        a,b=limits
        return list(zip((a+b)/2+(b-a)/2*nodes,weights))
    sums = np.zeros((4,3))
    gap = 180.
    for x,wx in along(PATCH[0]):
        for y,wy in along(PATCH[1]):
            for beam,wb in hard_nodes(beam_n):
                for j,rho in enumerate(OPENINGS):
                    p=hard_event(x,y,beam,rho)
                    p[0,2:] = rho/2*np.array([sine,cosine])
                    p[-1,2:] = -p[0,2:]
                    assert np.max(np.abs(p.sum(axis=0)))<1e-12
                    assert np.max(np.abs(np.sum(p*p*ETA,axis=1)))<1e-12
                    sep = np.degrees(np.arccos(np.clip((p[:,1:]/p[:,:1])@directions.T,-1,1))).min()
                    gap = min(gap,float(sep))
                    row,weight=moments(beam,rho,grams,directions,moment,True,p)["all"]
                    sums[j]+=wx*wy*wb*weight*np.array([1,row[0],row[1]])
    return sums,gap


def extract(sums):
    mean,quad = (sums[:,i]/sums[:,0] for i in (1,2))
    table=np.column_stack((mean,quad,quad/mean))
    diff=-np.diff(table,axis=0)/np.array([3*t*t/4 for t in OPENINGS[:-1]])[:,None]
    ext=(4*diff[1:]-diff[:-1])/3
    np.testing.assert_allclose(ext[0],ext[1],rtol=.003,atol=.02)
    return ext[1].tolist()


if __name__=="__main__":
    grams=gram()
    records={}
    sums=[]
    for angle in (0,45,90,135):
        s,gap=scan(angle,2,2,32,grams)
        sums.append(s)
        records[str(angle)]={"coefficients":extract(s),"min_soft_hard_gap":gap}
        print(angle,records[str(angle)],flush=True)
    fine={}
    for angle in (0,90):
        s,gap=scan(angle,2,3,48,grams)
        fine[str(angle)]={"coefficients":extract(s),"min_soft_hard_gap":gap}
        print("refined",angle,fine[str(angle)],flush=True)
    print(json.dumps({"columns":["mean_K","mean_K_cos2phi","normalized_contrast_K"],
                      "angles":records,"refined":fine,
                      "four_angle_weighted_average":extract(sum(sums))},indent=2))
