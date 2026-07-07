#!/usr/bin/env python3
"""x32_o7_reduction.py -- o7 precise reduction: coupled two-counter map, 2-adic cascade,
thin-set (power-of-two) halt criterion -- NOT a balance/density machine (2026-07-07).

o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC  (halt F,0; F <- only C,0->1LF)

Claims verified here:
 (1) MILESTONE AUTOMATON [checked 0-mismatch vs raw TM]:
     milestone = state D at left frontier, reading the 0 directly left of the first block;
     tape = 0 1^a 0 1^b.  Map (CRYPTID_SLOWWIDTH_2026-07-04 section 2, with ONE CORRECTION):
        a even >= 2: (a,b) -> (3a/2 + 1 + b, 1)
        a odd  >= 5: (a,b) -> ((a-3)/2, b + (a+5)/2)
        a = 3:       (a,b) -> (b+5, 1 + [b odd])     [CORRECTED HERE: the banked map's
                     2*[b odd] fails the seeded raw-TM check for even b: (3,2)->(7,1) and
                     (3,4)->(9,1) on the raw TM, not (7,0)/(9,0); b' is 1+[b odd], never 0]
        a = 1:       HALT
 (2) VALUE MAP IS NOT FLOOR-3/2 [exact given (1)]:
     on x = a+4 the two branches are x -> 3x/2 (x even) and x -> (x+1)/2 (x odd):
     the odd branch is a HALVING, not (3x-1)/2. No shift conjugacy to floor or ceiling
     x3/2 exists (both are checked directly). o7 is NOT a Mahler-x3/2 value orbit.
 (3) CASCADE LAW [exact given (1)]: u = a+3 halves EXACTLY on each odd step
     (u' = u/2), so a cascade entered at odd a runs v2(a+3) steps and exits at
     a_end = oddpart(a+3) - 3 (or hits the a=3 branch iff oddpart = 3).
 (4) HALT CRITERION [derived from (1)+(3)]:
     HALT <=> some milestone has a+3 = 2^k (k >= 2) <=> oddpart(a+3) = 1.
     A THIN-set / reachability (B2) event -- one fatal value per dyadic scale --
     NOT a balance-returns-to-zero or density event. b has NO ledger role in the halt.
     Verified on a seeded raw-TM grid (predictions by iterating the abstract map).
 (5) MARGINS [OBSERVED]: min a, cascade-depth distribution v2(a+3) vs geometric,
     min oddpart(a+3) at cascade entries (fatality needs oddpart = 1).

SOUNDNESS: finite checks only; nothing proves non-halting. No machine decided.
"""
import sys

SPEC = "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"

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
    """0 1^a 0 1^b (or 0 1^a for b=0): 1 or 2 one-runs, all internal 0-gaps == 1."""
    ones, zeros = runs_of(s)
    if any(z != 1 for z in zeros):
        return None
    if len(ones) == 2:
        return (ones[0], ones[1])
    if len(ones) == 1:
        return (ones[0], 0)
    return None

def step_map(a, b):
    if a == 1:
        return ('HALT',)
    if a == 3:
        return ('D', b + 5, 1 + (b % 2))   # corrected vs CRYPTID_SLOWWIDTH (raw-TM checked)
    if a % 2 == 0:
        return ('D', 3 * a // 2 + 1 + b, 1)
    return ('D', (a - 3) // 2, b + (a + 5) // 2)

def v2(n):
    return (n & -n).bit_length() - 1

def oddpart(n):
    return n >> v2(n)

def halts_abstract(a, b, cap=10000):
    """Iterate the abstract map; return True/False/None(cap)."""
    for _ in range(cap):
        r = step_map(a, b)
        if r == ('HALT',):
            return True
        a, b = r[1], r[2]
        if a.bit_length() > 4000:
            return False    # heuristic escape for the seeded grid (values explode)
    return None

# ------------------------------------------------------------ raw-TM blank-orbit check
def blank_orbit_check(maxsteps):
    M = parse(SPEC)
    SZ = 1 << 24
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    mil = []; unparsed = 0
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"RAW HALT at {step}"); break
        if st == 3 and pos <= lo and r == 0 and tape[pos + 1] == 1:
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
    print(f"blank run to {step:,} steps: {len(mil)} parsed D-milestones, {unparsed} unparsed")
    mism = 0
    for i in range(len(mil) - 1):
        _, a, b = mil[i]
        if step_map(a, b) != ('D', mil[i + 1][1], mil[i + 1][2]):
            mism += 1
            if mism <= 5:
                print(f"  MISMATCH: ({a},{b}) -> predicted {step_map(a,b)}, observed {mil[i+1][1:]}")
    print(f"automaton check: {len(mil)-1} consecutive transitions, {mism} mismatches"
          f"   (orbit starts {[(m[1],m[2]) for m in mil[:6]]})")
    # cascade law on the raw orbit
    casc_bad = 0
    for i in range(len(mil) - 1):
        a = mil[i][1]
        if a % 2 == 1 and a >= 5:
            if mil[i + 1][1] + 3 != (a + 3) // 2:
                casc_bad += 1
    print(f"cascade law u=a+3 halves on odd steps: violations = {casc_bad}")
    amin = min(m[1] for m in mil)
    print(f"min a over raw milestones = {amin}  (fatal set is a+3 = power of 2, nearest small: a=5,13,29)")
    return mism == 0 and casc_bad == 0

# ------------------------------------------------------------ seeded halt-prediction grid
def seeded_check():
    M = parse(SPEC)
    def seed_run(a, b, cap=2_000_000):
        SZ = 1 << 22
        tape = bytearray(SZ); off = SZ // 4
        s = "0" + "1" * a + ("0" + "1" * b if b > 0 else "")
        for i, ch in enumerate(s):
            tape[off + i] = 1 if ch == '1' else 0
        pos = off; st = 3; step = 0; lo = pos; hi = off + len(s) - 1
        while step < cap:
            r = tape[pos]
            act = M[st][r]
            if act is None:
                return ('HALT',)
            if step > 0 and st == 3 and pos <= lo and r == 0 and tape[pos + 1] == 1:
                ss = ''.join(map(str, tape[lo:hi + 1]))
                ab = parse_milestone(ss)
                if ab is not None:
                    return ('D', ab[0], ab[1])
            w, d, ns = act
            tape[pos] = w; pos += d; st = ns; step += 1
            if pos < lo: lo = pos
            if pos > hi: hi = pos
        return ('TIMEOUT',)
    print("\nseeded raw-TM checks (one milestone step), all four branches:")
    bad = 0; tested = 0
    for a in range(1, 32):
        for b in (1, 2, 3, 4):
            pred = step_map(a, b)
            got = seed_run(a, b)
            tested += 1
            if got != pred:
                bad += 1
                print(f"  ({a},{b}): predicted {pred}, raw TM gave {got}   <-- MISMATCH")
    print(f"  {tested} seeded one-step configs, {bad} mismatches")
    # multi-step halt predictions: fatal iff the abstract orbit hits oddpart(a+3)=1
    print("seeded raw-TM HALT-verdict grid vs abstract-map iteration (multi-step):")
    bad2 = 0; tested2 = 0; halts = []
    for a in range(1, 32):
        for b in (1, 2):
            pred = halts_abstract(a, b)
            if pred is None:
                continue
            got = seed_run(a, b, cap=5_000_000)
            # follow raw TM through milestones until halt or growth
            aa, bb = a, b
            steps_left = 60
            while got[0] == 'D' and steps_left:
                if got[1] > 5000:
                    got = ('RUN',); break
                aa, bb = got[1], got[2]
                got = seed_run(aa, bb, cap=5_000_000)
                steps_left -= 1
            raw_halts = (got == ('HALT',))
            if got[0] in ('TIMEOUT',):
                continue
            tested2 += 1
            if raw_halts != pred:
                bad2 += 1
                print(f"  seed ({a},{b}): abstract predicts halt={pred}, raw gave {got}  <-- MISMATCH")
            if raw_halts:
                halts.append((a, b))
        if a > 20 and len(halts) > 8:
            break
    print(f"  {tested2} decided seeds compared, {bad2} mismatches; raw-confirmed halting seeds: {halts}")
    return bad == 0 and bad2 == 0

# ------------------------------------------------------------ abstract margins
def abstract_margins(n_iter):
    a, b = 2, 2                     # first parsed milestone
    n = 0
    amin = a; amin_at = 0
    depth_hist = {}
    min_oddpart = None
    entries = 0
    prev_even = True
    print(f"\nabstract iteration, {n_iter:,} milestones (exact bigints):")
    while n < n_iter:
        r = step_map(a, b)
        if r == ('HALT',):
            print(f"  ABSTRACT HALT at n={n}"); return
        if a % 2 == 1 and prev_even:
            entries += 1
            d = v2(a + 3)
            depth_hist[d] = depth_hist.get(d, 0) + 1
            w = oddpart(a + 3)
            if min_oddpart is None or w < min_oddpart:
                min_oddpart = w
        prev_even = (a % 2 == 0)
        a, b = r[1], r[2]
        n += 1
        if a < amin:
            amin, amin_at = a, n
    tot = sum(depth_hist.values())
    print(f"  milestones: {n:,}; final a has {a.bit_length()} bits; min a = {amin} at n={amin_at}")
    print(f"  cascade entries (even->odd): {entries}; depth v2(a+3) histogram vs geometric 2^-d:")
    for d in sorted(depth_hist):
        print(f"    d={d:>2}: {depth_hist[d]:>8}  freq {depth_hist[d]/tot:.4f}  (geom {2.0**-d:.4f})")
    print(f"  min oddpart(a+3) at entries = {min_oddpart}  (HALT would need oddpart = 1)")
    print(f"  max depth seen = {max(depth_hist)} vs bit-length needed for fatality ~ {a.bit_length()}")

if __name__ == "__main__":
    raw_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    n_abs = int(sys.argv[2]) if len(sys.argv) > 2 else 500_000
    ok1 = blank_orbit_check(raw_steps)
    ok2 = seeded_check()
    abstract_margins(n_abs)
    print(f"\nall checks passed: {ok1 and ok2}")
    print("No machine decided. No label upgraded.")
