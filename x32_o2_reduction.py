#!/usr/bin/env python3
"""x32_o2_reduction.py -- o2 precise reduction: milestone automaton -> ceiling-3/2 ledger (2026-07-07).

o2 = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA  (halt F,0; F <- only D,0->0RF)

Claims verified here (labels reported in output):
 (1) MILESTONE AUTOMATON [checked 0-mismatch vs raw TM]:
     milestone = state A at left frontier reading 0, tape = 0 . 11 . (01)^a . 0 . 11 . (01)^b.
     D(a,b) map (CRYPTID_SLOWWIDTH_2026-07-04 section 1):
        a even:        D(a,b) -> D((3a+4)/2, b+2)
        a odd, b>=1:   D(a,b) -> D((3a+7)/2, b-1)
        a odd, b=0:    -> S(N), N=(3a+11)/2 ; S(N) -> HALT if N odd, else D((3N-2)/2, 1)
 (2) VALUE CONJUGACY [exact algebra given (1); confirmed numerically]:
     x = a+4 is divisible by 3 at every milestone; y = (a+4)/3 obeys y' = ceil(3y/2)
     EXACTLY on both D-branches; the b=0 escape branch is TWO ceiling steps
     (y odd, y=1 mod 4: y -> (3y+1)/2 [even] -> (9y+3)/4).  Parities: a even <=> y even;
     the b=0-halt case  a=1 mod 4 <=> y=3 mod 4.
     So o2's value kernel is the CEILING 3/2 map (the literal AEV Conj-1.6 side), seed y0 = 2.
 (3) LEDGER IDENTITY [exact given (1)]: db = +2 iff y even, -1 iff y odd
     => b_n = b_0 + 3*E_n - n (E_n = #even y in y_0..y_{n-1}) -- Antihydra's balance functional.
 (4) HALT CRITERION [derived from (1)]: HALT <=> b hits 0 at an odd-y milestone with
     y = 3 (mod 4); b=0 at y = 1 (mod 4) ESCAPES (two ceiling steps, b resets to 1).
     Verified by SEEDED raw-TM runs D(a,b) incl. b=0.
 (5) MARGINS [OBSERVED]: running even-density of the y-orbit, min b, worst prefix 3E-n.

SOUNDNESS: all checks are finite; nothing here proves non-halting. No machine decided.
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
    """Expect ones-runs [2]+[1]*a+[2]+[1]*b, all internal 0-gaps == 1. Return (a,b) or None."""
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

def step_map(a, b):
    """One step of the milestone automaton. Returns ('D', a', b') or ('HALT',)."""
    if a % 2 == 0:
        return ('D', (3 * a + 4) // 2, b + 2)
    if b >= 1:
        return ('D', (3 * a + 7) // 2, b - 1)
    N = (3 * a + 11) // 2
    if N % 2 == 1:
        return ('HALT',)
    return ('D', (3 * N - 2) // 2, 1)

# ------------------------------------------------------------ raw-TM blank-orbit check
def blank_orbit_check(maxsteps):
    M = parse(SPEC)
    SZ = 1 << 24
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    mil = []
    unparsed = 0
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
    print(f"blank run to {step:,} steps: {len(mil)} parsed A-milestones, {unparsed} unparsed (transients)")
    mism = 0
    for i in range(len(mil) - 1):
        _, a, b = mil[i]
        if step_map(a, b) != ('D', mil[i + 1][1], mil[i + 1][2]):
            mism += 1
            if mism <= 5:
                print(f"  MISMATCH: D({a},{b}) -> predicted {step_map(a,b)}, observed D{mil[i+1][1:]}")
    print(f"automaton check: {len(mil)-1} consecutive transitions, {mism} mismatches")

    bad3 = sum(1 for _, a, _ in mil if (a + 4) % 3 != 0)
    ys = [(a + 4) // 3 for _, a, _ in mil]
    ceil_bad = sum(1 for i in range(len(ys) - 1) if ys[i + 1] != ceil32(ys[i]))
    led_bad = sum(1 for i in range(len(mil) - 1)
                  if mil[i + 1][2] - mil[i][2] != (2 if ys[i] % 2 == 0 else -1))
    print(f"value law: (a+4) not divisible by 3: {bad3} of {len(mil)};"
          f" y'=ceil(3y/2) violations: {ceil_bad}  (y ladder: {ys[:9]} ...)")
    print(f"ledger law db = +2 (y even) / -1 (y odd): violations: {led_bad}")
    bs = [b for _, _, b in mil]
    print(f"ledger on raw orbit: b0={bs[0]}, min b = {min(bs)}, final b = {bs[-1]}, "
          f"drift = {(bs[-1]-bs[0])/(len(bs)-1):+.4f}/milestone")
    return mism == 0 and bad3 == 0 and ceil_bad == 0 and led_bad == 0

# ------------------------------------------------------------ seeded S-branch / halt check
def seeded_check():
    M = parse(SPEC)
    def seed_run(a, b, cap=3_000_000):
        SZ = 1 << 22
        tape = bytearray(SZ); off = SZ // 4
        s = "0" + "11" + "01" * a + "0" + "11" + "01" * b
        for i, ch in enumerate(s):
            tape[off + i] = 1 if ch == '1' else 0
        pos = off; st = 0; step = 0; lo = pos; hi = off + len(s) - 1
        while step < cap:
            r = tape[pos]
            act = M[st][r]
            if act is None:
                return ('HALT',)
            if step > 0 and st == 0 and pos <= lo and r == 0:
                ss = ''.join(map(str, tape[lo:hi + 1]))
                ab = parse_milestone(ss)
                if ab is not None:
                    return ('D', ab[0], ab[1])
            w, d, ns = act
            tape[pos] = w; pos += d; st = ns; step += 1
            if pos < lo: lo = pos
            if pos > hi: hi = pos
        return ('TIMEOUT',)
    print("\nseeded raw-TM checks of all branches incl. b=0 (S branch):")
    bad = 0; tested = 0; halts = []
    for a in range(1, 42):
        for b in ([0, 1, 2] if a % 2 == 1 else [0, 1]):
            pred = step_map(a, b)
            got = seed_run(a, b)
            tested += 1
            if got != pred:
                bad += 1
                print(f"  D({a},{b}): predicted {pred}, raw TM gave {got}   <-- MISMATCH")
            if pred == ('HALT',) and got == ('HALT',):
                halts.append(a)
    print(f"  {tested} seeded configs, {bad} mismatches")
    print(f"  confirmed HALT seeds D(a,0): a = {halts}  (exactly a = 1 mod 4, i.e. y = 3 mod 4)")
    return bad == 0

# ------------------------------------------------------------ abstract long iteration (margins)
def abstract_margins(n_iter):
    a, b = 2, 1                      # first parsed milestone D(2,1); y0 = 2
    E = 0; n = 0                     # ceiling-step count n and even-y count E
    minb = b; minb_at = 0
    minb_oddy = 10**18; minb_oddy_at = 0
    min_prefix = 10**18; min_prefix_at = 0
    escapes = 0
    cps = sorted({10, 100, 1000, 10000, 50000, n_iter})
    print(f"\nabstract iteration, {n_iter:,} ceiling steps (exact bigints):")
    print(f"  {'n':>7} {'even-dens':>10} {'b':>8} {'3E-n':>8} {'digits(y)':>9}")
    ci = 0
    while n < n_iter:
        y = (a + 4) // 3
        assert (a + 4) % 3 == 0
        ye = (y % 2 == 0)
        res = step_map(a, b)
        if res == ('HALT',):
            print(f"  ABSTRACT HALT at n={n} (b=0, y%4={y%4})")
            return
        escape = (not ye) and b == 0
        a2, b2 = res[1], res[2]
        # conjugacy invariant check
        y2 = (a2 + 4) // 3
        expect = ceil32(ceil32(y)) if escape else ceil32(y)
        assert y2 == expect and (a2 + 4) % 3 == 0, (a, b, a2)
        if escape:
            escapes += 1
            y_mid = ceil32(y)
            E += (0 if y % 2 else 1) + (0 if y_mid % 2 else 1)
            n += 2
        else:
            E += 1 if ye else 0
            n += 1
        a, b = a2, b2
        bal = 3 * E - n
        if b < minb:
            minb, minb_at = b, n
        if (y % 2 == 1) and b < minb_oddy:
            minb_oddy, minb_oddy_at = b, n
        if bal < min_prefix:
            min_prefix, min_prefix_at = bal, n
        while ci < len(cps) and n >= cps[ci]:
            digs = int(y.bit_length() * 0.30103) + 1
            print(f"  {n:>7} {E/n:>10.5f} {b:>8} {bal:>8} {digs:>9}")
            ci += 1
    print(f"  escapes (b=0 at y=1 mod 4): {escapes}")
    print(f"  min b = {minb} at n={minb_at}; min b entering odd-y steps = {minb_oddy} at n={minb_oddy_at}")
    print(f"  worst prefix 3E_n - n = {min_prefix} at n={min_prefix_at}   (b_n = b_0 + 3E_n - n exactly)")

if __name__ == "__main__":
    raw_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    n_abs = int(sys.argv[2]) if len(sys.argv) > 2 else 100_000
    ok1 = blank_orbit_check(raw_steps)
    ok2 = seeded_check()
    abstract_margins(n_abs)
    print(f"\nall checks passed: {ok1 and ok2}")
    print("No machine decided. No label upgraded.")
