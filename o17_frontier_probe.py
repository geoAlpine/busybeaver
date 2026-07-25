#!/usr/bin/env python3
"""o17 frontier probe (2026-07-25) — the ONE place today's exact frontier calculus touches (K).

o17's halt IS a left-frontier event (the head walks off the left edge of the written region).
`route_o17_locality.py` refuted bounded-window and periodic-in-j predicates for the family
C(3j) = 0^inf [A0] 1^(3j) 0^inf ("no modulus"). A FRONTIER-ADVANCE statistic is neither bounded-
window nor obviously periodic, so it is not strictly covered. ANALYSIS_2026-07-25.md section VI
said this deserves ONE firing under M0 before being dismissed. This is that firing.

Question: does any frontier statistic of C(3j) separate the halters from the non-halters?

No machine decided. No label upgraded.
"""
SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
def parse(spec):
    M=[]
    for st in spec.split('_'):
        row=[]
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0]=='-' else (int(t[0]), 1 if t[1]=='R' else -1, ord(t[2])-65))
        M.append(row)
    return M
M = parse(SPEC)

def run(k, maxsteps):
    SZ = 1 << 21; tape = bytearray(SZ); off = SZ//2
    pos = off; st = 0
    for i in range(k): tape[off+1+i] = 1
    lo = 0; hi = k                      # written-region frontiers, relative to off
    lext = 0                            # number of LEFT-frontier extensions
    rext = 0
    for step in range(1, maxsteps+1):
        r = tape[pos]
        if st == 5 and r == 0:          # F reads blank = HALT (left-frontier overflow)
            return ('HALT', step, lo, hi, lext, rext)
        w, d, st = M[st][r]
        tape[pos] = w; pos += d
        p = pos - off
        if p < lo: lo = p; lext += 1
        if p > hi: hi = p; rext += 1
    return ('RUN', maxsteps, lo, hi, lext, rext)

print("j    3j   fate            steps      leftfront  rightfront  L-ext  R-ext   L/steps")
H=[]; NH=[]
for j in range(1, 41):
    fate, steps, lo, hi, lext, rext = run(3*j, 6_000_000)
    (H if fate=='HALT' else NH).append(j)
    print(f"{j:<4} {3*j:<4} {fate:<14} {steps:<10} {lo:<10} {hi:<11} {lext:<6} {rext:<7} {lext/steps:.3e}")
print(f"\nhalters   : {H}")
print(f"non-halters: {NH}")
print("\nseparation test: does any of (leftfront, L-ext, L/steps) split the two classes?")
