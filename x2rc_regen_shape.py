#!/usr/bin/env python3
"""x2rc_regen_shape.py -- pin the REGEN(k) EXIT SHAPE bit-for-bit: does the
carry-completion land E on a boundary 0 with

    left  = (01)^{Lc+N} ++ marker        (N = 2^{k-1}-2)
    right = 0^3 1^{2^k-3} 0^2 descCascade(k-3) 0^2 0^7 R
          = 0^3 descCascade(k-2) 0^9 R          <-- the COLLAPSE

i.e. the cascadeReg(k) invariant that lean/X2.lean's `descent_glue` CONSUMES (§5ag).

Measured on the REAL orbit (x2bd_sim.build(2)) at the descent starts for a=5,6,7,
which §5ag records as raw 13453 / 33830 / 114703, plus the REGEN(4) exit.

Run-length parses below are MAXIMAL (runs are read greedily to exhaustion), so the
`0^2 / 1^m` block splits are unambiguous -- see x2qb_exact.py for the technique.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def descCascade(d):
    """Lean §5ag: descCascade 0 = 1^1; descCascade (d+1) = 1^{2^{d+3}-3} 0^2 descCascade d,
    i.e. for an index n >= 1: descCascade n = 1^{2^{n+2}-3} 0^2 descCascade (n-1)."""
    if d == 0:
        return [1]
    return [1] * (2 ** (d + 2) - 3) + [0, 0] + descCascade(d - 1)


def cascadeReg_right(k, pad=40):
    """The TARGET Lean right register of `descent_glue`'s IN at level k:
    0^3 1^{2N+1} 0^2 descCascade(d+1) 0^2 0^7 R, with N = 2^{k-1}-2, d+1 = k-3."""
    N = 2 ** (k - 1) - 2
    return ([0, 0, 0] + [1] * (2 * N + 1) + [0, 0] + descCascade(k - 3)
            + [0, 0] + [0] * 7 + [0] * pad)


def collapsed_right(k, pad=40):
    """The SAME thing after the collapse 1^{2^k-3} 0^2 descCascade(k-3) = descCascade(k-2)."""
    return [0, 0, 0] + descCascade(k - 2) + [0] * 9 + [0] * pad


def runs(bits, cap=None):
    out = []
    i = 0
    while i < len(bits):
        j = i
        while j < len(bits) and bits[j] == bits[i]:
            j += 1
        out.append((bits[i], j - i))
        i = j
        if cap and len(out) >= cap:
            break
    return out


def snap(n):
    sim = build(2)
    sim.step()
    while sim.n < n:
        assert sim.step(), f"HALT before {n}"
    return sim


def check(k, n):
    """At raw step n, is the config exactly cascadeReg(k)?"""
    sim = snap(n)
    head = sim.h
    # Lean's `right` field: cells right of head.  Off-list cells are BLANK (Lean: `mvR`
    # on `[]` yields `false`), so pad with 0s to compare against a longer target.
    right = sim.R[::-1] + [0] * 64
    left = [sim.L[-1 - i] for i in range(len(sim.L))]   # Lean's `left`: nearest-first

    print(f"\n=== REGEN({k}) exit / descent(a={k}) start @ raw n={n} ===")
    print(f"  state={sim.st}  head={head}  pos={sim.pos}")
    print(f"  right runs (maximal): {runs(right, 12)}")
    print(f"  left  runs (maximal): {runs(left, 8)}")

    ok_state = (sim.st == 'E' and head == 0)
    print(f"  [E on a boundary 0]            : {ok_state}")

    # --- RIGHT: compare against the target, allowing R := trailing blanks.
    tgt = cascadeReg_right(k, pad=0)
    core = tgt[:len(tgt)]
    ok_right = right[:len(core)] == core
    print(f"  [right = 0^3 1^{2**k-3} 0^2 descCascade({k-3}) 0^2 0^7 ..] : {ok_right}"
          f"   (prefix of {len(core)} cells; R := the rest)")

    # --- the COLLAPSE identity, checked as data.
    ok_collapse = cascadeReg_right(k, 0) == collapsed_right(k, 0)
    print(f"  [1^{2**k-3} 0^2 descCascade({k-3}) == descCascade({k-2})] : {ok_collapse}")

    # --- LEFT: is it (01)^{Lc+N} ++ marker for some Lc >= 0? N = 2^{k-1}-2.
    N = 2 ** (k - 1) - 2
    m = 0
    while 2 * m + 1 < len(left) and left[2 * m] == 0 and left[2 * m + 1] == 1:
        m += 1
    print(f"  [left comb (01)^m maximal m]   : m={m}   (need m >= N = {N}: {m >= N})")
    print(f"    -> Lc = m - N = {m - N}" if m >= N else "    -> COMB TOO SHORT")
    return ok_state and ok_right and ok_collapse and m >= N


if __name__ == "__main__":
    # §5ag / braid_topgrind_a5 record these as the measured descent (TOPGRIND) starts.
    SITES = {4: 6708, 5: 13453, 6: 33830, 7: 114703}
    res = {}
    for k, n in SITES.items():
        res[k] = check(k, n)
    print("\n=== VERDICT ===")
    for k, v in res.items():
        print(f"  cascadeReg({k}) holds on the real orbit: {v}")
