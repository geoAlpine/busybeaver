#!/usr/bin/env python
"""
SOUNDNESS-CRITICAL test of the o17 k-window / REG barrier.

Mechanism: any certificate L (step-closed, halt-free, L >= reachable) has allowed m-grams
G_L >= grams(reachable) =: G*, so L >= L*_m := tight m-gram over-approximation of reachable.
If L*_m ACCEPTS a config c that REACHES A HALT, then c in L, step-closure forces the halt
config into L, violating halt-freeness => NO m-window certificate exists.

We test c = "A 0 1^k" (FAR encoding: marker A, head cell 0, then 1^k) for HALTER k
(k%3 in {1,2}, all proven to halt). Uses the trusted far_dfa.FAR + far.step_str.
"""
import sys, os
sys.path.insert(0, "/Users/aokiyousuke/quantum-ecc/busybeaver")
from far_dfa import FAR, reachable_configs, canon
from far import step_str, trim
from bouncer_prove2 import parse as far_parse
import bb_sim

O17 = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

# ---- confirm the FAR encoding "A 0 1^k" reaches a halt, via the trusted far.step_str ----
def halts_via_far(k, budget=20_000_000):
    M = far_parse(O17)
    # config string U q c_h V = "A","0","1"*k  (marker A on head cell 0, ones to the right)
    s = ["A", "0"] + ["1"] * k
    for _ in range(budget):
        s, halted = step_str(M, s)
        if halted:
            return True
        s = trim(s)
    return False

print("="*72)
print("STEP 0: confirm 'A 0 1^k' (FAR encoding) halts for halter k, via far.step_str")
print("="*72)
for k in [1, 2, 4, 5, 7, 8]:
    h = halts_via_far(k)
    print(f"  k={k} (k%3={k%3}): far.step_str halts={h}")

print("\n" + "="*72)
print("STEP 1: build tight m-gram over-approx L*_m from reachable(o17), test halter accept")
print("="*72)
# collect a long reachable run once (configs are FAR-encoded strings)
N = 200_000
configs, halted = reachable_configs(O17, N)
print(f"  reachable run: {len(configs)} configs, halted={halted} (expect False)")
assert not halted

for m in range(2, 13):
    far = FAR(O17, configs, m)
    # find a halter k with k>=m, k%3 in {1,2}
    accepted = []
    for k in range(m, m + 30):
        if k % 3 == 0:
            continue
        c = canon(["A", "0"] + ["1"] * k)
        if far.accepts(c):
            accepted.append(k)
    # also test the start is accepted (sanity) and a runner k%3==0 is accepted
    start_ok = far.accepts(canon(["A"]))
    runner_k = next(k for k in range(max(m,3), m+30) if k % 3 == 0)
    runner_acc = far.accepts(canon(["A", "0"] + ["1"] * runner_k))
    print(f"  m={m:2d}: |G|={len(far.G):5d}  start_in_L={start_ok}  "
          f"runner(k={runner_k}) in L={runner_acc}  HALTERS-accepted k={accepted[:6]}"
          f"{'  <-- BARRIER FIRES' if accepted else '  (no halter accepted)'}")

print("\n" + "="*72)
print("STEP 2: cross-check far_dfa.FAR.verify() outcome at each m (should FAIL, not certify)")
print("="*72)
for m in range(2, 9):
    far = FAR(O17, configs, m)
    ok, msg = far.verify()
    print(f"  m={m}: verify -> {'CERTIFIED(!!)' if ok else 'FAIL'}  : {msg[:80]}")
sys.stdout.flush()
