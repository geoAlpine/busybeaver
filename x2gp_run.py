#!/usr/bin/env python3
"""x2gp_run.py -- cross-check §5p `outer_tick_noCarry_run` against the RAW orbit.

Two independent checks of the n=2 no-carry RUN proved in X2.lean §5p:

  (1) SAME-CONFIG cross-check: take the exact anchor config the Lean `#eval` uses
      (register <t=1, work=13>, left comb (10)^3, empty tails) and run 36 Python
      `step`s (independent bigint sim), confirming it lands on the predicted output
      register <5,9> config -- Lean kernel vs Python sim agree.

  (2) ON-PATH check: build(2), run the real doubling-phase orbit forward, and
      confirm the anchor's local window (left `1^3 0 (10)^3`, right `1^13 0^2`)
      actually OCCURS at an E-on-0 boundary, and that 36 steps from there advance
      the odometer by two no-carry ticks exactly as the run predicts.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, Sim, TT


def raw_step(L, h, R, st, pos):
    """One Lean-faithful step on explicit lists (L nearest-first top=L[-1])."""
    t = TT[(st, h)]
    if t is None:
        return None
    w, mv, ns = t
    h = w
    if mv == +1:
        L = L + [h]
        h = R.pop() if R else 0
    else:
        R = R + [h]
        h = L.pop() if L else 0
    return L, h, R, ns, pos + mv


def run_steps(L, h, R, st, pos, n):
    for _ in range(n):
        s = raw_step(list(L), h, list(R), st, pos)
        if s is None:
            return None
        L, h, R, st, pos = s
    return L, h, R, st, pos


# ---- (1) SAME-CONFIG cross-check (matches the Lean #eval exactly) -------------
# anchor input: E on 0, left nearest-first = 1^3 0 (10)^3, right = 1^13 0^2
left_in  = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0][::-1]   # store top=L[-1]=nearest
h_in     = 0
R_in     = ([1] * 13 + [0, 0])[::-1]              # store reversed so pop()=nearest
out = run_steps(left_in, h_in, R_in, 'E', 0, 36)
assert out is not None, "HALT within 36 steps -- run is NOT halt-free!"
L2, h2, R2, st2, pos2 = out
left_nf  = L2[::-1]
right_hf = [h2] + R2[::-1]
# predicted output: register <5,9>: left = 1^11 0 (10)^1, right = 1^9 0^2, E, pos=4
exp_left  = [1] * 11 + [0, 1, 0]
exp_right = [0] + [1] * 9 + [0, 0]
print("(1) same-config cross-check (Lean #eval config, 36 Python steps):")
print(f"    final state/pos = {st2}/{pos2}  (expect E/4)")
print(f"    left  nearest-first = {left_nf}")
print(f"    right head-first    = {right_hf}")
ok1 = (st2 == 'E' and pos2 == 4 and left_nf == exp_left and right_hf == exp_right)
print(f"    MATCH predicted <5,9> output: {ok1}")

# ---- (2) ON-PATH check: does this window occur in the real build(2) orbit? ----
print("\n(2) on-path check (build(2) doubling-phase orbit):")
sim = build(2)
# advance to M6(2) (5th milestone) -- start of the doubling phase
miles = 0
sim.step()
while sim.n < 60_000_000:
    if sim.is_milestone():
        miles += 1
        if miles == 5:
            break
    if not sim.step():
        print("    HALT"); sys.exit(1)
m6 = sim.n
print(f"    M6(2) doubling phase begins at raw n = {m6}")

# scan forward for an E-on-0 boundary whose local window matches the anchor
found = None
scan_cap = m6 + 40000
while sim.n < scan_cap:
    if sim.st == 'E' and sim.h == 0:
        lnf = sim.L[::-1]
        rhf = [sim.h] + sim.R[::-1]
        if (len(lnf) >= 10 and lnf[:10] == [1, 1, 1, 0, 1, 0, 1, 0, 1, 0]
                and len(rhf) >= 16 and rhf[:16] == [0] + [1] * 13 + [0, 0]):
            found = sim.n
            snap = (list(sim.L), sim.h, list(sim.R), sim.st, sim.pos)
            break
    if not sim.step():
        break

if found is None:
    print("    anchor window NOT found in scanned region "
          f"[{m6}, {scan_cap}) -- (the exact n depends on comb depth; check (1)).")
else:
    print(f"    anchor window `1^3 0 (10)^3 . 1^13 0^2` OCCURS at raw n = {found}")
    # run 36 real steps from the found boundary; compare to prediction on the prefix
    L, h, R, st, pos = snap
    out2 = run_steps(L, h, R, st, pos, 36)
    L3, h3, R3, st3, pos3 = out2
    lnf3 = L3[::-1]
    rhf3 = [h3] + R3[::-1]
    ok2 = (st3 == 'E'
           and lnf3[:14] == [1] * 11 + [0, 1, 0]
           and rhf3[:12] == [0] + [1] * 9 + [0, 0]
           and pos3 - pos == 4)
    print(f"    after 36 real steps: state {st3}, dpos = {pos3 - pos} (expect 4)")
    print(f"    left  prefix = {lnf3[:14]}")
    print(f"    right prefix = {rhf3[:12]}")
    print(f"    MATCH run prediction (two no-carry ticks): {ok2}")
