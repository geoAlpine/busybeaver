#!/usr/bin/env python3
"""x2tb_reset14.py -- settle the origin of the roadmap's B5 "CONSTANT reset 14".

PROVENANCE (traced, this audit).  The roadmap's B5 row (TRACK_B_ROADMAP section 1A,
"reset structure: CONSTANT 14") descends from CARRY_DICHOTOMY, whose probes are
cd_probe.py / cd_probe2.py.  cd_probe2.py's docstring asks the question in so many
words:  "(2) 1RB0LB (noisy-maxrun x2): is peak law EXACTLY v'=2v+1 (peaks 9*2^k-1)
with constant reset 14?".  Both call mse_extract.simulate, and

    mse_extract.simulate DOES maintain BOTH lo and hi (mse_extract.py:106-121).

So the roadmap's 14 is NOT the x2b5 lo/hi truncation bug (fault F1).  Its scan
extent is correct and its maxrun values are true full-tape values.  Reproduced
exactly here: resets tail = [4, 8, 14, 14, 14, 14].

What 14 actually is: `min(v[a:b])` where v is sampled ONLY at record-extreme
excursions (fault F2 -- a min over a biased sparse subsample).  A sparse min is an
UPPER BOUND on the true minimum.  So:

  * true per-generation min of maxrun <= 14  for every generation that reported 14;
  * therefore x2b5_braid's "floors" 16,28,46,88,166,328,646 CANNOT be per-generation
    minima of maxrun -- they are a different statistic (the value at the next
    state-C left-record milestone after the peak), and both readings can be, and are,
    simultaneously true of different quantities.

THIS PROBE decides between the two remaining possibilities for the true floor:
  (a) it really is CONSTANT 14  -> the roadmap's reset column is right, for the
      min-over-the-generation reading, and 14 is a genuine invariant;
  (b) it is not constant        -> the roadmap's 14 is a sparse-sampling artifact.

Method: dense stride-1 sampling (the ONLY sampling that can witness a true minimum
-- maxrun can drop by an arbitrary amount in ONE step when a write splits a run, so
no stride>1 sample is sound for a min).  Extent from x2tb_sim.feats (tape-derived).

Decides NO halting.  No label upgraded.
"""

import sys
from x2tb_sim import MACHINES, run

B5 = MACHINES['B5']


def peak_times(cap=12_000_000):
    """PASS 1 (sparse).  Step at which each register peak fires.

    This uses the roadmap's OWN instrument.  That is deliberate and sound: a peak
    VALUE and its TIME are max/timing statistics, the class that survived both
    faults (6b6d739: "the step column is BYTE-IDENTICAL before and after the fix").
    Only the MIN taken from this series is untrustworthy -- which is exactly what
    pass 2 replaces.
    """
    sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
    from mse_extract import simulate, _segments
    outc, step, fast, slow, ftail, nL, nR = simulate(B5, cap)
    v = [f[3] for f in fast]
    segs = _segments(v)
    segs = segs[:-1] if len(segs) > 1 else segs
    out = []
    for a, b in segs:
        j = max(range(a, b), key=lambda i: v[i])
        out.append((v[j], fast[j][0]))       # (peak value, step of peak)
    return out


def dense_floors(cap, bounds, SZ=1 << 13):
    """PASS 2 (dense, stride 1).  TRUE min of full-tape maxrun in each [t_k, t_{k+1})."""
    floors = {i: None for i in range(len(bounds) - 1)}
    edges = [t for _, t in bounds]

    def cb(step, st, t1, mx, w, lo, hi):
        if step < edges[0] or step >= edges[-1]:
            return
        # locate the interval containing this step
        i = 0
        for j in range(len(edges) - 1):
            if edges[j] <= step < edges[j + 1]:
                i = j
                break
        f = floors[i]
        if f is None or mx < f:
            floors[i] = mx

    outc, steps, _ = run(B5, cap, SZ=SZ, sample_every=1, on_sample=cb)
    return outc, steps, floors


def sparse_repro():
    """Reproduce the roadmap's reading with its own instrument (mse_extract)."""
    sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
    from mse_extract import simulate, _segments
    outc, step, fast, slow, ftail, nL, nR = simulate(B5, 12_000_000)
    v = [f[3] for f in fast]
    segs = _segments(v)
    segs = segs[:-1] if len(segs) > 1 else segs
    pk = [max(v[a:b]) for a, b in segs]
    rs = [min(v[a:b]) for a, b in segs]
    return pk, rs


if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 14_000_000

    print("=== (1) reproduce the roadmap's own instrument (mse_extract/cd_probe2) ===")
    pk, rs = sparse_repro()
    print(f"  peaks  (sparse, record-extreme samples): {pk[-8:]}")
    print(f"  resets (sparse min over segment)       : {rs[-8:]}   <-- the roadmap's 'CONSTANT 14'")

    # pass 1 must run PAST the dense cap, or the last generation has no closing peak
    bounds = peak_times(max(3 * cap, 12_000_000))
    bounds = [b for b in bounds if b[1] <= cap]
    print(f"\n  peak (value, step) from pass 1: {bounds}")

    print(f"\n=== (2) DENSE stride-1 TRUE per-generation floor of full-tape maxrun (cap {cap}) ===")
    outc, steps, floors = dense_floors(cap, bounds)
    print(f"  outc={outc} steps={steps}")
    print(f"  {'gen':>4} {'from peak':>10} {'to peak':>9} {'TRUE min maxrun (dense)':>24} "
          f"{'sparse min':>11}")
    vals = []
    for i in range(len(bounds) - 1):
        if floors[i] is None:
            continue
        vals.append(floors[i])
        sp = rs[-(len(bounds) - 1) + i] if len(rs) >= len(bounds) - 1 else '?'
        print(f"  {i:>4} {bounds[i][0]:>10} {bounds[i+1][0]:>9} {floors[i]:>24} {sp:>11}")
    print(f"\n  dense floors: {vals}")
    if len(set(vals[1:])) == 1:
        print(f"  ==> the TRUE per-generation floor IS CONSTANT at {vals[-1]}.")
    else:
        print("  ==> the TRUE per-generation floor is NOT constant.")
