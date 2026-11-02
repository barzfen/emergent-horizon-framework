# EHF-AMP-FOUND-04A Result Audit

## Correct status

The 126-channel modular census completed successfully, but the automatic verdict
`EHF_AMP_FOUND_04A_ELEVEN_TO_TEN_MODULAR_TAIL_LAW_CANDIDATE_FOUND`
is too strong.

The reported `minimal_constant_tail_width = 4` is tautological because a
four-label suffix is the complete subset \(A={a<b<c<d}\). No nontrivial pure
tail law was found at widths 1, 2, or 3.

## Main positive structure

A three-rightmost-label law fails in only seven of the 56 three-label suffix
classes. Every failure occurs at deleted-tail boundary \(d=10\), and every
rank split is exactly one dimension:

- `5,6,10`: ranks `182,183`
- `5,7,10`: ranks `244,245`
- `5,8,10`: ranks `269,270`
- `5,9,10`: ranks `269,270`
- `6,7,10`: ranks `266,267`
- `6,8,10`: ranks `290,291`
- `6,9,10`: ranks `290,291`

Equivalently, the GF(2) census is a three-tail near-law with a one-dimensional
boundary correction controlled by the smallest selected label.

The rank is componentwise monotone across all 126 subsets.

Complete target recovery occurs in exactly 21 channels and is equivalent to

\[
b\ge 7.
\]

## Field dependence

The representative GF(3) audit disagreed with GF(2) in two rank classes:

\[
35\to36,\qquad 59\to60.
\]

A follow-up GF(3) check of every channel in those classes gave:

- all four GF(2)-rank-35 channels have GF(3) rank 36;
- all three GF(2)-rank-59 channels have GF(3) rank 60.

Thus these are systematic characteristic-two defects, not isolated execution
errors. The suffix constancy pattern survives these corrections.

A full GF(3) census is still needed because one representative per GF(2) rank
class cannot exclude hidden within-class field dependence.

## Exact consequences already available

- The GF(3)-rank-36 channels are source-limited with source relation dimension
  36, so their rational transmitted rank is exactly 36.
- The GF(2)-rank-296 channels saturate the target relation space. Together with
  exact containment, this certifies rational target relation dimension 296 and
  exact complete recovery for those 21 channels.
- Lower unsaturated modular ranks remain lower bounds until exact or
  upper-bounded.

## Recommended next probe

`EHF-AMP-FOUND-04B: Full Multi-Prime Boundary-Corrected Three-Tail Audit`

It should run all 126 channels over GF(3), audit GF(5), certify the seven
boundary splits, separate exact ranks from modular lower bounds, and use
verdict logic that requires a nontrivial width less than four.
