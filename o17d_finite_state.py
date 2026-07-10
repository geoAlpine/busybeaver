#!/usr/bin/env python3
"""
o17 DECISION ATTEMPT -- the FINITE-STATE-vs-VALUE crux, decided by test (2026-07-10).

The safety bit at a marker-5 gate is b(d) = F_mu(5, d) in {3 (safe), 8 (HALT)}.
THE question (ATTACK_PLAN B3 / O17_GATE_LAW s3): is b computed by a FINITE automaton
reading the digit vector d (-> the gate STATE is finite -> the branch sequence is
eventually periodic -> o17 DECIDABLE), or does it depend on the vector's ARITHMETIC /
deep structure (-> (K)-like, honest OPEN)?

Two sound tests over an exact ensemble (each b(d) is an exact finite TM run):

  TEST 1  SCALAR-MOD.  If b were a function of a scalar gate-VALUE N = sum d_i * base^i
          reduced mod M, then a residue automaton on N would decide it and the
          symbolic-mod tower extension would apply.  We test EVERY (base in 2..8,
          M in 2..64) -- an exhaustive sweep, far beyond the prior base-3-only check.

  TEST 2  MYHILL-NERODE.  If b is computed by ANY finite automaton reading d left->
          right, the number of Nerode classes (prefixes distinguished by some suffix)
          is FINITE and saturates.  We measure the class count as a function of prefix
          length.  GROWTH with length == no finite automaton == unbounded gate-state.

Nothing about halting is decided; all outputs are exact finite computations.
"""
import sys
from itertools import product
from collections import defaultdict

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else
                       (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)

def decode(tape, pos, hi):
    bl = []
    i = pos + 1
    while i <= hi:
        while i <= hi and tape[i] == 0:
            i += 1
        j = i
        while j <= hi and tape[j] == 1:
            j += 1
        if j > i:
            bl.append((i, j - i))
        i = j
    if not bl:
        return 0, []
    for (s1, l1), (s2, l2) in zip(bl, bl[1:]):
        if s2 - (s1 + l1) != 1:
            return None, None
    marker = bl[0][1]
    digs = []
    for _, l in bl[1:]:
        if l % 3 != 2:
            return None, None
        digs.append((l - 2) // 3)
    return marker, digs

def Fmu(mu, digs, cap=20_000_000):
    """Return next marker mu' in {3,5,8=HALT} or None if capped/off-language."""
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(14, (width * 8).bit_length())
    tape = bytearray(SZ)
    off = SZ // 3
    p = off + 1
    for i in range(mu):
        tape[p] = 1; p += 1
    for d in digs:
        p += 1
        for i in range(3 * d + 2):
            tape[p] = 1; p += 1
    pos = off; st = 0; step = 0; hi = p - 1
    L1 = off + 1
    while step < cap:
        r = tape[pos]
        if st == 5 and r == 0:
            return 8
        if step and st == 0 and r == 0 and pos < L1:
            mu2, d2 = decode(tape, pos, hi)
            return mu2
        ww, d, ns = M[st][r]
        if ww == 1:
            if pos < L1:
                L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0:
                q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
    return None

def main():
    # ------- build ensemble of marker-5 configs, record branch b in {3,8} -------
    maxlen = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    maxdig = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    print(f"=== ensemble: mu=5, lengths 1..{maxlen}, digits 0..{maxdig} ===")
    branch = {}   # tuple(d) -> b in {3,8}
    for m in range(1, maxlen + 1):
        for d in product(range(maxdig + 1), repeat=m):
            b = Fmu(5, list(d))
            if b in (3, 8):
                branch[d] = b
    n38 = sum(1 for v in branch.values() if v == 8)
    print(f"  configs: {len(branch)}  (HALT-branch mu'=8: {n38}, safe mu'=3: {len(branch)-n38})")
    print()

    # ------- TEST 1: scalar N = sum d_i base^i  mod M -------
    print("=== TEST 1: is b a function of a scalar N=sum d_i*base^i  mod M? ===")
    def Nval(d, base):
        return sum(x * base**i for i, x in enumerate(d))
    any_decides = False
    for base in range(2, 9):
        best = None
        for Mm in range(2, 65):
            g = defaultdict(set)
            for d, b in branch.items():
                g[Nval(d, base) % Mm].add(b)
            if all(len(v) == 1 for v in g.values()):
                best = Mm; break
        # also reversed digit order
        bestr = None
        for Mm in range(2, 65):
            g = defaultdict(set)
            for d, b in branch.items():
                g[Nval(tuple(reversed(d)), base) % Mm].add(b)
            if all(len(v) == 1 for v in g.values()):
                bestr = Mm; break
        msg = []
        msg.append(f"M={best}" if best else "none<=64")
        msg.append(f"rev M={bestr}" if bestr else "rev none<=64")
        if best or bestr: any_decides = True
        print(f"  base {base}: LSB-first {msg[0]:>10}   MSB-first {msg[1]}")
    print(f"  ANY scalar-mod residue decides b? {any_decides}")
    print("  (a 'none' means: no residue of N in that base mod any M<=64 determines the")
    print("   halt branch -> no scalar gate-value -> tower-exponent reduction has no target)")
    print()

    # ------- TEST 2: Myhill-Nerode class growth -------
    print("=== TEST 2: Myhill-Nerode -- does a finite automaton compute b? ===")
    # prefixes p (read left->right = marker side first), suffixes s appended.
    # b(p+s) probed over a fixed suffix battery; two prefixes equivalent iff identical
    # signatures.  Nerode-class count that GROWS with |p| == no finite automaton.
    suf_len = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    suf_dig = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    suffixes = []
    for sl in range(0, suf_len + 1):
        for s in product(range(suf_dig + 1), repeat=sl):
            suffixes.append(s)
    print(f"  suffix battery: {len(suffixes)} suffixes (len 0..{suf_len}, dig 0..{suf_dig})")
    cache = {}
    def bval(d):
        if d not in cache:
            cache[d] = Fmu(5, list(d))
        return cache[d]
    for plen in range(0, maxlen + 1):
        prefixes = [tuple(p) for p in product(range(maxdig + 1), repeat=plen)]
        sigs = {}
        classes = set()
        for p in prefixes:
            sig = tuple(bval(p + s) for s in suffixes)
            classes.add(sig)
        print(f"  |prefix|={plen}: {len(prefixes):>5} prefixes -> {len(classes):>5} Nerode classes")
    print()
    print("  READING: if the class count keeps GROWING with prefix length (does not")
    print("  saturate), b is NOT computed by any finite automaton over the digit vector")
    print("  -> the gate-state is genuinely unbounded -> value/arithmetic-dependent (K-like).")

if __name__ == "__main__":
    main()
