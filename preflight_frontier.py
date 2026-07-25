#!/usr/bin/env python3
"""PRE-FLIGHT (2026-07-25): the cheapest transparency discriminator for BB(6) cryptids.

From the x2 closure: a carry-TRANSPARENT machine's milestone right-frontier advances by an exact
power of the tape base each epoch (x2 MEASURED: 2^11, 2^12). An orbit-dependent (Mahler / (K))
frontier does not. This needs NO milestone extractor and NO reverse-engineering: it reads the
frontier-record sequence directly and groups it into epochs by the stalls between record bursts.

Reports, per machine: the last burst-end frontier positions, their consecutive differences, and
the ratio. Ratio 2.0 with power-of-two differences => TRANSPARENT CANDIDATE (x2-like).

No machine decided. No label upgraded.
"""
import sys

SPECS = [
 ("x2 (PROVEN non-halt)", "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"),
 ("Antihydra",            "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
 ("Space Needle",         "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"),
 ("Lucy's Moonlight",     "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
 ("o2",  "1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"),
 ("o3",  "1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC"),
 ("o4",  "1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---"),
 ("o5",  "1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB"),
 ("o7",  "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"),
 ("o8",  "1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE"),
 ("o10", "1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC"),
 ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"),
 ("o12", "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB"),
 ("o13", "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA"),
 ("o14", "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE"),
 ("o15", "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"),
 ("o16", "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE"),
 ("o17", "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"),
 ("o18", "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"),
]

def parse(spec):
    T = []
    for blk in spec.split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k+3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1, ord(f[2])-65))
        T.append(row)
    return T

def frontier_records(T, N, span):
    tape = bytearray(2*span); pos = span; st = 0
    mx = 0; mn = 0; recR = []; recL = []
    for t in range(1, N+1):
        e = T[st][tape[pos]]
        if e is None: return ('HALT', t, recR, recL)
        w, d, st = e
        tape[pos] = w; pos += d
        r = pos - span
        if r > mx: mx = r; recR.append((t, r))
        if r < mn: mn = r; recL.append((t, -r))
        if pos < 1 or pos >= 2*span-1: return ('OVERFLOW', t, recR, recL)
    return ('RUN', N, recR, recL)

def bursts(rec, N, frac=60):
    """frontier values at the END of each record burst (a stall > N/frac closes a burst)"""
    if not rec: return []
    G = max(1, N // frac); out = []
    for i in range(len(rec)-1):
        if rec[i+1][0] - rec[i][0] > G: out.append(rec[i][1])
    out.append(rec[-1][1])
    return out

def ispow2(n): return n > 0 and (n & (n-1)) == 0

def report(name, spec, N, span):
    T = parse(spec)
    status, t, recR, recL = frontier_records(T, N, span)
    for side, rec in (('R', recR), ('L', recL)):
        b = bursts(rec, N)[-6:]
        d = [b[i+1]-b[i] for i in range(len(b)-1)]
        rat = [round(b[i+1]/b[i], 4) for i in range(len(b)-1) if b[i]]
        p2 = all(ispow2(x) for x in d) if d else False
        tag = ""
        if len(rat) >= 2:
            if p2 and all(abs(r-2.0) < 0.02 for r in rat[-2:]): tag = "  <<< POWER-OF-2 (x2-like)"
            elif all(abs(r-1.5) < 0.03 for r in rat[-2:]):      tag = "  <<< ratio 3/2 (Mahler)"
            elif all(abs(r-2.667) < 0.05 for r in rat[-2:]):    tag = "  <<< ratio 8/3 (Mahler)"
        print(f"  {side}: bursts={b}  diffs={d}  ratios={rat}{tag}")
    print(f"  [{status} @{t}]")

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    span = 1 << 17
    for name, spec in SPECS:
        print(f"\n=== {name} ===")
        report(name, spec, N, span)
