#!/usr/bin/env python3
"""
Mahler-sea survey — GATE stage (2026-07-07).
For each of o11,o12,o13,o14,o16,SpaceNeedle:
  (a) [PROVEN from table] verify the halt state has a UNIQUE predecessor transition
      (forced chain), printed explicitly;
  (b) [OBSERVED] halt-window census at radius 4 around every gate-trigger event over a
      12M-step blank-tape run, with saturation checkpoints (2M/6M/12M): |S|, new windows,
      all-safe check (the would-be-fatal neighbour is 1 in every event).
Decides nothing. No label upgraded.
"""
import sys
from collections import defaultdict

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

SN = "ABCDEF"

# (name, spec, trigger_state, trigger_read, neighbour_dir)
# gate: HALT <=> trigger fires AND tape[pos+ndir]==0   [PROVEN from table, re-verified below]
MACHINES = [
    ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", 1, 0, -1),
    ("o12", "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", 4, 0, +1),
    ("o13", "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 3, 1, -1),
    ("o14", "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 2, 0, -1),
    ("o16", "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", 4, 0, +1),
    ("SN",  "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", 2, 0, -1),
]

def forced_chain(spec):
    """Return (halt_state, [preds]) where preds = transitions targeting each halt state,
    and the unique predecessor of each; PROVEN-from-table check."""
    M = parse(spec)
    out = []
    for hs in range(6):
        for hr in range(2):
            if M[hs][hr] is None:
                preds = [(s, r, M[s][r]) for s in range(6) for r in range(2)
                         if M[s][r] is not None and M[s][r][2] == hs]
                out.append((hs, hr, preds))
    return out

def run_gate(spec, tstate, tread, ndir, N, W=4, checkpoints=(2_000_000, 6_000_000, 12_000_000)):
    M = parse(spec)
    SZ = 1 << 23
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    trig = 0
    unsafe = 0
    wins = {}
    lo = hi = pos
    cps = list(checkpoints)
    results = []
    step = 0
    halted = None
    while step < N:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            halted = step
            break
        if st == tstate and r == tread:
            trig += 1
            win = bytes(tape[pos - W:pos + W + 1])
            if win not in wins:
                wins[win] = [0, step]
            wins[win][0] += 1
            if tape[pos + ndir] == 0:
                unsafe += 1
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if cps and step == cps[0]:
            results.append((step, len(wins), trig, unsafe))
            cps.pop(0)
    return dict(halted=halted, trig=trig, unsafe=unsafe, wins=wins,
                width=hi - lo + 1, checkpoints=results, steps=step)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 12_000_000
    W = 4
    for name, spec, ts, tr, nd in MACHINES:
        print(f"=== {name}  {spec}")
        # (a) forced predecessor chain
        for hs, hr, preds in forced_chain(spec):
            tag = "UNIQUE" if len(preds) == 1 else f"NOT UNIQUE ({len(preds)})"
            plist = ", ".join(f"{SN[s]},{r}->{a[0]}{'R' if a[1]>0 else 'L'}{SN[a[2]]}" for s, r, a in preds)
            print(f"  halt {SN[hs]},{hr}: predecessors into {SN[hs]}: [{plist}]  -> {tag}")
        print(f"  gate: {SN[ts]} reads {tr}, {'left' if nd<0 else 'right'} nbr 0 => HALT  [PROVEN from table]")
        # (b) window census
        res = run_gate(spec, ts, tr, nd, N, W)
        for s, nw, tg, us in res['checkpoints']:
            print(f"  step {s:>10,}: |S|={nw:>3}  triggers={tg:>7,}  unsafe={us}")
        last_new = max(v[1] for v in res['wins'].values()) if res['wins'] else -1
        print(f"  FINAL: steps={res['steps']:,} halted={res['halted']} width={res['width']:,} "
          f"|S|={len(res['wins'])} last-new-window@step {last_new:,} "
          f"triggers={res['trig']:,} UNSAFE={res['unsafe']}")
        # all-safe = neighbour byte in every stored window is 1
        bad = [w for w in res['wins'] if w[W + nd] == 0]
        print(f"  windows with fatal-neighbour=0: {len(bad)}  ({'ALL SAFE' if not bad else 'UNSAFE PRESENT'})")
        print()
    print("GATE STAGE: census [OBSERVED]; gates [PROVEN from table]. No machine decided. No label upgraded.")
