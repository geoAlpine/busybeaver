#!/usr/bin/env python
"""
o10 / o15 OUTER-LAYER TRANSPARENCY PROBE  (2026-07-25)

Task: decide whether o10's OUTER refill orbit or o15's OUTER collision structure
admits an EXACT forall-transport of the x2 (carry-transparent) kind -- i.e. whether
the HALT predicate is decided by a TRANSPARENT (bounded/predictable-carry) outer layer,
or whether it inherits the INNER Mahler (base-3/2, base-8/3) opacity.

Everything re-derived against the RAW TM with a bounded-tape simulator (config planting).
No cryptid_map tags trusted (CRYPTID_REDUCTIONS.md warns they were over-fit).

o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC   (halt = state F reads 0)
o15 = 1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA   (halt = state A reads 1)
"""
from __future__ import annotations

O10 = "1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC"
O15 = "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"


def parse(spec):
    m = {}
    for i, g in enumerate(spec.split("_")):
        st = chr(ord("A") + i)
        m[st] = {}
        for s in (0, 1):
            w, mv, nx = g[s * 3:s * 3 + 3]
            m[st][s] = (int(w) if w in "01" else 0, mv, nx)
    return m


HALT = {"Z", "H", "-"}


class Machine:
    """Raw TM on a dict tape; supports planting arbitrary configs and running to halt/budget."""

    def __init__(self, spec):
        self.tbl = parse(spec)

    def run_from(self, tape, head, state, budget):
        """tape: dict[int]->0/1. Returns (halted, steps, head, state, tape)."""
        tape = dict(tape)
        steps = 0
        while steps < budget:
            sym = tape.get(head, 0)
            w, mv, nx = self.tbl[state][sym]
            tape[head] = w
            head += 1 if mv == "R" else -1
            steps += 1
            if nx in HALT:
                return True, steps, head, state, tape
            state = nx
        return False, steps, head, state, tape

    def run_blank(self, budget):
        return self.run_from({}, 0, "A", budget)


def blocks_of(tape):
    """Return (lo, hi, run-length-encoding list of (sym,len)) over the occupied span."""
    if not tape:
        return 0, 0, []
    lo, hi = min(tape), max(tape)
    rle = []
    for i in range(lo, hi + 1):
        s = tape.get(i, 0)
        if rle and rle[-1][0] == s:
            rle[-1][1] += 1
        else:
            rle.append([s, 1])
    return lo, hi, [(s, n) for s, n in rle]


# ============================================================================
print("=" * 78)
print("PART 0.  Simulator self-check on BB champions")
print("=" * 78)
for spec, exp in [("1RB1LB_1LA1RZ", 6), ("1RB1RZ_1LB0RC_1LC1LA", 21),
                  ("1RB1LB_1LA0LC_1RZ1LD_1RD0RA", 107)]:
    h, st, *_ = Machine(spec).run_blank(1000)
    print(f"  {spec:32s} halted={h} steps={st} expected={exp}  {'OK' if st==exp else 'FAIL'}")

# ============================================================================
print("\n" + "=" * 78)
print("PART 1.  o10 HALT MECHANIC:  C/F eat-sweep of a run of L ones halts iff L ODD")
print("=" * 78)
# State C entering a run of 1s from the right, moving left. Per O10_REDUCTION.md:
# C:1->0LF, F:1->0LC, F:0->HALT, C:0->1LD(exit). Plant: head in state C at the
# rightmost 1 of a maximal run of L ones with a 0 to the left, and 0 to the right.
mo10 = Machine(O10)
print("  L  : halted? (expect halt iff L odd)")
for L in range(1, 11):
    # tape: positions 1..L are 1; position 0 is 0 (left stop); position L+1 is 0.
    tape = {i: 1 for i in range(1, L + 1)}
    h, steps, head, state, _ = mo10.run_from(tape, L, "C", 10000)
    exp = (L % 2 == 1)
    print(f"  L={L:2d}: halted={h!s:5s} steps={steps:4d}  expect_halt={exp!s:5s} "
          f"{'OK' if h == exp else 'FAIL'}")

# ============================================================================
print("\n" + "=" * 78)
print("PART 2.  o10 INNER ORBIT from blank tape:  m -> ceil(3m/2), b decrement, eat-length parity")
print("=" * 78)
# Recurrent config (state E, head at left end): 1 0^a 1^b 0 1 with a = 2m-8.
# Instrument the RAW blank-tape run: detect state-E left-end visits, decode (a,b) -> m.
def o10_epochs(budget):
    tbl = mo10.tbl
    tape = {}
    head = 0
    state = "A"
    steps = 0
    seen = []
    minhead = 0  # global leftmost cell reached so far
    while steps < budget:
        # Cheap trigger: only attempt a (costly) decode when the head sets a NEW
        # leftmost record while in state E -- the left end of 1 0^a 1^b 0 1.
        if head < minhead:
            minhead = head
            if state == "E":
                lo, hi, rle = blocks_of(tape)
                if head <= lo and len(rle) >= 5 and rle[0] == (1, 1) \
                        and rle[1][0] == 0 and rle[2][0] == 1 and rle[1][1] % 2 == 0:
                    a = rle[1][1]; b = rle[2][1]; m = (a + 8) // 2
                    if not seen or seen[-1][1] != m:
                        seen.append((steps, m, b, a))
        sym = tape.get(head, 0)
        w, mv, nx = tbl[state][sym]
        tape[head] = w
        head += 1 if mv == "R" else -1
        steps += 1
        if nx in HALT:
            return seen, steps, True
        state = nx
    return seen, steps, False

seen, steps, halted = o10_epochs(2_000_000)
print(f"  blank run to {steps} steps, halted={halted}; E-left-end snapshots (dedup by m):")
import math
prev = None
uniq = []
for (stp, m, b, a) in seen:
    if prev is None or m != prev:
        uniq.append((stp, m, b, a))
        prev = m
for i, (stp, m, b, a) in enumerate(uniq[:22]):
    pred = math.ceil(3 * uniq[i-1][1] / 2) if i > 0 else None
    ok = "" if pred is None else (" ceil(3m/2)_OK" if pred == m else f" MISMATCH(pred {pred})")
    print(f"    step={stp:9d}  m={m:6d}  b={b:3d}  a=2m-8={a:6d}  a_even={a%2==0}{ok}")

# ============================================================================
print("\n" + "=" * 78)
print("PART 3.  o10 UNDERFLOW BASE RULE  (raw TM from planted 1 0^{2m-8} 1^b 0 1)")
print("=" * 78)
# Build the clean config directly and run, classify halt vs refill for small b.
def o10_plant(m, b):
    a = 2 * m - 8
    # tape: 1 0^a 1^b 0 1 ; head at left end (pos 0), state E
    tape = {}
    pos = 0
    tape[pos] = 1; pos += 1
    for _ in range(a):
        tape[pos] = 0; pos += 1
    for _ in range(b):
        tape[pos] = 1; pos += 1
    tape[pos] = 0; pos += 1
    tape[pos] = 1; pos += 1
    return tape

print("  Testing halt vs continue for terminal b in {0,1,2}, m=5..20  (budget 5e6):")
print("  Predicted: b=0 halt iff m odd; b=1 halt iff m=2 mod4; b=2 halt iff m=3 mod4")
for b in (0, 1, 2):
    row = []
    for m in range(5, 21):
        tape = o10_plant(m, b)
        h, st, *_ = mo10.run_from(tape, 0, "E", 5_000_000)
        row.append((m, h))
    # predicted rule
    def pred(m, b):
        if b == 0: return m % 2 == 1
        if b == 1: return m % 4 == 2
        if b == 2: return m % 4 == 3
    bad = [(m, h, pred(m, b)) for m, h in row if h != pred(m, b)]
    halts = [m for m, h in row if h]
    print(f"    b={b}: halt at m={halts}   rule-mismatches={bad if bad else 'NONE'}")

# ============================================================================
print("\n" + "=" * 78)
print("PART 4.  o10 TRANSPARENCY TEST:  is the HALT predicate a function of the OUTER")
print("         layer only, or does it read the INNER ceil(3m/2) parity (base-3/2) ?")
print("=" * 78)
# Build S_halt = {C_t : m_t odd} from the ceil(3m/2) orbit from m=6, C_t cumulative b consumed.
m = 6        # EXACT big-int:  ceil(3m/2) = (3m+1)//2  (math.ceil(3*m/2) overflows float past 2^53)
C = 0
Shalt = []
mparity = []
NSTEP = 5000
for t in range(NSTEP):
    dec = 1 + (m % 2)  # b loses 1+[m odd]
    C += dec
    if m % 2 == 1:
        Shalt.append(C)
    mparity.append(m % 2)
    m = (3 * m + 1) // 2
print("  ceil(3m/2)-from-6 parity sequence (m odd?) first 48:")
print("   ", "".join(str(p) for p in mparity[:48]))
# Is the parity sequence eventually periodic with small period? Test periods up to 200.
def has_small_period(seq, maxp=200, tail=2000):
    s = seq[:tail]
    for p in range(1, maxp + 1):
        if all(s[i] == s[i + p] for i in range(len(s) - p)):
            return p
    return None
p = has_small_period(mparity)
print(f"  small period (<=200) in the m-parity string (2000 terms)? {p if p else 'NONE FOUND'}")
for N in (120, 500, 2000, 5000):
    print(f"  odd-density over {N:5d} steps = {sum(mparity[:N]) / N:.4f}  (base-3/2 equidistribution ~0.5)")
print(f"  S_halt first 20 = {Shalt[:20]}")
print("  --> The halt predicate S_halt = {C_t : m_t ODD} is DEFINED by the inner-orbit")
print("      parity string above.  Its transparency = transparency of ceil(3m/2) parity.")

print("\nDONE part o10.")
