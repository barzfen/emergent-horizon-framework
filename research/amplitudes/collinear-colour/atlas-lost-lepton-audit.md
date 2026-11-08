# Lost-lepton background in the ATLAS same-sign W measurement

The [photon-beam reconstruction study](electroweak-photon-reconstruction.md)
showed how a neutral channel could enter a same-sign category when
leptons went missing. A published ATLAS measurement supplies a
collider example of how to estimate this kind of background. ATLAS
studied same-sign W pairs produced with two jets in 139 inverse
femtobarns of 13 TeV proton–proton data. The relevant background
is WZ with two jets, including the virtual-photon contribution
grouped with it in the paper.

## How the estimate is constrained

1. **Select the same-sign candidates.** The signal region requires
   two same-sign electrons or muons, missing transverse momentum,
   and two jets with a combined mass above 500 GeV and a rapidity
   separation above two. A third lepton triggers a veto. A WZ
   event can pass when one lepton escapes the veto, typically
   because it lies outside the detector's geometric acceptance.
2. **Use a three-lepton control sample.** The WZ control region
   replaces the veto with a requirement for one extra lepton with
   transverse momentum above 15 GeV. It requires a two-jet mass
   above 200 GeV and a three-lepton mass above 106 GeV. A subset
   enriched in strong-production WZ events constrains the shape
   of the simulated two-jet mass spectrum.
3. **Fit the signal and background together.** ATLAS includes the
   three-lepton WZ control region as a single count in the fit,
   along with the same-sign signal region and a lower two-jet-mass
   control region. The signal strength and the overall scale of
   the strong-production WZ background are free parameters.
   Simulation supplies the relation between the expected WZ
   yields in the three-lepton and same-sign selections. The
   fitted WZ scale is 0.67 relative to the simulated normalization
   used by the fit. It is a normalization parameter, distinct
   from a probability for losing a lepton.

The selection, reweighting and fit are described in sections 4,
5.1 and 7.1–7.3 of the [ATLAS paper](https://doi.org/10.1007/JHEP04(2024)026).

## How much WZ enters the same-sign sample?

Table 5 of the paper reports the following combined counts after
the fit. The observed total is the count in the data. The WZ
rows and the expected total are fitted yields.

| Component in the same-sign selection | Events |
| --- | ---: |
| WZ with two jets, strong production | 56 ± 6 |
| WZ with two jets, electroweak production | 14.9 ± 1.2 |
| All expected signal and background | 468 ± 21 |
| Observed data | 475 |

The two WZ contributions give approximately 71 events, or
`(56 + 14.9) / 468 = 15.1%` of the fitted total. This audit
uses the reported central values. A precision uncertainty on
the fraction would require the fit correlations. The estimate
is a share of the selected sample, whereas a lost-lepton
probability would use the original WZ population as its denominator.

The link to the photon-beam calculation is the classification
mechanism. ATLAS constrains a lost-lepton WZ background with
collider data and simulation. The photon-beam test measures
migration from a different process on a fixed simulated patch,
using a simplified angular resolution rule. The ATLAS fitted
fraction and the photon-beam ratio refer to their own selections.
