#!/usr/bin/env python3
"""x2tb_sim.py -- Track B re-audit: a tape-derived-extent simulator (2026-07-17).

WHY THIS FILE EXISTS
--------------------
Two distinct instrument faults corrupted Track B evidence, BOTH of which let a
scan report a number that was never a property of the whole tape:

  (F1) TRUNCATED EXTENT (the x2b5_* bug, 6b6d739).  The probe maintained `lo` at
       left-record milestones but never updated `hi`, so every scan ran over
       range(lo, 0+1) -- the LEFT HALF-TAPE.  B5's tape is mirror-symmetric about
       the origin, so the half-tape reading looked coherent.  Max-statistics
       survived (a max is dominated by the symmetric half); every MIN-statistic
       built on the same scan was wrong.

  (F2) SPARSE-SAMPLE MINIMA (the mse_extract/cd_probe fault, this audit).  The
       extent is correct, but the observable is only RECORDED at record-extreme
       excursions.  A `min` taken over that biased subsample is NOT the tape's
       minimum over the macro-period.  Max/timing statistics survive; minima do not.

STRUCTURAL DEFENCE
------------------
`feats()` takes ONLY the tape.  It derives its own extent with bytearray.find /
.rfind (C-level scans of the whole allocated array).  There is no `lo`/`hi`
parameter to pass, so F1 is not expressible in this API.  Caller bookkeeping is
used ONLY to decide WHEN to sample, never HOW FAR to scan.

F2 is not a code bug but a reading discipline: this module reports what it
sampled and when, and callers must not read a `min` over sparse samples as a
floor.  `run()` exposes `sample_every` so a claim about minima can be re-taken
densely.

All arithmetic is exact (int).  Decides NO halting.  No label upgraded.
"""

import sys

HALT = None


def parse(spec):
    """'1RB0LB_...' -> flat rule table R[state*2 + sym] = (write, delta, next*2) | None."""
    R = []
    for st in spec.split('_'):
        for t in (st[0:3], st[3:6]):
            if t[0] == '-' or t[2] in '-Z':
                R.append(None)
            else:
                R.append((int(t[0]), 1 if t[1] == 'R' else -1, (ord(t[2]) - ord('A')) * 2))
    return R


def extent(tape):
    """(lo, hi) of the written 1s, DERIVED FROM THE TAPE. (-1,-1) if blank.

    This is the whole point of the module: the extent is a function of the tape
    and nothing else.  No caller can truncate it."""
    lo = tape.find(1)
    if lo < 0:
        return -1, -1
    return lo, tape.rfind(1)


def feats(tape):
    """(total1, maxrun, width, lo, hi) over the FULL tape. Tape-derived extent only."""
    lo, hi = extent(tape)
    if lo < 0:
        return 0, 0, 0, -1, -1
    total1 = tape.count(1)
    seg = tape[lo:hi + 1]
    maxrun = max(len(b) for b in seg.split(b'\x00'))
    return total1, maxrun, hi - lo + 1, lo, hi


def run(spec, maxsteps, SZ=1 << 17, sample_every=None, on_sample=None):
    """Simulate from a blank tape.

    Sampling: at every tape-extent record (either side) -- generic, machine-agnostic,
    and dense (one sweep = one record).  If `sample_every` is given, sample on that
    step stride INSTEAD: use this whenever a claim concerns a MINIMUM, since a min
    over record-extreme samples is fault F2.  `sample_every=1` is the only sampling
    that can witness a true per-generation minimum.

    `on_sample(step, state, total1, maxrun, width, lo, hi)` streams samples instead of
    accumulating them (dense runs otherwise exhaust memory).

    Returns (outcome, steps, samples) with samples = [(step, state, total1, maxrun,
    width, lo, hi)] -- every observable computed by feats() over the full tape.
    """
    R = parse(spec)
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st2 = 0
    step = 0
    rlo = rhi = pos          # sampling TRIGGER only -- never a scan bound
    samples = []
    outc = 'MAX'
    while step < maxsteps:
        a = R[st2 + tape[pos]]
        if a is None:
            outc = 'HALT'
            break
        w, d, ns = a
        tape[pos] = w
        pos += d
        st2 = ns
        step += 1
        if pos < 4 or pos > SZ - 4:
            outc = 'OVR'
            break
        hit = False
        if sample_every is None:
            if pos < rlo or pos > rhi:
                if pos < rlo:
                    rlo = pos
                else:
                    rhi = pos
                hit = True
        elif step % sample_every == 0:
            hit = True
        if hit:
            t1, mx, w_, lo, hi = feats(tape)
            if on_sample is not None:
                on_sample(step, st2 // 2, t1, mx, w_, lo, hi)
            else:
                samples.append((step, st2 // 2, t1, mx, w_, lo, hi))
    return outc, step, samples


# ---- the machines (TRACK_B_ROADMAP_2026-07-16.md section 1 / 1B) ----
MACHINES = {
    'B1': '1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE',
    'B2': '1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD',
    'B3': '1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC',
    'B4': '1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD',
    'B5': '1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD',
    'W1': '1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---',
    'W2': '1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE',
    'W3': '1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE',
}

# Which observable each roadmap row uses as its register proxy (roadmap section 1).
REGISTER_OBS = {
    'B1': 'maxrun', 'B2': 'maxrun', 'B3': 'total1', 'B4': 'total1',
    'B5': 'maxrun', 'W1': 'total1', 'W2': 'total1', 'W3': 'total1',
}
OBS_IDX = {'total1': 2, 'maxrun': 3, 'width': 4}


if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    for name, spec in MACHINES.items():
        outc, step, S = run(spec, cap)
        last = S[-1] if S else None
        print(f"{name}  outc={outc:4} steps={step:>10} nsamp={len(S):>6} last={last}")
