"""Plot the retained finite model; requires matplotlib, numpy and scipy."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

here = Path(__file__).parent
r = json.loads((here/'results.json').read_text())
n = r['states']
ones = set(r['ones'])
wall = np.array([sum((a in ones)!=(b in ones) for a,b in zip(c,c[1:]+c[:1])) for c in r['carrier']['states']])
f = (wall==2).astype(float)-r['equilibrium_two_wall_probability']
fig,axes = plt.subplots(1,2,figsize=(10.8,4.2),layout='constrained')
for row in r['rows']:
    epsilon = row['epsilon']
    L = np.zeros((n,n))
    for name,rate in (('fast_edges',1),('slow_edges',epsilon)):
        for i,j in r['carrier'][name]:
            L[i,i]+=rate;L[j,j]+=rate;L[i,j]-=rate;L[j,i]-=rate
    values,vectors = eigh(L)
    weights = (vectors[:,1:].T@f)**2/(f@f)
    for ax,rescale in zip(axes,(False,True)):
        t = np.logspace(-2,5 if not rescale else 1.4,300)
        y = weights@np.exp(-values[1:,None]*(t/epsilon if rescale else t))
        ax.semilogx(t,y,label=f'{epsilon:g}')
for ax in axes:
    ax.set_ylim(-.02,1.02)
    ax.grid(alpha=.22)
    ax.set_ylabel('Normalized excess two-domain signal')
axes[0].set_xlabel('Time (short-edge rate = 1)')
axes[1].set_xlabel('Rescaled time: epsilon × time')
axes[0].set_title('Rare long moves delay signal loss')
axes[1].set_title('Small-rate curves approach a common scale')
axes[0].legend(title='Long-edge rate',fontsize=8)
fig.suptitle('EHF-REV-02 · One 96-state MICRO/Pi component · Supplied rate law',fontsize=11)
fig.savefig(here/'rate-sensitivity.png',dpi=180)
print(here/'rate-sensitivity.png')
