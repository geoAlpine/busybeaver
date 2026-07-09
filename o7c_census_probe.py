#!/usr/bin/env python3
"""o7c_census_probe.py -- Task B completeness probe. Independently re-confirm (raw TM, this run)
that the named cryptids NOT in the PAPER_CENSUS table -- o5, o8, o12 -- are Type-I x(p/q) value
processes (a single clean multiplier on their reset/collapse orbit), and contrast o7 (no single
multiplier). Crude reset-peak extraction: track the longest 1-run (for x3/2 machines) or longest
0-run (for the x4/3 gap machine o5) and read consecutive local-maxima ratios.

This is [OBSERVED] recon re-confirming banked [VERIFIED] catalogue values (CATALOGUE_O2_O5,
CATALOGUE_O7_O12, MAHLER_SEA_CLASSIFICATION). It decides nothing. No machine decided.
"""
import sys

SPECS = {
    "o5":  "1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB",   # Erdos ternary, x4/3, 0^k gap halt
    "o8":  "1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE",   # Antihydra family, x3/2 nested
    "o12": "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB",   # x3/2 sea machine
    "o7":  "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC",   # NON-Type-I: even x3/2 / odd x1/2 halving
}
# which run to track for the reset/collapse peak: '1' longest one-run, '0' longest zero-run
TRACK = {"o5": "0", "o8": "1", "o12": "1", "o7": "1"}

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

def max_run(tape, lo, hi, sym):
    best = cur = 0
    for i in range(lo, hi + 1):
        if tape[i] == sym:
            cur += 1; best = max(best, cur)
        else:
            cur = 0
    return best

def probe(name, spec, cap):
    M = parse(spec); track = 1 if TRACK[name] == '1' else 0
    SZ = 1 << 23
    tape = bytearray(SZ); pos = SZ // 2; st = 0; step = 0; lo = hi = pos
    peaks = []; last_peak = 0; rising = True
    while step < cap:
        r = tape[pos]; act = M[st][r]
        if act is None:
            print(f"  {name}: RAW HALT at step {step}"); return
        w, d, ns = act; tape[pos] = w; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
        # sample the extreme run periodically at left/right frontier turn-arounds
        if step % 4096 == 0:
            mr = max_run(tape, lo, hi, track)
            # record a new running-max local maximum (reset peak)
            if mr > last_peak:
                last_peak = mr
    # collect the coarse local maxima of the max-run signal by resampling
    sig = []
    # re-run lightweight: record max-run at coarse grid, extract strict running maxima
    tape = bytearray(SZ); pos = SZ // 2; st = 0; step = 0; lo = hi = pos
    grid = max(cap // 2000, 1)
    while step < cap:
        r = tape[pos]; act = M[st][r]
        if act is None: break
        w, d, ns = act; tape[pos] = w; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
        if step % grid == 0:
            sig.append(max_run(tape, lo, hi, track))
    # strict running maxima = reset peaks
    peaks = []
    m = 0
    for v in sig:
        if v > m:
            m = v; peaks.append(v)
    # dedup consecutive equal, keep the growth sequence
    peaks = [p for i, p in enumerate(peaks) if i == 0 or p != peaks[i-1]]
    tail = peaks[-8:] if len(peaks) >= 8 else peaks
    ratios = [round(tail[i+1]/tail[i], 3) for i in range(len(tail)-1)]
    print(f"  {name} ({'0-run' if track==0 else '1-run'} peaks): {tail}")
    print(f"       consecutive ratios: {ratios}")

def o8_reset_orbit(cap):
    """Proper milestone extraction for o8 (Antihydra shape 0 1^a 0 1^b, milestone = state A at
    left frontier reading 0 with a 1 to the right). Clean reset orbit = a-values at b=1.
    Mirrors x32_o7_reduction's D-milestone method. Independently re-confirms o8's x3/2."""
    M = parse(SPECS["o8"])
    SZ = 1 << 23
    tape = bytearray(SZ); pos = SZ // 2; st = 0; step = 0; lo = hi = pos
    resets = []
    def parse_ms(s):
        s = s.strip('0'); ones=[]; zeros=[]; i=0
        while i < len(s):
            j=i
            while j < len(s) and s[j]==s[i]: j+=1
            (ones if s[i]=='1' else zeros).append(j-i); i=j
        if any(z!=1 for z in zeros): return None
        if len(ones)==2: return (ones[0],ones[1])
        if len(ones)==1: return (ones[0],0)
        return None
    while step < cap:
        r = tape[pos]; act = M[st][r]
        if act is None: break
        if st == 0 and pos <= lo and r == 0 and tape[pos+1] == 1:      # state A, left frontier
            ab = parse_ms(''.join(map(str, tape[lo:hi+1])))
            if ab is not None and ab[1] == 1:                          # clean reset b=1
                resets.append(ab[0])
        w,d,ns = act; tape[pos]=w; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    # dedup consecutive
    orb = [p for i,p in enumerate(resets) if i==0 or p!=resets[i-1]]
    tail = orb[-14:]
    ratios = [round(tail[i+1]/tail[i],3) for i in range(len(tail)-1)]
    print(f"  o8 clean-reset a (b=1), state-A milestone: {tail}")
    print(f"       consecutive ratios: {ratios}   (inner chain -> 3/2 = Antihydra family)")

if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 8_000_000
    print(f"Reset/collapse-peak multiplier probe (raw TM, cap={cap:,} steps):")
    print("[NOTE] the generic max-run auto-probe below reproduces the KNOWN 'wrong event' artifact")
    print("(the sqrt(t) ENVELOPE, not the reset orbit) that the catalogues warn about -- so its")
    print("ratios are NOT a clean confirmation. The correct hand-milestone extraction follows for o8.")
    for name in ("o5", "o8", "o12", "o7"):
        probe(name, SPECS[name], cap)
    print("\nProper hand-milestone extraction (independent Type-I re-confirmation):")
    o8_reset_orbit(cap)
    print("No machine decided. No label upgraded.")
