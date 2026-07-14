#!/usr/bin/env python3
"""x2cu_middle.py -- verify the carry MIDDLE build-up run is EXACTLY an instance of
the PROVEN outer_tick_noCarry_run (the ascending no-carry sweep), by extracting the
config cell-for-cell at the run boundaries and matching to Odo.toCfg.

outer_tick_noCarry_run n p t work M' R : from register <t, work+2n> with pow10 n
on the left comb, runSteps t n steps -> register <t+2n, work>, head p->p+2n.

toCfg <t,work> pos M R = <E, pos, ( ones(2t+1) ++ (false::M), false, ones work ++ (false::false::R) )>.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def cfg_at(n):
    sim = build(2); sim.step()
    while sim.n < n:
        assert sim.step()
    L = [sim.L[-1 - i] for i in range(len(sim.L))]   # nearest-first
    R = [sim.R[-1 - i] for i in range(len(sim.R))]   # nearest-first
    return sim.st, sim.pos, sim.h, L, R


def leading_ones(seq):
    i = 0
    while i < len(seq) and seq[i] == 1:
        i += 1
    return i, seq[i:]


def show(n, tag):
    st, pos, h, L, R = cfg_at(n)
    lo, Lrest = leading_ones(L)
    ro, Rrest = leading_ones(R)
    print(f"  {tag} n={n}: st={st} pos={pos} h={h}")
    print(f"      L: ones({lo}) then {Lrest[:12]}")
    print(f"      R: ones({ro}) then {Rrest[:14]}")
    return st, pos, h, L, R


def check_run(n0, n1, tag):
    print(f"=== {tag}: run n=[{n0},{n1}] ({n1-n0} steps) ===")
    st0, pos0, h0, L0, R0 = show(n0, "IN ")
    st1, pos1, h1, L1, R1 = show(n1, "OUT")
    # decode register from IN: left = ones(2t+1) ++ false :: M ; head E on 0 (h=0)
    lo0, Lr0 = leading_ones(L0)          # 2t+1
    lo1, Lr1 = leading_ones(L1)          # 2(t+2n)+1
    ro0, _ = leading_ones(R0)            # work + 2n  (working block incl.)
    ro1, _ = leading_ones(R1)            # work
    print(f"  left solid: {lo0} -> {lo1}  (delta {lo1-lo0})")
    print(f"  right block: {ro0} -> {ro1}  (delta {ro0-ro1})")
    print(f"  head pos: {pos0} -> {pos1}  (delta {pos1-pos0})")
    print(f"  head state/read IN: {st0}/{h0}  OUT: {st1}/{h1}")
    # infer t, n
    if lo0 % 2 == 1 and (lo1 - lo0) % 4 == 0:
        t = (lo0 - 1) // 2
        n = (lo1 - lo0) // 4
        from_runsteps = 4 * n * t + 4 * n * n + 6 * n
        print(f"  => matches outer_tick_noCarry_run with t={t}, n={n}: "
              f"runSteps={from_runsteps} (actual {n1-n0}) "
              f"{'OK' if from_runsteps == n1-n0 else 'MISMATCH'}")
        # comb consumed on left must be pow10 n right after the ones block
        comb = Lr0[:2 * n]
        print(f"  comb after solid block (should be (10)^{n} = {[1,0]*n}): {comb}  "
              f"{'OK' if comb == [1,0]*n else 'NO'}")
        print(f"  left tail after comb (M'): {Lr0[2*n:2*n+8]}")
        print(f"  left tail OUT after solid (M'): {Lr1[:8]}  "
              f"{'MATCH' if Lr0[2*n:] == Lr1 else 'DIFF'}")
        print(f"  right OUT after work block: {R1[ro1:ro1+10]}")
        print(f"  right IN  after work block: {R0[ro0:ro0+10]}")


if __name__ == "__main__":
    # C4 MIDDLE build-up run: 6717 -> 6821 (t=1..7, n=4)
    check_run(6717, 6821, "C4 MIDDLE ascending no-carry run")
    print()
    # C5 MIDDLE build-up run: 7150 -> 7846 (should be t=1.., big n)
    check_run(7150, 7846, "C5 MIDDLE ascending no-carry run")
