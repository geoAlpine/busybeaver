#!/usr/bin/env python3
"""T7 BOUNDARY (2026-07-22): does the REAL orbit satisfy ladderFold's premise?

ladderFold (lean/T7Ladder.lean) proves the ABSTRACT ladder: from a regenIn b config carrying the
nested marker `ladderMarker b n` and pad `ladderPad b n`, n rungs reach regenIn (b+n).  For this to
apply to h_doub we must show the real M6(g) orbit PRESENTS that nested data.  This measures it.

ladderStep k consumes, from the FRONT of regenIn k's marker parameter, one layer
   layer_k = 0 0 1 (01)^{2^k - 2}        (as bits: false false true, then pow01(2^k-2))
leaving the marker of regenIn (k+1).  So on the real orbit the marker at regenIn k should be
   marker_k = layer_k ++ marker_{k+1},   i.e. ladderMarker peels exactly one layer per rung.
Likewise the pad: pad_k = zeros(2^k) ++ pad_{k+1}.

regenIn k config (lean/X2.lean:6682):
  left  = ones(2^k-3) ++ [false,true,false,false,true] ++ pow01(2^{k-1}-2) ++ MARKER_k
  right = false :: descCascade(k-4) ++ zeros(z) ++ REST_k       (z = 2^{k-1}+9 canonical)
This script extracts MARKER_k and the pad at each rung on the g=2 orbit and checks the recursion.
"""
from x2t7_lib import run, classify, E, ones_run_left, rle_right


def pow01_len_from(tape, i):
    """Count consecutive '01' pairs (false,true) starting at absolute index i; return (pairs, next_i)."""
    n = 0
    while i + 1 < len(tape) and tape[i] == 0 and tape[i + 1] == 1:
        n += 1
        i += 2
    return n, i


def left_bits_reversed(tape, pos, limit=200000):
    """The left tape (indices < pos), returned in LEFT-TO-RIGHT reading order for the machine,
    i.e. from far-left toward pos.  We actually want the structure reading AWAY from the head:
    left[0] is the cell just left of pos.  regenIn's `left` list is head-adjacent-first."""
    out = []
    i = pos - 1
    stop = max(0, pos - limit)
    while i >= stop:
        out.append(tape[i])
        i -= 1
    return out  # out[0] = cell at pos-1 (head-adjacent), matching Cfg.left convention


def parse_regenIn_left(tape, pos, k):
    """Given a regenIn k config with head at pos, parse left = ones(2^k-3) ++ [0,1,0,0,1]
    ++ pow01(2^{k-1}-2) ++ MARKER.  Return MARKER as a bit list (head-adjacent-first), or None."""
    L = left_bits_reversed(tape, pos)
    blk = (1 << k) - 3
    # ones(2^k-3): blk ones
    if L[:blk] != [1] * blk:
        return None
    i = blk
    # [false,true,false,false,true]  (regenIn: false::true::false::false::true)
    if L[i:i + 5] != [0, 1, 0, 0, 1]:
        return None
    i += 5
    # pow01(2^{k-1}-2) = (false true) repeated 2^{k-1}-2
    want_pairs = (1 << (k - 1)) - 2
    for _ in range(want_pairs):
        if L[i] != 0 or L[i + 1] != 1:
            return None
        i += 2
    return L[i:]  # the MARKER, head-adjacent-first


def layer_bits(k, maxpairs):
    """layer_k = false false true (01)^{2^k-2}, head-adjacent-first, truncated to maxpairs pairs."""
    p = (1 << k) - 2
    p = min(p, maxpairs)
    return [0, 0, 1] + [0, 1] * p, (1 << k) - 2


# ---------------------------------------------------------------- g=2 rung positions (measured)
RUNGS = {5: 739656, 6: 740809, 7: 745442, 8: 763979, 9: 838036, 10: 1133853, 11: 2315814}
HI = max(RUNGS.values()) + 10

print("=== extracting regenIn k configs on the g=2 orbit ===")
snap = {}
targets = set(RUNGS.values())


def hook(step, st, pos, tape):
    if step in targets:
        snap[step] = (pos, bytes(tape))


run(HI, hook=hook)

markers = {}
for k, s in RUNGS.items():
    pos, tp = snap[s]
    ta = bytearray(tp)
    mk = parse_regenIn_left(ta, pos, k)
    if mk is None:
        print(f"  k={k}: FAILED to parse regenIn {k} shape at step {s} (instrument problem?)")
        continue
    # report the marker's leading structure
    lead = mk[:8]
    markers[k] = mk
    print(f"  k={k} @ {s}: marker starts {lead}...  (len {len(mk)})")

# ---------------------------------------------------------------- test the layer-peel recursion
print("\n=== does marker_k begin with layer_k = 00 1 (01)^{2^k-2}, and the rest = marker_{k+1}? ===")
for k in range(5, 11):
    if k not in markers or (k + 1) not in markers:
        continue
    mk, mk1 = markers[k], markers[k + 1]
    p = (1 << k) - 2
    layer = [0, 0, 1] + [0, 1] * p
    if mk[:len(layer)] == layer:
        rest = mk[len(layer):]
        match = (rest == mk1)
        # how much of rest matches mk1
        common = 0
        for a, b in zip(rest, mk1):
            if a == b:
                common += 1
            else:
                break
        print(f"  k={k}: marker_k STARTS with layer_k (00 1 (01)^{p}). "
              f"rest len {len(rest)} vs marker_{k+1} len {len(mk1)}; "
              f"{'EXACT MATCH' if match else f'first {common} bits agree'}")
    else:
        # find where it diverges
        common = 0
        for a, b in zip(mk, layer):
            if a == b:
                common += 1
            else:
                break
        print(f"  k={k}: marker_k does NOT start with layer_k — agrees {common}/{len(layer)} bits. "
              f"marker head {mk[:12]}, layer head {layer[:12]}")

# ---------------------------------------------------------------- the base marker (top of ladder)
print("\n=== marker at the TOP rung (k=11) — the ladder 'base marker' beyond the stack ===")
if 11 in markers:
    print(f"  marker_11 (len {len(markers[11])}): {markers[11][:20]}...")
