#!/usr/bin/env python3
"""x2rt_validate.py -- ADVERSARIAL independent re-validation of x2cc_fast.py.

Unlike x2cc_fast.validate (which only compares pos/state/step at checkpoints and
the final 1-count), this compares the ENTIRE written tape region (lo..hi) between
the raw TM and the accelerated simulator at every checkpoint. A bulk-write bug that
happens to leave head/state correct but corrupts interior cells is caught here.

Transition table is re-derived from the SPEC string independently (not importing
mse_extract.parse) so the sim's own parser is not trusted."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_fast import Fast

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"

# independent parse
def build_T(spec):
    T = []
    for blk in spec.split('_'):
        row = []
        for h in (blk[0:3], blk[3:6]):
            if '-' in h:
                row.append(None)
            else:
                row.append((int(h[0]), 1 if h[1] == 'R' else -1, ord(h[2]) - ord('A')))
        T.append(row)
    return T

def run(nsteps, ncheck=200):
    T = build_T(SPEC)
    SZ = 1 << 24
    tape = bytearray(SZ)
    pos, st = SZ // 2, 0
    lo = hi = pos
    checks = set(int(nsteps * i / ncheck) for i in range(1, ncheck + 1))
    checks.add(nsteps)
    checkpoints = []  # (step, pos, st, lo, hi, bytes(region))
    halted_at = None
    for step in range(nsteps + 1):
        if step in checks:
            checkpoints.append((step, pos, st, lo, hi, bytes(tape[lo:hi + 1])))
        r = tape[pos]
        tr = T[st][r]
        if tr is None:
            halted_at = step
            checkpoints.append((step, pos, st, lo, hi, bytes(tape[lo:hi + 1])))
            break
        w, d, ns = tr
        tape[pos] = w
        pos += d
        st = ns
        if pos < lo: lo = pos
        elif pos > hi: hi = pos

    # fast sim, run to each checkpoint step and compare full region
    f = Fast(SZ)
    ok = True
    for (s, p, q, rlo, rhi, region) in checkpoints:
        f.run(s)
        # fast tape absolute offset: Fast starts pos at SZ//2 == same as raw (both SZ//2)
        freg = bytes(f.tape[rlo:rhi + 1])
        same = (f.step == s and f.pos == p and f.st == q and freg == region)
        if not same:
            ok = False
            print(f"MISMATCH @step {s}:")
            print(f"  fast: step={f.step} pos={f.pos} st={f.st}")
            print(f"  raw : step={s} pos={p} st={q}")
            if freg != region:
                # find first differing cell
                for k in range(len(region)):
                    if k >= len(freg) or freg[k] != region[k]:
                        print(f"  first tape diff at abs cell {rlo+k}: raw={region[k]} fast={freg[k] if k<len(freg) else 'oob'}")
                        break
                print(f"  raw 1-count in region={region.count(1)} fast 1-count={freg.count(1)}")
            break
    print(f"checkpoints={len(checkpoints)} halted={halted_at}")
    print("FULL-TAPE VALIDATED step-exact" if ok else "FAILED (see above)")
    return ok

if __name__ == "__main__":
    n = int(float(sys.argv[1])) if len(sys.argv) > 1 else 100_000_000
    run(n)
