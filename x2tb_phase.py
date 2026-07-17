#!/usr/bin/env python3
"""x2tb_phase.py -- the cost-ratio test for a PHASE-CONDITIONED register (2026-07-17).

WHY.  x2tb_braid.py reads each machine's register as the running record of a
full-tape observable.  That gate REFUSES B5: B5's global maxrun record is an
arithmetic ramp (records ... 1634, 1637, 1640, 1643, step +3), not a doubler.  Yet
B5 demonstrably HAS a doubling register: peaks 9*2^k-1, k=1..8 (6b6d739).

The resolution is that B5's register is PHASE-CONDITIONED: it is the full-tape maxrun
sampled only when the machine is in state C at a left-extent record.  At those instants
the max run IS the register; at other instants a longer, separately-growing run exists,
which is what the global record tracks.  So B5's register is a real object, but it is
NOT the global max, and the generic instrument cannot see it.

This probe therefore reads the register under the SAME phase condition as x2b5_braid,
but with the extent derived from the tape (x2tb_sim.feats), so fault F1 is inexpressible.
It reports the same cost ratio: t_k = step of the k-th register peak, ratio t_k/t_{k-1}.

B1 is NOT read here: under this same phase condition B1 yields only 8 milestones, i.e.
state-C-at-left-record is B5's phase, not B1's.  B1's register IS the global maxrun
record, so B1 passes x2tb_braid's doubling gate and is measured there -- where it scores
3.968 against its INDEPENDENTLY KNOWN Theta(4^k) wall (the TOPGRIND, ebec409/6d8d692).
That is the positive control for the generic instrument.  Each machine is read by the
instrument whose gate it passes, and neither instrument is trusted where its gate fails.

Decides NO halting.  No label upgraded.
"""

import sys
from x2tb_sim import MACHINES, parse, feats

# (machine, state that conditions the register, which extent record) per x2b5_braid
PHASE = {
    'B5': ('C', 'left'),
}


def register_series(name, cap, SZ=1 << 15):
    """[(step, full-tape maxrun)] at each phase-conditioned milestone."""
    spec = MACHINES[name]
    st_name, side = PHASE[name]
    want = ord(st_name) - ord('A')
    R = parse(spec)
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st2 = 0
    step = 0
    rlo = rhi = pos          # TRIGGER only -- never a scan bound
    traj = []
    while step < cap:
        a = R[st2 + tape[pos]]
        if a is None:
            return 'HALT', step, traj
        w, d, ns = a
        tape[pos] = w
        pos += d
        st2 = ns
        step += 1
        if pos < 4 or pos > SZ - 4:
            return 'OVR', step, traj
        rec = (pos < rlo) if side == 'left' else (pos > rhi)
        if pos < rlo:
            rlo = pos
        if pos > rhi:
            rhi = pos
        if rec and st2 // 2 == want:
            traj.append((step, feats(tape)[1]))
    return 'MAX', step, traj


def peaks_of(traj, family):
    """First step at which the phase-conditioned register attains each family value."""
    out = []
    seen = set()
    for step, v in traj:
        if v in family and v not in seen:
            seen.add(v)
            out.append((v, step))
    return out


if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 40_000_000
    FAMILY = {
        'B5': {9 * 2 ** k - 1 for k in range(1, 12)},      # 17,35,71,143,...
    }
    for name in (sys.argv[2:] or ['B5']):
        outc, step, traj = register_series(name, cap)
        pk = peaks_of(traj, FAMILY[name])
        print(f"\n=== {name}  {MACHINES[name]}")
        print(f"    outc={outc} steps={step} nmilestone={len(traj)} "
              f"phase=state {PHASE[name][0]} @ {PHASE[name][1]}-extent record")
        print(f"    {'peak':>8} {'step':>14} {'ratio':>8}")
        prev = None
        ratios = []
        for v, s in pk:
            r = s / prev if prev else 0.0
            if prev:
                ratios.append(r)
                print(f"    {v:>8} {s:>14} {r:>8.3f}")
            else:
                print(f"    {v:>8} {s:>14} {'-':>8}")
            prev = s
        tail = ratios[-4:]
        if tail:
            med = sorted(tail)[len(tail) // 2]
            print(f"    tail ratios {[round(x, 3) for x in tail]}  median={med:.3f}")
            print(f"    ==> {'LINEAR (braid-free)' if med < 2.6 else 'QUADRATIC cost Theta(v^2)' if med > 3.4 else 'AMBIGUOUS'}")
    print("\n2 = linear/braid-free ; 4 = Theta(v^2) per doubling = the B1/x2 cost signature")
    print("No machine decided. No label upgraded.")
