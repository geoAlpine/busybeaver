#!/usr/bin/env python3
"""D8 TEST 1 -- o4 run-cap R<=3 kill-test.

Odometer:  3G' = 4G + e(rho),  rho = G mod 3,  e = {0:9, 1:14, 2:1}
Ledger:    a'  = a + delta(rho),  delta = {1:-1, 2:+4, 0:+6}
Seed:      G_0 = 3, a_0 = 3  (template-regime milestone G=43 occurs at n=5)
W_n = G_n + 14.  Run-structure theorem (O4_RUN_STRUCTURE_2026-07-07 sec.1):
      maximal run of rho starting at G equals v_3(G - x_rho), x_1 = -14,
      so maximal rho=1 run starting at G_n is exactly v_3(W_n).

Fatal frequency condition: freq{rho=1} >= 4/5 in some prefix.
On the subshift {all rho=1 runs <= R} the exact max-mean cycle is R/(R+1).
R <= 3  =>  3/4 < 4/5  =>  o4 DECIDED non-halting.
So: does the real orbit ever produce a rho=1 run of length >= 4?
(Length >= 4 does NOT mean o4 halts; it only kills this sufficient condition.)
"""
import sys, time

E = {0: 9, 1: 14, 2: 1}
DELTA = {0: 6, 1: -1, 2: 4}

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
VALIDATE_UNTIL = 200_000


def v3(x):
    r = 0
    while x % 3 == 0:
        x //= 3
        r += 1
    return r


def main():
    t0 = time.time()
    G = 3
    a = 3
    # ---- anchors from O4_LEDGER_ANALYSIS_2026-07-06.md sec.5 ----
    anchors = {0: (3, 3, 0), 5: (43, 17, 1), 9: (151, 30, 1), 12: (367, 37, 1),
               20: (3727, 63, 1), 26: (20983, 90, 1), 31: (88462, 99, 1),
               36: (372814, 115, 1)}
    anchor_ok, anchor_bad = [], []

    run = 0
    maxrun = 0
    first_at = {}          # run length -> (generation where the run STARTS, G value)
    runstart = None
    hist = {}              # run length -> count of maximal runs of that length
    min_a_at_rho1 = None
    a40 = None
    thm_checked = 0
    thm_bad = 0
    checkpoints = []
    next_cp = 1000

    for n in range(N):
        rho = G % 3
        if n in anchors:
            g, aa, rr = anchors[n]
            (anchor_ok if (G == g and a == aa and rho == rr) else anchor_bad).append(
                (n, G, a, rho, g, aa, rr))
        if n == 40:
            a40 = a
        if rho == 1:
            if min_a_at_rho1 is None or a < min_a_at_rho1:
                min_a_at_rho1 = a
            if run == 0:
                runstart = n
                # closed-form cross-check: run length must equal v3(G+14)
                if n < VALIDATE_UNTIL:
                    thm_checked += 1
                    pred = v3(G + 14)
                    hist_pred = pred
            run += 1
        else:
            if run > 0:
                hist[run] = hist.get(run, 0) + 1
                if run not in first_at:
                    first_at[run] = (runstart, run)
                if run > maxrun:
                    maxrun = run
                if runstart is not None and runstart < VALIDATE_UNTIL:
                    if hist_pred != run:
                        thm_bad += 1
                run = 0
        a += DELTA[rho]
        G = (4 * G + E[rho]) // 3
        if n + 1 == next_cp:
            checkpoints.append((n + 1, maxrun, G.bit_length(), time.time() - t0))
            next_cp *= 10

    el = time.time() - t0
    print("=== D8 TEST 1: o4 rho=1 run cap ===")
    print(f"generations simulated N = {n+1}")
    print(f"final G bit-length      = {G.bit_length()}  (base-3 digits ~ {int(G.bit_length()*0.6309)})")
    print(f"final ledger a          = {a}")
    print(f"wall time               = {el:.1f} s")
    print()
    print("-- INSTRUMENT VALIDATION --")
    print(f"ledger/odometer anchors matched: {len(anchor_ok)}/{len(anchors)}")
    for r in anchor_ok:
        print(f"   OK  n={r[0]:3d} G={r[1]} a={r[2]} rho={r[3]}")
    for r in anchor_bad:
        print(f"   BAD n={r[0]:3d} got G={r[1]} a={r[2]} rho={r[3]} expected G={r[4]} a={r[5]} rho={r[6]}")
    print(f"a_40 = {a40} (doc records a_40 = 124)")
    print(f"min a at any rho=1 generation = {min_a_at_rho1} (doc: 9, at startup G=7)")
    print(f"run-structure closed form run == v3(G+14): checked {thm_checked} runs, "
          f"mismatches {thm_bad}")
    print()
    print("-- RUN STATISTICS --")
    print(f"MAX rho=1 run length observed = {maxrun}")
    for L in sorted(hist):
        fa = first_at[L][0]
        print(f"   run length {L}: count {hist[L]:>10}  first at generation n={fa}")
    for L in (3, 4, 5):
        if L in first_at:
            print(f"   >>> FIRST run of length {L}: generation n={first_at[L][0]}")
        else:
            print(f"   >>> NO run of length {L} in {n+1} generations")
    print()
    print("-- MAXRUN vs GENERATIONS --")
    print(f"{'N':>12} {'maxrun':>7} {'bits(G)':>9} {'sec':>8}")
    for cp in checkpoints:
        print(f"{cp[0]:>12} {cp[1]:>7} {cp[2]:>9} {cp[3]:>8.1f}")
    print(f"{n+1:>12} {maxrun:>7} {G.bit_length():>9} {el:>8.1f}")
    tot = sum(hist.values())
    ones = sum(L * c for L, c in hist.items())
    print()
    print(f"total maximal rho=1 runs = {tot}; total rho=1 steps = {ones}; "
          f"freq(rho=1) = {ones/(n+1):.6f}  (fatal threshold 0.8)")
    print(f"mean run length = {ones/tot:.4f}")
    print(f"unconditional cap (RUN_STRUCTURE sec.2): run at gen n <= 0.262n+O(1) "
          f"-> {0.262*(n+1):.0f} at N")


main()
