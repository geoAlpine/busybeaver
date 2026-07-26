#!/usr/bin/env python3
"""
o4 a-ledger measurement (exact big-int), cross-checked against the Lean defs
in lean/Suffix.lean (cOdo, ledgerNext) and lean/Completion.lean (Gseq, aseq).

Gseq:  G0 = 43,  G_{n+1} = 4*G_n//3 + cOdo(G_n)
cOdo:  G%3==0 -> 3 ; G%3==1 -> 5 ; G%3==2 -> 1
aseq:  a0 = 18,  a_{n+1} = ledgerNext(G_n, a_n)
ledgerNext: G%3==1 -> a-1 (DRAIN) ; G%3==2 -> a+4 ; G%3==0 -> a+6
Conjecture o4_ledger: for all n, aseq n >= 1.
"""
import sys

def cOdo(G):
    r = G % 3
    return 3 if r == 0 else (5 if r == 1 else 1)

def deltaLedger(G):
    r = G % 3
    return -1 if r == 1 else (4 if r == 2 else 6)

def run(N):
    G = 43
    a = 18
    minA = a
    argmin = 0
    # residue counts of G mod 3
    c0 = c1 = c2 = 0
    # drain / refill totals
    drain = 0   # count of G%3==1 steps
    refill4 = 0 # G%3==2
    refill6 = 0 # G%3==0
    # run-length statistics of consecutive drain (G%3==1) steps
    cur_run = 0
    max_run = 0
    run_hist = {}
    # excursion / running-min tracking: track downward excursions of a
    running_max = a
    max_drawdown = 0  # max (running_max - a) so far
    for n in range(N):
        r = G % 3
        if r == 0: c0 += 1; refill6 += 1
        elif r == 1: c1 += 1; drain += 1
        else: c2 += 1; refill4 += 1
        # run of drains
        if r == 1:
            cur_run += 1
        else:
            if cur_run > 0:
                run_hist[cur_run] = run_hist.get(cur_run, 0) + 1
                if cur_run > max_run: max_run = cur_run
            cur_run = 0
        d = deltaLedger(G)
        a_next = a + d
        G = 4 * G // 3 + cOdo(G)
        a = a_next
        if a < minA:
            minA = a; argmin = n + 1
        if a > running_max: running_max = a
        dd = running_max - a
        if dd > max_drawdown: max_drawdown = dd
    if cur_run > 0:
        run_hist[cur_run] = run_hist.get(cur_run, 0) + 1
        if cur_run > max_run: max_run = cur_run
    tot = c0 + c1 + c2
    return dict(N=N, G_final_bits=G.bit_length(), a_final=a, minA=minA, argmin=argmin,
               c0=c0, c1=c1, c2=c2, f0=c0/tot, f1=c1/tot, f2=c2/tot,
               drift=(-drain + 4*refill4 + 6*refill6)/tot,
               max_run=max_run, run_hist=run_hist, max_drawdown=max_drawdown)

if __name__ == "__main__":
    for N in [1000, 10000, 100000, 1000000]:
        s = run(N)
        print(f"N={s['N']:>8}  minA={s['minA']:>4} @n={s['argmin']:<8} a_final(bits~{s['G_final_bits']})")
        print(f"          f0(G%3=0,+6)={s['f0']:.5f} f1(G%3=1,-1 DRAIN)={s['f1']:.5f} f2(G%3=2,+4)={s['f2']:.5f}")
        print(f"          drift/step={s['drift']:.5f}  max drain-run={s['max_run']}  max_drawdown={s['max_drawdown']}")
        # tail of drain-run histogram
        rh = s['run_hist']
        print(f"          drain-run hist (len:count) = { {k: rh[k] for k in sorted(rh)} }")
        print()
