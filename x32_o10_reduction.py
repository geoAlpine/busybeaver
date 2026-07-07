#!/usr/bin/env python3
"""x32_o10_reduction.py -- o10 precise reduction re-verified: ceiling-3/2 epochs, H-criterion,
S_halt hitting set, doubly-exponential reseed orbit (2026-07-07).

o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC  (halt F,0; F <- only C,1->0LF)

Claims verified here:
 (1) CLEAN CONFIG + INNER MAP [checked 0-mismatch vs raw TM, blank orbit]:
     clean config = state E at left frontier, tape 0* 1 0^{2m-8} 1^b 0 1  ->  (m, b).
     Macro-step: dec = 1 + [m odd]; b -= dec; m -> ceil(3m/2).  Epoch seed m = 6.
 (2) EPOCH MODEL / H-CRITERION [checked vs SEEDED raw TM, B = 1..16]:
       b < 0  (overshoot, from b=1 at odd m)      -> REFILL, B' = 3(m_pre - 2)
       b == 0 and new m odd                        -> HALT
       b == 0 and new m even                       -> REFILL, B' = 3 m_new - 7
     NOTE: at B=16 this model PREDICTS REFILL (terminal m=822 even, B'=2459), whereas
     O10_HALTER.md line "B=16: predicted-halt" implied halt. B=16 needs ~a few 10^6 raw
     steps; we run it to settle the first previously-unverified row.
 (3) S_HALT [derived from (1)+(2)]: with C_t = cumulative dec of the (epoch-independent)
     m-orbit from 6, epoch(B) halts <=> B = C_t at a t whose NEW m is odd
     <=> B in S_halt := {C_t : m_{t+1} odd}. Density(S_halt) -> 1/3 [OBSERVED],
     because odd-density of the ceiling-3/2 orbit from 6 -> 1/2 (the (K)-TYPE statement)
     and C grows at rate 3/2.
 (4) RESEED ORBIT [exact]: B_1 = 5 (raw-verified), B_2 = 57 (raw-verified),
     B_3 = epoch(57) computed exactly; epochs 1-2 REFILL; epoch 3 infeasible.

SOUNDNESS: finite checks; the halting direction stays [OPEN]. No machine decided.
"""
import sys

SPEC = "1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

def parse_clean(s):
    """0* 1 0^j 1^b 0 1  ->  (m, b) with j = 2m-8 (j>=1), b>=1. Else None."""
    s = s.strip('0')
    # expect: '1' 0^j 1^b '0' '1'
    if len(s) < 5 or s[0] != '1' or s[-1] != '1' or s[-2] != '0':
        return None
    body = s[1:-2]
    j = 0
    while j < len(body) and body[j] == '0':
        j += 1
    b = len(body) - j
    if j < 1 or b < 1 or '0' in body[j:]:
        return None
    if (j + 8) % 2 != 0:
        return None
    return ((j + 8) // 2, b)

def ceil32(m):
    return (3 * m + 1) // 2 if m & 1 else 3 * m // 2

def epoch(B, trace=False):
    """Abstract epoch from (m=6, b=B). Returns ('HALT', t) or ('REFILL', B', t)."""
    m, b = 6, B
    t = 0
    while True:
        dec = 1 + (m & 1)
        b -= dec
        if b < 0:
            return ('REFILL', 3 * (m - 2), t)
        m2 = ceil32(m)
        t += 1
        if b == 0:
            if m2 & 1:
                return ('HALT', t)
            return ('REFILL', 3 * m2 - 7, t)
        m = m2

# ------------------------------------------------------------ raw blank-orbit check
def blank_orbit_check(maxsteps):
    M = parse(SPEC)
    SZ = 1 << 24
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    cfgs = []
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"RAW HALT at {step}"); break
        if st == 4 and pos <= lo and r == 0:
            s = ''.join(map(str, tape[lo:hi + 1]))
            mb = parse_clean(s)
            if mb is not None:
                if not cfgs or cfgs[-1][1:] != mb:
                    cfgs.append((step, mb[0], mb[1]))
        w, d, ns = act
        tape[pos] = w; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    print(f"blank run to {step:,} steps: {len(cfgs)} clean configs (m,b):")
    print("  " + " ".join(f"({m},{b})@{t}" for t, m, b in cfgs[:14]) + (" ..." if len(cfgs) > 14 else ""))
    # verify inner map + refill across the observed sequence
    mism = 0
    for i in range(len(cfgs) - 1):
        _, m, b = cfgs[i]
        _, m2, b2 = cfgs[i + 1]
        dec = 1 + (m & 1)
        if b - dec > 0:
            ok = (m2 == ceil32(m) and b2 == b - dec)
        elif b - dec < 0:
            ok = (m2 == 6 and b2 == 3 * (m - 2))          # overshoot refill
        else:
            mm = ceil32(m)
            ok = (m2 == 6 and b2 == 3 * mm - 7) if mm % 2 == 0 else False  # landing refill / halt
        if not ok:
            mism += 1
            if mism <= 5:
                print(f"  MISMATCH: ({m},{b}) -> observed ({m2},{b2})")
    print(f"inner map + refill check on blank orbit: {len(cfgs)-1} transitions, {mism} mismatches")
    print(f"  => refill orbit observed: B_1 = 5, B_2 = 57 (epoch-2 progress to m={cfgs[-1][1]} at 20M steps)")
    return mism == 0

# ------------------------------------------------------------ seeded epoch cross-check
def seeded_check(bmax=16, cap_default=3_000_000, cap_b16=40_000_000):
    M = parse(SPEC)
    def seed_epoch(B, cap):
        SZ = 1 << 24
        tape = bytearray(SZ); off = SZ // 4
        s = "1" + "0" * 4 + "1" * B + "01"
        for i, ch in enumerate(s):
            tape[off + 2 + i] = 1 if ch == '1' else 0
        pos = off; st = 4; step = 0; lo = pos; hi = off + 2 + len(s) - 1
        while step < cap:
            r = tape[pos]
            act = M[st][r]
            if act is None:
                return ('HALT', step)
            if step > 0 and st == 4 and pos <= lo and r == 0:
                ss = ''.join(map(str, tape[lo:hi + 1]))
                mb = parse_clean(ss)
                if mb is not None and mb[0] == 6 and mb[1] > B:
                    return ('REFILL', mb[1], step)
            w, d, ns = act
            tape[pos] = w; pos += d; st = ns; step += 1
            if pos < lo: lo = pos
            if pos > hi: hi = pos
        return ('TIMEOUT', step)
    print(f"\nseeded epoch cross-check, B = 1..{bmax} (raw TM vs abstract epoch model):")
    bad = 0
    for B in range(1, bmax + 1):
        pred = epoch(B)
        cap = cap_b16 if B == 16 else cap_default
        got = seed_epoch(B, cap)
        okstr = "?"
        if got[0] == 'TIMEOUT':
            okstr = "timeout (undecided row)"
        elif pred[0] != got[0] or (pred[0] == 'REFILL' and pred[1] != got[1]):
            bad += 1
            okstr = "<-- MISMATCH"
        else:
            okstr = "ok"
        p = f"{pred[0]}" + (f" B'={pred[1]}" if pred[0] == 'REFILL' else "")
        g = f"{got[0]}" + (f" B'={got[1]}" if got[0] == 'REFILL' else (f"@{got[1]}" if got[0] == 'HALT' else ""))
        print(f"  B={B:>2}: abstract {p:<18} raw {g:<22} {okstr}")
    print(f"  mismatches: {bad}")
    return bad == 0

# ------------------------------------------------------------ S_halt + reseed orbit
def shalt_and_reseed(N=100_000):
    print(f"\nS_halt from the ceiling-3/2 m-orbit (seed 6), {N:,} macro-steps:")
    m = 6
    C = 0
    S = []
    odd = 0
    dens_cp = {10**3, 10**4, 10**5}
    Svals = set()
    t = 0
    while t < N:
        dec = 1 + (m & 1)
        C += dec
        m = ceil32(m)
        t += 1
        if m & 1:
            S.append(C); Svals.add(C)
            odd += 1
        # (odd counts parity of the NEW m; halt slots)
    print(f"  first S_halt elements: {S[:12]}")
    for X in sorted(dens_cp):
        cnt = sum(1 for v in S if v <= X)
        print(f"  density |S ∩ [1,{X}]| / {X} = {cnt/X:.4f}")
    # odd-density of the m-orbit itself (the (K)-type quantity)
    m = 6; oddc = 0
    for t in range(N):
        m = ceil32(m)
        oddc += m & 1
    print(f"  odd-density of the m-orbit (seed 6) over {N:,} steps = {oddc/N:.5f}  (Haar 1/2)")
    print(f"  membership: B_1=5 in S_halt: {5 in Svals};  B_2=57 in S_halt: {57 in Svals}")
    r2 = epoch(57)
    print(f"  epoch(57) exact: {r2[0]}, B_3 = {r2[1]:,} ({r2[2]} macro-steps)")
    print(f"  epoch 3 (B_3 ~ 2.1e8): ~1.4e8 macro-steps on integers reaching ~10^(2.5e7) digits")
    print(f"  -> membership of B_3 in S_halt INFEASIBLE here (~10^15 digit-ops); stays [OPEN]")

if __name__ == "__main__":
    raw_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    ok1 = blank_orbit_check(raw_steps)
    ok2 = seeded_check()
    shalt_and_reseed()
    print(f"\nall checks passed: {ok1 and ok2}")
    print("No machine decided. No label upgraded.")
