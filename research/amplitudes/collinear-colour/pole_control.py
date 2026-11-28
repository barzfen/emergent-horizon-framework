"""Compare leading-parent and full hard amplitudes at identical momenta."""
import json
import numpy as np
from angular_ensemble import grid
from six_soft import ETA, COUNT, amplitudes, gram
from shape_average import PATCH, OPENINGS, hard_event
from weighted_angles import hard_nodes
from plane_scan import extract


def rotated_event(x,y,beam,rho,axis):
    p=hard_event(x,y,beam,rho)
    p[0,2:]=rho/2*axis
    p[-1,2:]=-p[0,2:]
    return p


def tensor_stats(v,hard,soft):
    weight=np.einsum('ah,ab,bh->',v.conj(),hard,v,optimize=True).real
    assert weight>0
    corr=np.einsum('ah,aibj,bh->ij',v.conj(),soft,v,optimize=True).real/weight
    np.testing.assert_allclose(corr.sum(axis=1),0,atol=1e-10)
    return weight,corr


def baseline(x,y,beam,axis,grams):
    words,hard,soft=grams
    mask=(COUNT>=2)&(COUNT<=4)
    def even(h):
        plus=amplitudes(rotated_event(x,y,beam,h,axis),words)[:,mask]
        minus=amplitudes(rotated_event(x,y,beam,-h,axis),words)[:,mask]
        return h*(plus-minus)/2
    coarse, fine=even(.002),even(.001)
    leading=(4*fine-coarse)/3
    reverse=[words.index((w[0],*w[1:-1][::-1],w[-1])) for w in words]
    assert np.linalg.norm(leading+leading[reverse])<1e-6*np.linalg.norm(leading)
    projected=(leading-leading[reverse])/2
    weight,corr=tensor_stats(projected,hard,soft)
    ref_weight,ref_corr=tensor_stats((fine-fine[reverse])/2,hard,soft)
    np.testing.assert_allclose(corr,ref_corr,atol=2e-4)
    assert abs(weight/ref_weight-1)<2e-4
    return weight,corr


def integration(angle,beam_n,soft_n,grams):
    angle=np.radians(angle)
    cosine,sine=np.cos(angle),np.sin(angle)
    axis=np.array([sine,cosine])
    directions,moment=grid(20,40,soft_n)
    directions[:,1:]=directions[:,1:]@np.array([[cosine,-sine],[sine,cosine]])
    nodes,weights=np.polynomial.legendre.leggauss(2)
    def along(limits):
        a,b=limits
        return list(zip((a+b)/2+(b-a)/2*nodes,weights))
    words,hard,soft=grams
    mask=(COUNT>=2)&(COUNT<=4)
    sums={k:np.zeros((4,3)) for k in ("full","pole_matched_weights","pole_frozen_weights")}
    for x,wx in along(PATCH[0]):
        for y,wy in along(PATCH[1]):
            for beam,wb in hard_nodes(beam_n):
                pole_weight,pole_corr=baseline(x,y,beam,axis,grams)
                for j,t in enumerate(OPENINGS):
                    p=rotated_event(x,y,beam,t,axis)
                    actual_weight,actual_corr=tensor_stats(t*amplitudes(p,words)[:,mask],hard,soft)
                    inverse=1/(p[:,0,None]-p[:,1:]@directions.T)
                    kinematic=-np.einsum('ia,a,ja->ij',p,ETA,p)
                    for name,weight,corr in (("full",actual_weight,actual_corr),
                                              ("pole_matched_weights",actual_weight,pole_corr),
                                              ("pole_frozen_weights",pole_weight,pole_corr)):
                        r=np.einsum('ij,ik,jk->k',kinematic*corr,inverse,inverse)
                        sums[name][j]+=wx*wy*wb*weight*np.array([1,np.mean(r),np.mean(r*moment)])
    return {name:extract(values) for name,values in sums.items()}


if __name__=="__main__":
    grams=gram()
    report={}
    for angle in (0,90):
        coarse=integration(angle,2,32,grams)
        fine=integration(angle,3,48,grams)
        for name in fine:
            np.testing.assert_allclose(fine[name],coarse[name],rtol=.025,atol=.15)
        report[str(angle)]={"coarse":coarse,"fine":fine}
        print(angle,report[str(angle)],flush=True)
    print(json.dumps({"columns":["mean_K","mean_K_cos2phi","normalized_contrast_K"],
                      "angles":report},indent=2))
