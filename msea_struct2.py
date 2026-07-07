#!/usr/bin/env python3
"""
Mahler-sea survey — STRUCTURE stage v2 (2026-07-07).
Milestones = documented extreme+state events (CATALOGUE_IRREGULAR / CATALOGUE_O13_SN),
not raw gate triggers (those are mid-sweep reshuffles, the known wrong event).

Per machine:
  (1) template test: run-compressed shape classes (runs of equal small blocks -> 'v^rep',
      blocks>4 -> '*'); saturation = rigid-template-compatible. RLE-based, no period cap
      (Space Needle x5/2 sweeps included; the old period<=8 detector cap does not apply).
  (2) counter-law: correction distribution  c = m' - floor(p*m/q)  over consecutive
      designated generation events, for the documented p/q; clean law = few c values.
      Constant series excluded (m' == m pairs not counted as law hits).
  (3) outer-orbit sparsity: clean-collapse/reset events + times (tower-sparse axis).
All [OBSERVED]/[numeric-exact on stated generations]. Decides nothing.
"""
import sys
from collections import Counter

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

SN = "ABCDEF"

# name, spec, milestone_state (index), side ('L'/'R')
MILESTONES = [
    ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", 1, 'R'),  # R-extreme, state B
    ("o12", "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", 2, 'L'),  # L-extreme, state C
    ("o13", "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 2, 'L'),  # L-extreme, state C
    ("o14", "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 4, 'L'),  # L-extreme, state E
    ("o16", "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", 0, 'R'),  # R-extreme, state A
    ("SN",  "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", 0, 'L'),  # L-extreme, state A
]

def rle_blocks(tape, lo, hi):
    blocks = []
    i = lo
    while i <= hi:
        if tape[i]:
            j = i
            while j <= hi and tape[j]:
                j += 1
            blocks.append(j - i)
            i = j
        else:
            i += 1
    return blocks

def run_milestones(spec, mstate, side, N, max_snap=6000):
    M = parse(spec)
    SZ = 1 << 23
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    lo = hi = pos
    snaps = []
    last_rle = None
    step = 0
    while step < N:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            break
        at_ext = (pos <= lo) if side == 'L' else (pos >= hi)
        if st == mstate and at_ext and len(snaps) < max_snap:
            b = rle_blocks(tape, lo, hi)
            if b != last_rle:
                snaps.append((step, b))
                last_rle = list(b)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return snaps

def shape(blocks, T=4):
    """Run-compress: runs (>=3) of the same small value -> (v,'^'); blocks>T -> '*'."""
    toks = ['*' if b > T else b for b in blocks]
    out = []
    i = 0
    while i < len(toks):
        j = i
        while j < len(toks) and toks[j] == toks[i]:
            j += 1
        if j - i >= 3 and toks[i] != '*':
            out.append((toks[i], '^'))
        else:
            out.extend(toks[i:j])
        i = j
    return tuple(out)

def corr_dist(series, p, q, label):
    """Correction distribution c = m' - floor(p*m/q) over consecutive non-constant pairs."""
    cs = Counter()
    for i in range(len(series) - 1):
        m0, m1 = series[i], series[i + 1]
        if m0 >= 2 and m1 != m0:
            cs[m1 - (p * m0) // q] += 1
    tot = sum(cs.values())
    if tot == 0:
        print(f"    law[{label}] x{p}/{q}: no non-constant pairs")
        return
    top = cs.most_common(6)
    cover = sum(c for _, c in top[:3])
    print(f"    law[{label}] x{p}/{q}: corrections {dict(top)}  top-3 cover {cover}/{tot} ({100*cover/tot:.0f}%)")

def analyze(name, snaps):
    print(f"=== {name}: {len(snaps)} milestone snapshots (extreme+state, deduped)")
    if len(snaps) < 3:
        for s, b in snaps:
            print(f"    step {s}: {b}")
        return
    shapes = [shape(b) for _, b in snaps]
    seen, firsts = set(), []
    for i, sh in enumerate(shapes):
        if sh not in seen:
            seen.add(sh)
            firsts.append(i)
    half = len(shapes) // 2
    new_late = sum(1 for i in firsts if i >= half)
    verdict = "RIGID-template-compatible" if new_late == 0 else f"{new_late} new shapes in 2nd half"
    print(f"  shapes: {len(seen)} distinct / {len(shapes)} gens; {verdict}")
    for sh, ct in Counter(shapes).most_common(5):
        print(f"    x{ct:<6} {sh}")

    if name == "o11":
        # pattern [k] + [1]*m : sea count m, leading k
        gens = [(s, b[0], len(b) - 1) for s, b in snaps if len(b) >= 2 and b[0] > 1 and all(x == 1 for x in b[1:])]
        print(f"  clean [1^k 0 (10)^m] milestones: {len(gens)}")
        ms = [m for _, _, m in gens]
        ks = [k for _, k, _ in gens]
        print(f"    sea m head: {ms[:14]}  tail: {ms[-6:]}")
        corr_dist(ms, 3, 2, "sea m")
        dk = Counter(ks[i + 1] - ks[i] for i in range(len(ks) - 1))
        print(f"    leading k deltas: {dict(dk.most_common(6))}")
        col = [(s, b) for s, b in snaps if len(b) == 1]
        print(f"    pure-collapse [1^k] events: {[(s, b[0]) for s, b in col][:8]}")
    elif name in ("o12", "o13"):
        allm = [(s, b) for s, b in snaps if len(b) >= 2]
        # within-epoch: a -> a-2, b -> b+3
        da = Counter()
        for i in range(len(allm) - 1):
            b0, b1 = allm[i][1], allm[i + 1][1]
            if len(b0) >= 2 and len(b1) >= 2:
                da[(b1[0] - b0[0], b1[1] - b0[1])] += 1
        print(f"    within-epoch (da,db) top: {dict(da.most_common(5))}")
        subs = [(s, b[0]) for s, b in allm if len(b) >= 2 and b[1] == 4]
        aser = [a for _, a in subs]
        print(f"  sub-cycle starts (2nd block == 4): {len(subs)}; a head: {aser[:12]} tail: {aser[-4:]}")
        corr_dist(aser, 3, 2, "a-start")
        col = [(s, b[0]) for s, b in snaps if len(b) == 1]
        print(f"    pure-collapse [1^k] events: {col[:8]}")
    elif name == "o14":
        allm = [(s, b) for s, b in snaps if len(b) >= 2]
        subs = [(s, b[0]) for s, b in allm if len(b) >= 3 and b[1] == 7]
        aser = [a for _, a in subs]
        print(f"  sub-cycle starts (2nd block == 7): {len(subs)}; a head: {aser[:12]} tail: {aser[-4:]}")
        corr_dist(aser, 3, 2, "a-start")
        # marker tail census: last 3 blocks
        tails = Counter(tuple(b[-3:]) for _, b in allm)
        print(f"    marker-tail (last 3 blocks) census: {dict(tails.most_common(4))}")
    elif name == "o16":
        # pattern [k, ..., defect, sea of 1s]; k = first block
        ks = [b[0] for _, b in snaps if len(b) >= 2]
        dk = Counter(ks[i + 1] - ks[i] for i in range(len(ks) - 1))
        print(f"    leading k deltas: {dict(dk.most_common(6))}   k head: {ks[:12]} tail: {ks[-4:]}")
        # defect==4 milestones: sea = count of 1-blocks after the defect-4 position
        seas = []
        for s, b in snaps:
            if 4 in b[1:]:
                di = len(b) - 1 - b[::-1].index(4)
                tail = b[di + 1:]
                if tail and all(x == 1 for x in tail):
                    seas.append(len(tail))
        print(f"  defect-4 milestones: {len(seas)}; sea head: {seas[:12]} tail: {seas[-4:]}")
        corr_dist(seas, 3, 2, "sea")
    elif name == "SN":
        allm = [(s, b) for s, b in snaps if len(b) == 2]
        da = Counter()
        for i in range(len(allm) - 1):
            b0, b1 = allm[i][1], allm[i + 1][1]
            da[(b1[0] - b0[0], b1[1] - b0[1])] += 1
        print(f"    within-epoch (da,db) top on 2-block gens: {dict(da.most_common(5))}")
        resets = [(s, b[1]) for s, b in allm if b[0] == 1]
        bser = [b for _, b in resets]
        print(f"  clean resets [1,0,1^b]: {len(resets)}; b series: {bser}")
        corr_dist(bser, 5, 2, "reset b")
        print(f"    reset times: {[s for s, _ in resets]}")
    print()

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    for name, spec, ms, side in MILESTONES:
        snaps = run_milestones(spec, ms, side, N)
        analyze(name, snaps)
    print("STRUCTURE v2 [OBSERVED/numeric-exact on stated gens]. No machine decided. No label upgraded.")
