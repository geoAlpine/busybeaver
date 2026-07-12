#!/usr/bin/env python3
"""x2lb_crosscheck.py -- cross-check the PURE Layer-B binary-counter odometer
(lean/X2.lean §5n `LayerB`) against the REAL doubling-phase orbit.

Mirrors the Lean defs EXACTLY:
  binVal(bs) = sum bit_i * 2^i           (LSB first)
  binInc     = ripple-carry +1
  odoEntry K = toBits K 0 (all clear),  odoFinal K = toBits K (2^K-1) (all set)
  T_model    = odoValue(odoFinal K) - odoValue(odoEntry K) = 2^K - 1

Checks:
  (1) the +1 law: binVal(binInc bs) = binVal bs + 1  (incl. across ripple)
  (2) the level-j overflow threshold = 2^j - 1
  (3) the ripple depth = run of leading 1s, <= width  (matches x2wf_pure.py)
  (4) the digit-doubling chain 1,5,13,29,61,... = carryDigit = 2^{n+2}-3
  (5) STEP-COUNT: T_model = 2^K-1 vs the REAL tape round-trip count T_tape
      (x2wf_measure.py: 3852 @K=10, 9729 @K=11, 19470 @K=12) -- reports the GAP.
"""

# ---- exact mirror of the Lean LayerB defs ----
def binVal(bs):                      # bs: list of 0/1, LSB first
    return sum(b << i for i, b in enumerate(bs))

def binInc(bs):
    bs = bs[:]
    i = 0
    while i < len(bs) and bs[i] == 1:
        bs[i] = 0
        i += 1
    if i < len(bs):
        bs[i] = 1
    else:
        bs.append(1)
    return bs

def ripple_depth(bs):
    d = 0
    for b in bs:
        if b == 1: d += 1
        else: break
    return d

def toBits(w, v):
    return [(v >> i) & 1 for i in range(w)]

def carryDigit(n):
    d = 1
    for _ in range(n): d = 2 * d + 3
    return d

# real tape round-trip counts (x2wf_measure.py, confirmed this session for g=2,3)
T_TAPE = {10: 3852, 11: 9729, 12: 19470}

if __name__ == "__main__":
    # (1) +1 law over a full width-6 sweep (crosses all ripple depths)
    ok1 = all(binVal(binInc(toBits(6, v))) == v + 1 for v in range(2**6 - 1))
    print(f"(1) +1 law (binVal(binInc)=binVal+1), width6, v=0..62: {'PASS' if ok1 else 'FAIL'}")

    # (2) threshold = 2^j - 1
    thr = [binVal([1] * j) for j in range(1, 6)]
    print(f"(2) level-j overflow threshold 2^j-1: {thr} = {[2**j - 1 for j in range(1,6)]} "
          f"{'PASS' if thr == [2**j-1 for j in range(1,6)] else 'FAIL'}")

    # (3) ripple depth = run of leading ones (a level-3 carry ripples 3 then sets bit 3)
    st = [1,1,1,0,0,1]
    inc = binInc(st)
    ok3 = (ripple_depth(st) == 3 and inc == [0,0,0,1,0,1])
    print(f"(3) level-3 carry {st}->{inc}, depth={ripple_depth(st)}: {'PASS' if ok3 else 'FAIL'}")

    # (4) digit-doubling chain
    chain = [carryDigit(n) for n in range(5)]
    ok4 = (chain == [1,5,13,29,61] == [2**(n+2)-3 for n in range(5)])
    print(f"(4) carryDigit chain {chain} = 2^(n+2)-3: {'PASS' if ok4 else 'FAIL'}")

    # (5) STEP-COUNT cross-check: T_model vs T_tape
    print("(5) STEP-COUNT cross-check (T_model = 2^K-1 vs real tape round-trips):")
    print(f"    {'K':<4}{'T_model=2^K-1':<16}{'T_tape':<10}{'ratio':<8}")
    for K in (10, 11, 12):
        Tm = 2**K - 1
        Tt = T_TAPE[K]
        print(f"    {K:<4}{Tm:<16}{Tt:<10}{Tt/Tm:<8.3f}")
    print("    => MISMATCH (expected): the pure-counter tick is one CARRY; the tape")
    print("       chew-start is one block-decrement-by-2.  One carry at level j spans a")
    print("       Theta(2^j) tape block-chew, so T_tape ~ (K-const)*2^K > T_model=2^K-1.")
    print("    DECISIVE: T_tape has NO clean recurrence -- 9729 = 2*3852 + 2025 but")
    print(f"       19470 = 2*9729 + {19470 - 2*9729} (residuals 2025 vs {19470-2*9729} differ), reflecting the")
    print("       g-parity boundary corrections: leading digit 2039 != 2045, the -4K+8")
    print("       residual.  So NO clean pure register reproduces T_tape exactly; it is")
    print("       irreducibly tape-determined.  Reproducing it tick-for-tick is the")
    print("       tape<->register faithfulness lemma (Layer C), the design's multi-session")
    print("       wall.  Layer B is faithful to the counter STRUCTURE (checks 1-4 PASS),")
    print("       NOT to the tape granularity; Layer B alone does NOT decide the machine.")
