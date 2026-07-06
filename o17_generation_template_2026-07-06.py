#!/usr/bin/env python3
"""
o17 generation-template test (2026-07-06).  [task 2 of the halt-flavor pin -- the o4 lens]

o4's decomposition: generation event-stream == prefix . body^r . suffix, with ONE prefix hash,
ONE body hash, THREE suffix hashes (class = G mod 3); only sweep lengths and r vary.
Question: does o17 admit the same rigid template?

Generation := one odometer tick (the right-end (E,0) reversal, o17_core_counter's atomic step).
Per generation we take the (state,read) event stream, collapse maximal runs of any repeated
cycle of period <= 6 into (cycle, count), and hash the SHAPE (tokens with counts stripped).
  - o4-like template  => O(1) distinct shapes, shape length bounded.
  - growing-string dynamics => #shapes grows with #generations, shape length grows.
[OBSERVED]; nothing about halting is claimed. No machine decided.
"""
import sys
from collections import Counter

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

def compress(ev):
    """Run-length compress: greedily collapse maximal repeats of period p<=6."""
    out = []
    i, n = 0, len(ev)
    while i < n:
        best_p, best_reps = 1, 1
        for p in range(1, 7):
            if i + 2 * p > n:
                break
            reps = 1
            while i + (reps + 1) * p <= n and ev[i + reps * p:i + (reps + 1) * p] == ev[i:i + p]:
                reps += 1
            if reps >= 2 and reps * p > best_reps * best_p:
                best_p, best_reps = p, reps
        if best_reps >= 2:
            out.append((tuple(ev[i:i + best_p]), best_reps))
            i += best_p * best_reps
        else:
            out.append((tuple(ev[i:i + 1]), 1))
            i += 1
    return out

def shape(tokens):
    return tuple(pat for pat, cnt in tokens)

def gen_streams(seed_L, maxsteps):
    """Yield per-generation event lists, generation = right-end tick."""
    SZ = 1 << 22
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, seed_L + 1):
        tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos; prevdir = 0
    cur = []
    gens = []
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            break
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            gens.append(cur); cur = []
        cur.append(st * 2 + r)
        prevdir = d
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return gens

def shape2(s1):
    """Second-level compression: tokens -> symbol ids -> compress again (template-of-templates)."""
    sym = {}
    seq = []
    for pat in s1:
        if pat not in sym:
            sym[pat] = len(sym)
        seq.append(sym[pat])
    return shape(compress(seq))

def analyze(name, seed_L, maxsteps):
    gens = gen_streams(seed_L, maxsteps)
    gens = gens[1:]  # drop the pre-first-tick startup
    shapes = []
    lens = []
    sh2 = set()
    for ev in gens:
        toks = compress(ev)
        shapes.append(shape(toks))
        lens.append(len(toks))
        sh2.add(shape2(shapes[-1]))
    distinct = len(set(shapes))
    print(f"== {name}: {len(gens)} generations (ticks) in {maxsteps} steps ==")
    print(f"   distinct compressed SHAPES: {distinct}  ({distinct}/{len(gens)} = "
          f"{distinct/max(1,len(gens)):.2f});  LEVEL-2 shapes: {len(sh2)}")
    print(f"   shape token-length: min={min(lens)}, max={max(lens)}, "
          f"first 20={lens[:20]}")
    qs = [lens[len(lens)*q//10] for q in range(1, 10)]
    print(f"   token-length deciles over generations: {qs}")
    # how often is a shape a REPEAT of an earlier one (o4: almost always)?
    seen = {}
    new_at = []
    for i, s in enumerate(shapes):
        if s not in seen:
            seen[s] = i
            new_at.append(i)
    print(f"   new-shape generation indices (first 25): {new_at[:25]}")
    print(f"   last new shape at generation {new_at[-1]} of {len(gens)}")
    # shape-frequency profile
    cnt = Counter(shapes)
    top = cnt.most_common(5)
    print(f"   top shape multiplicities: {[c for _, c in top]}")
    print()
    return distinct, len(gens)

if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    analyze("blank orbit", 0, cap)
    analyze("core seed L=9 (j=3, runner)", 9, cap)
    analyze("core seed L=15 (j=5, halter@794965)", 15, 900_000)
