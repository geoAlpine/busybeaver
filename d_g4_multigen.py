#!/usr/bin/env python3
"""Consistent principal-ladder analysis for g=2,3,4.
Principal rung k = FIRST regenIn k in the phase; verify cascadeReg k at s_k+exitSteps(k);
gap(k)=s_{k+1}-(s_k+exitSteps(k)); head=s_5-M6(g); tail=M1(g+1)-cascadeReg_top."""
import x2t7_lib
x2t7_lib.SPAN = 1 << 18
x2t7_lib.ORIGIN = x2t7_lib.SPAN
from x2t7_lib import run, rle_right, ones_run_left

def exitSteps(k): return 2**(2*k-3) + k*2**(k-1) + 2**(k-2) + 2
def gaplaw(k):    return 4**k - 3*2**k + 7

def descCascade_blocks(d):
    out = [ (1 << (j + 2)) - 3 for j in range(d, 0, -1) ]
    out.append(1); return out
def match_descCascade(rle, start, dmax=11):
    for d in range(dmax, 0, -1):
        want = descCascade_blocks(d); ok, i = True, start
        for bi, blen in enumerate(want):
            if i >= len(rle) or rle[i][0] != 1 or rle[i][1] != blen:
                ok = False; break
            i += 1
            if bi < len(want) - 1:
                if i >= len(rle) or rle[i][0] != 0 or rle[i][1] != 2:
                    ok = False; break
                i += 1
        if ok: return d
    return None
def classify_full(pos, tape):
    rle = rle_right(tape, pos, limit=40000)
    if not rle: return None
    if rle[0] == (0, 1):
        d = match_descCascade(rle, 1)
        if d is not None:
            k = d + 4
            if ones_run_left(tape, pos) == (1 << k) - 3:
                return ("regenIn", k)
    if rle[0][0] == 0 and rle[0][1] == 3 and len(rle) > 2 and rle[1][0] == 1:
        blk = rle[1][1]; k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and k >= 4 and rle[2] == (0, 2):
            d = match_descCascade(rle, 3)
            if d is not None and d == k - 3:
                return ("cascadeReg", k)
    return None

def scan_phase(M6, M1next):
    firstReg, firstCasc = {}, {}
    def hook(step, st, pos, tape):
        if st != 4 or tape[pos] != 0: return
        if tape[pos+1] != 0: return
        b2 = tape[pos+2]
        if not (b2 == 1 or (b2 == 0 and tape[pos+3] == 0 and tape[pos+4] == 1)): return
        r = classify_full(pos, tape)
        if r is None: return
        kind, k = r
        if kind == "regenIn" and k not in firstReg: firstReg[k] = step
        if kind == "cascadeReg" and k not in firstCasc: firstCasc[k] = step
    run(M1next + 5, hook=hook, hook_from=M6)
    return firstReg, firstCasc

GENS = {
    2: (733076,  2852091),
    3: (2852510, 11329301),
    4: (11329720, 44986995),
}

for g in (2, 3, 4):
    M6, M1n = GENS[g]
    kmax = g + 9
    fR, fC = scan_phase(M6, M1n)
    print(f"\n########## g={g}  phase [{M6},{M1n}] len={M1n-M6}  ladder k=5..{kmax} ##########")
    print(f"{'k':>3} {'s_k(regenIn)':>13} {'cascadeReg':>12} {'exitSteps ok':>12} {'gap(k)':>12} {'law':>12} {'diff':>6}")
    covered = 0
    s = {}
    for k in range(5, kmax+1):
        s[k] = fR.get(k)
    for k in range(5, kmax+1):
        sk = fR.get(k); ck = fC.get(k)
        es = exitSteps(k)
        okexit = (ck is not None and sk is not None and ck - sk == es)
        covered += es
        if k < kmax and fR.get(k+1) is not None and ck is not None:
            gap = fR[k+1] - ck
            law = gaplaw(k)
            print(f"{k:>3} {sk:>13} {ck:>12} {str(okexit):>12} {gap:>12} {law:>12} {gap-law:>+6}")
        else:
            print(f"{k:>3} {sk:>13} {ck:>12} {str(okexit):>12} {'(top rung)':>12}")
    ctop = fC.get(kmax)
    s5 = fR.get(5)
    head = s5 - M6 if s5 else None
    tail = M1n - ctop if ctop else None
    print(f"head (M6->s_5) = {head}   tail (cascadeReg_top -> M1({g+1})) = {tail}")
    frac = covered / (M1n - M6)
    print(f"sum exitSteps (verified transports) = {covered}  coverage = {frac:.4%}")
