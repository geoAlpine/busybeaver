#!/usr/bin/env python3
"""o7d_reach_odd.py -- complementary SOUND reachable-set model for o7, on the b-free cascade
map F, reduced modulo an ODD modulus m.

F(u_e): w=oddpart(u_e), d=v2(u_e); b_exit=1+(u_e-w)+d; u_1=(3w-1)/2+b_exit; x_1=u_1+1;
        v=v2(x_1); u_e' = 3^v * oddpart(x_1) - 1.   HALT <=> w==1.

Mod an odd m, 2 and 3 are invertible.  The 2-adic valuations d=v2(u_e), v=v2(x_1) are
INDEPENDENT of u_e mod m, so we SOUNDLY over-approximate by enumerating every residue class of
d (period Pd = lcm(ord_m 2, m)) and of v (period Pv = lcm(ord_m 2, ord_m 3)).  The true (d,v)
are always among those enumerated => the closure R_m is a sound superset of the real cascade-entry
residues.  H_m = {2^k mod m}.  If R_m avoids H_m => o7 NON-HALT [PROVEN given the automaton].
"""
import sys
from math import gcd
from collections import deque

def multiorder(a, m):
    a %= m
    if gcd(a, m) != 1: return None
    o = 1; x = a % m
    while x != 1:
        x = (x * a) % m; o += 1
        if o > m + 1: return None
    return o

def lcm(a, b): return a * b // gcd(a, b)

def seq_period(base, m):
    """(preperiod, period) of base^v mod m for v>=0 (handles base not coprime to m)."""
    seen = {}; x = 1 % m; v = 0
    while x not in seen:
        seen[x] = v; x = (x * base) % m; v += 1
    return seen[x], v - seen[x]

def reach_odd(m):
    assert m % 2 == 1
    inv2 = pow(2, -1, m)
    o2 = multiorder(2, m)                    # 2 coprime to odd m => always defined
    pp3, per3 = seq_period(3, m)             # 3^v may be non-invertible if 3|m
    Pd = lcm(o2, m)                          # d mod ord_m(2) (for w) and d mod m (additive b_exit)
    Pv = pp3 + lcm(o2, per3) + 1             # covers inv2^v (period o2) and 3^v (eventual)
    inv2_pows = [pow(inv2, d, m) for d in range(max(Pd, Pv) + 2)]
    three_pows = [pow(3, v, m) for v in range(Pv + 2)]
    H = set(pow(2, k, m) for k in range(2, 2 + o2 + 2))   # {2^k mod m}
    # seed: first real cascade entry u_e = 14
    seed = 14 % m
    seen = {seed}; dq = deque([seed])
    while dq:
        r = dq.popleft()
        for d in range(1, Pd + 1):
            w = (r * inv2_pows[d]) % m                 # oddpart(u_e) mod m
            if w % m == 1 % m:
                continue  # w==1 residue = HALT-consistent; not a forward successor
            b_exit = (1 + (r - w) + d) % m
            u1 = ((3 * w - 1) * inv2 + b_exit) % m
            x1 = (u1 + 1) % m
            for v in range(1, Pv + 1):
                oddx = (x1 * inv2_pows[v]) % m
                un = (three_pows[v] * oddx - 1) % m
                if un not in seen:
                    seen.add(un); dq.append(un)
    Hu = H & seen
    return {'m': m, 'o2': o2, 'o3': None, 'Pd': Pd, 'Pv': Pv,
            'nreach': len(seen), 'nH': len(H), 'Hu': len(Hu),
            'separated': len(Hu) == 0, 'reach_is_full': len(seen) == m}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(reach_odd(int(sys.argv[1]))); sys.exit()
    print(f"{'m':>7} {'ord2':>5} {'Pd':>7} {'Pv':>7} {'|R_m|':>8} {'m':>7} {'|H|':>5} {'|Hu|':>5} {'sep?':>6}")
    for m in [3,5,7,9,11,13,15,17,19,21,23,25,27,31,33,35,45,49,63,81,99,121,125,127,243,729]:
        try:
            r = reach_odd(m)
        except Exception as e:
            print(f"{m:>7}  err {e}"); continue
        tag = '*** SEPARATED ***' if r['separated'] else ('FULL' if r['reach_is_full'] else 'proper-but-hits-H')
        print(f"{m:>7} {r['o2']:>5} {r['Pd']:>7} {r['Pv']:>7} {r['nreach']:>8} {m:>7} "
              f"{r['nH']:>5} {r['Hu']:>5} {str(r['separated']):>6}   {tag}")
    print("No machine decided (until a SEPARATED row appears and is verified).")
