#!/usr/bin/env python3
"""Angle-A re-measurement: the 4-point template pre-flight on the island candidates.

Re-derives from the RAW orbit (doc claims are evidence, not verdict):
  1. transparency  : width ratio -> 2 exactly (base-2 doubler; carry-chain 0)
  2. frontier reg. : growing-side frontier advance is a clean power of 2 per epoch
  3. frame period  : the milestone marker word's repetition unit (COMB (10)^k vs CASCADE)
  4. seam          : milestone state / head-step uniform => clean epoch recurrence

For each machine: detect growing side, snapshot milestone tapes (frontier-record
clusters), dump head-relative RLE marker word, and the (width,time) ratio ladder.

Usage:  python3 island_preflight.py [STEPS]
"""
import sys

def parse(spec):
    T = []
    for blk in spec.split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k+3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1, ord(f[2]) - 65))
        T.append(row)
    return T

SPECS = [
    ("x2", "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"),
    ("D",  "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---"),
    ("E",  "1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---"),
    ("F",  "1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---"),
    ("H",  "1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---"),
    ("G",  "1RB0LA_1RC0RE_0RD---_1LA0LD_1LD1RF_1RA1LB"),
    ("I",  "1RB0LA_1RC0RE_0RD---_1LA1LF_1LD1RF_1RA1LB"),
]

def rle(bits):
    """Run-length encode a 0/1 list -> list of (val,count)."""
    out = []
    for b in bits:
        if out and out[-1][0] == b:
            out[-1][1] += 1
        else:
            out.append([b, 1])
    return [(v, c) for v, c in out]

def rle_str(runs, maxparts=26):
    parts = []
    for v, c in runs:
        parts.append(f"{v}^{c}" if c > 1 else f"{v}")
    if len(parts) > maxparts:
        parts = parts[:maxparts] + [f"...(+{len(parts)-maxparts} runs)"]
    return " ".join(parts)

GATES = [128, 256, 512, 1024, 2048, 3000]

def run(name, spec, N):
    T = parse(spec)
    span = 1 << 21
    tape = bytearray(2 * span)
    pos = span; st = 0; mx = 0; mn = 0
    recL = []; recR = []; status = 'RUN'
    gate_snapL = {}; gate_snapR = {}   # width-gate -> snapshot (first crossing)
    for t in range(1, N + 1):
        e = T[st][tape[pos]]
        if e is None:
            status = f'HALT@{t}'; break
        w, d, st = e; tape[pos] = w; pos += d; r = pos - span
        newrec = None
        if r > mx:
            mx = r; recR.append((t, mx - mn)); newrec = 'R'
        if r < mn:
            mn = r; recL.append((t, mx - mn)); newrec = 'L'
        if newrec:
            wdt = mx - mn
            gs = gate_snapR if newrec == 'R' else gate_snapL
            for g in GATES:
                if wdt >= g and g not in gs:
                    lo = span + mn; hi = span + mx
                    bits = list(tape[lo:hi+1])
                    gs[g] = (t, wdt, pos - span, st, pos - lo, bits)
        if pos < 1 or pos >= 2*span - 1:
            status = f'OVF@{t}'; break
    growL = len(recL) > len(recR)
    rec = recL if growL else recR
    gs = gate_snapL if growL else gate_snapR
    side = 'L' if growL else 'R'
    print(f"\n{'='*78}\n=== {name}  {spec}  [{status}]  growing side={side}  steps={N:.0e} ===")
    # ratio ladder: cluster frontier records with gap>1.0*t (coarse epochs)
    idx = [i for i in range(len(rec)) if i == 0 or rec[i][0]-rec[i-1][0] > 1.0*rec[i-1][0]]
    ws = [rec[i][1] for i in idx][-9:]
    ts = [rec[i][0] for i in idx][-9:]
    wr = [round(ws[i+1]/ws[i], 4) for i in range(len(ws)-1) if ws[i]]
    tr = [round(ts[i+1]/ts[i], 3) for i in range(len(ts)-1) if ts[i]]
    print(f"  epoch widths : {ws}")
    print(f"  width ratio  : {wr}")
    print(f"  time  ratio  : {tr}")
    print(f"  --- marker words at width-gates (head-relative RLE, growing side) ---")
    for g in GATES:
        if g not in gs:
            continue
        (t, wdt, hp, mst, hr, bits) = gs[g]
        runs = rle(bits)
        print(f"   gate>={g:>5} t={t:>10} width={wdt:>6} head_pos={hp:>7} state={chr(65+mst)} head_idx={hr}")
        print(f"      RLE: {rle_str(runs, 34)}")

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5*10**6
    for name, spec in SPECS:
        run(name, spec, N)
