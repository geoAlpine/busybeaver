#!/usr/bin/env python3
"""x2p_lifetime.py -- decisive boundedness test for the phase automaton.
A bounded PHASE-AWARE automaton can exclude 'E meets an odd gap' only if the transient
odd gaps have BOUNDED lifetime (steps between a maximal odd-run's birth and its removal)
AND the head's E-visit to a region is a bounded phase-distance from the erasure that
settled it.  If odd-gap lifetimes are BOUNDED -> a finite phase window suffices (hopeful).
If they GROW with generation (unbounded) -> the phase state is unbounded, the automaton
does not close, and the ordering is counter-dependent (o4 wall).

We track, per left-boundary cell, the birth step of a maximal odd-run>=3 and its death,
and report the lifetime distribution and the MAX lifetime as a function of step (to see
if it grows).  Also, separately, the max lifetime of a length-EXACTLY-3 gap."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse
from collections import Counter

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def maxrun_odd_set(tape, lo, hi):
    """return dict: left_cell -> run_len for maximal 0-runs of odd length>=3 bounded by 1
    on the left (right boundary need not be seen if at hi)."""
    out = {}
    i = lo
    while i <= hi:
        if tape[i] == 0:
            j = i
            while j <= hi and tape[j] == 0: j += 1
            L = j - i
            left_ok = (i - 1 >= lo and tape[i - 1] == 1)
            right_ok = (j <= hi)  # right boundary is a 1 (since tape[j]!=0) within support
            if left_ok and right_ok and L >= 3 and L % 2 == 1:
                out[i] = L
            i = j
        else:
            i += 1
    return out


def run(maxsteps, W=40, SZ=1 << 22):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    # track odd gaps only in a window around head (they only change near head)
    alive = {}   # left_cell -> (birth_step, len)
    lifetimes = []
    life3 = []
    max_life_by_epoch = []
    epoch = 200000
    cur_max = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        # only re-scan a window near head (odd gaps born/die at the head)
        a = max(lo, pos - W); b = min(hi, pos + W)
        cur = {}
        i = a
        while i <= b:
            if tape[i] == 0:
                j = i
                while j <= b + 5 and j <= hi and tape[j] == 0: j += 1
                L = j - i
                if i - 1 >= lo and tape[i - 1] == 1 and j <= hi and L >= 3 and L % 2 == 1:
                    cur[i] = L
                i = j
            else:
                i += 1
        # births
        for c, L in cur.items():
            if c not in alive:
                alive[c] = (step, L)
        # deaths (was alive & in window, now gone or changed length-parity/merged)
        for c in list(alive.keys()):
            if a <= c <= b and c not in cur:
                birth, L0 = alive.pop(c)
                lt = step - birth
                lifetimes.append(lt)
                if L0 == 3: life3.append(lt)
                if lt > cur_max: cur_max = lt
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if step % epoch == 0:
            max_life_by_epoch.append((step, cur_max))
            cur_max = 0
    lifetimes.sort()
    print(f"steps={step:,}  odd-gap(>=3) births tracked = {len(lifetimes)}")
    if lifetimes:
        print(f"  lifetime: min={lifetimes[0]} median={lifetimes[len(lifetimes)//2]} "
              f"p99={lifetimes[int(len(lifetimes)*0.99)]} MAX={lifetimes[-1]}")
    if life3:
        life3.sort()
        print(f"  gap-EXACTLY-3 lifetimes: n={len(life3)} min={life3[0]} "
              f"median={life3[len(life3)//2]} MAX={life3[-1]}")
    print(f"  max odd-gap lifetime per {epoch}-step epoch (does it GROW?):")
    print("   ", [m for _, m in max_life_by_epoch])


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    run(cap)
