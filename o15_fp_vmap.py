# o15 fixed-point hunt, part 1: the big-block branch maps V' = (8V+c)/3 and their 3-adic
# fixed points (o4 run-structure analogue, O4_RUN_STRUCTURE_2026-07-07.md).
#
# (a) EXTRACT the exact affine law per (queue-class, V mod 3) from concrete generation runs
#     (run_gen from o15_template_scan: exact guarded simulation, no acceleration).
# (b) ALGEBRA: fixed point of V'=(8V+c)/3 solves 5x=-c => x=-c/5 in Z_3 (5 a 3-adic unit);
#     distance law V'-x = (8/3)(V-x) => v3 drops by exactly 1 per same-branch step;
#     so v3(V - x) = v3(5V + c)  (since V - x = (5V+c)/5, v3(5)=0).
# (c) TEST the o4 closed form on the SCALAR MODEL (queue ignored): maximal run of residue
#     rho starting at V equals v3(5V + c_rho) -- exhaustively on a large range.
# (d) TEST against the REAL transducer: where the queue perturbs V', measure the deviation.
import sys
from o15_template_scan import run_gen

def v3(n):
    n = abs(n)
    if n == 0:
        return 10**9
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k

# ---------- (a) extract single-block laws ----------
print("== (a) single-block law extraction: [V] -> landing, V=20..500 ==")
laws = {}   # residue -> set of (c, prepended-queue) observed, with V' = (8V+c)/3
bad = []
for V in range(20, 501):
    status, land, steps, unsafe, mg, toks, bad0 = run_gen([V], record=False)
    assert status == 'LAND' and unsafe == 0 and bad0 == 0, (V, status, unsafe, bad0)
    rho = V % 3
    Vp = land[-1]
    c = 3 * Vp - 8 * V
    key = (c, tuple(land[:-1]))
    laws.setdefault(rho, {}).setdefault(key, []).append(V)
for rho in sorted(laws):
    for (c, q), Vs in sorted(laws[rho].items()):
        print(f"  V==%d mod 3: V' = (8V%+d)/3, prepended queue {list(q)}   ({len(Vs)} cases, V in [{min(Vs)},{max(Vs)}])" % (rho, c))
assert set(laws[2].keys()) == {(11, ())}
assert set(laws[0].keys()) == {(9, ())}
assert set(laws[1].keys()) == {(-17, (6,))}
print("  [exact on the grid] c = {rho=0: +9, rho=1: -17 (prepends 6), rho=2: +11}")

# ---------- (a') queued split law: [d, V], V==1 mod 3, d>=3 ----------
print("\n== (a') queued split law [d,V] (V==1 mod 3, d>=3): V' constant ==")
cset = {}
for d in range(3, 13):
    for V in (31, 52, 100, 151, 301, 400):
        status, land, steps, unsafe, mg, toks, bad0 = run_gen([d, V], record=False)
        assert status == 'LAND' and unsafe == 0, (d, V, status)
        Vp = land[-1]
        c = 3 * Vp - 8 * V
        pred = ([d - 3] if d > 3 else []) + [1, 1, Vp]
        cset[(c, land == pred)] = cset.get((c, land == pred), 0) + 1
print("  observed (c, landing==[d-3,1,1,V']):", cset)
print("  [exact on the grid] queued split: V' = (8V-5)/3, leading digit drains -3, emits [1,1]")

# ---------- (b) fixed points ----------
print("\n== (b) 3-adic fixed points x = -c/5 (5x = -c), PROVEN algebra ==")
from fractions import Fraction
for rho, c in ((0, 9), (1, -17), (2, 11), ('1q', -5)):
    x = Fraction(-c, 5)
    # x mod 3 in Z_3: inverse of 5 mod 3 is 2
    xm3 = (-c * 2) % 3
    print(f"  branch c={c:+d}: x = {x} in Z_3, x mod 3 = {xm3}" + ("  (INTEGER x=1)" if c == -5 else ""))
# checks: x mod 3 must equal the residue class the branch serves
assert (-9 * 2) % 3 == 0 and (17 * 2) % 3 == 1 and (-11 * 2) % 3 == 2 and (5 * 2) % 3 == 1

# ---------- (c) scalar-model run law, exhaustive ----------
# Scalar model: V_{n+1} = (8 V_n + c(V_n mod 3))/3 with c as above (queue IGNORED; the
# rho=1 branch uses c=-17; this matches the true dynamics only while the queue stays
# out of the way -- that is exactly what part (d) and o15_fp_queue.py measure).
print("\n== (c) scalar-model run law: maximal run of residue rho from V == v3(5V + c_rho)? ==")
C = {0: 9, 1: -17, 2: 11}
def run_len_scalar(V, c):
    """maximal number of consecutive steps staying in the same residue class rho=c-class,
    starting at V (V assumed == rho mod 3), iterating V -> (8V+c)/3 with the SAME c."""
    rho = (-c * 2) % 3
    assert V % 3 == rho
    n = 0
    while V % 3 == rho:
        V = (8 * V + c) // 3
        n += 1
        if n > 100:
            break
    return n

LIM = 200_000
mism = 0
for V in range(3, LIM + 1):
    rho = V % 3
    c = C[rho]
    pred = v3(5 * V + c)
    got = run_len_scalar(V, c)
    if pred != got:
        mism += 1
        if mism < 10:
            print(f"  MISMATCH V={V}: pred {pred} got {got}")
print(f"  same-branch run law, V=3..{LIM}: mismatches = {mism}")

# rho=1 with the QUEUED constant -5 (the law actually in force after the first split):
mism2 = 0
for V in range(4, LIM + 1, 3):  # V == 1 mod 3
    pred = v3(5 * V - 5)   # = v3(V-1) since v3(5)=0
    got = run_len_scalar(V, -5)
    if pred != got:
        mism2 += 1
        if mism2 < 10:
            print(f"  MISMATCH (c=-5) V={V}: pred {pred} got {got}")
print(f"  queued-split run law (c=-5, x=1): v3(V-1) vs run, V==1 mod 3 up to {LIM}: mismatches = {mism2}")

# mixed rho=1 run: first step c=-17, then c=-5: closed form for total run?
# after first step V1=(8V-17)/3; total run = 1 + v3(V1 - 1) = 1 + v3(8V - 20) - v3(3)... compute:
# V1 - 1 = (8V-20)/3 = 8(V - 5/2)/3 -> v3(V1-1) = v3(8V-20) - 1 = v3(2(4V-10)) - 1 = v3(4V-10) - 1? careful with 2s: v3 ignores 2s.
mism3 = 0
for V in range(4, LIM + 1, 3):
    n = 0
    W = V
    # first step (single-block split, c=-17)
    if W % 3 == 1:
        W = (8 * W - 17) // 3
        n += 1
        n += run_len_scalar(W, -5) if W % 3 == 1 else 0
    pred = 1 + v3(8 * V - 20) - 1   # = v3(8V-20): v3((8V-20)/3) = v3(8V-20)-1, +1 for first step
    if pred != n:
        mism3 += 1
        if mism3 < 10:
            print(f"  MISMATCH mixed V={V}: pred {pred} got {n}")
print(f"  MIXED rho=1 run (c=-17 then c=-5): total run = v3(8V-20) = v3(2V-5): mismatches = {mism3}")

# ---------- (d) real transducer vs scalar model ----------
print("\n== (d) true transducer runs vs the scalar-model prediction ==")
print("  iterate the TRUE generation map (concrete) from single-block seeds; compare the")
print("  V-residue itinerary with the scalar model until the queue perturbs V'.")
for V0 in (39, 41, 43, 82, 121, 245, 364, 500):
    blocks = [V0]
    scal = V0
    div = None
    itin_true, itin_scal = [], []
    for g in range(9):
        rho_t = blocks[-1] % 3
        rho_s = scal % 3
        itin_true.append(rho_t)
        itin_scal.append(rho_s)
        status, land, steps, unsafe, mg, toks, bad0 = run_gen(blocks, record=False)
        if status != 'LAND':
            div = f"status={status} at gen {g}"
            break
        assert unsafe == 0
        blocks = land
        scal = (8 * scal + C[rho_s]) // 3
        if blocks[-1] != scal and div is None:
            div = f"gen {g + 1}: true V={blocks[-1]} vs scalar {scal} (delta {blocks[-1] - scal}), queue={blocks[:-1]}"
        if blocks[-1] > 4000:
            break
    print(f"  V0={V0}: true itinerary {itin_true} | scalar {itin_scal} | first V-divergence: {div}")
