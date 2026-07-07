#!/usr/bin/env python3
"""
o17 regularity test for the milestone map F (2026-07-07).

QUESTION (the formulation question): is the branch mu' = F_mu(mu, d) a REGULAR
predicate of the digit string -- i.e. a function of the residue word (d_i mod q)
-- and is the excursion tick count T a WEIGHTED-AUTOMATON value (affine in each
digit within a residue class)?

Every F evaluation is an exact finite TM run ([PROVEN] per value); the regularity
conclusion is [OBSERVED on the stated ensemble].  Nothing decided.
"""
import sys, random
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

def F(mu, digs, cap=100_000_000):
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(15, (width * 16).bit_length())
    tape = bytearray(SZ)
    off = SZ // 3
    p = off + 1
    for i in range(mu):
        tape[p] = 1; p += 1
    for d in digs:
        p += 1
        for i in range(3 * d + 2):
            tape[p] = 1; p += 1
    pos = off; st = 0; step = 0; hi = p - 1; prevdir = 0
    n = 0
    L1 = off + 1
    while step < cap:
        r = tape[pos]
        if st == 5 and r == 0:
            return dict(kind='HALT', steps=step, ticks=n, mu=8, digs=None)
        if step and st == 0 and r == 0 and pos < L1:
            # decode
            bl = []
            i = pos + 1
            while i <= hi:
                while i <= hi and tape[i] == 0: i += 1
                j = i
                while j <= hi and tape[j] == 1: j += 1
                if j > i: bl.append(j - i)
                i = j
            mu2 = bl[0] if bl else 0
            d2 = [(x - 2) // 3 for x in bl[1:]]
            return dict(kind='M', steps=step, ticks=n, mu=mu2, digs=d2)
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
        prevdir = d
        if ww == 1:
            if pos < L1: L1 = pos
        elif ww == 0 and pos == L1:
            q = pos + 1
            while q <= hi and tape[q] == 0: q += 1
            L1 = q if q <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < hi + 1 and pos > hi: pass
        if pos > hi: hi = pos
    return dict(kind='CAP', steps=step, ticks=n, mu=None, digs=None)

CACHE = {}
def Fc(mu, digs):
    k = (mu, tuple(digs))
    if k not in CACHE:
        CACHE[k] = F(mu, list(digs))
    return CACHE[k]

def main():
    random.seed(20260707)
    # ---------- ensemble ----------
    ens = []
    for d1 in range(18):
        ens.append([d1])
    for digs in product(range(12), repeat=2):
        ens.append(list(digs))
    for digs in product(range(9), repeat=3):
        ens.append(list(digs))
    for digs in product(range(6), repeat=4):
        ens.append(list(digs))
    print(f"ensemble size {len(ens)} vectors x 2 markers")
    data = []
    for mu0 in (3, 5):
        for digs in ens:
            r = Fc(mu0, digs)
            data.append((mu0, tuple(digs), r))
    ncap = sum(1 for _, _, r in data if r['kind'] == 'CAP')
    print(f"evaluated {len(data)} (CAP: {ncap})")
    print()

    # ---------- (A) branch = f(residue word)? ----------
    print("=== (A) branch mu' as a function of the residue word (d_i mod q) ===")
    for q in (2, 3, 6, 12):
        bad = 0; classes = defaultdict(set)
        for mu0, d0, r in data:
            if r['kind'] == 'CAP': continue
            classes[(mu0, len(d0), tuple(x % q for x in d0))].add(r['mu'])
        nbad = sum(1 for v in classes.values() if len(v) > 1)
        print(f"  q={q:>2}: {len(classes)} classes, ambiguous: {nbad}"
              + ("   <-- DECIDES" if nbad == 0 else ""))
        if q == 6 and nbad:
            ex = [(k, sorted(v)) for k, v in classes.items() if len(v) > 1][:6]
            for k, v in ex:
                print(f"        clash {k} -> {v}")
    print()

    # ---------- (B) +6-shift affine test for T (and branch constancy) ----------
    print("=== (B) shift test: d_i -> d_i + 6k, k=0..3: branch constant? T affine in k? ===")
    bases = []
    for _ in range(50):
        m = random.randint(1, 5)
        bases.append([random.randint(0, 7) for _ in range(m)])
    bases += [[0], [1], [0, 2], [2, 0, 4], [0, 0, 2, 2, 6], [0, 2, 0, 0, 0, 0, 0, 4]]
    n_tests = n_branch_ok = n_affine_ok = 0
    slope_by_class = defaultdict(set)
    for mu0 in (3, 5):
        for base in bases:
            for i in range(len(base)):
                seq = []
                ok = True
                for k in range(4):
                    d = list(base); d[i] += 6 * k
                    r = Fc(mu0, d)
                    if r['kind'] == 'CAP': ok = False; break
                    seq.append(r)
                if not ok: continue
                n_tests += 1
                mus = {r['mu'] for r in seq}
                if len(mus) == 1: n_branch_ok += 1
                Ts = [r['ticks'] for r in seq]
                d2 = [Ts[k+2] - 2*Ts[k+1] + Ts[k] for k in range(2)]
                if d2 == [0, 0]:
                    n_affine_ok += 1
                    slope = Ts[1] - Ts[0]
                    cls = (mu0, len(base), tuple(x % 6 for x in base), i)
                    slope_by_class[cls].add(slope)
                else:
                    print(f"    NOT AFFINE: mu={mu0} base={base} coord {i}: T={Ts}  mu'={[r['mu'] for r in seq]}")
                if len(mus) != 1:
                    print(f"    BRANCH VARIES: mu={mu0} base={base} coord {i}: mu'={[r['mu'] for r in seq]}  T={Ts}")
    print(f"  shift tests: {n_tests}; branch constant along +6 shifts: {n_branch_ok}; T affine in shift: {n_affine_ok}")
    multi = {k: v for k, v in slope_by_class.items() if len(v) > 1}
    print(f"  slope well-defined per (mu, m, residue word, coord): {'YES' if not multi else f'no ({len(multi)} clashes)'}")
    print()

    # ---------- (C) steps affine too? ----------
    print("=== (C) same shift test for STEPS (the physical gate-time increment) ===")
    n_aff = n_tot = 0
    for mu0 in (3, 5):
        for base in bases[:25]:
            for i in range(len(base)):
                seq = []
                ok = True
                for k in range(4):
                    d = list(base); d[i] += 6 * k
                    r = Fc(mu0, d)
                    if r['kind'] == 'CAP': ok = False; break
                    seq.append(r['steps'])
                if not ok: continue
                n_tot += 1
                d2 = [seq[k+2] - 2*seq[k+1] + seq[k] for k in range(2)]
                if d2 == [0, 0]: n_aff += 1
                else: print(f"    steps not affine: mu={mu0} base={base} i={i}: {seq}")
    print(f"  steps affine along +6 shifts: {n_aff}/{n_tot}")
    print()

    # ---------- (D) next digit VECTOR class: is residue word of output a function too? ----------
    print("=== (D) is the OUTPUT residue word (mu', d' mod 6, m') a function of the input class? ===")
    classes = defaultdict(set)
    for mu0, d0, r in data:
        if r['kind'] != 'M': continue
        out = (r['mu'], len(r['digs']), tuple(x % 6 for x in r['digs']))
        classes[(mu0, len(d0), tuple(x % 6 for x in d0))].add(out)
    nbad = sum(1 for v in classes.values() if len(v) > 1)
    print(f"  classes: {len(classes)}, output-class ambiguous: {nbad}"
          + ("   <-- CLOSED: F descends to a map on residue words!" if nbad == 0 else ""))
    if nbad:
        ex = [(k, sorted(v)[:3]) for k, v in classes.items() if len(v) > 1][:8]
        for k, v in ex:
            print(f"    clash {k} -> {v}")

if __name__ == "__main__":
    main()
