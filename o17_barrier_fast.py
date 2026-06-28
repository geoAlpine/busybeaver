#!/usr/bin/env python
"""
o17 no-REG/k-window barrier: pin the embedded-family halt structure (FAST bytearray sim),
cross-checked against bb_sim on a sample for soundness.
o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB  (halt = F reads 0).
"""
import sys
sys.path.insert(0, "/Users/aokiyousuke/quantum-ecc/busybeaver")
import bb_sim

O17 = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            if t[0] == '-' or t[2] == 'Z':
                row.append(None)
            else:
                row.append((int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M
Mt = parse(O17)
HALTSTATE = 5  # F ; halt when F reads 0 (its row[0] is None)

def fast_run(init_cells, start_off, maxsteps, sz_log=24):
    SZ = 1 << sz_log; tape = bytearray(SZ); off = SZ // 2
    for k, v in init_cells.items():
        tape[off + k] = v
    pos = off + start_off; st = 0
    for step in range(1, maxsteps + 1):
        r = tape[pos]
        cell = Mt[st][r]
        if cell is None:
            return step  # halt
        w, d, ns = cell
        tape[pos] = w; pos += d; st = ns
        if pos <= 0 or pos >= SZ - 1:
            raise RuntimeError("tape overflow")
    return None

def layout_A(k):  # [A:0] 1^k
    return {i + 1: 1 for i in range(k)}

# ---- cross-check vs bb_sim: blank start + a few family members with a slow dict sim ----
def dict_run(init_cells, start_off, maxsteps):
    machine = bb_sim.parse(O17)
    tape = dict(init_cells); head = start_off; state = 'A'; steps = 0
    HS = {"Z", "H", "-"}
    while steps < maxsteps:
        sym = tape.get(head, 0)
        write, move, nxt = machine[state][sym]
        tape[head] = write
        head += 1 if move == "R" else -1
        steps += 1
        if nxt in HS:
            return steps
        state = nxt
    return None

print("="*72); print("CROSS-CHECK vs bb_sim"); print("="*72)
halted, steps, ones = bb_sim.run(O17, max_steps=1_000_000)
print(f"[XCHK] blank bb_sim: halted={halted} steps={steps} (expect no halt) ",
      "OK" if not halted else "FAIL")
for k in [1, 2, 3, 6, 12, 24]:
    a = fast_run(layout_A(k), 0, 2_000_000)
    b = dict_run(layout_A(k), 0, 2_000_000)
    print(f"[XCHK] k={k}: fast={a} dict(bb_sim convention)={b} match={a==b}")
    assert a == b, "mismatch"
print(f"[CAL] k=6 -> {fast_run(layout_A(6),0,10**6)} (anchor: 206)")
print()

print("="*72); print("FAMILY 0A01^k, k=1..120, budget 1e7"); print("="*72)
BUD = 10_000_000
res = {}
for k in range(1, 121):
    r = fast_run(layout_A(k), 0, BUD)
    res[k] = r
    print(f"  k={k:3d} (k%3={k%3}): {'HALT@'+str(r) if r is not None else 'RUN(>1e7)'}")

print("\n" + "="*72); print("SUMMARY BY RESIDUE"); print("="*72)
for rc in (0, 1, 2):
    ks = [k for k in res if k % 3 == rc]
    halted = [k for k in ks if res[k] is not None]
    runners = [k for k in ks if res[k] is None]
    print(f"k%3=={rc}: HALT {len(halted)}/{len(ks)}")
    if rc != 0:
        print(f"   runners (should be empty if 'k%3!=0 always halts'): {runners}")
    else:
        print(f"   HALTERS (j,k,time): " + ", ".join(f"({k//3},{k},{res[k]})" for k in halted))
        print(f"   RUNNERS j: {[k//3 for k in runners]}")

print("\n" + "="*72)
print("PUSH k=3j runners to budget 1e8 (catch delayed halters; non-monotonicity)")
print("="*72)
runners0 = [k for k in res if k % 3 == 0 and res[k] is None]
late = {}
for k in runners0:
    r = fast_run(layout_A(k), 0, 100_000_000)
    late[k] = r
    print(f"  k={k:3d} (j={k//3}): {'HALT@'+str(r) if r is not None else 'RUN(>1e8)'}")

# final consolidated halter list for k=3j
print("\n" + "="*72); print("CONSOLIDATED k=3j HALTERS (incl. delayed)"); print("="*72)
allh = {k: res[k] for k in res if k % 3 == 0 and res[k] is not None}
allh.update({k: late[k] for k in late if late[k] is not None})
for k in sorted(allh):
    print(f"  j={k//3:2d} k={k:3d} halt@{allh[k]}")
still = sorted([k for k in res if k % 3 == 0 and res[k] is None and late.get(k) is None])
print(f"  still-running k=3j (>1e8): {still}  (j={[k//3 for k in still]})")
# monotonicity check among halters
hs = sorted(allh.items())
nonmono = any(hs[i][1] > hs[i+1][1] for i in range(len(hs)-1))
print(f"  halt-times non-monotone in k? {nonmono}")
sys.stdout.flush()
