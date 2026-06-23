#!/usr/bin/env python3.11
"""
PALW -- explicit multi-symbol single-tape TM that CHECKS "is a binary palindrome"
EVERY cycle.  Witness for the certification-hierarchy separation

        2-automatic  ⊊  context-free      (via the Squeeze Lemma)

S = { n : the base-2 representation of n is a palindrome }  (OEIS A006995, decimal
1,3,5,7,9,15,17,21,27,31,33,...).  Binary palindromes form a context-free,
non-regular language; hence S is NOT 2-automatic but IS context-free-numeration.

Cycle-start state: CS.  Milestone config = (state CS, head at LEFT end of a clean
contiguous block 1^v, rest blank, EXCEPT a fixed mode-flag cell at index -1).

Each visit to CS on clean 1^v:
  1. set flag = ENTRY ; DUPLICATE 1^v -> 1^v M 1^v.
  2. CONVERT the right copy unary->binary (repeated halving, emitting bits LSB..MSB
     into a digit region right of a separator G).
  3. PALINDROME-TEST the digit string (compare ends inward, markers c0/c1).
       FAIL (flag ENTRY)   -> HALT          [v is not a binary palindrome]
       PASS (flag ENTRY)   -> CLEANUP -> ADV0
  ADV0 on 1^v (v a palindrome, flag ADVANCE present at cell -1):
  4. INCREMENT 1^v -> 1^{v+1} ; DUPLICATE ; CONVERT ; PAL-TEST.
       FAIL (flag ADVANCE) -> CLEANUP scratch (flag KEPT) -> ADV0   [keep incrementing]
       PASS (flag ADVANCE) -> CLEANUP scratch, CLEAR flag -> CS      [next binary palindrome]
  -> loop forever, CS-milestones = the binary palindromes in increasing order.

  FLAG DISCIPLINE (separation-critical, property C): the mode-flag (FE/FA) sits in the
  fixed cell index -1 and is NON-BLANK throughout the ENTRY-check AND the entire
  ADVANCE-search (it is set to FA when entering advance and KEPT until a palindrome is
  found).  It is cleared to blank only at the instant control returns to state CS.
  Therefore the ONLY tape configurations that are a clean contiguous 1-block with the
  ENTIRE rest of the tape blank are exactly the CS milestones -- no scratch/advance state
  ever exhibits a blank-rest clean block, so no trap state recurs on arbitrary lengths.

VERIFICATION (sound gate) is in palw_verify.py: (A) CS-milestone sequence from 1^1,
(B) per-w HALT iff w not a binary palindrome, (C) every clean left-anchored block in
any state has binary-palindrome length.

Alphabet (ints):
  B blank, O one, M left-wall, X crossed-one, b0/b1 binary digits, G digit-separator,
  c0/c1 matched-digit markers, A copy-progress mark,
  FE flag=ENTRY, FA flag=ADVANCE  (live only in the fixed cell index -1).
"""

B, O, M, X, b0, b1, G, c0, c1, A, FE, FA = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
HALT = None

NAMES = {B:'.',O:'1',M:'M',X:'x',b0:'0',b1:'1',G:'G',c0:'a',c1:'b',A:'A',FE:'E',FA:'V'}


def run(D, tape, head, state, cap=2_000_000, trace=False):
    tape = dict(tape)
    for t in range(cap):
        s = tape.get(head, B)
        row = D.get(state)
        if trace:
            ks=[k for k,v in tape.items() if v!=B] or [head]
            lo=min(min(ks),head); hi=max(max(ks),head)
            line=''.join(NAMES.get(tape.get(i,B),'?') for i in range(lo,hi+1))
            print(f"  t={t} {state:14s} {line}  @{head}")
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

# ---------- CS : set flag ENTRY, then DUPLICATE ----------
# head at leftmost O of clean 1^v (cell 0). Write flag FE at cell -1, return, duplicate.
    "CS":        {O:(O,-1,"CS_FLAG"), B:(B,+1,"HALT")},     # v>=1 always; empty -> HALT
    "CS_FLAG":   {B:(FE,+1,"DUP0")},                        # write ENTRY flag left of block
    # DUP0: head back on leftmost O. begin DUPLICATE 1^v -> 1^v M 1^v.
    "DUP0":      {O:(O,+1,"DUP_R"), B:(B,+1,"HALT")},
    "DUP_R":     {O:(O,+1,"DUP_R"), B:(M,-1,"DUP_BK")},
    "DUP_BK":    {O:(O,-1,"DUP_BK"), M:(M,-1,"DUP_BK"), FE:(FE,+1,"DPICK"), FA:(FA,+1,"DPICK")},
    "DPICK":     {A:(A,+1,"DPICK"), O:(A,+1,"DCARRY"), M:(M,+1,"DDONE")},
    "DCARRY":    {O:(O,+1,"DCARRY"), A:(A,+1,"DCARRY"), M:(M,+1,"DCARRY2")},
    "DCARRY2":   {O:(O,+1,"DCARRY2"), B:(O,-1,"DRET")},
    "DRET":      {O:(O,-1,"DRET"), M:(M,-1,"DRETL")},
    "DRETL":     {A:(A,-1,"DRETL"), O:(O,-1,"DRETL"), FE:(FE,+1,"DPICK"), FA:(FA,+1,"DPICK")},
    "DDONE":     {O:(O,-1,"DDONE"), M:(M,-1,"DDONEL")},
    "DDONEL":    {A:(A,-1,"DDONEL"), O:(O,-1,"DDONEL"), FE:(FE,+1,"UNMARK"), FA:(FA,+1,"UNMARK")},
    "UNMARK":    {A:(O,+1,"UNMARK"), O:(O,+1,"UNMARK"), M:(M,+1,"CONV_INIT")},
    # tape: <flag> 1^v M 1^v, head at leftmost O of RIGHT copy.

# ---------- CONVERT right copy unary -> binary (verified) ----------
    "CONV_INIT": {O:(O,+1,"CONV_INIT"), B:(G,-1,"CONV_TOM")},
    "CONV_TOM":  {O:(O,-1,"CONV_TOM"), X:(X,-1,"CONV_TOM"), M:(M,+1,"H_ROUND")},
    "H_ROUND":   {O:(X,+1,"H_KEEP"), X:(X,+1,"H_ROUND"), B:(B,+1,"TOG_DONE"), G:(G,+1,"PAL_L")},
    "H_KEEP":    {O:(O,+1,"H_CROSS"), X:(X,+1,"H_KEEP"), B:(B,+1,"TOG_E1"), G:(G,+1,"EMIT1")},
    "H_CROSS":   {O:(X,+1,"H_KEEP"), X:(X,+1,"H_CROSS"), B:(B,+1,"TOG_E0"), G:(G,+1,"EMIT0")},
    "TOG_E1":    {B:(B,+1,"TOG_E1"), G:(G,+1,"EMIT1")},
    "TOG_E0":    {B:(B,+1,"TOG_E0"), G:(G,+1,"EMIT0")},
    "TOG_DONE":  {B:(B,+1,"TOG_DONE"), G:(G,+1,"PAL_L")},
    "EMIT0":     {b0:(b0,+1,"EMIT0"), b1:(b1,+1,"EMIT0"), B:(b0,-1,"RP_TOG")},
    "EMIT1":     {b0:(b0,+1,"EMIT1"), b1:(b1,+1,"EMIT1"), B:(b1,-1,"RP_TOG")},
    "RP_TOG":    {b0:(b0,-1,"RP_TOG"), b1:(b1,-1,"RP_TOG"), G:(G,-1,"RP_TOM")},
    "RP_TOM":    {O:(O,-1,"RP_TOM"), X:(X,-1,"RP_TOM"), B:(B,-1,"RP_TOM"), M:(M,+1,"ERASEX")},
    "ERASEX":    {O:(O,+1,"ERASEX"), X:(B,+1,"ERASEX"), B:(B,+1,"ERASEX"), G:(G,-1,"GBACK")},
    "GBACK":     {O:(O,-1,"GBACK"), B:(B,-1,"GBACK"), M:(M,+1,"GATH")},
    "GATH":      {O:(O,+1,"GATH"), B:(B,+1,"GFIND"), G:(G,-1,"GHOME")},
    "GFIND":     {B:(B,+1,"GFIND"), O:(B,-1,"GCARRY"), G:(G,-1,"GHOME")},
    "GCARRY":    {B:(B,-1,"GCARRY"), O:(O,+1,"GPLACE"), M:(M,+1,"GPLACE")},
    "GPLACE":    {B:(O,+1,"GATH")},
    "GHOME":     {G:(G,-1,"GHOME"), B:(B,-1,"GHOME"), O:(O,-1,"GHOME"), M:(M,+1,"H_ROUND")},
    "CONV_DONE": {G:(G,+1,"PAL_L")},   # head on G; step into digits -> palindrome test

# ---------- PALINDROME test on digit region ----------
    "PAL_L":     {b0:(b0,-1,"PAL_L"), b1:(b1,-1,"PAL_L"), c0:(c0,-1,"PAL_L"), c1:(c1,-1,"PAL_L"),
                  G:(G,+1,"PAL_FINDL")},
    "PAL_FINDL": {c0:(c0,+1,"PAL_FINDL"), c1:(c1,+1,"PAL_FINDL"),
                  b0:(c0,+1,"PAL_R0"), b1:(c1,+1,"PAL_R1"),
                  B:(B,-1,"PAL_PASS")},
    "PAL_R0":    {b0:(b0,+1,"PAL_R0"), b1:(b1,+1,"PAL_R0"), c0:(c0,+1,"PAL_R0"), c1:(c1,+1,"PAL_R0"),
                  B:(B,-1,"PAL_CMP0")},
    "PAL_R1":    {b0:(b0,+1,"PAL_R1"), b1:(b1,+1,"PAL_R1"), c0:(c0,+1,"PAL_R1"), c1:(c1,+1,"PAL_R1"),
                  B:(B,-1,"PAL_CMP1")},
    "PAL_CMP0":  {c0:(c0,-1,"PAL_CMP0"), c1:(c1,-1,"PAL_CMP0"),
                  b0:(c0,+1,"PAL_NEXT"), b1:(b1,+1,"PAL_FAIL"), G:(G,+1,"PAL_PASS")},
    "PAL_CMP1":  {c0:(c0,-1,"PAL_CMP1"), c1:(c1,-1,"PAL_CMP1"),
                  b1:(c1,+1,"PAL_NEXT"), b0:(b0,+1,"PAL_FAIL"), G:(G,+1,"PAL_PASS")},
    "PAL_NEXT":  {b0:(b0,-1,"PAL_NEXT"), b1:(b1,-1,"PAL_NEXT"), c0:(c0,-1,"PAL_NEXT"),
                  c1:(c1,-1,"PAL_NEXT"), B:(B,-1,"PAL_NEXT"), G:(G,+1,"PAL_FINDL")},

# ---------- verdict dispatch on the mode flag (cell -1) ----------
# Both PAL_PASS and PAL_FAIL: first CLEANUP the scratch to restore clean 1^v, then
# walk to the flag cell and branch.  Cleanup leaves head at leftmost O (cell 0); flag
# still at cell -1.  We read it: FE/FA decides next state, and we RESET it appropriately.
    "PAL_PASS":  {x:(x,0,"CLN_PASS") for x in (B,O,M,X,b0,b1,G,c0,c1)},
    "PAL_FAIL":  {x:(x,0,"CLN_FAIL") for x in (B,O,M,X,b0,b1,G,c0,c1)},

# CLEANUP: erase everything from M rightward (M, scratch, G, digits, markers) to blank,
# leaving the clean left block 1^v.  Then home to leftmost O.
# We are somewhere in the scratch/digit region. Walk LEFT to M, then erase rightward.
    # walk LEFT to M (left wall of scratch). Then erase scratch+G+digits rightward:
    # from M go RIGHT to G, erase digits right of G to the terminal blank, then walk
    # LEFT erasing G and the M..G region (blanks/X) and M itself, stopping at the block.
    "CLN_PASS":  {b0:(b0,-1,"CLN_PASS"), b1:(b1,-1,"CLN_PASS"), c0:(c0,-1,"CLN_PASS"),
                  c1:(c1,-1,"CLN_PASS"), G:(G,-1,"CLN_PASS"), X:(X,-1,"CLN_PASS"),
                  O:(O,-1,"CLN_PASS"), B:(B,-1,"CLN_PASS"), M:(M,+1,"CLNP_TOG")},
    "CLNP_TOG":  {B:(B,+1,"CLNP_TOG"), X:(X,+1,"CLNP_TOG"), G:(B,+1,"CLNP_DIG")},
    "CLNP_DIG":  {b0:(B,+1,"CLNP_DIG"), b1:(B,+1,"CLNP_DIG"), c0:(B,+1,"CLNP_DIG"),
                  c1:(B,+1,"CLNP_DIG"), B:(B,-1,"CLNP_BK")},
    "CLNP_BK":   {B:(B,-1,"CLNP_BK"), X:(B,-1,"CLNP_BK"), M:(B,-1,"HOME_P"),
                  O:(O,-1,"CLNP_BK")},  # erase blanks/X; erase M; O of block -> keep, go home
    # (O case shouldn't occur before M, but kept safe: scratch is right of M.)
    # HOME_P walks LEFT over the clean block's O's and any blanks to the flag cell (-1).
    # Reads flag, CLEARS it to blank, steps +1 onto leftmost O (cell0), dispatches.
    "HOME_P":    {B:(B,-1,"HOME_P"), O:(O,-1,"HOME_P"),
                  FE:(FA,+1,"ADV0"),   # ENTRY pass -> advance phase; KEEP a flag (FA) so the
                                       #   advance-search configs are never blank-rest clean
                  FA:(B,+1,"CS")},     # ADVANCE pass -> reached next palindrome -> CLEAR flag -> CS

    "CLN_FAIL":  {b0:(b0,-1,"CLN_FAIL"), b1:(b1,-1,"CLN_FAIL"), c0:(c0,-1,"CLN_FAIL"),
                  c1:(c1,-1,"CLN_FAIL"), G:(G,-1,"CLN_FAIL"), X:(X,-1,"CLN_FAIL"),
                  O:(O,-1,"CLN_FAIL"), B:(B,-1,"CLN_FAIL"), M:(M,+1,"CLNF_TOG")},
    "CLNF_TOG":  {B:(B,+1,"CLNF_TOG"), X:(X,+1,"CLNF_TOG"), G:(B,+1,"CLNF_DIG")},
    "CLNF_DIG":  {b0:(B,+1,"CLNF_DIG"), b1:(B,+1,"CLNF_DIG"), c0:(B,+1,"CLNF_DIG"),
                  c1:(B,+1,"CLNF_DIG"), B:(B,-1,"CLNF_BK")},
    "CLNF_BK":   {B:(B,-1,"CLNF_BK"), X:(B,-1,"CLNF_BK"), M:(B,-1,"HOME_F"),
                  O:(O,-1,"CLNF_BK")},
    "HOME_F":    {B:(B,-1,"HOME_F"), O:(O,-1,"HOME_F"),
                  FE:(B,+1,"HALT"),    # ENTRY fail -> HALT (started on a non-palindrome)
                  FA:(FA,+1,"ADV0")},  # ADVANCE fail -> keep flag, keep incrementing

# ---------- ADV0 : INCREMENT 1^v -> 1^{v+1}, set flag ADVANCE, then DUPLICATE ----------
# head at leftmost O (cell 0). Append one O at the right end of the block.
    # ADV0: head at leftmost O (cell0). Append one O at right end -> 1^{v+1}.
    # ADV0: head at leftmost O (cell0), flag FA present at cell -1. Append one O at right.
    "ADV0":      {O:(O,+1,"ADV_R"), B:(B,+1,"HALT")},
    "ADV_R":     {O:(O,+1,"ADV_R"), B:(O,-1,"ADV_BK")},     # write new O at right end
    "ADV_BK":    {O:(O,-1,"ADV_BK"), FA:(FA,+1,"DUP0")},    # walk to flag cell(-1) -> +1 to cell0, DUPLICATE

    "HALT":      {x:None for x in range(12)},
}
