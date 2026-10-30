"""Scientific figure for RW-004; regenerates curves from the saved protocol."""
import json
from fractions import Fraction as F
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import probe as p

HERE = Path(__file__).resolve().parent
x = json.loads((HERE/'results.json').read_text())
triads = [x['triad_a'], x['triad_c']]
plt.rcParams.update({'font.size':10, 'svg.fonttype':'none', 'axes.spines.top':False,
                     'axes.spines.right':False})
fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
for name, label, color in [('prepare0_read1','Prepare cycle 0; read cycle 1','#7653b7'),
                         ('prepare2_read_position2','Prepare cycle 2; position detector','#187f88')]:
    initial, detector = p.PROTOCOLS[name]
    ys = [p.probability_curve(p.eig(p.old.lift(t,F(1))),initial,detector) for t in triads]
    axs[0].plot(p.TIMES,100*np.abs(ys[0]-ys[1]),label=label,color=color,lw=2)
    rows = [r for r in x['access_rows'] if r['protocol']==name and r['kappa']!='0']
    axs[1].plot([float(F(r['kappa'])) for r in rows],
                [100*r['max_probability_gap_on_grid'] for r in rows],
                'o-',label=label,color=color,lw=2,ms=4)
axs[0].set(xscale='log',xlim=(0.01,100),xlabel='Observation time (mean hop-time units)',
           ylabel='Absolute probability gap (percentage points)',title='A. Time window at switching rate 1')
axs[1].set(xscale='log',xlabel='Switching rate / spatial hop rate',
           ylabel='Largest gap on the declared time grid (pp)',title='B. Both weak and fast switching suppress the gap')
for ax in axs:
    ax.grid(alpha=.18)
    ax.set_ylim(bottom=0)
axs[0].legend(frameon=False,fontsize=8,loc='upper left')
fig.suptitle('EHF-RW-004: finite classical detection signal on the matched five-vertex pair',fontsize=11)
fig.savefig(HERE/'signal.svg')
print('Saved signal.svg')
