# o15 fixed-point hunt, part 2: the QUEUE transducer -- exact per-residue rewriting rules,
# where a leading 2 can be created, and whether "[2,2] forms" is a finite congruence.
# All landings are exact concrete simulation (run_gen: guarded tape, no acceleration).
import sys
from o15_template_scan import run_gen

def land(blocks):
    status, out, steps, unsafe, mg, toks, bad0 = run_gen(blocks, record=False)
    return status, out, steps, unsafe, bad0

# ---------- (A) rho=2 (V==2 mod 3): does ONLY the last digit fuse? ----------
print("== (A) rho=2 rule: [.., d_last, V] -> [.., d_last + (8V+11)/3] ? ==")
ok = bad = 0
for V in (50, 53, 101, 200, 299):
    if V % 3 != 2:
        continue
    for q in ([1], [2], [5], [9], [1, 1], [2, 2], [6, 3], [4, 2, 1], [2, 2, 2], [1, 2, 3, 4]):
        status, out, steps, unsafe, bad0 = land(q + [V])
        pred = q[:-1] + [q[-1] + (8 * V + 11) // 3]
        tag = "OK" if out == pred else f"DIFF pred={pred}"
        if out == pred:
            ok += 1
        else:
            bad += 1
            print(f"  [{q}+{V}] -> {out}   {tag}  (unsafe={unsafe})")
        assert status == 'LAND' and unsafe == 0, (q, V, status, unsafe)
print(f"  rho=2 last-digit-fusion law: {ok} OK, {bad} deviations")

# ---------- (B) rho=1 (split): leading behaviour incl. the d=1,2 anomalies ----------
print("\n== (B) rho=1 rule: leading digit at a split ==")
for dlead in range(1, 10):
    for rest in ([], [1, 1], [5, 2]):
        for V in (52, 100, 301):
            if V % 3 != 1:
                continue
            q = [dlead] + rest
            status, out, steps, unsafe, bad0 = land(q + [V])
            print(f"  [{q}+{V}] -> {status} {out}  unsafe={unsafe}")
print("  (expected clean: d>=3 -> [d-3]+rest+[1,1,(8V-5)/3]; anomalies d=1,2 shown raw)")

# ---------- (C) rho=0: the carry cascade, systematic ----------
print("\n== (C) rho=0 cascade: [queue, V] -> ?  (V=51 and 300 unless noted) ==")
print("  single digit:")
for d in range(1, 16):
    for V in (51, 300):
        status, out, steps, unsafe, bad0 = land([d, V])
        print(f"    [{d},{V}] -> {out}  unsafe={unsafe}")
print("  two digits (d1,d2 in 1..8, V=51):")
for d1 in range(1, 9):
    row = []
    for d2 in range(1, 9):
        status, out, steps, unsafe, bad0 = land([d1, d2, 51])
        assert unsafe == 0 or status == 'HALT', (d1, d2, status, unsafe)
        row.append(f"{d2}:{out}")
    print(f"    d1={d1}: " + "  ".join(row))
print("  three digits (selected):")
for q in ([1, 1, 1], [2, 2, 2], [3, 3, 3], [6, 6, 6], [1, 2, 3], [3, 2, 1], [2, 1, 1], [1, 1, 2],
          [5, 5, 5], [4, 4, 4], [9, 9, 9], [2, 2, 1], [1, 2, 2], [2, 1, 2]):
    status, out, steps, unsafe, bad0 = land(q + [51])
    print(f"    [{q}+51] -> {status} {out}  unsafe={unsafe}")

# ---------- (D) leading-2 creation census over true trajectories ----------
print("\n== (D) leading-2 creation census: iterate the TRUE map, log every leading-digit change ==")
# Seeds: a spread of single blocks; run each until V > 200000 or 25 gens.
events2 = []
expose22 = []
SEEDS = range(30, 100)
for V0 in SEEDS:
    blocks = [V0]
    hist = [list(blocks)]
    for g in range(25):
        rho = blocks[-1] % 3
        status, out, steps, unsafe, bad0 = land(blocks)
        if status != 'LAND':
            print(f"  seed {V0}: gen {g} {status} from {blocks}")
            break
        assert unsafe == 0
        prev = blocks
        blocks = out
        hist.append(list(blocks))
        if len(blocks) >= 2 and blocks[0] == 2:
            events2.append((V0, g + 1, prev, list(blocks)))
        if len(blocks) >= 3 and blocks[0] == 2 and blocks[1] == 2:
            expose22.append((V0, g + 1, prev, list(blocks)))
        if blocks[-1] > 2500:
            break
print(f"  seeds {SEEDS.start}..{SEEDS.stop-1}: leading-2 milestones: {len(events2)}, leading-[2,2] milestones: {len(expose22)}")
for e in events2[:40]:
    print("    lead2:", e)
for e in expose22:
    print("    LEAD22:", e)

# ---------- (E) which residue class creates the leading digit changes ----------
print("\n== (E) leading-digit transition table observed in (D)-style runs ==")
# re-run, classifying (rho, lead_before) -> lead_after
from collections import defaultdict
tab = defaultdict(set)
for V0 in SEEDS:
    blocks = [V0]
    for g in range(25):
        rho = blocks[-1] % 3
        lead_b = blocks[0] if len(blocks) >= 2 else None
        status, out, steps, unsafe, bad0 = land(blocks)
        if status != 'LAND':
            break
        lead_a = out[0] if len(out) >= 2 else None
        tab[(rho, lead_b)].add(lead_a)
        blocks = out
        if blocks[-1] > 2500:
            break
for k in sorted(tab, key=str):
    print(f"    rho={k[0]} lead_before={k[1]} -> lead_after in {sorted(tab[k], key=str)}")
