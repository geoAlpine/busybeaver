#!/usr/bin/env python3.11
"""
SQW -- explicit multi-symbol single-tape TM that CHECKS perfect-square-ness EVERY cycle.

Analogue of pow2w_machine.py but for perfect squares {1,4,9,16,25,...}.

Cycle-start state: CS.
Milestone config = (state CS, head at LEFT end of a clean contiguous block 1^v, rest blank).

Each cycle from CS on clean 1^v (with v=k^2):
  1. DUPLICATE  1^v -> 1^v M 1^v.
  2. CHECK right copy is a perfect square by subtracting consecutive odds 1,3,5,...
     A perfect square k^2 = 1+3+5+...+(2k-1).  We repeatedly subtract the next odd from the
     right copy.  If it hits EXACTLY 0 after subtracting the k-th odd (2k-1) -> PASS, v=k^2.
     If the remaining right block is > 0 but SMALLER than the next odd (overshoot) -> HALT.
  3. On PASS: the next odd after 2k-1 is 2k+1.  ADD (2k+1) ones to the LEFT copy ->
     (k+1)^2 = v + (2k+1).  Erase M and right region.  Result clean 1^{(k+1)^2}, return to CS.
  4. Loop forever.

CRUX (remember 2k+1): we keep a scratch "ODD" tally to the RIGHT of the right copy.  Before each
subtraction we INCREASE the odd tally by 2 (it starts at 1).  We subtract that many 1's from the
right copy (crossing them with X).  On exact-0 PASS, the ODD tally currently holds (2k-1); we
increase it by 2 -> (2k+1), then move those tally-ones onto the LEFT copy as appended 1's.

ENCODING / layout during a check:
   [ left copy 1^v ] M [ right copy: 1's and X's ] D [ odd tally: 1's ] (rest blank)
   D is a marker separating right copy from the odd tally.

Alphabet (ints): B=0 blank, O=1 one, M=2 left-wall marker, X=3 crossed (subtracted) one,
                 D=4 tally-separator marker, T=5 tally-one, A=6 copy-progress mark.
"""

B, O, M, X, D, T, A, S = 0, 1, 2, 3, 4, 5, 6, 7
HALT = None


def run(DT, cells, head, state, cap=2_000_000):
    tape = dict(cells)
    for t in range(cap):
        s = tape.get(head, 0)
        row = DT.get(state)
        if row is None or s not in row:
            return ("STUCK", t, state, s, tape, head)
        tr = row[s]
        if tr is None:
            return ("HALT", t, tape, head, state)
        w, mv, ns = tr
        tape[head] = w
        head += mv
        state = ns
    return ("CAP", cap, tape, head, state)


# ===========================================================================
# TRANSITION TABLE
# ===========================================================================
DTAB = {

    # ----- DUPLICATE: 1^v -> 1^v M 1^v.  Enter at CS, head on leftmost O. -----
    "CS":       {O: (O, +1, "CS_R"), B: (B, +1, "HALT")},
    "CS_R":     {O: (O, +1, "CS_R"), B: (M, -1, "CS_BK")},   # write M at right end of left block
    "CS_BK":    {O: (O, -1, "CS_BK"), M: (M, -1, "CS_BK"), B: (B, +1, "DPICK")},

    # DPICK: leftmost un-copied O (skip A); mark it A; carry one O to far right (after M block).
    "DPICK":    {A: (A, +1, "DPICK"), O: (A, +1, "DCARRY"), M: (M, +1, "DDONE")},
    "DCARRY":   {O: (O, +1, "DCARRY"), A: (A, +1, "DCARRY"), M: (M, +1, "DCARRY2")},
    "DCARRY2":  {O: (O, +1, "DCARRY2"), B: (O, -1, "DRET")},
    "DRET":     {O: (O, -1, "DRET"), M: (M, -1, "DRETL")},
    "DRETL":    {A: (A, -1, "DRETL"), O: (O, -1, "DRETL"), B: (B, +1, "DPICK")},

    # DDONE: hit M with all left O's marked A. Restore A->O, go to CHECK init.
    "DDONE":    {O: (O, -1, "DDONE"), M: (M, -1, "DDONEL")},
    "DDONEL":   {A: (A, -1, "DDONEL"), O: (O, -1, "DDONEL"), B: (B, +1, "UNMARK")},
    "UNMARK":   {A: (O, +1, "UNMARK"), O: (O, +1, "UNMARK"), M: (M, +1, "INIT_TALLY")},
    # tape now: 1^v M 1^v, head at leftmost O of the RIGHT copy.

    # ----- INIT_TALLY: place the odd-tally region "D T" (separator + one tally-one = odd value 1). -----
    # Walk right to end of right copy, then write D then one T, then return to left of right copy.
    "INIT_TALLY":   {O: (O, +1, "INIT_TALLY"), X: (X, +1, "INIT_TALLY"), B: (D, +1, "INIT_T1")},
    "INIT_T1":      {B: (T, -1, "INIT_BK")},
    "INIT_BK":      {T: (T, -1, "INIT_BK"), D: (D, -1, "INIT_BK2")},
    "INIT_BK2":     {O: (O, -1, "INIT_BK2"), X: (X, -1, "INIT_BK2"), M: (M, +1, "SUB_BEGIN")},
    # head at leftmost cell of right copy. tally currently holds 1 (=first odd).

    # ----- SUBTRACTION ROUND: subtract (current odd = #T's) ones from right copy. -----
    # We pair each T in the tally with one O in the right copy: cross one O (O->X) per T consumed.
    # Method: for one round, walk right-copy crossing O's, but we need to cross exactly (#T) of them.
    # Implementation: repeatedly (a) find leftmost un-consumed T (mark it consumed=use X-on-tally? we
    # instead COUNT down by temporarily) ... Simpler: cross one O per T by a carry loop.
    #
    # SUB_BEGIN: head at leftmost cell of right copy. Find leftmost O (skip X). If none (all X) -> the
    # right copy is exhausted; decide PASS/HALT based on whether tally was fully consumed THIS round.
    #
    # We track per-round consumption by marking tally-T's as "spent" using value... reuse: we cross an O
    # for each T, walking T's one at a time. Use a sub-marker on the tally: convert T->A while spending,
    # then restore A->T after the round (so tally length is preserved = current odd).
    #
    # Round loop:
    #   SUB_NEXT_T: go to tally, find leftmost T (skip spent A).
    #       if found T: mark it A (spent), go cross one O in right copy.
    #       if no T (all A): round complete -> restore A->T, then go to NEXT round (odd+=2) OR if right
    #                        copy fully crossed exactly -> PASS handling.
    #   After spending a T we CROSS one O. If no O available (right copy exhausted mid-round) -> overshoot.

    # Start a round: ensure we're positioned, then look for a T to spend.
    "SUB_BEGIN":    {O: (O, +1, "SUB_BEGIN"), X: (X, +1, "SUB_BEGIN"), D: (D, +1, "SUB_FINDT")},
    # SUB_FINDT: at tally, find leftmost T to spend.
    "SUB_FINDT":    {A: (A, +1, "SUB_FINDT"), T: (A, -1, "SUB_GOCROSS"), B: (B, -1, "SUB_RESTORE_L")},
    # No more T this round (hit B right of tally). Walk LEFT restoring A->T back to D, then check empty.
    # SUB_GOCROSS: spent a T (now head just left of it / on prev tally cell). Walk left to right copy,
    # cross leftmost remaining O. If right copy has no O left -> overshoot path.
    "SUB_GOCROSS":  {A: (A, -1, "SUB_GOCROSS"), T: (T, -1, "SUB_GOCROSS"), D: (D, -1, "SUB_CROSS")},
    "SUB_CROSS":    {X: (X, -1, "SUB_CROSS"), O: (X, +1, "SUB_AFTER"),  # cross the leftmost-from-right O
                     M: (M, +1, "SUB_OVERSHOOT")},  # reached M w/o finding O => right copy exhausted mid-round
    # Wait: SUB_CROSS walks LEFT crossing X's then crosses the FIRST O it meets. But that crosses the
    # RIGHTMOST O of the still-present O run (since X's accumulate on the right of the O-run? no).
    # The right copy is O...O then X...X (we cross from the right end inward). Let's define: O's on the
    # left, X's on the right. So crossing the rightmost O each time keeps O's contiguous on the left.
    # SUB_CROSS comes from D going left: first cells are X's (already crossed), then O's. The FIRST O
    # from the right is the rightmost O. Cross it -> X. Good. Then go back to spend next T.
    "SUB_AFTER":    {X: (X, +1, "SUB_AFTER"), D: (D, +1, "SUB_FINDT")},  # back to tally for next T
    # If we hit M while scanning left for an O: the O-run was empty => exhausted with tally not done.
    # Distinguish: exhausted exactly at round boundary is fine (handled in SUB_ROUND_DONE). Exhausted
    # MID-round (a T still wanted an O) => overshoot.
    "SUB_OVERSHOOT": {M: (M, +1, "HALT_PREP"), O: (O, +1, "HALT_PREP"), B: (B, +1, "HALT_PREP"),
                      X: (X, +1, "HALT_PREP"), D: (D, +1, "HALT_PREP"), T: (T, +1, "HALT_PREP"),
                      A: (A, +1, "HALT_PREP")},

    # SUB_RESTORE_L: tally fully spent this round (all A). Walk LEFT restoring A->T until D.
    #   Then check right copy:
    #   if right copy has 0 O's left (all X) -> PASS (exact square: subtracted 1+3+..+(2k-1)=k^2).
    #   else start NEXT round with odd+=2 (append 2 more T's to tally) and continue.
    "SUB_RESTORE_L": {A: (T, -1, "SUB_RESTORE_L"), T: (T, -1, "SUB_RESTORE_L"), D: (D, -1, "SRD_SCAN")},
    # head now just left of D (in right copy region). Scan left for any O.
    "SRD_SCAN":     {X: (X, -1, "SRD_SCAN"), O: (O, -1, "SRD_FOUNDO"), M: (M, +1, "PASS_FROM_M")},
    # SRD_FOUNDO: right copy still has O's -> grow odd by 2 (append 2 T's) then next round.
    "SRD_FOUNDO":   {O: (O, -1, "SRD_FOUNDO"), X: (X, -1, "SRD_FOUNDO"), M: (M, +1, "GROW_GO")},
    # go to tally end and append 2 T's, then begin next round.
    "GROW_GO":      {O: (O, +1, "GROW_GO"), X: (X, +1, "GROW_GO"), D: (D, +1, "GROW_TO_END")},
    "GROW_TO_END":  {T: (T, +1, "GROW_TO_END"), B: (T, +1, "GROW_T2")},
    "GROW_T2":      {B: (T, -1, "GROW_BK")},
    "GROW_BK":      {T: (T, -1, "GROW_BK"), D: (D, -1, "GROW_BK2")},
    "GROW_BK2":     {O: (O, -1, "GROW_BK2"), X: (X, -1, "GROW_BK2"), M: (M, +1, "SUB_BEGIN")},

    # ----- PASS: right copy exhausted EXACTLY. tally currently holds (2k-1) T's. -----
    # PASS_FROM_M entered head just right of M (on first cell of right copy, which is all X now).
    # Layout: 1^v M X^v D T^(2k-1), head on the first X (or on D if v==0, impossible since v>=1).
    # Plan: (1) grow tally to 2k+1; (2) erase M and all X's to B  ->  1^v ___ D T^(2k+1);
    #       (3) GATHER the T's leftward against the left block, T->O; erase D;  ->  1^{v+(2k+1)};
    #       (4) home to leftmost O, state CS.

    # (1) walk right to tally end, append 2 T's.
    "PASS_FROM_M":  {X: (X, +1, "PASS_TO_D"), D: (D, +1, "PASS_GROW_END")},
    "PASS_TO_D":    {X: (X, +1, "PASS_TO_D"), D: (D, +1, "PASS_GROW_END")},
    "PASS_GROW_END":{T: (T, +1, "PASS_GROW_END"), B: (T, +1, "PASS_GROW_T2")},
    "PASS_GROW_T2": {B: (T, -1, "PASS_ERASE_BK")},
    # (2) walk left to M erasing X's; erase M too; result 1^v ___ D T^(2k+1).
    "PASS_ERASE_BK":{T: (T, -1, "PASS_ERASE_BK"), D: (D, -1, "PASS_ERASE_X"),
                     B: (B, -1, "PASS_ERASE_BK")},
    "PASS_ERASE_X": {X: (B, -1, "PASS_ERASE_X"), M: (B, +1, "PASS_ERASE_D"),
                     B: (B, -1, "PASS_ERASE_X")},
    # erase the D separator too (head just right of erased M). Walk right to D, erase it.
    "PASS_ERASE_D": {B: (B, +1, "PASS_ERASE_D"), D: (B, +1, "PASS_GHOME")},
    # head just right of erased D, on first T.  Tape: 1^v ___gap___ T^(2k+1) ___.
    # First place a RIGHT SENTINEL S just past the T-run's right end (so the gather has a terminator).
    "PASS_GHOME":   {T: (T, +1, "PASS_PUT_S"), B: (B, +1, "PASS_GHOME")},  # walk right to run end
    "PASS_PUT_S":   {T: (T, +1, "PASS_PUT_S"), B: (S, -1, "PASS_GLEFT")},  # write S past run, go left
    "PASS_GLEFT":   {T: (T, -1, "PASS_GLEFT"), B: (B, -1, "PASS_GLEFT"), O: (O, +1, "PASS_GFETCH")},
    # GATHER: at first blank right of block. Fetch leftmost T, plug this blank. When no T before S, done.
    "PASS_GFETCH":  {B: (B, +1, "PASS_GSEEK"), T: (O, +1, "PASS_CONVERT0")},  # block already abuts T -> convert
    "PASS_GSEEK":   {B: (B, +1, "PASS_GSEEK"), T: (B, -1, "PASS_GBACK"), S: (B, -1, "PASS_GDONE")},
    "PASS_GBACK":   {B: (B, -1, "PASS_GBACK"), O: (O, +1, "PASS_GPLUG")},
    "PASS_GPLUG":   {B: (O, +1, "PASS_GLEFT")},   # plug leftmost gap-blank with O, restart
    # PASS_GDONE: hit S with no T left (all moved). S already erased. Walk LEFT to the block, home.
    "PASS_GDONE":   {B: (B, -1, "PASS_HOME"), O: (O, +1, "PASS_GDONE")},
    # ---- CONVERT path (block edge abuts T-run, gap already closed) ----
    "PASS_CONVERT0":{T: (O, +1, "PASS_CONVERT0"), S: (B, -1, "PASS_HOME"), B: (B, -1, "PASS_HOME"),
                     O: (O, +1, "PASS_CONVERT0")},
    # PASS_HOME: walk LEFT over trailing blanks to the block, then to its leftmost O, then to CS.
    "PASS_HOME":    {B: (B, -1, "PASS_HOME"), O: (O, -1, "PASS_HOME2"), S: (B, -1, "PASS_HOME")},
    "PASS_HOME2":   {O: (O, -1, "PASS_HOME2"), B: (B, +1, "CS")},

    # ----- overshoot -> HALT -----
    "HALT_PREP":    {B: HALT, O: HALT, M: HALT, X: HALT, D: HALT, T: HALT, A: HALT, S: HALT},
    "HALT":         {B: HALT, O: HALT, M: HALT, X: HALT, D: HALT, T: HALT, A: HALT, S: HALT},
}


# ===========================================================================
# VERIFICATION HARNESS
# ===========================================================================
import math


def is_square(n):
    if n < 1:
        return False
    r = int(math.isqrt(n))
    return r * r == n


def clean_block_at(tape, head):
    """If tape is a clean contiguous 1-block with head at its LEFT end and rest blank,
    return its length; else return None."""
    if tape.get(head, 0) != O:
        return None
    if tape.get(head - 1, 0) != B:
        return None
    i = head
    while tape.get(i, 0) == O:
        i += 1
    length = i - head
    for k, val in tape.items():
        if val == B:
            continue
        if val == O and head <= k < head + length:
            continue
        return None
    return length


def cs_milestones(DT, v0, cap, scan_all=False, need=10):
    cells = {i: O for i in range(v0)}
    tape = dict(cells)
    head = 0
    state = "CS"
    seen = []
    all_clean = []
    bl = clean_block_at(tape, head)
    if bl is not None:
        seen.append((state, bl))
        if scan_all:
            all_clean.append((state, bl))
    for t in range(cap):
        s = tape.get(head, 0)
        row = DT.get(state)
        if row is None or s not in row:
            return ("STUCK", t, state, s, seen, all_clean)
        tr = row[s]
        if tr is None:
            return ("HALT", t, state, seen, all_clean)
        w, mv, ns = tr
        tape[head] = w
        head += mv
        state = ns
        if scan_all:
            bl = clean_block_at(tape, head)
            if bl is not None:
                all_clean.append((state, bl))
        if state == "CS":
            bl = clean_block_at(tape, head)
            if bl is not None:
                seen.append((state, bl))
                if len(seen) >= need:
                    return ("ENOUGH", t, state, seen, all_clean)
            else:
                return ("DIRTY_CS", t, state, seen, all_clean)
    return ("CAP", cap, state, seen, all_clean)


def main():
    print("=" * 70)
    print("SQW verification (perfect squares)")
    print("=" * 70)

    # ---- (A) From CS on 1^1: squares sequence ----
    print("\n(A) From CS on 1^1 (cap=5,000,000):")
    status, t, st, seen, _ = cs_milestones(DTAB, 1, 5_000_000, need=10)
    lengths = [l for (_, l) in seen]
    print("   status:", status, "step:", t, "state:", st)
    print("   CS milestone lengths:", lengths)
    expected = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    okA = (status in ("ENOUGH", "CAP")) and lengths[:len(expected)] == expected[:len(lengths)] and lengths[:7] == [1,4,9,16,25,36,49]
    print("   expected prefix [1,4,9,16,25,36,49,...]:", "PASS" if okA else "FAIL")

    # ---- (B) per-w halt / no-halt ----
    print("\n(B) per-w (2..50) squares no-halt, non-squares halt:")
    okB = True
    rows = []
    NOHALT_CAP = 3_000_000
    HALT_CAP = 2_000_000
    squares = {1, 4, 9, 16, 25, 36, 49}
    for w in list(range(1, 51)):
        cells = {i: O for i in range(w)}
        if is_square(w):
            res = run(DTAB, cells, 0, "CS", cap=NOHALT_CAP)
            kind = res[0]
            ok = (kind == "CAP")
            rows.append((w, "sq ", kind, "-", "PASS" if ok else "FAIL"))
        else:
            res = run(DTAB, cells, 0, "CS", cap=HALT_CAP)
            kind = res[0]
            ok = (kind == "HALT")
            step = res[1] if kind in ("HALT", "STUCK", "CAP") else "-"
            rows.append((w, "non", kind, step, "PASS" if ok else "FAIL"))
        if not ok:
            okB = False
    for (w, typ, kind, step, verdict) in rows:
        print(f"   w={w:2d} {typ:3s} -> {kind:5s} step={step!s:>9} {verdict}")

    # ---- (C) separation ----
    print("\n(C) separation property (from 1^1, scanning ALL states, cap=500,000):")
    statusC, tC, stC, seenC, all_clean = cs_milestones(DTAB, 1, 500_000, scan_all=True, need=8)
    print("   scan status:", statusC, "stopped step:", tC)
    msset = {}
    for (s_, l_) in all_clean:
        msset.setdefault(s_, set()).add(l_)
    print("   ALL clean-block-at-left states & lengths:",
          {k: sorted(v) for k, v in msset.items()})
    allsq = all(is_square(l) for (_, l) in all_clean)
    cs_lengths = sorted(set(l for (s_, l) in all_clean if s_ == "CS"))
    cs_all_sq = all(is_square(l) for l in cs_lengths)
    okC = allsq and cs_all_sq
    print("   CS milestone lengths:", cs_lengths)
    print("   EVERY clean-unary-block-at-left config (any state) is SQUARE:",
          "PASS" if allsq else "FAIL")
    print("   -> no state recurs on arbitrary/non-square lengths:", "PASS" if okC else "FAIL")

    print("\n" + "=" * 70)
    print("SUMMARY: A=%s  B=%s  C=%s" % ("PASS" if okA else "FAIL",
                                          "PASS" if okB else "FAIL",
                                          "PASS" if okC else "FAIL"))
    print("=" * 70)


if __name__ == "__main__":
    main()
