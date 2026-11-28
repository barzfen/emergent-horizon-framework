# Visible-particle tagging on the photon-beam patch

The [leptonic decay test](electroweak-photon-decays.md) applied
cuts with known parent bosons. This calculation asks what happens
when a classifier sees only leptons and photons. It measures losses
and wrong assignments separately on the same production patch.

## Selection

Use the same tree production and spin-correlated narrow-width
decays. Sample each W or Z rest-frame decay direction and contract
the full production helicity amplitudes coherently with the decay
amplitudes. Sum photon helicities incoherently. The sample uses
massless charged leptons, labels each parent decay electron or muon
with equal probability, and samples the two Z chiralities with their
squared couplings. A Z produces two leptons of the same flavour.
Branching fractions are factored out, as in the earlier comparison.

Keep visible objects with `|eta| < 2.5` and either `pT > 0.25 mW`
or `pT > mW`. To model limited separation, visit the passing
objects in decreasing transverse momentum. Keep the first available
object and remove any softer object within the specified
`delta R` in the pseudorapidity–azimuth plane. Apply the same rule
to leptons and photons. Momentum and charge of surviving objects
are exact. This is a uniform separation model with no smearing,
missing-momentum reconstruction, or background processes.

| Category | Visible selection |
| --- | --- |
| WW | Two positive and two negative leptons, no photon. Tag the closest same-sign pair. |
| ZZ | Three positive and three negative leptons, no photon. Choose two disjoint opposite-sign same-flavour pairs closest to the Z mass. |
| Zγ | Two positive and two negative leptons, one photon. Choose the opposite-sign same-flavour pair closest to the Z mass. |
| γγ | One positive and one negative lepton, two photons. |
| Unassigned | Any other outcome, including a failed Z mass window. |

Every Z candidate must lie within 10% of the Z mass. The two mixed
ordered production channels share one reconstructed category.
The W tag uses the charged leptons alone. Parent labels enter
only after classification, when evaluating the migration matrix
and whether the tag picked the original selected pair. With exact
momenta and all objects resolved, true Z daughters have the
correct invariant mass by construction.

## Results

| Minimum pT / mW | Minimum separation | All objects | Reconstructed | WW efficiency | ZZ efficiency | WW label purity |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.25 | 0.00 | 0.196 | 0.196 | 76.2% | 73.8% | 99.3% |
| 0.25 | 0.10 | 0.204 | 0.205 | 74.4% | 61.4% | 98.5% |
| 0.25 | 0.20 | 0.233 | 0.237 | 66.4% | 25.0% | 95.0% |
| 0.25 | 0.30 | 0.295 | 0.304 | 42.2% | 0.1% | 73.8% |
| 1.00 | 0.00 | 0.203 | 0.209 | 48.3% | 39.1% | 92.7% |
| 1.00 | 0.10 | 0.212 | 0.219 | 47.0% | 30.8% | 91.0% |
| 1.00 | 0.20 | 0.242 | 0.253 | 41.3% | 9.9% | 84.4% |
| 1.00 | 0.30 | 0.295 | 0.307 | 24.4% | 0.0% | 66.4% |

With no separation requirement, the all-objects diagnostics
reproduce the earlier decay integral to within 0.00052.
At the tight momentum threshold and separation 0.20, the
all-objects diagnostic rises from 0.203 to 0.242. Including
misclassifications raises it to 0.253. WW retains 41.3% of
its production weight in its proper category, while ZZ retains
9.9%. Another 17.3% of the original ZZ weight migrates to WW.
Consequently, about 16% of the WW-labelled weight came from ZZ
at this cut in the branching-normalized mixture.

At separations 0.10 and 0.20, every strict ZZ loss due to
separation involved two objects from different parents in the
sample. At 0.30, a close pair from the same Z and a close pair
from different parents were often both present. This attribution
uses parent labels after the event has been classified, and applies
only to events in which every object passed the momentum and
pseudorapidity cuts.

Among accepted genuine WW events, the closest same-sign lepton
pair always matched the selected parent pair on the sampled patch.
This pairing check is separate from deciding whether an event
was genuinely WW. The ratio survives and can increase as
resolution worsens, even while the WW category becomes less pure.

Moving from production order three to four changes the ratios
by at most 0.00083. Doubling the Sobol sample from 2,048 to 4,096
per scramble changes the means by at most 0.00073. The largest
span across the four reconstructed ratios is 0.00227.

The all-objects diagnostic uses truth weights from events where
every visible object passed and survived. The reconstructed
diagnostic uses the assigned categories, including migrations.
Both use the same factor of three as the stable-boson test.
Purities refer to the branching-normalized mixture on this patch.

## Reproduction

Run `OPENBLAS_NUM_THREADS=1 python3 electroweak_photon_reconstruction.py 3 4`
with NumPy and SciPy. Four independently scrambled Sobol samples
of 4,096 points each integrate the joint decay angles, chirality and
flavour at each production node. The [saved results](electroweak-photon-reconstruction-results.json)
include replicate ratios and weighted migration matrices. Rows
are truth channels and columns are the visible classifications.
The code checks daughter mass shells and momentum conservation,
the decay kernel normalization, the resolution ordering, and
closure of the migration rows.

The [ATLAS lost-lepton audit](atlas-lost-lepton-audit.md) traces
how an experiment constrains a related background using a
three-lepton control sample and simulated events.
