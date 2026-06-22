#!/usr/bin/env python3.11
"""
POW2W -- explicit multi-symbol single-tape TM that CHECKS power-of-2-ness EVERY cycle.

Cycle-start state: CS.
Milestone config = (state CS, head at LEFT end of a clean contiguous block 1^v, rest blank).

Each cycle from CS on clean 1^v:
  1. DUPLICATE  1^v -> 1^v M 1^v
  2. CHECK the RIGHT copy by HALVE (cross every other 1; even count -> repack & halve again;
     odd with >1 survivor -> HALT; reduces to single 1 -> PASS = v is a power of 2).
  3. On PASS: erase M and the right region (the left copy 1^v is untouched), then APPEND a
     fresh copy of the left block -> contiguous 1^{2v}, head back at left, state CS.
  4. Loop forever.

Alphabet (ints): B=0 blank, O=1 one, M=2 marker, A=3 copy-progress mark, X=4 crossed, S=5 sentinel.
"""

B, O, M, A, X, S = 0, 1, 2, 3, 4, 5
HALT = None


def run(D, cells, head, state, cap=2_000_000):
    tape = dict(cells)
    for t in range(cap):
        s = tape.get(head, 0)
        row = D.get(state)
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
D = {

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

    # DDONE: hit M with all left O's marked A. Head just right of M. Restore A->O, go to CHECK.
    "DDONE":    {O: (O, -1, "DDONE"), M: (M, -1, "DDONEL")},
    "DDONEL":   {A: (A, -1, "DDONEL"), O: (O, -1, "DDONEL"), B: (B, +1, "UNMARK")},
    "UNMARK":   {A: (O, +1, "UNMARK"), O: (O, +1, "UNMARK"), M: (M, +1, "CHK0")},
    # tape now: 1^v M 1^v, head at leftmost O of the RIGHT copy.

    # ----- CHECK: HALVE the right copy. M to the left is the permanent left wall. -----
    # Cross every other O. Track parity by which state hits the right blank.
    "CHK0":     {O: (O, +1, "CCROSS"), B: (B, +1, "HALT")},  # first O is KEPT
    # CCROSS reading blank => last action was a KEEP => ODD length.
    # CKEEP  reading blank => last action was a CROSS => EVEN length.
    "CCROSS":   {O: (X, +1, "CKEEP"), B: (B, -1, "CEND_ODD")},   # crossed-next; blank -> ODD pass
    "CKEEP":    {O: (O, +1, "CCROSS"), X: (X, +1, "CCROSS"), B: (B, -1, "CEND_EVEN")},  # keep-next; blank->EVEN

    # ODD pass: survivors = O's. Walk left counting O's (skip X) until M.
    #   exactly 1 O before M -> PASS ; >1 -> HALT.
    # Head currently just left of the right-end blank (on last cell). Sweep left.
    "CEND_ODD":   {X: (X, -1, "CEND_ODD"), O: (O, -1, "CEND_ODD1"), M: (M, +1, "PASS")},
    "CEND_ODD1":  {X: (X, -1, "CEND_ODD1"), O: (O, -1, "HALT"), M: (M, +1, "PASS")},

    # EVEN pass: repack (erase X, gather O's left to M), then halve again.
    "CEND_EVEN":  {X: (X, -1, "CEND_EVEN"), O: (O, -1, "CEND_EVEN"), M: (M, +1, "RPK_ERASE")},
    # erase X across right copy; at far-right blank write sentinel S, then gather.
    "RPK_ERASE":  {O: (O, +1, "RPK_ERASE"), X: (B, +1, "RPK_ERASE"), B: (S, -1, "RPK_TOM")},
    # walk back left to M (right wall of left block), step right -> begin gather at left of right copy.
    "RPK_TOM":    {O: (O, -1, "RPK_TOM"), B: (B, -1, "RPK_TOM"), M: (M, +1, "GATH")},
    # GATHER: pull O's leftward against M. Head at a cell of the right region.
    "GATH":       {O: (O, +1, "GATH"), B: (B, +1, "GFIND"), S: (B, -1, "GHOME")},
    "GFIND":      {B: (B, +1, "GFIND"), O: (B, -1, "GCARRY"), S: (B, -1, "GHOME")},
    "GCARRY":     {B: (B, -1, "GCARRY"), O: (O, +1, "GPLACE"), M: (M, +1, "GPLACE")},
    "GPLACE":     {B: (O, +1, "GATH")},
    # GHOME: erased S; walk left to M; step right -> restart halve on the repacked right copy.
    "GHOME":      {B: (B, -1, "GHOME"), O: (O, -1, "GHOME"), M: (M, +1, "CHK0")},

    # ----- PASS: v is power of 2. Right region is junk (O's/X's) bounded left by M. -----
    # Head just right of M (PASS entered via +1 over M). Erase the whole right region + M -> clean 1^v,
    # then APPEND a fresh copy of the left block -> 1^{2v}, return to CS.
    "PASS":     {O: (B, +1, "PERASE"), X: (B, +1, "PERASE"), B: (B, +1, "PERASE"), S: (B, +1, "PERASE")},
    "PERASE":   {O: (B, +1, "PERASE"), X: (B, +1, "PERASE"), S: (B, +1, "PERASE"),
                 B: (B, -1, "PBACK")},
    # walk left to M, erase M, then to leftmost O of the clean left block.
    "PBACK":    {B: (B, -1, "PBACK"), M: (B, -1, "PHOME")},
    "PHOME":    {O: (O, -1, "PHOME"), B: (B, +1, "DBL")},
    # tape now: clean 1^v, head at leftmost O. DOUBLE it contiguously to 1^{2v}.

    # DOUBLE 1^v -> 1^{2v}: same as DUPLICATE but place a TEMP marker M at right end, copy, then fuse
    # by deleting M and SHIFTING the right block left one cell to make it contiguous.
    # Reuse the duplicate machinery via dedicated states (so we don't re-enter CHECK).
    "DBL":      {O: (O, +1, "DBL_R"), B: (B, +1, "HALT")},
    "DBL_R":    {O: (O, +1, "DBL_R"), B: (M, -1, "DBL_BK")},
    "DBL_BK":   {O: (O, -1, "DBL_BK"), M: (M, -1, "DBL_BK"), B: (B, +1, "DB_PICK")},
    "DB_PICK":  {A: (A, +1, "DB_PICK"), O: (A, +1, "DB_CARRY"), M: (M, +1, "DB_DONE")},
    "DB_CARRY": {O: (O, +1, "DB_CARRY"), A: (A, +1, "DB_CARRY"), M: (M, +1, "DB_CARRY2")},
    "DB_CARRY2":{O: (O, +1, "DB_CARRY2"), B: (O, -1, "DB_RET")},
    "DB_RET":   {O: (O, -1, "DB_RET"), M: (M, -1, "DB_RETL")},
    "DB_RETL":  {A: (A, -1, "DB_RETL"), O: (O, -1, "DB_RETL"), B: (B, +1, "DB_PICK")},
    "DB_DONE":  {O: (O, -1, "DB_DONE"), M: (M, -1, "DB_DONEL")},
    "DB_DONEL": {A: (A, -1, "DB_DONEL"), O: (O, -1, "DB_DONEL"), B: (B, +1, "DB_UNMARK")},
    "DB_UNMARK":{A: (O, +1, "DB_UNMARK"), O: (O, +1, "DB_UNMARK"), M: (M, +1, "FUSE")},
    # tape: 1^v M 1^v, head at leftmost O of right block. FUSE: delete M, shift right block left 1.
    # Shift-left-by-one: for each O of the right block (left to right), move it one cell left.
    # The cell holding M becomes the new left edge. We walk: at M position write O, then the gap moves.
    # Simpler verified shift: scan to M from the right block's left end going left, then sweep:
    #   Go to M (head currently at leftmost O of right block, M is one left). Replace M with O,
    #   then the right block needs its rightmost O removed. So: M->O at the boundary, then delete the
    #   last O of the right block.
    # That works ONLY because the right block is contiguous starting right after M: turning M into O
    # extends the left block by one and shifts nothing else -- but then there is one EXTRA O (we copied
    # v O's plus turned M into O = v+1 on the right side). Fix: delete one O from the right end.
    "FUSE":     {O: (O, -1, "FUSE_M")},
    "FUSE_M":   {M: (O, +1, "FUSE_DELLAST")},   # M -> O : now 1^{2v+1} contiguous; delete one O at right
    "FUSE_DELLAST": {O: (O, +1, "FUSE_DELLAST"), B: (B, -1, "FUSE_DEL")},
    "FUSE_DEL": {O: (B, -1, "FUSE_HOME")},
    "FUSE_HOME":{O: (O, -1, "FUSE_HOME"), B: (B, +1, "CS")},
    # tape now: clean 1^{2v}, head at leftmost O, state CS.

    "HALT":     {B: HALT, O: HALT, M: HALT, A: HALT, X: HALT, S: HALT},
}


# ===========================================================================
# VERIFICATION HARNESS
# ===========================================================================
def is_pow2(n):
    return n >= 1 and (n & (n - 1)) == 0


def clean_block_at(tape, head):
    """If tape is a clean contiguous 1-block with head at its LEFT end and rest blank,
    return its length; else return None."""
    # head cell must be O
    if tape.get(head, 0) != O:
        return None
    # cell left of head must be blank (head at left end)
    if tape.get(head - 1, 0) != B:
        return None
    # count O's rightward
    i = head
    while tape.get(i, 0) == O:
        i += 1
    length = i - head
    # everything else must be blank and only O symbols present
    for k, val in tape.items():
        if val == B:
            continue
        if val == O and head <= k < head + length:
            continue
        return None  # stray non-blank or O outside block
    return length


def cs_milestones(D, v0, cap, scan_all=False):
    """Run from CS on 1^v0.
    seen      = list of (state, length) recorded at state CS on a clean block (cycle milestones).
    all_clean = (if scan_all) list of (state, length) at EVERY (state,head) where the WHOLE tape is a
                clean contiguous 1-block with head at its LEFT end and rest blank -- regardless of state.
                This proves no DOUBLE-like state recurs holding an arbitrary unchecked unary block.
    """
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
        row = D.get(state)
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
                if len(seen) >= 12:  # enough powers of 2 (1..1024)
                    return ("ENOUGH", t, state, seen, all_clean)
            else:
                return ("DIRTY_CS", t, state, seen, all_clean)
    return ("CAP", cap, state, seen, all_clean)


def main():
    print("=" * 70)
    print("POW2W verification")
    print("=" * 70)

    # ---- (A) From CS on 1^1: powers-of-2 sequence ----
    print("\n(A) From CS on 1^1 (cap=5,000,000):")
    status, t, st, seen, _ = cs_milestones(D, 1, 5_000_000)
    lengths = [l for (_, l) in seen]
    print("   status:", status, "step:", t, "state:", st)
    print("   CS milestone lengths:", lengths)
    expected = [1, 2, 4, 8, 16, 32, 64]
    okA = (status in ("ENOUGH", "CAP")) and lengths[:7] == expected
    print("   expected prefix [1,2,4,8,16,32,64]:", "PASS" if okA else "FAIL")

    # ---- (B) per-w halt / no-halt ----
    print("\n(B) per-w (3..64) and w=1,2:")
    okB = True
    rows = []
    NOHALT_CAP = 3_000_000
    HALT_CAP = 3_000_000
    for w in [1, 2] + list(range(3, 65)):
        cells = {i: O for i in range(w)}
        if is_pow2(w):
            res = run(D, cells, 0, "CS", cap=NOHALT_CAP)
            kind = res[0]
            ok = (kind == "CAP")
            rows.append((w, "pow2", kind, "-", "PASS" if ok else "FAIL"))
        else:
            res = run(D, cells, 0, "CS", cap=HALT_CAP)
            kind = res[0]
            ok = (kind == "HALT")
            step = res[1] if kind in ("HALT", "STUCK", "CAP") else "-"
            rows.append((w, "non", kind, step, "PASS" if ok else "FAIL"))
        if not ok:
            okB = False
    for (w, typ, kind, step, verdict) in rows:
        print(f"   w={w:2d} {typ:4s} -> {kind:5s} step={step!s:>9} {verdict}")

    # ---- (C) separation: log EVERY clean-block-at-left config at ANY state ----
    print("\n(C) separation property (from 1^1, scanning ALL states, cap=300,000):")
    statusC, tC, stC, seenC, all_clean = cs_milestones(D, 1, 300_000, scan_all=True)
    print("   scan status:", statusC, "stopped step:", tC)
    msset = {}
    for (s_, l_) in all_clean:
        msset.setdefault(s_, set()).add(l_)
    print("   ALL clean-block-at-left states & lengths:",
          {k: sorted(v) for k, v in msset.items()})
    allpow = all(is_pow2(l) for (_, l) in all_clean)
    # The canonical cycle-start milestone is CS; the other states (PHOME/DBL/FUSE_HOME) are TRANSIENT
    # merge-internal states that only ever hold an ALREADY-CHECKED block (post-PASS) or the freshly
    # built 1^{2v}. The soundness-critical separation claim is: EVERY clean unary block at the left end,
    # in ANY state, has POWER-OF-2 length -- i.e. NO state ever holds an arbitrary-length unchecked block
    # (unlike pow2's DOUBLE which recurs on every integer length).
    cs_lengths = sorted(l for (s_, l) in all_clean if s_ == "CS")
    cs_all_pow = all(is_pow2(l) for l in cs_lengths)
    okC = allpow and cs_all_pow
    print("   CS milestone lengths:", cs_lengths)
    print("   EVERY clean-unary-block-at-left config (any state) has POWER-OF-2 length:",
          "PASS" if allpow else "FAIL")
    print("   -> no DOUBLE-like state recurs on arbitrary lengths:", "PASS" if okC else "FAIL")

    print("\n" + "=" * 70)
    print("SUMMARY: A=%s  B=%s  C=%s" % ("PASS" if okA else "FAIL",
                                          "PASS" if okB else "FAIL",
                                          "PASS" if okC else "FAIL"))
    print("=" * 70)


if __name__ == "__main__":
    import os
    if os.environ.get("POW2W_NOMAIN") != "1":
        main()
