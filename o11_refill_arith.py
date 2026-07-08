#!/usr/bin/env python3
"""
o11 refill-law deep dive, part 5: THE ARITHMETIC MODEL + predict-and-confirm + census
(2026-07-08).

MODEL (pure arithmetic; grid-exact rules R1-R6 of o11_refill_rules.py, iterated):
  T(m) = floor(3m/2)+4.  Epoch seed k (leading block; sea re-seeded m=2 by R6).
  r = k mod 4, sample index e = (k-r)/4, sample m* = T^e(m_seed):
    r=2 : HALT (R4, at the epoch's terminal collapse)
    r=0 : HALT iff m* even (R5: end-game (1, m*-1)); else collapse c = 3m*
    r=1 : HALT iff m* odd  (R5: end-game (1, m*));   else collapse c = 3m*+3
    r=3 : collapse c = 3m*+5 (m* odd) / 3m*+6 (m* even)   -- never halts in-epoch
  refill: k' = c-2, m_seed' = 2.
o11 (from blank, after the t=9 transient [1^3]) starts at k=1.
This script: (PC0) seeded epoch-4 reproduces the real orbit step-exactly;
(PC1) first-epoch outcomes on the (k,m) grid, exact; (PC2) multi-epoch halt
classification on the (k,m) grid and the pure-collapse [1^c] family, budget-censored;
(PC3) rule spot-checks at real-orbit magnitudes (m ~ 4156); census + margins.
Everything the model predicts is CHECKED against exact simulation where feasible;
beyond simulation the model is labeled [arithmetic consequence of grid-exact rules].
"""
import sys
from o11_refill_rules import T, make_tape, run, seed_run, decode, SPEC
from msea_struct2 import parse, rle_blocks

def model(k, m_seed=2, mcap=10**7, max_epochs=64):
    """Iterate the arithmetic model. Returns (verdict, epochs, detail):
    verdict in {'HALT','ESCAPE','MAX'}; epochs = [(k, r, e, m*, c or None)]."""
    epochs = []
    for _ in range(max_epochs):
        r = k % 4
        e = (k - r) // 4
        m = m_seed
        for _ in range(e):
            m = T(m)
            if m > mcap:
                return ('ESCAPE', epochs, (k, r, 'm* exceeds cap'))
        if r == 2:
            epochs.append((k, r, e, m, None))
            return ('HALT', epochs, ('R4', k, m))
        if r == 0:
            epochs.append((k, r, e, m, None if m % 2 == 0 else 3 * m))
            if m % 2 == 0:
                return ('HALT', epochs, ('R5-odd', k, m - 1))
            c = 3 * m
        elif r == 1:
            epochs.append((k, r, e, m, None if m % 2 == 1 else 3 * m + 3))
            if m % 2 == 1:
                return ('HALT', epochs, ('R5-odd', k, m))
            c = 3 * m + 3
        else:  # r == 3
            c = 3 * m + 5 if m % 2 else 3 * m + 6
            epochs.append((k, r, e, m, c))
        if c > mcap:
            return ('ESCAPE', epochs, (k, r, 'c exceeds cap'))
        k, m_seed = c - 2, 2
    return ('MAX', epochs, None)

def cost_estimate(epochs):
    """~2.75 * m_end^2 per epoch (calibrated on the standalone grid halts)."""
    tot = 0
    for k, r, e, m, c in epochs:
        tot += 2.75 * m * m + 40 * k + 50
    return tot

# ---------- plain runners ----------
def sim_first_event(k, m, budget=200_000_000):
    """Seed milestone (k,m); run to first COLLAPSE or HALT (through milestones)."""
    M = parse(SPEC)
    tape, lo, last1 = make_tape(k, m)
    pos = last1 + 1
    hi = pos
    st = 1
    step = 0
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return ('HALT', step)
        if st == 5 and pos >= hi and step > 0:
            b = rle_blocks(tape, lo, hi)
            if len(b) == 1:
                return ('COLLAPSE', b[0])
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos > hi: hi = pos
        elif pos < lo: lo = pos
    return ('BUDGET', None)

def sim_halt_only(blocks, gaps, state, off, budget):
    """Seed arbitrary config; run to HALT or budget. Returns halt step or None."""
    M = parse(SPEC)
    n1 = sum(blocks) + sum(gaps)
    SZ = 512 + 64 * n1 + 65536  # generous; per-epoch growth is bounded by the budget
    tape = bytearray(SZ)
    p = 512
    for i, b in enumerate(blocks):
        for _ in range(b):
            tape[p] = 1; p += 1
        if i < len(gaps):
            p += gaps[i]
    last1 = p - 1
    while not tape[last1]:
        last1 -= 1
    pos = last1 + off
    st = state
    step = 0
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return step
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos >= len(tape) - 8:
            raise RuntimeError("tape bounds")
    return None

# ---------- PC0: seeded epoch 4 reproduces the real orbit ----------
def pc0():
    print("=== PC0: seeded (301,2) vs real orbit (epoch 4 head)")
    real = [(0, (301, 2)), (54, (297, 7)), (220, (293, 14)), (730, (289, 25)),
            (1958, (285, 41)), (4946, (281, 65)), (12014, (277, 101))]
    M = parse(SPEC)
    tape, lo, last1 = make_tape(301, 2)
    pos = last1 + 1
    hi = pos
    st = 1
    step = 0
    got = []
    lastb = None
    while step < 15000:
        r = tape[pos]
        act = M[st][r]
        if st == 1 and pos >= hi:
            b = rle_blocks(tape, lo, hi)
            if b != lastb:
                got.append((step, decode(b)))
                lastb = list(b)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos > hi: hi = pos
    ok = got[:7] == real
    print(f"  seeded milestone (step-delta, (k,m)) chain == real-orbit chain (7 gens): {ok}")
    if not ok:
        print(f"  got:  {got[:7]}\n  real: {real}")
    return ok

# ---------- PC1: first-epoch outcomes, exact ----------
def pc1(kmax=17, mmax=16):
    print(f"=== PC1: first-epoch outcome, (k,m) grid k=2..{kmax}, m=1..{mmax} (exact)")
    bad = 0; tot = 0
    for k in range(2, kmax + 1):
        for m in range(1, mmax + 1):
            v, eps, det = model(k, m, max_epochs=1)
            kk, rr, ee, mm, cc = eps[0]
            want = ('HALT', None) if v == 'HALT' and len(eps) == 1 else ('COLLAPSE', cc)
            kind, pay = sim_first_event(k, m)
            tot += 1
            good = (kind == want[0]) and (want[1] is None or pay == want[1])
            if not good:
                bad += 1
                if bad <= 8:
                    print(f"  MISMATCH ({k},{m}): sim {kind} {pay}, model {want}")
    print(f"  exact: {tot-bad}/{tot}")

# ---------- PC2: multi-epoch halt classification, budget-censored ----------
def pc2_grid(kmax=17, mmax=16, budget=20_000_000, mcap=6000):
    print(f"=== PC2a: multi-epoch halt classification, (k,m) grid, budget {budget:,}")
    refut = 0; must = 0; cens = 0; ok_halt = 0; ok_no = 0
    for k in range(2, kmax + 1):
        for m in range(1, mmax + 1):
            v, eps, det = model(k, m, mcap=mcap)
            est = cost_estimate(eps)
            h = sim_halt_only([k] + [1] * m, [1] * m, 1, +1, budget)
            if v == 'HALT' and est < 0.5 * budget:
                must += 1
                if h is None:
                    refut += 1
                    print(f"  REFUTATION ({k},{m}): model must-halt (est {est:.0f}), sim ran full budget")
                else:
                    ok_halt += 1
            elif v in ('ESCAPE', 'MAX') or est >= 0.5 * budget:
                cens += 1
                if h is not None and v != 'HALT':
                    refut += 1
                    print(f"  REFUTATION ({k},{m}): sim HALT@{h} but model verdict {v}")
                elif h is None:
                    ok_no += 1
    print(f"  must-halt confirmed: {ok_halt}/{must}; censored cells: {cens} "
          f"(non-halt within budget where model escapes: {ok_no}); REFUTATIONS: {refut}")

def pc2_pure(cmax=58, budget=40_000_000, mcap=6000):
    print(f"=== PC2b: pure-collapse [1^c] standalone, c=3..{cmax} (state F, head on last 1), budget {budget:,}")
    refut = 0; rows = {0: [], 1: [], 2: [], 3: []}
    for c in range(3, cmax + 1):
        v, eps, det = model(c - 2, 2, mcap=mcap)
        est = cost_estimate(eps)
        h = sim_halt_only([c], [], 5, 0, budget)
        if v == 'HALT' and est < 0.5 * budget:
            tag = 'H' if h is not None else '!'
            if h is None:
                refut += 1
                print(f"  REFUTATION c={c}: model must-halt, sim survived budget")
        else:
            tag = '?' if h is None else '!'
            if h is not None and v != 'HALT':
                refut += 1
                print(f"  REFUTATION c={c}: sim HALT@{h}, model {v}")
            elif h is not None:
                tag = 'h'  # model halt but est >= budget/2 — halted anyway, consistent
        rows[c % 4].append((c, tag))
    for r in range(4):
        s = ' '.join(f"{c}{t}" for c, t in rows[r])
        print(f"  c%4={r}: {s}")
    print(f"  H = model-must-halt confirmed by run; h = model-halt confirmed (est>budget/2); "
          f"? = censored (model escape/large, sim no halt); REFUTATIONS: {refut}")

# ---------- PC3: rule spot checks at real-orbit magnitudes ----------
def pc3():
    print("=== PC3: single-rule spot checks at real-orbit magnitudes")
    spots_r1 = [(245, 4156), (301, 1226), (85, 1843), (61, 2768)]
    for k, m in spots_r1:
        kind, pay, s = seed_run(k, m)
        want = (k - 4, T(m))
        got = decode(pay) if kind == 'MIL' else (kind, pay)
        print(f"  R1 ({k},{m}) -> {got}  want {want}  {'OK' if got == want else 'MISMATCH'}")
    for m in (1226, 1843, 4156):
        kind, pay, s = seed_run(1, m)
        want = ('HALT' if m % 2 else ('COLLAPSE', 3 * m + 3))
        ok = (kind == 'HALT') if m % 2 else (kind == 'COLLAPSE' and pay == 3 * m + 3)
        print(f"  R5 (1,{m}) -> {kind} {pay if kind=='COLLAPSE' else ''}  {'OK' if ok else 'MISMATCH'}")
    for m in (1226, 1843):
        kind, pay, s = seed_run(3, m)
        cw = 3 * m + 5 if m % 2 else 3 * m + 6
        print(f"  R3 (3,{m}) -> {kind} {pay}  want COLLAPSE {cw}  {'OK' if kind=='COLLAPSE' and pay==cw else 'MISMATCH'}")
    for m in (1226, 1843):
        kind, pay, s = seed_run(2, m)
        print(f"  R4 (2,{m}) -> {kind}  want HALT  {'OK' if kind=='HALT' else 'MISMATCH'}")

# ---------- census ----------
def census():
    print("=== REAL-ORBIT CENSUS (draws = collapse values; the doubly-exp refill orbit)")
    print("  observed (exact sim): c = 3 (t=9, blank transient), 9 (t=46), 26 (t=271), 303 (t=28100)")
    v, eps, det = model(1, 2, mcap=10**16, max_epochs=6)
    print("  arithmetic continuation from k=1 [consequence of grid-exact rules; NOT machine-verified beyond t=40M]:")
    names = ['epoch 1', 'epoch 2', 'epoch 3', 'epoch 4', 'epoch 5', 'epoch 6']
    for i, (k, r, e, m, c) in enumerate(eps):
        par = 'even' if m % 2 == 0 else 'odd'
        safe = {0: 'safe iff m* odd', 1: 'safe iff m* even', 2: 'FATAL', 3: 'safe always'}[r]
        print(f"  {names[i]}: k={k} (r={r}, e={e})  m*={m} ({par}, m*%4={m%4})  [{safe}]  c={c}  c%4={c % 4 if c else '-'}")
    print(f"  model verdict after listed epochs: {v} {det}")
    m75 = 2
    for _ in range(75):
        m75 = T(m75)
    c5 = 3 * m75 + 3
    k5 = c5 - 2
    e5 = (k5 - 3) // 4
    t5 = 2.75 * (m75 ** 2)
    print(f"\n  the 5th draw: c5 = 3*T^75(2)+3 = {c5:,} == 1 (mod 4)  -> k5 = {k5:,} == 3 (mod 4)")
    print(f"    (epoch-4 survival hinged on T^75(2) = {m75:,} being EVEN — it is; T^75(2) mod 4 = {m75 % 4})")
    print(f"    t(5th collapse) ~ 2.75*m_end^2 ~ {t5:.2e} steps  [estimate]")
    print(f"  epoch 5 (k==3 mod 4): survives its own collapse UNCONDITIONALLY; draws c6 = 3*T^{e5}(2)+5/6")
    print(f"    e5 = {e5:,}; T^e5(2) has ~{int(e5 * 0.17609):,} digits — Mahler-hard, OPEN")
    print(f"    c6 fatal residues: T^e5(2) == 1,2 (mod 4) -> k6 == 2 (mod 4); == 0,3 (mod 4) -> k6 == 0 (mod 4) (then a parity coin)")
    print("\n  margins (the survived events, in order):")
    print("    e=0:  T^0(2)=2   even  needed even  (r=1)   -> survived   [coin 1]")
    print("    e=1:  T^1(2)=7   %4=3  needed %4 in {0,3}   -> k3=24 r=0  [coin 2]")
    print("    e=6:  T^6(2)=101 odd   needed odd   (r=0)   -> survived; 101%4=1 -> k4 r=1  [coin 3]")
    print("    e=75: T^75(2)    even  needed even  (r=1)   -> survived; %4=2 -> k5 r=3  [coin 4]")
    print("    e~1.15e14: OPEN — the next residue draw; naive P(safe)=1/2")
    print("\n  annealed [MODEL]: per-epoch survival = 1/2 in every live row (r=0,1: parity coin;")
    print("  r=3: next-row coin) => E[remaining epochs | r=3 now] = 2.6; P(survive n) ~ 2^-n.")
    print("  o11's naive halt-lean is p* = 1/2 PER EPOCH — sharper than the classification's 1/4,")
    print("  and the largest in the frontier; what protects it observationally is that epochs are")
    print("  doubly-exponentially long (t5 ~ 1e28.8) and 4 coins have already come up safe.")

if __name__ == "__main__":
    ok0 = pc0()
    pc1()
    pc2_grid()
    pc2_pure()
    pc3()
    census()
    print("\nNo machine decided. No label upgraded.")
