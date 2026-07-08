#!/usr/bin/env python3
"""
o16 FIXED-POINT CLOSED FORMS + machine extraction (2026-07-08).
Companion to o11_refill_fixedpoint.py -- the same o4/O15/Antihydra fixed-point trick
applied to o16's inner sea engine, plus the tower-sparse-gate / ledger interaction.

o16 = 1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE   (halt = F reads 0, R-side 00-race).
Milestone shape [k | 1^s sea | defect d]; clean sea law (defect==4 pairs):
    T(s) = floor(3s/2) + 2                     (REDUCE_O11_O16: 73,111,168 exact)

Two affine branches and their INTEGER fixed points (solve x = T(x) per parity):
    even s: s' = 3s/2 + 2       fixed point  x_e = -4   ( -x/2 = 2 )
    odd  s: s' = (3s+3)/2       fixed point  x_o = -3   ( 2x = 3x+3 )

THEOREM [two-line proof + exhaustive check]:
  distance to the branch fixed point multiplies by EXACTLY 3/2 on a same-branch step
    even: s'+4 = 3s/2+2+4 = (3/2)(s+4)
    odd : s'+3 = (3s+3)/2+3 = (3/2)(s+3)
  and branch membership is 2-divisibility of that distance (s even <=> 2|s+4;
  s odd <=> 2|s+3). Since 3 is a 2-adic unit each same-branch step lowers v2 of the
  distance by exactly 1, so
    maximal even-run starting at even s = v2(s+4)
    maximal odd-run  starting at odd  s = v2(s+3)          [PROVEN]
  mod-4 dictionary (the residue that drives o16's phase race):
    s=0(4) <=> even & v2(s+4)>=2   s=2(4) <=> v2(s+4)=1
    s=1(4) <=> odd  & v2(s+3)>=2   s=3(4) <=> v2(s+3)=1
  Mirror coords: W=s+4 (even steps EXACTLY x3/2), U=s+3 (odd steps EXACTLY x3/2).
  => o16's residue itinerary is the v2-depth process of a x3/2 orbit -- the SAME object
  as Antihydra (v2/x3/2), o11 ((2,3) at x_e=-8,x_o=-7), o4 (v3/x4/3), o15 (v3/x8/3).

CRITICALITY (o16's row): run-cap slope log2(3/2)=0.585 [depth process, PROVEN];
budget = leading block k, RESETTING at each refill, drained at the CONSTANT rate -1
per sea step (k->k-1, catalogue "o11 with step -1"); e(k)=k self-determined terminal
index (vs o11's e=floor(k/4)). The drain does NOT couple to the residue itinerary, so
the ratio criterion is INAPPLICABLE within epochs (no in-epoch halt branch); ALL
fatality sits at the terminal phase-race, ONE exposure per epoch.

TOWER-SPARSE-GATE / LEDGER interaction (o16's distinguishing costume): the halt gate
(E/F rightward alternation reads a 0 at an F-phase cell before a 1 at an E-phase cell)
is entered only during the doubly-exponential refill reconfiguration -- 15 F-visits in
12M steps. So o16's residue LEDGER (the sea s mod 4) is READ only at the refill index,
even sparser than o11 (whose collapse is read every epoch). Gate sparsity = the ledger
is sampled at the doubly-exp refill orbit, and RESETTING wipes s between reads.
"""
import sys, math

def T(s):  return (3 * s) // 2 + 2
def v2(n): return (n & -n).bit_length() - 1
def run_len(s):
    p = s & 1; r = 0
    while (s & 1) == p:
        r += 1; s = T(s)
    return r
def closed(s): return v2(s + 3) if s & 1 else v2(s + 4)

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

def rle_blocks(tape, lo, hi):
    blocks = []; i = lo
    while i <= hi:
        if tape[i]:
            j = i
            while j <= hi and tape[j]: j += 1
            blocks.append(j - i); i = j
        else: i += 1
    return blocks

O16 = "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE"

if __name__ == "__main__":
    MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    N    = int(sys.argv[2]) if len(sys.argv) > 2 else 12_000_000

    # ---- exhaustive fixed-point run-law check ----
    bad = sum(1 for s in range(1, MMAX + 1) if run_len(s) != closed(s))
    print(f"[PROVEN] run closed forms (even v2(s+4), odd v2(s+3)) exhaustive s=1..{MMAX}: "
          f"{MMAX-bad}/{MMAX} exact")
    bad4 = sum(1 for s in range(1, MMAX + 1)
               if (s % 4 == 0) != (s % 2 == 0 and v2(s + 4) >= 2)
               or (s % 4 == 2) != (s % 2 == 0 and v2(s + 4) == 1)
               or (s % 4 == 1) != (s % 2 == 1 and v2(s + 3) >= 2)
               or (s % 4 == 3) != (s % 2 == 1 and v2(s + 3) == 1))
    print(f"[PROVEN] mod-4 <-> depth-level dictionary: {MMAX-bad4}/{MMAX} exact")
    badw = 0
    for s in range(1, 5000):
        if s % 2 == 0 and 2 * (T(s) + 4) != 3 * (s + 4): badw += 1
        if s % 2 == 1 and 2 * (T(s) + 3) != 3 * (s + 3): badw += 1
    print(f"[PROVEN] mirror coords (W=s+4 x3/2 even, U=s+3 x3/2 odd): "
          f"{'exact' if badw==0 else f'{badw} FAIL'} on s<5000")

    # ---- real machine: sea orbit, run law on-orbit, gate sparsity ----
    M = parse(O16); SZ = 1 << 23; tape = bytearray(SZ)
    pos = SZ // 2; st = 0; lo = hi = pos; step = 0
    seas = []; ks = []; times = []; last = None; Fentries = 0
    while step < N:
        r = tape[pos]; act = M[st][r]
        if act is None: break
        if st == 5: Fentries += 1
        if st == 0 and pos >= hi:
            b = rle_blocks(tape, lo, hi)
            if len(b) >= 3 and all(x == 1 for x in b[1:-1]) and b[-1] == 4:
                k = b[0]; s = len(b) - 2
                if (k, s) != last:
                    seas.append(s); ks.append(k); times.append(step); last = (k, s)
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    print(f"\n[OBSERVED] o16 real orbit ({N} steps): defect-4 milestones = {len(seas)}")
    print(f"  sea:   {seas}")
    print(f"  k:     {ks}")
    good = sum(1 for i in range(len(seas) - 1) if seas[i + 1] == T(seas[i]))
    print(f"  clean sea law s'=floor(3s/2)+2 on consecutive pairs: {good}/{len(seas)-1} "
          f"(rest = refill boundary jumps)")
    # run law on-orbit: iterate T from a clean seed and confirm runs = closed form
    onc = ono = 0
    for seed in [73, 111, 168]:
        if run_len(seed) == closed(seed): onc += 1
        ono += 1
    print(f"  run closed form at clean sea seeds {{73,111,168}}: {onc}/{ono}")
    print(f"\n[OBSERVED] TOWER-SPARSE GATE: F-state visits (ledger reads) in {N} steps = "
          f"{Fentries}  (o11 collapse fires every epoch; o16 only at doubly-exp refills)")
    print(f"[OBSERVED] max run on clean seeds <= log2(s+4): "
          f"{max(closed(s) for s in [73,111,168])} <= "
          f"{max(math.log2(s+4) for s in [73,111,168]):.1f}")

    print("\nCRITICALITY ROW: run-cap slope log2(3/2)=0.585 [PROVEN depth process]; "
          "budget = k, RESETTING, deterministic drain -1/sea-step, e(k)=k; single-run kill "
          "N/A; per-epoch exposure = 1 terminal draw; ratio criterion INAPPLICABLE in-epoch.")
    print("Fixed-point closed forms [PROVEN]; orbit facts [OBSERVED]. "
          "No machine decided. No label upgraded.")
