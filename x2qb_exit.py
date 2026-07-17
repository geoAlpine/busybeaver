#!/usr/bin/env python3
"""x2qb_exit.py -- MEASURE the TOPGRIND's Theta(2^a) doubling EXIT, a=5 and a=6.

SIMULATOR EVIDENCE (not a Lean theorem).  Locates the exit window, verifies the
braidCfg core endpoint bit-for-bit, then dumps the exit trace so the a-parametric
growth law can be read off and separated from the fixed part.

Predicted accounting (from lean/X2.lean §5ae):
  topGrindSteps a = 4^a - 3*2^a + 7 = entry(7) + braidRunSteps 0 N + exit(a)
  with N = 2^{a-1} - 2, braidRunSteps 0 N = 4N^2+6N, exit(a) = 2^{a+1} - 4.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def pow10(k): return [1, 0] * k
def ones(k):  return [1] * k

def runs(bits, k=14):
    out = []; i = 0
    while i < len(bits) and len(out) < k:
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b: j += 1
        out.append((b, j - i)); i = j
    return out

def left_nf(sim):  return sim.L[::-1]
def right_nf(sim): return sim.R[::-1]

def check_braidcfg(sim, r, Lc, blk, label):
    """Lean: <E, p, <pow10 Lc ++ marker, false, pow10(2r+1) ++ ones blk ++ 0::0::casc>>"""
    ok = (sim.st == 'E' and sim.h == 0)
    right = right_nf(sim); left = left_nf(sim)
    pref = pow10(2 * r + 1) + ones(blk) + [0, 0]
    ok_r = right[:len(pref)] == pref
    ok_l = left[:2 * Lc] == pow10(Lc)
    lmax = left[2 * Lc:2 * Lc + 2] != [1, 0]          # Lc maximal => unambiguous
    rmax = right[len(pref):len(pref) + 1] != [1] or blk == 0  # blk maximal
    good = ok and ok_r and ok_l and lmax
    print(f"  {label} step={sim.n}: braidCfg r={r} Lc={Lc} blk={blk} -> "
          f"E-on-0={ok} right={ok_r} leftcomb={ok_l} Lc-max={lmax}  ==> {good}")
    return good

def topgrind(a):
    N = 2 ** (a - 1) - 2
    return dict(a=a, N=N, entry=7, core=4 * N * N + 6 * N,
                exit=2 ** (a + 1) - 4, total=4 ** a - 3 * 2 ** a + 7,
                Lc0=2 ** (a - 1) - 1, blk0=2 ** a - 3)

# window starts (descent start == TOPGRIND start), from x2dg_boundary.py DESC
START = {5: 13453, 6: 33830}

for a in (5, 6):
    P = topgrind(a)
    s0 = START[a]
    s_core0 = s0 + P['entry']
    s_core1 = s_core0 + P['core']
    s_end = s_core1 + P['exit']
    print(f"=== a={a}: TOPGRIND [{s0},{s_end}]  entry={P['entry']} core={P['core']} "
          f"exit={P['exit']} total={P['total']} (check {P['entry']+P['core']+P['exit']})")
    assert P['entry'] + P['core'] + P['exit'] == P['total']

    sim = build(2); sim.step()
    while sim.n < s_core0: sim.step()
    check_braidcfg(sim, 0, P['Lc0'], P['blk0'], 'core-IN ')
    while sim.n < s_core1: sim.step()
    ok_in = check_braidcfg(sim, P['N'], 1, 1, 'core-OUT')

    # ---- the EXIT trace ----
    print(f"  --- EXIT {s_core1} -> {s_end} ({P['exit']} steps) ---")
    print(f"  IN  left  = {runs(left_nf(sim))}")
    print(f"  IN  right = {runs(right_nf(sim))}")
    trace = []
    while sim.n < s_end:
        sim.step()
        trace.append((sim.n, sim.st, sim.h, sim.pos))
    print(f"  OUT left  = {runs(left_nf(sim))}")
    print(f"  OUT right = {runs(right_nf(sim))}")
    print(f"  OUT state={sim.st} h={sim.h}")
    # state word of the exit
    word = ''.join(t[1] for t in trace)
    print(f"  exit state word ({len(word)}): {word}")
    print(f"  exit steps {P['exit']} == 2*(2N+2) = {2*(2*P['N']+2)}  (N={P['N']})")
    print(f"  deposit ones(4N+5) = {4*P['N']+5}  == 2^(a+1)-3 = {2**(a+1)-3}")
    print(f"  UNTOUCHED marker block: 2^(a+2)-2 = {2**(a+2)-2}  "
          f"(docstring's 2^(a+1)-4 = {2**(a+1)-4})")

    # --- THE REPARSE CLAIM: pow10(2N+1) ++ ones 1 ++ 0::0::casc == pow10(2N+2) ++ 0::casc
    lhs = pow10(2 * P['N'] + 1) + ones(1) + [0, 0]
    rhs = pow10(2 * P['N'] + 2) + [0]
    print(f"  REPARSE pow10(2N+1)++ones 1++[0,0] == pow10(2N+2)++[0] : {lhs == rhs}")

    # --- THE ENTRY (fixed 7 steps?) ---
    sim2 = build(2); sim2.step()
    while sim2.n < s0: sim2.step()
    print(f"  --- ENTRY {s0} -> {s_core0} ---")
    print(f"  IN  state={sim2.st} h={sim2.h} left={runs(left_nf(sim2), 6)}")
    print(f"  IN  right={runs(right_nf(sim2), 8)}")
    lin, rin, pin = left_nf(sim2)[:2 * P['Lc0'] + 4], right_nf(sim2)[:6], sim2.pos
    w2 = ''
    while sim2.n < s_core0:
        sim2.step(); w2 += sim2.st
    print(f"  entry state word ({len(w2)}): {w2}")
    print(f"  ENTRY IN  left(nf) [{2*P['Lc0']+4}] = {lin}")
    print(f"  ENTRY IN  right(nf)[6]  = {rin}   head=0  pos-delta={sim2.pos-pin}")
    print(f"  ENTRY OUT left(nf) [{2*P['Lc0']+4}] = {left_nf(sim2)[:2*P['Lc0']+4]}")
    print(f"  ENTRY OUT right(nf)[6]  = {right_nf(sim2)[:6]}")
    # is IN left == pow01 Lc0 ++ tail, OUT left == pow10 Lc0 ++ same tail?
    pow01 = [0, 1] * P['Lc0']
    print(f"  ENTRY IN left == (01)^{P['Lc0']} prefix : "
          f"{left_nf(sim2)[:0] == [] and lin[:2*P['Lc0']] == pow01}")
    print(f"  ENTRY OUT left == (10)^{P['Lc0']} prefix: "
          f"{left_nf(sim2)[:2*P['Lc0']] == pow10(P['Lc0'])}")
    print(f"  ENTRY tails equal (beyond the comb)?  IN {lin[2*P['Lc0']:]}  "
          f"OUT {left_nf(sim2)[2*P['Lc0']:2*P['Lc0']+4]}")

    # ================= FULL braid_topgrind ENDPOINT CHECK, bit-for-bit =================
    # Lean braid_topgrind N=2^{a-1}-2, Lc=1:
    #   IN  <E,p,<pow01 (1+N) ++ marker, false, 0::0::0::(ones (2N+1) ++ 0::0::casc)>>
    #   OUT <E,p+5+2N, <ones (4N+4) ++ (pow10 1 ++ true::marker), false, false::casc>>
    N = P['N']
    s = build(2); s.step()
    while s.n < s0: s.step()
    Lin, Rin, pos_in = left_nf(s), right_nf(s), s.pos
    # IN: left == pow01 (1+N) ++ marker, and the comb split must be MAXIMAL
    combI = [0, 1] * (1 + N)
    ok_lin = Lin[:2 * (1 + N)] == combI
    max_lin = Lin[2 * (1 + N):2 * (1 + N) + 2] != [0, 1]   # marker must not extend the (01) comb
    marker = Lin[2 * (1 + N):]
    ok_rin = (s.st == 'E' and s.h == 0
              and Rin[:3 + (2 * N + 1) + 2] == [0, 0, 0] + ones(2 * N + 1) + [0, 0])
    max_rin = Rin[3 + (2 * N + 1)] != 1      # block 1^{2N+1} maximal (next cell is 0)
    casc = Rin[3 + (2 * N + 1) + 2:]
    while s.n < s_end: s.step()
    Lout, Rout = left_nf(s), right_nf(s)
    # OUT: exactly the Lean RHS
    exp_L = ones(4 * N + 4) + [1, 0] + [1] + marker
    exp_R = [0] + casc
    ok_out = (s.st == 'E' and s.h == 0
              and Lout[:len(exp_L)] == exp_L[:len(Lout)] and Rout == exp_R)
    ok_steps = (s_end - s0) == 7 + (4 * N * N + 6 * N) + (4 * N + 4)
    ok_pos = (s.pos - pos_in) == 5 + 2 * N
    print(f"  === braid_topgrind {N} 1 ON-PATH CHECK (Lean statement, bit-for-bit) ===")
    print(f"    IN  left=pow01({1+N})++marker: {ok_lin}  comb-MAXIMAL: {max_lin}")
    print(f"    IN  right=0^3++ones({2*N+1})++0^2++casc: {ok_rin}  block-MAXIMAL: {max_rin}")
    print(f"    marker head = {marker[:3]}  (Lean: true::marker rides untouched)")
    print(f"    OUT == ones({4*N+4})++pow10 1++true::marker | false::casc : {ok_out}")
    print(f"    steps {s_end-s0} == 7+braidRunSteps(0,{N})+(4*{N}+4): {ok_steps}   "
          f"pos delta == 5+2N={5+2*N}: {ok_pos}")
    print(f"    ALL: {all([ok_lin, max_lin, ok_rin, max_rin, ok_out, ok_steps, ok_pos])}")
    print()
