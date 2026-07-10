#!/usr/bin/env python3
"""x2p_localparity.py -- THE decisive experiment for the parity-separation bet.
Route A PROVED the LENGTH of an E-opened gap is not a function of local block context
(same (1^5,1^13) pair -> many even lengths). This tests the WEAKER claim the parity
separation needs: is the PARITY (g mod 2) of an E-opened gap a function of a bounded
local context?  For every event (state E, reads 0 at the LEFT end of a maximal 0-run of
length g>=2) capture the RLE of R runs to the LEFT (already-swept, settled) and R runs
to the RIGHT (excluding the gap itself), and test whether context -> g%2 is well-defined
(no context mapping to BOTH parities).  Do it for R = 1,2,3,4.

If parity is locally determined (0 conflicts) for some finite R, a local finite-state
parity certificate is plausible.  If parity ALSO conflicts (same context -> even AND odd),
the ordering/parity is genuinely counter-dependent and the separation FAILS (o4 wall)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse
from collections import defaultdict

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def run(maxsteps, Rs, SZ=1 << 23):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    # ctxmap[R][context] = set of parities seen
    ctxmap = {R: defaultdict(set) for R in Rs}
    lenctx = {R: defaultdict(set) for R in Rs}  # same but full length, for comparison
    nev = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        if st == 4 and r == 0 and pos > lo and tape[pos - 1] == 1:
            j = pos
            while j < hi and tape[j] == 0: j += 1
            g = j - pos
            if 2 <= g:      # E opens a real gap
                # build RLE to left of pos and right of j
                # left runs (going leftward from pos-1)
                def left_runs(nR):
                    out = []; i = pos - 1
                    while i >= lo and len(out) < nR:
                        c = tape[i]; n = 0
                        while i >= lo and tape[i] == c:
                            n += 1; i -= 1
                        out.append((c, n))
                    return tuple(out)
                def right_runs(nR):
                    out = []; i = j
                    while i <= hi and len(out) < nR:
                        c = tape[i]; n = 0
                        while i <= hi and tape[i] == c:
                            n += 1; i += 1
                        out.append((c, n))
                    return tuple(out)
                for R in Rs:
                    ctx = (left_runs(R), right_runs(R))
                    ctxmap[R][ctx].add(g % 2)
                    lenctx[R][ctx].add(g)
                nev += 1
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    print(f"E-opens-gap(g>=2) events = {nev}  (to step {step:,})")
    for R in Rs:
        conf_par = sum(1 for v in ctxmap[R].values() if len(v) > 1)
        conf_len = sum(1 for v in lenctx[R].values() if len(v) > 1)
        allpar = set()
        for v in ctxmap[R].values(): allpar |= v
        print(f"  R={R}: distinct contexts={len(ctxmap[R]):>4}  "
              f"PARITY-conflicts={conf_par:>3}  (length-conflicts={conf_len:>3})  "
              f"parities seen overall={sorted(allpar)}")
        if conf_par:
            # show one conflicting context
            for ctx, v in ctxmap[R].items():
                if len(v) > 1:
                    print(f"      e.g. context L={ctx[0]} R={ctx[1]} -> parities {sorted(v)} lens {sorted(lenctx[R][ctx])}")
                    break


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    run(cap, [1, 2, 3, 4])
