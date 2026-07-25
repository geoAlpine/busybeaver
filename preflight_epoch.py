#!/usr/bin/env python3
"""PRE-FLIGHT epoch-ratio probe (2026-07-25) — move 3 of ANALYSIS_2026-07-25.md.

The x2 closure says a carry-TRANSPARENT machine's epoch width ratio is a power of the tape base
(x2: exactly 2). An odd prime in the Mahler multiplier makes it opaque = (K).

Epoch detection needs no reverse-engineering: on the side where the frontier advances in bursts,
cluster the frontier records SCALE-FREELY (a gap > t/4 opens a new epoch, which works because
epochs grow geometrically), and read the total tape width at each epoch start.

CALIBRATION (this is what makes it trustworthy): x2 -> 2.0 (PROVEN doubler), Antihydra -> 3/2,
o15 -> 8/3, o18 -> 8/3, o3 -> 4/3, o5 -> 4/3 — every independently-known value is recovered.

No machine decided. No label upgraded.
"""
import sys
exec(open('preflight_frontier.py').read().split("if __name__")[0])

def clusters(rec):
    out = []
    for i in range(len(rec)):
        if i == 0 or rec[i][0] - rec[i-1][0] > rec[i-1][0]/4: out.append(i)
    return out

def run(name, spec, N, span):
    T = parse(spec)
    tape = bytearray(2*span); pos = span; st = 0; mx = 0; mn = 0
    recL = []; recR = []; status = 'RUN'
    for t in range(1, N+1):
        e = T[st][tape[pos]]
        if e is None: status = f'HALT@{t}'; break
        w, d, st = e
        tape[pos] = w; pos += d
        r = pos - span
        if r > mx: mx = r; recR.append((t, r, mx-mn))
        if r < mn: mn = r; recL.append((t, -r, mx-mn))
        if pos < 1 or pos >= 2*span-1: status = f'OVF@{t}'; break
    for side, rec in (('L', recL), ('R', recR)):
        if len(rec) < 4:
            print(f"{name:<22} {side:>4}  (too few records)  {status}"); continue
        ws = [rec[i][2] for i in clusters(rec)][-7:]
        rats = [round(ws[i+1]/ws[i], 4) for i in range(len(ws)-1) if ws[i]]
        tag = ""
        if len(rats) >= 2:
            last = rats[-2:]
            for v, lbl in ((2.0, "2.0  TRANSPARENT CANDIDATE"), (1.5, "3/2 Mahler"),
                           (8/3, "8/3 Mahler"), (4/3, "4/3"), (2.5, "5/2"), (3.0, "3.0"),
                           (4.0, "4.0  TRANSPARENT CANDIDATE")):
                if all(abs(x-v) < 0.03*v for x in last): tag = f"  <<< {lbl}"; break
        print(f"{name:<22} {side:>4}  {str(ws):<40} {rats}{tag}  {status if status!='RUN' else ''}")

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 4*10**7
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    span = 1 << 20
    for name, spec in SPECS:
        if only and not any(o in name for o in only): continue
        run(name, spec, N, span)
