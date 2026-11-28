"""Helicity and hard-angle control of the leading-soft angular correction."""
from collections import defaultdict
from itertools import combinations
from math import cos, sin, radians, sqrt, prod
import json
import numpy as np

from color_probe import bracket
from orders import tensor_rows
from soft_probe import current, I, METRIC


def colour_gram():
    tensors = defaultdict(lambda: defaultdict(int))
    for key,word,value in tensor_rows(5):
        tensors[word][key] += value
    words = sorted(tensors)
    flat = lambda key: sum(a*8**(4-j) for j,a in enumerate(key))
    inverse_metric = np.array([1/sqrt(prod(METRIC[(i//8**j)%8] for j in range(5)))
                               for i in range(8**5)])
    def dense(tensor):
        out = np.zeros(8**5)
        for key,value in tensor.items():
            out[flat(key)] = float(value)
        return out*inverse_metric
    arr = np.array([dense(tensors[w]) for w in words])
    hard = arr@arr.T
    soft = np.zeros((30,30))
    for c in I:
        vectors = np.array([dense(current(tensors[w],[int(i==j) for i in range(5)],c))
                            for w in words for j in range(5)])
        soft += vectors@vectors.T/METRIC[c]
        assert np.max(np.abs(vectors.reshape(6,5,-1).sum(axis=1))) < 1e-12
    return words,hard,soft.reshape(6,5,6,5)


def event(angle,t):
    angle = radians(angle)
    e, x = 6+3*t*t, -3*t*t
    boost = x/e
    # Opposite incoming directions in their rest frame, then boost so the
    # incoming sum agrees exactly with the outgoing momenta.
    beams = [(e+s*x*cos(angle),x+s*e*cos(angle),0,s*sqrt(e*e-x*x)*sin(angle))
             for s in (1,-1)]
    p = np.array([(3*(1+t*t),3*(1-t*t),0,6*t),*(-np.array(beams)),
                  (6,-6,0,0),(3*(1+t*t),3*(1-t*t),0,-6*t)])
    assert np.max(np.abs(p.sum(axis=0)))<1e-12
    assert np.max(np.abs(p[:,0]**2-(p[:,1:]**2).sum(axis=1)))<1e-12
    def spinor(row):
        E,X,_,Z = row*np.sign(row[0])
        return (1,X/(E+Z)) if E+Z>E-Z else (X/(E-Z),1)
    angles = ((1+t,1-t),*(spinor(row) for row in p[1:3]),(1,-1),(1-t,1+t))
    return p,angles


def radiation(angle,t,directions,grams):
    words,hard,soft = grams
    p,angles = event(angle,t)
    partial = np.array([t/prod(bracket(angles[a],angles[b])
                    for a,b in zip(w,w[1:]+w[:1])) for w in words])
    norm = partial@hard@partial
    corr = np.einsum('a,aibj,b->ij',partial,soft,partial)/norm
    denominators = p[:,0,None]-p[:,1:]@directions.T
    metric = np.diag([1,-1,-1,-1])
    eikonal = -(p@metric@p.T)*corr
    values = np.einsum('ij,ik,jk->k',eikonal,1/denominators,1/denominators)
    # Explicit sum over the ten MHV and ten parity-conjugate hard helicities.
    # With real angle spinors, all differ only by a common scalar in colour space.
    bracket_weights = np.array([bracket(angles[i],angles[j])**8
                                for i,j in combinations(range(5),2)])
    numerator = 2*np.sum(bracket_weights[:,None]*(norm*values),axis=0)
    denominator = 2*sum(bracket_weights)*norm
    np.testing.assert_allclose(numerator/denominator,values,rtol=1e-12)
    return values


def grid(low,high,n):
    low,high = cos(radians(high)),cos(radians(low))
    u = low+(np.arange(n)+.5)*(high-low)/n
    phi = (np.arange(4*n)+.5)*2*np.pi/(4*n)
    u,phi = np.meshgrid(u,phi,indexing='ij')
    r = np.sqrt(1-u*u)
    return np.stack((u,r*np.sin(phi),r*np.cos(phi)),axis=-1).reshape(-1,3),np.cos(2*phi).ravel()


def extract(angle,directions,grams,t):
    # Cancel the leading constant with two nonzero openings and use evenness.
    r1 = radiation(angle,t,directions,grams)
    r2 = radiation(angle,t/2,directions,grams)
    r3 = radiation(angle,t/4,directions,grams)
    coarse = (r1-r2)/(3*t*t/4)
    fine = (r2-r3)/(3*t*t/16)
    return (4*fine-coarse)/3


def main():
    grams = colour_gram()
    point = np.array([[0.,1.,0.]])
    assert abs(extract(90,point,grams,.004)[0]-14/3)<1e-6
    angles = [65,75,90,105,115]
    band = (20,40)
    directions,moment = grid(*band,96)
    rows = {}
    coarse_directions,coarse_moment = grid(*band,48)
    for angle in angles:
        coeff = extract(angle,directions,grams,.004)
        check = extract(angle,directions,grams,.002)
        assert np.max(np.abs(coeff-check))<.01
        mean,m2 = float(np.mean(coeff)),float(np.mean(coeff*moment))
        coarse = extract(angle,coarse_directions,grams,.004)
        np.testing.assert_allclose([np.mean(coarse),np.mean(coarse*coarse_moment)],
                                   [mean,m2],rtol=.0004)
        base = radiation(angle,.00025,directions,grams)-.00025**2*check
        r0,q0 = np.mean(base),np.mean(base*moment)
        shape_change = (m2-q0/r0*mean)/r0
        assert shape_change>0
        rows[angle] = [mean,m2,float(shape_change)]
    assert abs(rows[90][0]-2833.05765)<.01
    print(json.dumps({"columns":["mean_K","mean_K_cos2phi","quadratic_normalized_moment"],"hard_angles_degrees":rows,"soft_annulus_degrees":band,
                      "equal_event_average":np.mean(list(rows.values()),axis=0).tolist()},indent=2))


if __name__ == "__main__":
    main()
