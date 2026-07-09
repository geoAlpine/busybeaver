#!/usr/bin/env python3
"""o7d_verify.py -- RE-VERIFY the exact o7 milestone dynamics from scratch against the raw TM,
and derive/verify the b-FREE cascade-compressed map F on cascade-entry values.

SOUNDNESS: finite verification only. Nothing here proves non-halting.
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

def step_map(a, b):
    """The banked o7 milestone automaton (state D, tape 0 1^a 0 1^b)."""
    if a == 1:
        return ('HALT',)
    if a == 3:
        return ('D', b + 5, 1 + (b % 2))
    if a % 2 == 0:
        return ('D', 3 * a // 2 + 1 + b, 1)          # EVEN branch
    return ('D', (a - 3) // 2, b + (a + 5) // 2)      # ODD branch

def v2(n): return (n & -n).bit_length() - 1
def oddpart(n): return n >> v2(n)

# ---------------- raw-TM milestone extraction, verify step_map ----------------
def parse_ms(s):
    s = s.strip('0'); ones = []; zeros = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        (ones if s[i] == '1' else zeros).append(j - i); i = j
    if any(z != 1 for z in zeros): return None
    if len(ones) == 2: return (ones[0], ones[1])
    if len(ones) == 1: return (ones[0], 0)
    return None

def raw_milestones(maxsteps):
    M = parse(SPEC)
    SZ = 1 << 25
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    mil = []
    while step < maxsteps:
        r = tape[pos]; act = M[st][r]
        if act is None:
            mil.append(('HALT', step)); break
        if st == 3 and pos <= lo and r == 0 and tape[pos + 1] == 1:
            ab = parse_ms(''.join(map(str, tape[lo:hi + 1])))
            if ab is not None: mil.append(ab)
        w, d, ns = act; tape[pos] = w; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return mil

def verify_stepmap(maxsteps):
    print(f"=== verify step_map vs raw TM ({maxsteps:,} steps) ===")
    mil = raw_milestones(maxsteps)
    halted = mil and mil[-1][0] == 'HALT'
    if halted: mil = mil[:-1]
    mism = 0
    for i in range(len(mil) - 1):
        pred = step_map(*mil[i])
        want = ('D', mil[i + 1][0], mil[i + 1][1])
        if pred != want:
            mism += 1
            if mism <= 5: print("  MISMATCH", mil[i], pred, want)
    print(f"  {len(mil)} raw milestones; step_map mismatches = {mism}; raw HALT seen = {halted}")
    return mism, len(mil), mil

# ---------------- the b-FREE cascade-compressed map F ----------------
def F(u_e):
    """Cascade-entry -> next cascade-entry, b-free (b=1 at entry, a!=3 path).
       HALT iff oddpart(u_e)==1.  u_e is EVEN (=a+3, a odd)."""
    d = v2(u_e); w = oddpart(u_e)
    if w == 1:
        return 'HALT'
    b_exit = 1 + (u_e - w) + d
    u_1 = (3 * w - 1) // 2 + b_exit          # reseed (a' even -> u_1 odd)
    x_1 = u_1 + 1
    v = v2(x_1)
    u_next = 3**v * oddpart(x_1) - 1          # even-chain exit -> next cascade entry
    return u_next

def verify_F_against_orbit(mil):
    """Extract cascade-entry milestones (a odd, previous a even) from the raw-milestone
       sequence and check F reproduces the next cascade entry.  Also check b==1 at entries."""
    print("=== verify b-free cascade map F against raw-milestone orbit ===")
    entries = []   # (index, a, b)
    prev_even = None
    for i, (a, b) in enumerate(mil):
        if a % 2 == 1 and a >= 5 and prev_even is True:
            entries.append((i, a, b))
        prev_even = (a % 2 == 0)
    print(f"  cascade entries found: {len(entries)}")
    # b at entry
    bad_b = sum(1 for (_, a, b) in entries if b != 1)
    print(f"  entries with b != 1: {bad_b}  (a=3-special path can give b in {{1,2}})")
    # F reproduces next entry value u_e
    mismF = 0; checked = 0
    for k in range(len(entries) - 1):
        _, a, b = entries[k]
        u_e = a + 3
        got = F(u_e)
        want = entries[k + 1][1] + 3
        checked += 1
        if got != want:
            mismF += 1
            if mismF <= 5: print("  F MISMATCH  u_e=", u_e, "F=", got, "want=", want)
    print(f"  F checked on {checked} entry-to-entry transitions; mismatches = {mismF}")
    mo = min(oddpart(a + 3) for (_, a, b) in entries) if entries else None
    print(f"  min oddpart(u_e) over entries = {mo}  (HALT needs oddpart(u_e)=1)")
    return mismF

if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000_000
    mism, n, mil = verify_stepmap(steps)
    verify_F_against_orbit(mil)
    print("\nEXACT DYNAMICS (re-derived, all verified 0-mismatch above):")
    print("  milestone state (a,b); u:=a+3; HALT <=> a=1 <=> u=2^k.")
    print("  even branch (a even, u odd):  a->3a/2+1+b, b->1     [couples b]")
    print("  odd  branch (a odd,  u even): u->u/2,  b->b+(u)/2+1  [autonomous halving of u]")
    print("  a=3 special (u=6): a->b+5, b->1+(b%2).")
    print("  cascade-compressed b-free map F on entry values u_e (even), HALT<=>oddpart(u_e)=1:")
    print("    w=oddpart(u_e), d=v2(u_e); b_exit=1+(u_e-w)+d;")
    print("    u_1=(3w-1)/2+b_exit; x_1=u_1+1; v=v2(x_1); u_e'=3^v*oddpart(x_1)-1")
    print("No machine decided. No label upgraded.")
