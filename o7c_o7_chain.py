#!/usr/bin/env python3
"""o7c_o7_chain.py -- o7 full 5-link treatment: the load-bearing NEW claim is that o7's two
branches carry TWO DIFFERENT multipliers (even x3/2, odd x1/2), so o7 is NOT a single x(p/q)
value odometer -- it breaks the Type-I 'one multiplier' requirement. Everything downstream
(halt = a+3 = 2^k, thin-set protection) is re-verified against the raw TM.

o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC  (halt F,0; F <- only C,0->1LF)

Reuses the milestone automaton from x32_o7_reduction.py (banked 0-mismatch: 29 raw + 124 seeded).
SOUNDNESS: finite checks only; nothing proves non-halting. No machine decided.
"""
import sys
from fractions import Fraction as Fr

SPEC = "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

def step_map(a, b):
    """The banked o7 milestone automaton (x32_o7_reduction.py, raw-TM 0-mismatch)."""
    if a == 1:
        return ('HALT',)
    if a == 3:
        return ('D', b + 5, 1 + (b % 2))
    if a % 2 == 0:
        return ('D', 3 * a // 2 + 1 + b, 1)          # EVEN branch  (couples in b)
    return ('D', (a - 3) // 2, b + (a + 5) // 2)      # ODD branch   (drains a into b)

def v2(n): return (n & -n).bit_length() - 1
def oddpart(n): return n >> v2(n)

# --------------------------------------------------------------- LINK 2/3: the two multipliers
def branch_multipliers():
    """Prove the two branches carry DIFFERENT multipliers -- the Type-I break.
    We test candidate affine forms b(v) = (p v + e)/q on the pure (autonomous) part of each branch.

    EVEN CHAIN (D4 in X32): b=1 stays 1 after every even step, so a is autonomous:
        a -> 3a/2 + 1 + 1 = 3a/2 + 2  (a even). On x=a+4:  x -> 3(a+4)/2 = 3x/2.
        => multiplier 3/2, fixed point x=0 i.e. a=-4, run length = v2(a+4).
    ODD CASCADE (D1 in X32): the odd branch a -> (a-3)/2. On u=a+3:  u -> u/2.
        => multiplier 1/2, fixed point u=0 i.e. a=-3, run length = v2(a+3).
        On x=a+4 the same odd branch reads x -> (x+1)/2  (a HALVING, multiplier 1/2, fixed pt 1).
    """
    print("=== LINK 2/3: branch multipliers (the Type-I 'single p/q' break) ===")
    ok = True

    # EVEN chain, autonomous at b=1: check a->3a/2+2 and the x=a+4 conjugacy x->3x/2, fixed pt -4.
    bad = 0
    for a in range(2, 200000, 2):
        got = step_map(a, 1)               # even step at b=1
        a2 = got[1]                        # = 3a/2 + 1 + 1
        if a2 != 3 * a // 2 + 2:      bad += 1
        if (a2 + 4) != 3 * (a + 4) // 2:   bad += 1    # x=a+4 -> 3x/2 exactly
    print(f"  EVEN branch (b=1): a->3a/2+2 and (a+4)->3(a+4)/2  -- multiplier 3/2, fixed pt a=-4;"
          f" violations={bad}")
    ok &= (bad == 0)
    # even-chain run length = v2(a+4): iterate even steps while a stays even
    bad = 0
    for a0 in range(2, 4000, 2):
        run, a, b = 0, a0, 1
        while a % 2 == 0 and a >= 2:
            got = step_map(a, b)
            a, b = got[1], got[2]
            run += 1
            if run > 200: break
        if run != v2(a0 + 4): bad += 1
    print(f"  EVEN chain length == v2(a+4) (fixed-point run law, ratio 3/2): violations={bad}")
    ok &= (bad == 0)

    # ODD cascade: u=a+3 -> u/2 exactly; run length = v2(a+3); multiplier 1/2 (NOT 3/2).
    bad = 0
    for a in range(5, 200000, 2):
        got = step_map(a, 7)               # odd step (b arbitrary; a-update is autonomous)
        a2 = got[1]
        if (a2 + 3) != (a + 3) // 2:  bad += 1          # u -> u/2
        if (a2 + 4) != (a + 4 + 1) // 2:  bad += 1       # x=a+4 -> (x+1)/2  (halving)
    print(f"  ODD  branch: (a+3)->(a+3)/2  and (a+4)->((a+4)+1)/2  -- multiplier 1/2, fixed pt a=-3;"
          f" violations={bad}")
    ok &= (bad == 0)
    # run law holds when the descending u = oddpart*2^j never hits u=4 (a=1 HALT) or u=6 (a=3 special);
    # i.e. exactly when oddpart(a+3) >= 5. oddpart in {1,3} are truncated by the special branches.
    bad = 0; trunc = 0
    for a0 in range(5, 200000, 2):
        run, a, b = 0, a0, 7
        while a % 2 == 1 and a >= 5:
            got = step_map(a, b)
            a, b = got[1], got[2]
            run += 1
            if run > 200: break
        if oddpart(a0 + 3) >= 5:
            if run != v2(a0 + 3): bad += 1
        else:
            trunc += 1                       # oddpart in {1,3}: special-branch truncation (fatal / a=3)
    print(f"  ODD  cascade length == v2(a+3) for oddpart>=5 (fixed-point run law, ratio 1/2):"
          f" violations={bad}  (special-branch truncations oddpart in {{1,3}}: {trunc})")
    ok &= (bad == 0)

    print("  >>> TWO DISTINCT MULTIPLIERS: even branch x3/2, odd branch x1/2.")
    print("      A Type-I cryptid has ONE p/q on BOTH branches (Antihydra: 3v/2 and (3v-1)/2, both x3/2).")
    print("      o7's odd branch is a pure halving, so no single x(p/q) value odometer governs o7.")
    return ok

# --------------------------------------------------------------- LINK 4: halt criterion, raw TM
def halt_criterion_raw(maxsteps):
    """HALT <=> some milestone has a+3 = 2^k (k>=2) <=> oddpart(a+3)=1. Re-confirm milestone
    automaton + cascade law on the blank orbit (0-mismatch expected)."""
    print(f"\n=== LINK 4: halt criterion (blank raw orbit to {maxsteps:,} steps) ===")
    M = parse(SPEC)
    SZ = 1 << 24
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    mil = []
    def parse_ms(s):
        s = s.strip('0'); ones=[]; zeros=[]; i=0
        while i < len(s):
            j=i
            while j < len(s) and s[j]==s[i]: j+=1
            (ones if s[i]=='1' else zeros).append(j-i); i=j
        if any(z!=1 for z in zeros): return None
        if len(ones)==2: return (ones[0],ones[1])
        if len(ones)==1: return (ones[0],0)
        return None
    while step < maxsteps:
        r = tape[pos]; act = M[st][r]
        if act is None:
            print(f"  RAW HALT at {step}"); break
        if st == 3 and pos <= lo and r == 0 and tape[pos+1] == 1:
            ab = parse_ms(''.join(map(str, tape[lo:hi+1])))
            if ab is not None: mil.append(ab)
        w,d,ns = act; tape[pos]=w; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    mism = sum(1 for i in range(len(mil)-1)
               if step_map(*mil[i]) != ('D', mil[i+1][0], mil[i+1][1]))
    casc = sum(1 for i in range(len(mil)-1)
               if mil[i][0]%2==1 and mil[i][0]>=5 and mil[i+1][0]+3 != (mil[i][0]+3)//2)
    amin = min(m[0] for m in mil)
    print(f"  {len(mil)} milestones; automaton mismatches={mism}; cascade u=u/2 violations={casc}")
    print(f"  min a = {amin}; fatal set a+3=2^k (a in 1,5,13,29,61,...); min oddpart(a+3) over orbit"
          f" = {min(oddpart(m[0]+3) for m in mil)} (HALT needs oddpart=1)")
    return mism == 0 and casc == 0

# --------------------------------------------------------------- LINK 5: thin-set protection
def thin_set_margins(n_iter):
    print(f"\n=== LINK 5: thin-set protection ({n_iter:,} abstract milestones) ===")
    a, b, n = 2, 2, 0
    depth = {}; prev_even = True; min_odd = None; entries = 0
    while n < n_iter:
        r = step_map(a, b)
        if r == ('HALT',):
            print(f"  ABSTRACT HALT at n={n}"); return
        if a % 2 == 1 and prev_even:
            entries += 1; d = v2(a+3); depth[d] = depth.get(d,0)+1
            w = oddpart(a+3)
            if min_odd is None or w < min_odd: min_odd = w
        prev_even = (a % 2 == 0)
        a, b = r[1], r[2]; n += 1
    tot = sum(depth.values())
    print(f"  final a: {a.bit_length()} bits; cascade entries={entries}; max depth={max(depth)}")
    print(f"  depth v2(a+3): d=1 {depth.get(1,0)/tot:.4f} (geom .5), d=2 {depth.get(2,0)/tot:.4f} (.25),"
          f" d=3 {depth.get(3,0)/tot:.4f} (.125)")
    print(f"  min oddpart(a+3) at entries = {min_odd}  (fatality needs oddpart -> 1; it never approaches 1)")
    print(f"  SPECIES: thin-set hitting; fatal set relative measure 2^-bitlen(a+3) -> 0;")
    print(f"  odd part regenerated per entry (RESET, no scalar ledger); B2 reachability wall.")

if __name__ == "__main__":
    raw = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    nit = int(sys.argv[2]) if len(sys.argv) > 2 else 500_000
    ok = branch_multipliers()
    ok &= halt_criterion_raw(raw)
    thin_set_margins(nit)
    print(f"\nall structural checks passed: {ok}")
    print("No machine decided. No label upgraded.")
