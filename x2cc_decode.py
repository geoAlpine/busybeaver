#!/usr/bin/env python3
"""x2cc_decode.py -- CARRY CALCULUS step 1+2: decode the low-part register and derive the
carry-gap ledger.  Parses the milestone ledger produced by x2cc_ledger.py and fits every
milestone against the parameterized templates

  mature generation g (g >= 3), K = g+8, U = 1 0^6:
   M1(g): G=22  low = U^(g-1) T_g            big = 2^K-3 (g even) / 2^K-9 (g odd)
          where T_even = 1 0^10,  T_odd = 1 0^4 (1 0)^6
   M2(g): G=4   low = 1 0^18 U^(g-1) T_g     big = same          -> gap event L=18
   M3(g): G=2   low = 1^5 0^2 1 0^14 U^(g-1) T_g                 -> gap event L=10
                                             (+ L=6 event iff g even)
   M4(g): G=4   low = 1^13 0^2 (1^5 0^2)^j C big = big-4 (redistributed)
          with (j, C) = (2g'-?, ...) fitted per parity (see fit below)
   M5(g): G=1   low = (1 0)^3 1^11 0^2 (1^5 0^2)^j C
   M6(g): G=2   low = (1 0)^4 1^9 0^2 (1^5 0^2)^j C

and reports EXACT mismatch counts.  Also derives the predicted per-generation E-met gap
multiset and matches it against the observed GAP lines (and against route A's x2t_gen
observations).  Everything exact; no fuzz."""
import sys, re
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')


def parse_ledger(path):
    miles, gaps = [], []
    for line in open(path):
        if line.startswith('MILE'):
            m = re.match(r'MILE step=\s*(\d+) G=\s*(\d+) n2=\s*(\d+)\s+low=\[(.*)\]\s+big=1\^(\d+)', line)
            if m:
                step, G, n2, low, big = int(m[1]), int(m[2]), int(m[3]), m[4], int(m[5])
                miles.append((step, G, n2, parse_rle(low), big))
        elif line.startswith('GAP'):
            m = re.match(r'GAP\s+step=\s*(\d+) L=\s*(\d+)\s+ctx: (.*)', line)
            if m:
                gaps.append((int(m[1]), int(m[2]), m[3].strip()))
    return miles, gaps


def parse_rle(s):
    out = []
    for tok in s.split():
        if '^' in tok:
            c, n = tok.split('^')
            out.append((int(c), int(n)))
        else:
            out.append((int(tok), 1))
    return out


def U(n):  # (1 0^6)^n
    return [(1, 1), (0, 6)] * n


def comb(n):  # (1 0)^n
    return [(1, 1), (0, 1)] * n


def merge(runs):
    out = []
    for c, n in runs:
        if n == 0:
            continue
        if out and out[-1][0] == c:
            out[-1] = (c, out[-1][1] + n)
        else:
            out.append((c, n))
    return out


def template(g, phase):
    """expected (G, low, big) for milestone `phase` (1..6) of mature generation g."""
    K = g + 8
    even = (g % 2 == 0)
    T = [(1, 1), (0, 10)] if even else [(1, 1), (0, 4)] + comb(6)
    big1 = 2**K - 3 if even else 2**K - 9
    # after the M3->M4 front repack the register is rewritten as (1^5 0^2)^j and big loses 4
    ncell = 7 * (g - 1) + (11 if even else 17)   # cells in U^(g-1) T
    if phase == 1:
        return 22, merge(U(g - 1) + T), big1
    if phase == 2:
        return 4, merge([(1, 1), (0, 18)] + U(g - 1) + T), big1
    if phase == 3:
        return 2, merge([(1, 5), (0, 2), (1, 1), (0, 14)] + U(g - 1) + T), big1
    # phases 4-6: fitted forms (see observed ledger)
    j = g + 1 if even else g
    tail = [(1, 1), (0, 2)] if even else [(1, 1), (0, 1)] * 10
    big2 = big1 if even else big1 - 4
    if phase == 4:
        return 4, merge([(1, 13), (0, 2)] + [(1, 5), (0, 2)] * j + tail), big2
    if phase == 5:
        return 1, merge(comb(3) + [(1, 11), (0, 2)] + [(1, 5), (0, 2)] * j + tail), big2
    if phase == 6:
        return 2, merge(comb(4) + [(1, 9), (0, 2)] + [(1, 5), (0, 2)] * j + tail), big2


def main(path):
    miles, gaps = parse_ledger(path)
    # generations: group milestones in 6s starting from the first G=22 with mature form
    # find indices of G=22 milestones
    starts = [i for i, (_, G, _, _, _) in enumerate(miles) if G in (22, 26)]
    print(f"{len(miles)} milestones, {len(gaps)} gap events (L>=3), {len(starts)} generation starts")
    mism = 0
    checked = 0
    gen_of_step = []
    for si, i in enumerate(starts):
        block = miles[i:i + 6]
        if len(block) < 6:
            break
        big = block[0][4]
        # identify g from big: big = 2^K-3 or 2^K-9, K=g+8
        K = big.bit_length()
        g = K - 8
        expected_big = 2**K - 3 if g % 2 == 0 else 2**K - 9
        if big != expected_big or g < 3:
            print(f"  [gen big={big}: immature/transient, skipped]")
            continue
        gen_of_step.append((block[0][0], miles[i + 6][0] if i + 6 < len(miles) else None, g))
        for ph in range(1, 7):
            step, G, n2, low, b = block[ph - 1]
            eG, elow, ebig = template(g, ph)
            ok = (G == eG and low == elow and b == ebig)
            checked += 1
            if not ok:
                mism += 1
                print(f"  MISMATCH g={g} phase={ph} step={step}:")
                print(f"    got G={G} big={b} low={low}")
                print(f"    exp G={eG} big={ebig} low={elow}")
    print(f"\nTEMPLATE FIT: {checked} milestone configs checked, {mism} mismatches")

    # ---- derived vs observed gap multisets ----
    print("\nper-generation E-met gap multisets (L>=3):")
    allok = True
    for (s0, s1, g) in gen_of_step:
        if s1 is None:
            break
        obs = sorted(L for (st, L, _) in gaps if s0 <= st < s1)
        pred = sorted([18, 10] + ([6] if g % 2 == 0 else []))
        tag = "OK " if obs == pred else "MISMATCH"
        if obs != pred:
            allok = False
        print(f"  g={g:>2} (big=2^{g+8}-{3 if g%2==0 else 9}): observed {obs}  predicted {pred}  {tag}")
    print("\nGAP DERIVATION:", "EXACT MATCH every mature generation" if allok else "MISMATCHES PRESENT")


if __name__ == "__main__":
    main(sys.argv[1])
