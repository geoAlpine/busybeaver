# o15 fixed-point hunt, part 3: the decisive experiments.
# (1) fatal-cylinder EXTENT: [2,2,buffer,V] -- which buffers protect?
# (2) finite-residue IMPOSSIBILITY: the [1]^k family makes V' mod 3 depend on queue depth k,
#     so NO finite-residue delta-map (o4-style) can drive the branch itinerary. Concrete.
# (3) natural-flow halt chase: iterate the TRUE map from small seeds whose law-predicted
#     trajectory assembles a leading [2,2] -- does the flow actually reach HALT?
# (4) leading-digit mod-3 bookkeeping on true trajectories (what creates lead == 2 mod 3).
# All runs: exact concrete simulation (run_gen), zero acceleration.
import sys
from o15_template_scan import run_gen

def land(blocks):
    status, out, steps, unsafe, mg, toks, bad0 = run_gen(blocks, record=False)
    return status, out, steps, unsafe

def v3(n):
    n = abs(n)
    if n == 0:
        return 10**9
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k

# ---------- (1) fatal-cylinder extent ----------
print("== (1) fatal-cylinder extent: [2,2] + buffer + [V] ==")
buffers = [[], [1], [1, 1], [1, 1, 1], [1] * 4, [1] * 8, [2], [2, 1], [1, 2], [2, 2],
           [3], [4], [5], [6], [3, 1, 1], [1, 3], [6, 1, 1]]
for V in (52, 100, 51, 99, 50, 98):
    row = []
    for buf in buffers:
        q = [2, 2] + buf + [V]
        status, out, steps, unsafe = land(q)
        row.append(('HALT' if status == 'HALT' else '.', buf))
    halted = [b for s, b in row if s == 'HALT']
    print(f"  V={V} (V%3={V % 3}): HALT buffers = {halted if halted else 'NONE'}")

# also: [2,2] deeper in the queue with a small head
print("  -- [head, 2,2, V] (does a head digit protect?):")
for head in (1, 2, 3, 4, 5, 6):
    for V in (52, 51):
        q = [head, 2, 2, V]
        status, out, steps, unsafe = land(q)
        print(f"    [{head},2,2,{V}] -> {status} {out if status == 'LAND' else ''}")

# ---------- (2) finite-residue impossibility, concrete family ----------
print("\n== (2) [1]^k family: V' and V' mod 3 as a function of queue DEPTH k (V=51, 300) ==")
for V in (51, 300):
    base = None
    seq = []
    for k in range(0, 9):
        status, out, steps, unsafe = land([1] * k + [V])
        assert status == 'LAND' and unsafe == 0
        Vp = out[-1]
        pred = (8 * (V + k) + 9 - 2 * k) // 3
        seq.append((k, Vp, Vp % 3, Vp == pred and len(out) == 1))
    print(f"  V={V}: (k, V', V'%3, law (8(V+k)+9-2k)/3 & full absorb): {seq}")
print("  => states agreeing on V and on ANY bounded queue window (depth j) but differing at")
print("     depth k>j land in DIFFERENT V' mod 3 classes: no finite-residue delta-map exists.")

# ---------- (3) natural-flow halt chase ----------
print("\n== (3) natural-flow chase: iterate the TRUE map; do trajectories assemble [2,2] and HALT? ==")
seeds = [[5, 5, 2, 52], [5, 5, 2, 100], [8, 5, 2, 52], [5, 8, 2, 52], [2, 5, 2, 52],
         [5, 5, 2, 51], [5, 5, 5, 52], [9, 5, 2, 100], [5, 5, 2, 301], [8, 8, 2, 52],
         [5, 2, 52], [5, 2, 100], [8, 2, 52], [11, 2, 52], [5, 2, 2, 52], [14, 52],
         [5, 5, 2, 151], [5, 5, 2, 202], [5, 5, 2, 250]]
for seed in seeds:
    blocks = list(seed)
    traj = [list(blocks)]
    verdict = 'ran out'
    for g in range(30):
        status, out, steps, unsafe = land(blocks)
        if status == 'HALT':
            verdict = f"HALT at gen {g + 1} from {blocks} (step {steps} of that gen)"
            break
        if status != 'LAND':
            verdict = f"{status} at gen {g + 1}"
            break
        blocks = out
        traj.append(list(blocks))
        if blocks[-1] > 3000:
            verdict = f"V>3000 at gen {g + 1}, no halt"
            break
    lead22 = [(i, t) for i, t in enumerate(traj) if len(t) >= 3 and t[0] == 2 and t[1] == 2]
    print(f"  seed {seed}: {verdict}")
    for i, t in lead22[:3]:
        print(f"      lead-[2,2] milestone at gen {i}: {t}")

# ---------- (4) leading-digit residue bookkeeping ----------
print("\n== (4) lead-digit creation laws seen on the (3) trajectories + queue-seeded census ==")
from collections import defaultdict
tab = defaultdict(set)
lead2_events = []
lead22_events = []
census_seeds = seeds + [[d1, d2, V] for d1 in (2, 5, 8) for d2 in (2, 5, 8) for V in (52, 53, 54)]
census_seeds += [[6, 5, 2, V] for V in (52, 53, 54, 100, 101, 102)]
for seed in census_seeds:
    blocks = list(seed)
    for g in range(30):
        rho = blocks[-1] % 3
        lead_b = blocks[0] if len(blocks) >= 2 else None
        status, out, steps, unsafe = land(blocks)
        if status != 'LAND':
            tab[(rho, lead_b)].add('HALT' if status == 'HALT' else status)
            break
        lead_a = out[0] if len(out) >= 2 else None
        tab[(rho, lead_b)].add(lead_a)
        if lead_a == 2 and lead_b != 2:
            lead2_events.append((tuple(seed), g + 1, list(blocks), list(out)))
        if len(out) >= 3 and out[0] == 2 and out[1] == 2 and not (len(blocks) >= 3 and blocks[0] == 2 and blocks[1] == 2):
            lead22_events.append((tuple(seed), g + 1, list(blocks), list(out)))
        blocks = out
        if blocks[-1] > 3000:
            break
print(f"  lead-2 creation events: {len(lead2_events)}")
for e in lead2_events[:12]:
    print(f"    {e[0]} gen {e[1]}: {e[2]} -> {e[3]}")
print(f"  lead-[2,2] creation events: {len(lead22_events)}")
for e in lead22_events[:12]:
    print(f"    {e[0]} gen {e[1]}: {e[2]} -> {e[3]}")
print("  (rho, lead_before) -> lead_after set:")
for k in sorted(tab, key=str):
    print(f"    rho={k[0]} lead={k[1]} -> {sorted(tab[k], key=str)}")
