#!/usr/bin/env python
"""
o17 no-REG/k-window barrier: pin the embedded-family halt structure rigorously.
o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB  (halt = F reads 0).
Cross-checks the embedded-family simulator against bb_sim.run on the FULL machine
(blank start) to guarantee identical step semantics.
"""
import re, sys
sys.path.insert(0, "/Users/aokiyousuke/quantum-ecc/busybeaver")
import bb_sim

O17 = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

# ---- our embedded-family simulator (dict tape, halt = F reads 0 OR '---' transition) ----
def parse(spec):
    M = {}
    for i, g in enumerate(spec.split('_')):
        s = chr(ord('A') + i); M[s] = {}
        for sym in (0, 1):
            w, m, nx = g[sym*3:sym*3+3]
            M[s][sym] = (int(w) if w in '01' else 0, m, nx)
    return M
M = parse(O17)
HALT = {'Z', 'H', '-'}

def run(cells, head, st, maxsteps):
    tape = dict(cells)
    for step in range(maxsteps):
        sym = tape.get(head, 0)
        w, mv, nx = M[st][sym]
        tape[head] = w
        head += 1 if mv == 'R' else -1
        if nx in HALT:
            return step + 1
        st = nx
    return None

# ---- CROSS-CHECK vs bb_sim on the full machine from blank ----
def crosscheck_blank():
    # reproduce blank run with our dict simulator (start state A, head 0, blank tape)
    ours = run({}, 0, 'A', 2_000_000)
    halted, steps, ones = bb_sim.run(O17, max_steps=2_000_000)
    bb = steps if halted else None
    print(f"[XCHK] blank: ours={ours}  bb_sim halted={halted} steps={steps}")
    # both should NOT halt within 2e6 (o17 is a cryptid from blank)
    assert (ours is None) and (not halted), "blank cross-check mismatch"
    print("[XCHK] blank: agree (no halt in 2e6) OK")

# Cross check the family: re-implement family run inside bb_sim-style and compare a few k.
def bb_style_family(k, maxsteps, layout):
    """Run the family with bb_sim's exact transition convention but a preset tape."""
    machine = bb_sim.parse(O17)
    tape = dict(layout(k))
    head = 0; state = 'A'; steps = 0
    HALTSET = {"Z", "H", "-"}
    while steps < maxsteps:
        sym = tape.get(head, 0)
        write, move, nxt = machine[state][sym]
        tape[head] = write
        head += 1 if move == "R" else -1
        steps += 1
        if nxt in HALTSET:
            return steps
        state = nxt
    return None

def layout_A(k):  # [A:0] 1^k    (head on 0, cells 1..k = 1)
    return {i + 1: 1 for i in range(k)}
def layout_B(k):  # [A:0] 0 1^k  (head on 0, cell1=0, cells 2..k+1 =1)
    c = {1: 0}
    for i in range(k): c[2 + i] = 1
    return c

print("="*72)
print("CROSS-CHECK with bb_sim")
print("="*72)
crosscheck_blank()
# layout calibration: which matches k=6 -> halt@206 ?
for nm, lay in [("A", layout_A), ("B", layout_B)]:
    r6 = run(lay(6), 0, 'A', 2_000_000)
    rbb = bb_style_family(6, 2_000_000, lay)
    print(f"[CAL] layout {nm}: k=6 ours={r6}  bb_style={rbb}  (target 206?) match={r6==rbb}")

# choose layout matching 206
LAY = None; LNAME = None
for nm, lay in [("A", layout_A), ("B", layout_B)]:
    if run(lay(6), 0, 'A', 2_000_000) == 206:
        LAY, LNAME = lay, nm; break
if LAY is None:
    LAY, LNAME = layout_A, "A(default)"
print(f"[CAL] chosen layout = {LNAME}\n")

print("="*72)
print(f"EMBEDDED FAMILY 0A01^k (layout {LNAME}): k=1..90, budget 1e7")
print("="*72)
BUD = 10_000_000
res = {}
for k in range(1, 91):
    r = run(LAY(k), 0, 'A', BUD)
    # cross-check via bb_sim-style for EVERY k (soundness)
    rbb = bb_style_family(k, BUD, LAY)
    assert r == rbb, f"family mismatch k={k}: ours={r} bb={rbb}"
    res[k] = r
    tag = f"HALT@{r}" if r is not None else f"RUN(>{BUD})"
    print(f"  k={k:3d} (k%3={k%3}): {tag}")

print("\n[XCHK] all k=1..90 family runs agree ours==bb_sim-style OK")

print("\n" + "="*72)
print("SUMMARY BY RESIDUE")
print("="*72)
for rc in (0, 1, 2):
    ks = [k for k in res if k % 3 == rc]
    halted = [k for k in ks if res[k] is not None]
    runners = [k for k in ks if res[k] is None]
    print(f"  k%3=={rc}: HALT {len(halted)}/{len(ks)}")
    if rc != 0:
        print(f"           halters: {halted}")
        print(f"           runners: {runners}")
    else:
        print(f"           k=3j HALTERS (j,k,time): "
              + ", ".join(f"({k//3},{k},{res[k]})" for k in halted))
        print(f"           k=3j RUNNERS (within {BUD}): {runners}")

# Push apparent k=3j non-halters to a larger budget (catch delayed halters)
print("\n" + "="*72)
print("PUSH k=3j apparent-runners to budget 3e8 (catch delayed halters)")
print("="*72)
runners0 = [k for k in res if k % 3 == 0 and res[k] is None]
for k in runners0:
    r = run(LAY(k), 0, 'A', 300_000_000)
    print(f"  k={k:3d} (j={k//3}): {'HALT@'+str(r) if r is not None else 'RUN(>3e8)'}")
sys.stdout.flush()
