#!/usr/bin/env python3
"""x32c_o2_chain.py -- x3/2-family census cleanup, TASK A (2026-07-08):
o2's COMPLETE ceiling chain, written Antihydra-style link by link, + criticality row.

o2 = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA   (halt F,0; unique edge into F: D,0 -> 0RF)

LINK 0  machine <-> milestone automaton D(a,b)              [OBSERVED, 0-mismatch]
    milestone = state A, head on a 0 cell, every cell strictly left of the head blank,
    tape from the head rightward =  0 . 11 . (01)^a . 0 . 11 . (01)^b  (head on the leading 0).
    automaton:
        a even:        D(a,b) -> D((3a+4)/2, b+2)
        a odd, b>=1:   D(a,b) -> D((3a+7)/2, b-1)
        a odd, b=0:    -> S(N), N=(3a+11)/2;  HALT if N odd, else D((3N-2)/2, 1)
                        (composed escape: D(a,0) -> D((9a+29)/4, 1) when a = 3 mod 4)
LINK 1  D(a,b) <-> (y,b), y=(a+4)/3, y' = ceil(3y/2)        [PROVEN given automaton]
    NEW here: 3 | a+4 is reached from ANY milestone in ONE step (a'+4 = 3(a+4)/2 or
    3(a+5)/2 or 9(a+5)/4) -- the conjugacy manifold is universal, not blank-orbit-only.
LINK 2  halt <=> b=0 at a milestone with y odd, y = 3 (mod 4)   [PROVEN given automaton;
    seeded raw-TM: a=1 mod 4 halts, a=3 mod 4 ESCAPES to D((9a+29)/4,1), incl. LARGE a]
LINK 3  non-halt <== ceiling-(K) seed 2 + finite check          [the (K) link stays OPEN]
    run form: halt <=> some odd run has s_i >= B_i + 2   (Antihydra: s_i >= B_i + 1);
    escape <=> s_i = B_i + 1 exactly (b=0 lands on the LAST odd milestone of the run,
    where v2(y+1)=1 <=> y=1 mod 4).
CRITICALITY  ceiling branches y -> (3y+r)/2, r=y mod 2; fixed points 2x=3x+r => x=-r
    (even 0, odd -1; the literal mirror of floor's +r): even-run = v2(y),
    odd-run = v2(y+1) EXACTLY; magnitude 2(3/2)^n <= y_n <= 3(3/2)^n - 1;
    run-cap slope log2(3/2)=0.585 [PROVEN given automaton], budget slope 1/2 [OBS=annealed],
    ratio log2(9/4) = 1.1699 -- Antihydra's number exactly.

SOUNDNESS: every check is finite; nothing here proves non-halting. No machine decided.
usage: x32c_o2_chain.py [raw_steps=100_000_000] [orbit_steps=1_000_000]
"""
import sys

SPEC = "1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

def runs_of(s):
    s = s.strip('0')
    ones, zeros = [], []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        (ones if s[i] == '1' else zeros).append(j - i)
        i = j
    return ones, zeros

def parse_milestone(s):
    """ones-runs [2]+[1]*a+[2]+[1]*b, all internal 0-gaps == 1 -> (a,b) or None."""
    ones, zeros = runs_of(s)
    if not ones or any(z != 1 for z in zeros):
        return None
    idx2 = [i for i, r in enumerate(ones) if r == 2]
    if len(idx2) != 2 or idx2[0] != 0:
        return None
    if any(r != 1 for i, r in enumerate(ones) if i not in idx2):
        return None
    return (idx2[1] - 1, len(ones) - idx2[1] - 1)

def ceil32(y):
    return -(-3 * y // 2)

def v2(n):
    return (n & -n).bit_length() - 1

def step_map(a, b):
    if a % 2 == 0:
        return ('D', (3 * a + 4) // 2, b + 2)
    if b >= 1:
        return ('D', (3 * a + 7) // 2, b - 1)
    N = (3 * a + 11) // 2
    if N % 2 == 1:
        return ('HALT',)
    return ('D', (3 * N - 2) // 2, 1)

# ---------------------------------------------------------------- LINK 0: raw blank orbit
def link0_blank(maxsteps):
    M = parse(SPEC)
    SZ = 1 << 24
    tape = bytearray(SZ)
    pos = SZ // 2; st = 0; step = 0; lo = hi = pos
    mil = []; unparsed = 0
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"RAW HALT at {step}"); break
        if st == 0 and pos <= lo and r == 0:
            s = ''.join(map(str, tape[lo:hi + 1]))
            ab = parse_milestone(s)
            if ab is not None:
                mil.append((step, ab[0], ab[1]))
            else:
                unparsed += 1
        w, d, ns = act
        tape[pos] = w; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    print(f"LINK 0 (blank orbit): {step:,} raw steps, {len(mil)} parsed A-milestones, "
          f"{unparsed} unparsed A-frontier events (transients)")
    print(f"  milestones (step, a, b): {[(s, a, b) for s, a, b in mil[:5]]} ... {mil[-1]}")
    mism = 0
    for i in range(len(mil) - 1):
        _, a, b = mil[i]
        if step_map(a, b) != ('D', mil[i + 1][1], mil[i + 1][2]):
            mism += 1
            print(f"  MISMATCH: D({a},{b}) -> predicted {step_map(a,b)}, observed D{mil[i+1][1:]}")
    print(f"  automaton check: {len(mil)-1} consecutive raw transitions, {mism} mismatches")
    return mism == 0, mil

# ---------------------------------------------------------------- LINK 0: seeded one-step grid
def seed_run(M, a, b, cap):
    SZ = 1 << 23
    tape = bytearray(SZ); off = SZ // 4
    s = "0" + "11" + "01" * a + "0" + "11" + "01" * b
    for i, ch in enumerate(s):
        tape[off + i] = 1 if ch == '1' else 0
    pos = off; st = 0; step = 0; lo = pos; hi = off + len(s) - 1
    while step < cap:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return ('HALT',), step
        if step > 0 and st == 0 and pos <= lo and r == 0:
            ss = ''.join(map(str, tape[lo:hi + 1]))
            ab = parse_milestone(ss)
            if ab is not None:
                return ('D', ab[0], ab[1]), step
        w, d, ns = act
        tape[pos] = w; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return ('TIMEOUT',), step

def link0_seeded(amax=80):
    M = parse(SPEC)
    bad = tested = 0
    for a in range(1, amax + 1):
        for b in (0, 1, 2, 3):
            pred = step_map(a, b)
            got, _ = seed_run(M, a, b, 3_000_000)
            tested += 1
            if got != pred:
                bad += 1
                print(f"  D({a},{b}): predicted {pred}, raw TM gave {got}   <-- MISMATCH")
    print(f"LINK 0 (seeded grid): {tested} one-step configs a=1..{amax}, b=0..3: {bad} mismatches")
    return bad == 0

# ---------------------------------------------------------------- LINK 1: conjugacy, universal manifold
def link1_grid(amax=300_000):
    bad_reach = bad_conj = bad_par = bad_halt = 0
    # (i) universal manifold: from ANY (a,b) one automaton step lands on 3 | a+4
    for a in range(1, amax):
        for res in (step_map(a, 1), step_map(a, 0)):
            if res[0] == 'D' and (res[1] + 4) % 3 != 0:
                bad_reach += 1
    # (ii) on the manifold: y=(a+4)/3 obeys y'=ceil(3y/2) on D-branches; escape = 2 ceilings;
    #      parity a even <=> y even; halt case N odd <=> a=1 mod 4 <=> y=3 mod 4
    for a in range(2, amax):
        if (a + 4) % 3:
            continue
        y = (a + 4) // 3
        if (a % 2 == 0) != (y % 2 == 0):
            bad_par += 1
        for b in (1, 2):
            res = step_map(a, b)
            if res[0] == 'D':
                if (res[1] + 4) % 3 or (res[1] + 4) // 3 != ceil32(y):
                    bad_conj += 1
        if a % 2 == 1:                      # b=0 branch
            res = step_map(a, 0)
            N = (3 * a + 11) // 2
            if (res == ('HALT',)) != (N % 2 == 1) or (N % 2 == 1) != (a % 4 == 1) \
               or (a % 4 == 1) != (y % 4 == 3):
                bad_halt += 1
            if res[0] == 'D':               # escape: two ceiling steps
                if (res[1] + 4) % 3 or (res[1] + 4) // 3 != ceil32(ceil32(y)) \
                   or res[1] != (9 * a + 29) // 4 or ceil32(y) % 2 != 0:
                    bad_conj += 1
    print(f"LINK 1 (grid a < {amax:,}): manifold-in-one-step violations {bad_reach}; "
          f"conjugacy violations {bad_conj}; parity violations {bad_par}; "
          f"halt-case mod-4 identity violations {bad_halt}")
    return bad_reach == bad_conj == bad_par == bad_halt == 0

# ---------------------------------------------------------------- LINK 2: halt/escape, seeded incl. LARGE
def link2_seeded():
    M = parse(SPEC)
    bad = 0; rows = []
    small = list(range(1, 202, 2))
    large = [401, 403, 801, 803, 1199, 1205, 2399, 2405]
    for a in small + large:
        exp = ('HALT',) if a % 4 == 1 else ('D', (9 * a + 29) // 4, 1)
        got, steps = seed_run(M, a, 0, 60_000_000)
        ok = (got == exp)
        if not ok:
            bad += 1
            print(f"  D({a},0): expected {exp}, raw TM gave {got}   <-- MISMATCH")
        if a in large:
            rows.append((a, a % 4, got[0] if got == ('HALT',) else f"escape->D({got[1]},{got[2]})", steps, ok))
    print(f"LINK 2 (seeded b=0): all odd a in 1..201 + large {large}: {bad} mismatches")
    print(f"  halt <=> a = 1 (mod 4); escape lands EXACTLY at D((9a+29)/4, 1)")
    for a, m4, verdict, steps, ok in rows:
        print(f"    a={a:>5} (mod4={m4}): {verdict}  [{steps:,} raw steps, {'ok' if ok else 'BAD'}]")
    return bad == 0

# ---------------------------------------------------------------- LINK 3 + criticality: blank y-orbit
def link3_orbit(N):
    y, b = 2, 1                     # first milestone D(2,1): y0=2, b0=1
    E = n = 0
    minb = b; minb_oddy = None; minb_oddy_at = 0
    zero_touch = 0
    # run bookkeeping
    run_par = y & 1; run_entry = y; run_len = 0
    n_even_runs = n_odd_runs = 0; sum_e = sum_s = 0
    runlaw_bad = ledger_id_bad = 0
    max_e = max_s = 0
    worst_drain = 0.0; worst_drain_at = -1
    cps = sorted({10**3, 10**4, 10**5, 5 * 10**5, N})
    ci = 0
    print(f"LINK 3 + criticality: blank y-orbit, {N:,} exact ceiling steps")
    print(f"  {'n':>8} {'even-dens':>10} {'b':>9} {'3E-n':>8} {'bits(y)':>8}")
    while n < N:
        par = y & 1
        if par != run_par:                              # a run just ended
            exp = v2(run_entry) if run_par == 0 else v2(run_entry + 1)
            if run_len != exp:
                runlaw_bad += 1
            if run_par == 0:
                n_even_runs += 1; sum_e += run_len; max_e = max(max_e, run_len)
            else:
                n_odd_runs += 1; sum_s += run_len; max_s = max(max_s, run_len)
            if par == 1:                                # odd-run ENTRY: identity + drain stats
                Bent = 1 + 2 * sum_e - sum_s
                if b != Bent:
                    ledger_id_bad += 1
                s_next = v2(y + 1)
                dr = s_next / Bent
                if dr > worst_drain:
                    worst_drain, worst_drain_at = dr, n
            run_par = par; run_entry = y; run_len = 0
        if par == 1 and b == 0:                         # S branch
            zero_touch += 1
            if y % 4 == 3:
                print(f"  ORBIT HALT at n={n}"); return False
            y = (9 * y + 3) // 4; E += 1; n += 2; b = 1     # escape: 2 ceiling steps
            run_par = y & 1; run_entry = y; run_len = 0     # (re-sync runs; unexercised)
            continue
        if par == 0:
            y = 3 * y // 2; b += 2; E += 1
        else:
            y = (3 * y + 1) // 2; b -= 1
        n += 1; run_len += 1
        minb = min(minb, b)
        if (y & 1) and (minb_oddy is None or b < minb_oddy):
            minb_oddy, minb_oddy_at = b, n
        while ci < len(cps) and n >= cps[ci]:
            print(f"  {n:>8} {E/n:>10.6f} {b:>9,} {3*E-n:>8,} {y.bit_length():>8,}")
            ci += 1
    print(f"  zero-touches (b=0 at odd y): {zero_touch}   [the escape hatch is UNEXERCISED on the blank orbit]")
    print(f"  min b = {minb} (worst prefix 3E_n - n = {minb-1});"
          f" min b at odd-y milestones = {minb_oddy} at n={minb_oddy_at}")
    print(f"  runs: {n_even_runs:,} even (mean {sum_e/n_even_runs:.4f}, max {max_e}), "
          f"{n_odd_runs:,} odd (mean {sum_s/n_odd_runs:.4f}, max {max_s})")
    print(f"  run laws e=v2(y), s=v2(y+1): {runlaw_bad} violations; "
          f"odd-entry ledger identity b = 1 + 2*sum(e) - sum(s): {ledger_id_bad} violations")
    print(f"  worst single-run drain s/B(entry) = {worst_drain:.4f} at n={worst_drain_at}  "
          f"(fatality needs s >= B+2, i.e. ratio > 1)")
    return runlaw_bad == 0 and ledger_id_bad == 0

# ---------------------------------------------------------------- run laws, exhaustive
def runlaw_exhaustive(ymax=200_000):
    bad = 0
    for y0 in range(1, ymax):
        y = y0; k = 0
        if y0 % 2 == 0:
            while y % 2 == 0:
                y = 3 * y // 2; k += 1
            if k != v2(y0):
                bad += 1
        else:
            while y % 2 == 1:
                y = (3 * y + 1) // 2; k += 1
            if k != v2(y0 + 1):
                bad += 1
    print(f"run laws exhaustive y=1..{ymax:,}: even-run=v2(y), odd-run=v2(y+1): {bad} mismatches")
    print("  (branch fixed points: 2x=3x+r => x=-r: x_even=0, x_odd=-1; "
          "y'-x = (3/2)(y-x) exactly on each branch)")
    return bad == 0

# ---------------------------------------------------------------- magnitude bounds, exact
def magnitude(nmax=2000):
    y = 2; bad = 0
    p3, p2 = 1, 1
    for n in range(nmax + 1):
        # 2*(3/2)^n <= y_n  and  y_n + 1 <= 3*(3/2)^n   (exact integer form)
        if not (2 * p3 <= y * p2 and (y + 1) * p2 <= 3 * p3):
            bad += 1
        y = ceil32(y); p3 *= 3; p2 *= 2
    print(f"magnitude bounds 2(3/2)^n <= y_n <= 3(3/2)^n - 1 exact to n={nmax}: {bad} violations")
    print("  => odd-run cap v2(y_n+1) <= log2(y_n+1) <= n*log2(3/2) + log2(3)  [PROVEN given automaton]")
    return bad == 0

# ---------------------------------------------------------------- induced odd map (ceiling gap lemma)
def induced_odd(N=100_000):
    """Ceiling-side mirror of Antihydra's GAP LEMMA: for odd o on the ceiling orbit,
    the next odd value is T(o) = 3^(G-1)(3o+1)/2^G with G = v2(3o+1), reached in G steps
    (1 odd step + an even run of length G-1 = v2((3o+1)/2)); G>=2 <=> o = 1 (mod 4).
    Kac/renewal: even-density >= 1/3 <=> mean G >= 3/2; level-2 truncation:
    mean G >= 1 + freq(o = 1 mod 4), so freq(o = 1 mod 4) >= 1/2 is sufficient."""
    o = 3                                   # y0 = 2 -> 3: first odd value
    bad = badmod = 0; sumG = 0; f1 = 0
    for _ in range(N):
        G = v2(3 * o + 1)
        nxt = (3 ** (G - 1) * (3 * o + 1)) >> G
        z = (3 * o + 1) // 2                # direct iteration cross-check
        steps = 1
        while z % 2 == 0:
            z = 3 * z // 2; steps += 1
        if z != nxt or steps != G:
            bad += 1
        if (G >= 2) != (o % 4 == 1):
            badmod += 1
        sumG += G; f1 += (o % 4 == 1)
        o = nxt
    print(f"induced odd map (o0=3), {N:,} returns: T(o)=3^(G-1)(3o+1)/2^G, G=v2(3o+1): "
          f"{bad} mismatches; G>=2 <=> o=1 mod 4: {badmod} violations")
    print(f"  mean G = {sumG/N:.5f} (needed >= 3/2, Haar 2); freq(o = 1 mod 4) = {f1/N:.5f} "
          f"(sufficient >= 1/2)")
    return bad == 0 and badmod == 0

# ---------------------------------------------------------------- seeded ensemble: escape fraction
def ensemble():
    events = escapes = halts = 0
    orbits = orbits_touch = orbits_multi = 0
    yform_bad = 0
    for a0 in range(1, 2000, 2):
        for b0 in (0, 1, 2):
            a, b = a0, b0
            ev = 0
            for _ in range(500):
                if a % 2 == 1 and b == 0:
                    events += 1; ev += 1
                    if (a + 4) % 3 == 0:            # on-manifold: check y-form of the criterion
                        yv = (a + 4) // 3
                        if (a % 4 == 3) != (yv % 4 == 1) or (a % 4 == 3) != (v2(yv + 1) == 1):
                            yform_bad += 1
                    if a % 4 == 1:
                        halts += 1; break
                    escapes += 1
                    a = (9 * a + 29) // 4; b = 1
                    continue
                r = step_map(a, b)
                a, b = r[1], r[2]
                if a.bit_length() > 1500:
                    break
            orbits += 1
            if ev: orbits_touch += 1
            if ev >= 2: orbits_multi += 1
    print(f"seeded ensemble (a odd 1..1999, b=0..2, {orbits} orbits): "
          f"{events} zero-touches in {orbits_touch} orbits ({orbits_multi} with >=2)")
    print(f"  outcomes: {halts} HALT (a=1 mod 4), {escapes} ESCAPE (a=3 mod 4) "
          f"-> escape fraction {escapes/events:.4f}")
    print(f"  y-form identity (escape <=> y=1 mod 4 <=> v2(y+1)=1, on-manifold touches): {yform_bad} violations")
    return yform_bad == 0

if __name__ == "__main__":
    raw_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000_000
    orbit_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 1_000_000
    ok0, _ = link0_blank(raw_steps)
    ok0b = link0_seeded()
    ok1 = link1_grid()
    ok2 = link2_seeded()
    ok3 = link3_orbit(orbit_steps)
    ok4 = runlaw_exhaustive()
    ok5 = magnitude()
    ok5b = induced_odd()
    ok6 = ensemble()
    import math
    rho = math.log2(1.5)
    print(f"\nCRITICALITY ROW (o2): run-cap slope rho = log2(3/2) = {rho:.5f} [PROVEN given automaton];")
    print(f"  budget slope beta = 1/2 [OBSERVED = annealed]; ratio rho/beta = log2(9/4) = {2*rho:.6f} > 1")
    print(f"  ruin base: increments {{+2,-1}} p=1/2 => eta = (sqrt5-1)/2 = {(5**0.5-1)/2:.6f} (same as Antihydra)")
    print(f"\nall checks passed: {all([ok0, ok0b, ok1, ok2, ok3, ok4, ok5, ok5b, ok6])}")
    print("No machine decided. No label upgraded.")
