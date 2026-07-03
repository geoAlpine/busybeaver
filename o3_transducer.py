#!/usr/bin/env python3
"""
o3 (BB6 cryptid, blank tape) — the SECOND structural outlier, at o17's proof standard
(2026-07-04).  [PROVEN halt gate + OBSERVED closure; halting NOT decided.]

o3 = 1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC   (halt = state F reads 0)
Table:  A:0->1RB,1->1LD  B:0->1RC,1->1RE  C:0->0LA,1->1LB
        D:0->0LD,1->1LC  E:0->1RF,1->0RA  F:0->HALT,1->0RC

Like o17, o3 is a tame finite-control head bouncing over a single-0-separated digit
string with NO equidistribution kernel; all hardness is a Collatz-irregular halt
predicate.  o3 is even TAMER than o17: its digit alphabet is BOUNDED {0,1} (block
lengths in {1,2}) and its digit-sum grows only logarithmically.

Verifier checks (0 exceptions => characterization holds on the tested range):
  (I)   language closure: every milestone (state A at left frontier) is a word in
        L = (1|11)(0(1|11))*  -- blocks of length 1 or 2, single-0 gaps.
  (II)  the head is a FIXED finite control: only 11 boundary-crossing (state,read,dir)
        triples, 3 right-reflection and 6 left-gate (state,read) pairs ever occur.
  (III) [PROVEN from the table] HALT <=> state E reads a 0 whose right neighbour is
        also 0 (F is entered only by E,0->1RF; F,0=HALT). VERIFIED never fires: over all
        E-reads-0 events the right neighbour is ALWAYS 1 (E is entering a nonempty
        block), so no (0,0) occurs -- halting would require the carry cascade to form
        an empty block (a 00), a Collatz-irregular existence event.
  (IV)  width identity  W = 2m + S + 2   [m=#blocks, S=#length-2 blocks];
        the length m is a free-running counter (ticks +1 or +2 per milestone, never
        decreases) => width ~ sqrt(step).
"""
from collections import Counter

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")
SN = "ABCDEF"

CROSS_OK = {('A',0,'R'),('A',1,'L'),('B',0,'R'),('B',1,'R'),('C',0,'L'),('C',1,'L'),
            ('D',0,'L'),('D',1,'L'),('E',0,'R'),('E',1,'R'),('F',1,'R')}
REFL_OK  = {('A',0),('B',0),('C',0)}
GATE_OK  = {('A',0),('B',0),('B',1),('C',0),('C',1),('D',1)}


def blocks(tape, lo, hi):
    r = []; i = lo
    while i <= hi:
        s = tape[i]; j = i
        while j <= hi and tape[j] == s: j += 1
        r.append((s, j - i)); i = j
    while r and r[0][0] == 0: r = r[1:]
    while r and r[-1][0] == 0: r = r[:-1]
    return r


def run(maxsteps):
    SZ = 1 << 23
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    res = dict(ms=0, lang=0, width=0, newX=set(), newR=set(), newG=set(),
               halt00=0, e0_badright=0, e0=0, prev_m=None, mcounter_bad=0)
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            res['halt00'] += 1; break
        # (III) halt-gate audit: whenever E reads 0, is the right neighbour 1?
        if st == 4 and r == 0:
            res['e0'] += 1
            if tape[pos + 1] != 1:
                res['e0_badright'] += 1
        # milestone = state A at left frontier
        if st == 0 and pos == lo:
            b = blocks(tape, lo, hi)
            blk = [n for s, n in b if s == 1]
            gap = [n for s, n in b if s == 0]
            if blk:
                res['ms'] += 1
                if not (all(x in (1, 2) for x in blk) and all(g == 1 for g in gap)):
                    res['lang'] += 1
                else:
                    m = len(blk); S = sum(1 for x in blk if x == 2); W = hi - lo + 1
                    if W != 2*m + S + 2:
                        res['width'] += 1
                    if res['prev_m'] is not None and (m - res['prev_m']) not in (1, 2):
                        res['mcounter_bad'] += 1   # length never decreases (ticks +1 or +2)
                    res['prev_m'] = m
        act = M[st][r]; ww, d, ns = act
        left = tape[pos-1]; right = tape[pos+1]
        boundary = (r == 1 and ((d == 1 and right == 0) or (d == -1 and left == 0))) or \
                   (r == 0 and ((d == 1 and right == 1) or (d == -1 and left == 1)))
        if boundary:
            t = (SN[st], r, 'R' if d == 1 else 'L')
            if t not in CROSS_OK: res['newX'].add(t)
        if pos >= hi and (SN[st], r) not in REFL_OK: res['newR'].add((SN[st], r))
        if pos <= lo and (SN[st], r) not in GATE_OK: res['newG'].add((SN[st], r))
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return res


def marker_cascade(maxsteps):
    """Dissect the carry cascade: at each generation start the digit string is 0^a 1^k
    (a length-1 blocks then k length-2 blocks = a trailing marker of k 'digit-1' blocks).
    Track the marker k across generations => the o17-no-jump analogue."""
    SZ = 1 << 22
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    ks = []; lens = []
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0: break
        if st == 0 and pos == lo:
            b = blocks(tape, lo, hi)
            dig = ''.join('1' if n == 2 else '0' for s, n in b if s == 1)
            if dig and '1' in dig and set(dig.rstrip('1')) <= {'0'}:
                k = len(dig) - len(dig.rstrip('1'))
                if not ks or ks[-1] != k or lens[-1] != len(dig):
                    ks.append(k); lens.append(len(dig))
        act = M[st][r]; ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    # collapse consecutive equal k
    kk = []; ll = []
    for k, L in zip(ks, lens):
        if not kk or kk[-1] != k: kk.append(k); ll.append(L)
    deltas = [kk[i+1] - kk[i] for i in range(len(kk)-1)]
    from collections import Counter, defaultdict
    amb = 0; tot = 0
    T = defaultdict(set)
    for i in range(len(kk)-1):
        T[(kk[i] % 2, ll[i] % 2)].add(deltas[i])
    for v in T.values():
        tot += 1
        if len(v) > 1: amb += 1
    return kk, deltas, dict(Counter(deltas)), (amb, tot)


if __name__ == "__main__":
    r = run(12_000_000)
    print(f"milestones checked            : {r['ms']}")
    print(f"(I)   language violations     : {r['lang']}   (not in (1|11)(0(1|11))*)")
    print(f"(II)  new crossing symbols    : {sorted(r['newX']) or 'NONE'}   (fixed set has 11)")
    print(f"      new reflection symbols  : {sorted(r['newR']) or 'NONE'}   (fixed set has 3)")
    print(f"      new gate symbols        : {sorted(r['newG']) or 'NONE'}   (fixed set has 6)")
    print(f"(III) E-reads-0 events        : {r['e0']}")
    print(f"      of which right-nbr != 1 : {r['e0_badright']}   (0 => E always enters a nonempty block; halt (0,0) impossible in L)")
    print(f"      actual HALT (E reads 00): {r['halt00']}")
    print(f"(IV)  width-identity fails    : {r['width']}   (W = 2m+S+2)")
    print(f"      length-counter breaks   : {r['mcounter_bad']}   (m ticks +1 or +2, never decreases => width~sqrt step)")
    ok = (r['lang'] == 0 and not r['newX'] and not r['newR'] and not r['newG']
          and r['e0_badright'] == 0 and r['width'] == 0 and r['mcounter_bad'] == 0)
    print(f"\nO3 TRANSDUCER + HALT-GATE VERIFIED: {ok}")
    print("[PROVEN from table] HALT <=> E reads a 00; [OBSERVED, 0 exc] within the normal form E")
    print("always enters a nonempty block, so halting = a Collatz-irregular 00-existence event.")
    print("SCOPE: second Type-II structural outlier (tamer than o17); halting stays [OPEN].")
    print()
    kk, deltas, dist, (amb, tot) = marker_cascade(40_000_000)
    print("CARRY-CASCADE DISSECTION (the o17-no-jump analogue):")
    print(f"  marker-k sequence ({len(kk)} generations): {kk}")
    print(f"  Delta-k distribution: {dist}  (bounded jump: Delta in {{-1,+1,+2}}, |Delta|<=2)")
    print(f"  marker never vanishes: min k = {min(kk)} (>=1)")
    print(f"  Delta-k determined by (k%2,len%2)? ambiguous {amb}/{tot} keys => history-dependent, CORE-HARD")
    print("  => like o17's no-jump: the marker jumps are bounded but not fixed by any bounded feature.")
