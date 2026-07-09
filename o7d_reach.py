#!/usr/bin/env python3
"""o7d_reach.py -- SOUND forward-reachable-set automaton for o7 at the MILESTONE level.

State: (u mod M, b mod M),  M = 2^J * m,  u := a+3.
Transitions (from the raw-TM-verified milestone automaton), with every /2 handled by the
2-adic 2-way lift  x/2 -> {x/2, x/2 + M/2}  (SOUND: the true value is always included; the
low J bits of u are tracked exactly => this is the depth-J parity look-ahead).

  u odd  (a even, EVEN branch):  t=(3u-1) mod M;  u' in half(t) + b ;  b'=1
  u even (a odd,  ODD branch):   for h in half(u):  u'=h, b'=(b+h+1) mod M
  u==6 mod M  (possible a=3):    ALSO include special  u'=(b+8), b'=1+(b%2)   [over-approx]
  u==4 mod M  (possible a=1):    HALT-consistent residue (u=4 is a power of 2, in H_M)

HALT <=> u = 2^k (k>=2).  H_M = { 2^k mod M : k>=2 }.
DECISION: if the u-projection of the reachable closure R_M avoids H_M entirely => o7 NON-HALT
[PROVEN given the automaton].  Otherwise report the halt-consistent residue that is reached.
"""
import sys
from collections import deque

def powers_of_two_mod(M):
    """All residues 2^k mod M, k>=2 (eventually periodic)."""
    s = set(); x = 4 % M; seen = set()
    k = 2
    while (x, k if k < 64 else -1) not in seen:
        # collect until the 2^k mod M sequence cycles
        s.add(x)
        # detect cycle on value once k is past the 2-adic part
        key = x
        if key in seen and k > M.bit_length() + 64:
            break
        seen.add(key)
        x = (x * 2) % M
        k += 1
        if k > M.bit_length() + 4 * M.bit_length() + 200:
            break
    return s

def reach(J, m, cap=60_000_000, verbose=True):
    M = 2 ** J * m
    half_off = M // 2
    H = powers_of_two_mod(M)
    # seed: real orbit start (a=2,b=2) -> u=5, b=2
    start = (5 % M, 2 % M)
    seen = {start}
    dq = deque([start])
    uproj = set()
    hit_residue = None
    steps = 0
    while dq:
        u, b = dq.popleft()
        uproj.add(u)
        if u in H and hit_residue is None:
            hit_residue = u
            # not a proof of halt (over-approx) -- just: no separation at this M
            break
        succ = []
        if u % 2 == 1:
            # EVEN branch
            t = (3 * u - 1) % M
            h0 = t // 2
            for h in (h0, (h0 + half_off) % M):
                succ.append(((h + b) % M, 1))
        else:
            # ODD branch (halving)
            h0 = u // 2
            for h in (h0, (h0 + half_off) % M):
                succ.append((h, (b + h + 1) % M))
            # possible a=3 special (u could be exactly 6): over-approximate by ALSO adding it
            if u % M == 6 % M:
                succ.append(((b + 8) % M, (1 + (b % 2)) % M))
        for s in succ:
            if s not in seen:
                seen.add(s); dq.append(s)
        steps += 1
        if len(seen) > cap:
            if verbose: print(f"  [cap {cap} hit; treating as FULL/no-separation]")
            hit_residue = 'CAP'
            break
    Hu = H & uproj
    return {
        'M': M, 'J': J, 'm': m,
        'nstates': len(seen), 'nuproj': len(uproj),
        'nH': len(H), 'Hu_size': len(Hu),
        'hit_residue': hit_residue,
        'separated': (hit_residue is None) and (len(Hu) == 0),
        'sampleHu': sorted(Hu)[:8],
    }

if __name__ == "__main__":
    ms = [1, 3, 5, 7]
    if len(sys.argv) > 1:
        # o7d_reach.py J m
        J = int(sys.argv[1]); m = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        r = reach(J, m)
        print(r)
    else:
        print(f"{'M':>12} {'J':>3} {'m':>3} {'states':>12} {'uproj':>10} {'|H|':>6} {'|Hu|':>6} {'sep?':>6}  note")
        for m in ms:
            for J in range(1, 15):
                r = reach(J, m, verbose=False)
                note = ''
                if r['hit_residue'] == 'CAP': note = 'CAP(full)'
                elif r['separated']: note = '*** SEPARATED ***'
                elif r['hit_residue'] is not None: note = f"halt-res {r['hit_residue']} reached"
                print(f"{r['M']:>12} {J:>3} {m:>3} {r['nstates']:>12} {r['nuproj']:>10} "
                      f"{r['nH']:>6} {r['Hu_size']:>6} {str(r['separated']):>6}  {note}")
                if r['nstates'] > 30_000_000:
                    break
        print("No machine decided (until a SEPARATED row is verified three ways).")
