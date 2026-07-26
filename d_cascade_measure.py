#!/usr/bin/env python3
"""The seam prerequisite — re-measure D's milestone words, then check the doc's recursion.

The seams (RESUME §3 item 1) need a SYMBOLIC word family: to chain the four proven laws across
an epoch, each law's output configuration must be the next law's input, and that is a statement
about `D`'s cascade word.  `D_SPEC_2026-07-26.md` §2 states the family in closed form and calls
it `[MEASURED, verified k = 4..9]`.

Project discipline is to re-derive a claim before building on it, so this instrument re-measures
`M1(k)` straight from the raw orbit and checks:

  (1) the milestone definition (first new LEFT-frontier record at `-8k`, in state A, left blank);
  (2) the explicit right words in §2's table;
  (3) the closed forms `a(k) = 39·2^{k-1} - 4`, `G(k) = 57·2^{k-3} - 3k + 9`,
      `w(k) = 117·2^{k-1} + 3k - 55`;
  (4) the block recursion `M1(k) -> M1(k+2)` (prefix stability).

Only then is it safe to encode `Dcascade` in Lean.
"""
import sys

# D^R, flat tables for speed
W0 = [1, 1, 0, 1, 1, 1]          # write on read 0, by state A..F
D0 = [-1, 1, 1, -1, 1, 1]
N0 = [1, 2, 3, 0, 1, 3]
W1 = [0, 0, 0, 0, 0, 0]
D1 = [-1, 1, 1, 1, -1, 0]
N1 = [0, 4, 1, 5, 3, -1]         # -1 = HALT (F1)
SC = "ABCDEF"

TARGET_K = int(sys.argv[1]) if len(sys.argv) > 1 else 7

def run_milestones(kmax):
    CAP = 1 << 25
    t = bytearray(2 * CAP)
    p = CAP; st = 0; n = 0
    lo = p                     # left-frontier record
    out = {}
    want = -8
    limit = {4: 3*10**5, 5: 1.3*10**6, 6: 5*10**6, 7: 2*10**7, 8: 8*10**7, 9: 3.2*10**8}[kmax]
    while n < limit:
        c = t[p]
        if c:
            if N1[st] < 0: break
            t[p] = W1[st]; p += D1[st]; st = N1[st]
        else:
            t[p] = W0[st]; p += D0[st]; st = N0[st]
        n += 1
        if p < lo:
            lo = p
            rel = p - CAP
            if rel % 8 == 0 and st == 0 and -rel // 8 <= kmax:
                k = -rel // 8
                if k not in out:
                    # right word up to the last 1
                    hi = p
                    j = p
                    end = CAP + (1 << 22)
                    while j < end:
                        if t[j]: hi = j
                        j += 1
                    right = list(t[p+1:hi+1])
                    left = list(t[max(0, p-40):p])
                    out[k] = (n, rel, right, any(left))
                    print(f"  M1({k}): t={n} pos={rel} left_blank={not any(left)} width={hi-p}")
                    if k == kmax: return out
    return out

def rle(bits):
    o = []
    for b in bits:
        if o and o[-1][0] == b: o[-1][1] += 1
        else: o.append([b, 1])
    return [(b, c) for b, c in o]

def word_str(bits):
    """parse as  (0^g (10)^a)*  1  and print in D_SPEC's notation"""
    toks = []; i = 0; n = len(bits)
    while i < n:
        g = 0
        while i < n and bits[i] == 0: g += 1; i += 1
        a = 0
        while i + 1 < n and bits[i] == 1 and bits[i+1] == 0: a += 1; i += 2
        if g or a: toks.append(f"0^{g} (10)^{a}" if g else f"(10)^{a}")
        if i < n and bits[i] == 1 and (i + 1 == n or bits[i+1] == 1):
            toks.append("1"); i += 1
            if i < n: toks.append(f"<<UNPARSED tail {bits[i:i+12]}>>"); break
    return " ".join(toks)

def blocks(bits):
    """-> [(gap, comb)...] and the trailing 1"""
    out = []; i = 0; n = len(bits)
    while i < n:
        g = 0
        while i < n and bits[i] == 0: g += 1; i += 1
        a = 0
        while i + 1 < n and bits[i] == 1 and bits[i+1] == 0: a += 1; i += 2
        if i < n and bits[i] == 1 and (i + 1 == n):
            out.append((g, a)); return out, True
        out.append((g, a))
    return out, False

print(f"=== (1) measuring M1(k) from the raw orbit, k <= {TARGET_K} ===")
ms = run_milestones(TARGET_K)

DOC = {
 4: "0^33 (10)^66 0^111 (10)^308 1",
 5: "0^2 (10)^4 0^5 (10)^15 0^60 (10)^132 0^222 (10)^620 1",
 6: "0^33 (10)^66 0^78 (10)^264 0^447 (10)^1244 1",
 7: "0^2 (10)^4 0^5 (10)^15 0^60 (10)^132 0^144 (10)^528 0^900 (10)^2492 1",
}
DOCT = {4: 291168, 5: 1196412, 6: 4846662, 7: 19488198}

print()
print("=== (2) measured word vs `D_SPEC` §2 table ===")
for k in sorted(ms):
    n, rel, right, leftnz = ms[k]
    w = word_str(right)
    okt = (n == DOCT.get(k))
    okw = (w == DOC.get(k))
    print(f"  k={k}: t {'OK' if okt else f'MISMATCH (doc {DOCT.get(k)})'}   "
          f"word {'OK' if okw else 'MISMATCH'}   left_blank={'OK' if not leftnz else 'NO'}")
    if not okw:
        print(f"      measured: {w}")
        print(f"      doc     : {DOC.get(k)}")

print()
print("=== (3) closed forms ===")
for k in sorted(ms):
    _, _, right, _ = ms[k]
    bl, ok1 = blocks(right)
    gL, aL = bl[-1]
    a_cf = 39 * 2**(k-1) - 4
    G_cf = 57 * 2**(k-3) - 3*k + 9
    w_cf = 117 * 2**(k-1) + 3*k - 55
    print(f"  k={k}: a={aL} (cf {a_cf} {'OK' if aL==a_cf else 'X'})   "
          f"G={gL} (cf {G_cf} {'OK' if gL==G_cf else 'X'})   "
          f"width={len(right)} (cf {w_cf} {'OK' if len(right)==w_cf else 'X'})   nblocks={len(bl)}")

print()
print("=== (4) block recursion  M1(k) -> M1(k+2)  (prefix stability) ===")
print("    doc: keep every block but the last; rewrite the last (G(k),a(k)) ->")
print("         (33·2^{k-3}+12, 66·2^{k-2}); then append two new blocks.")
for k in sorted(ms):
    if k + 2 not in ms: continue
    b1, _ = blocks(ms[k][2])
    b2, _ = blocks(ms[k+2][2])
    keep = b1[:-1]
    rewritten = (33 * 2**(k-3) + 12, 66 * 2**(k-2))
    pred = keep + [rewritten] + b2[len(keep)+1:]
    same_prefix = b2[:len(keep)] == keep
    same_rw = len(b2) > len(keep) and b2[len(keep)] == rewritten
    app = b2[len(keep)+1:]
    print(f"  k={k} -> {k+2}: prefix kept = {same_prefix}   last -> {rewritten} = {same_rw}"
          f"   appended {len(app)} block(s): {app}")

print()
print("=== (5) the doc's block CONSTRUCTION, re-derived and checked ===")
print("    jmax = k//2 ; for j = jmax..2 with e = k-2j:  e=0 ->(33,66)  e=1 ->(60,132)")
print("    e>=2 ->(33*2^(e-1)+12, 66*2^e) ;  k odd: prepend (2,4),(5,15) ;  append (G(k), a(k))")
def construct(k):
    jmax = k // 2
    bl = []
    for j in range(jmax, 1, -1):
        e = k - 2*j
        if e == 0: bl.append((33, 66))
        elif e == 1: bl.append((60, 132))
        else: bl.append((33 * 2**(e-1) + 12, 66 * 2**e))
    if k % 2 == 1: bl = [(2, 4), (5, 15)] + bl
    bl.append((57 * 2**(k-3) - 3*k + 9, 39 * 2**(k-1) - 4))
    return bl
allok = True
for k in sorted(ms):
    if k < 4: continue
    meas, _ = blocks(ms[k][2])
    got = construct(k)
    ok = (meas == got)
    allok &= ok
    print(f"  k={k}: {'OK' if ok else 'MISMATCH'}")
    if not ok:
        print(f"     measured  {meas}")
        print(f"     construct {got}")
print(f"  => construction reproduces every measured milestone k>=4: {allok}")
