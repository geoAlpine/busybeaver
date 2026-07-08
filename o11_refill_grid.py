#!/usr/bin/env python3
"""
o11 refill-law deep dive, part 2: STANDALONE EPOCH GRID (2026-07-08).
Seed a standalone epoch at the B/right-extreme milestone (k, m=2): tape 1^k 0 (10)^2,
state B, head one right of the last 1 (exactly the captured real-orbit milestone
placement). Run each seed to its FIRST pure-collapse event (state F at right extreme,
single RLE block) or HALT. Record: the in-epoch milestone chain (k countdown + sea m),
the end-game (last milestone before collapse), the collapse value c, and the
post-refill milestone (verify (c-2, 2)).
Goal: the EXACT map epoch-seed -> collapse value, per k0 mod 4 branch; and the exact
location/mechanism of the k0 = 2 (mod 4) within-epoch halts.  [OBSERVED grid; halts
are PROVEN-by-run fatal members.]
"""
import sys
from msea_struct2 import parse, rle_blocks

SPEC = "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"
SN = "ABCDEF"

def T(m):
    return (3 * m) // 2 + 4

def run_epoch(k0, m0=2, budget=120_000_000, sz_pow=24):
    """Seed [1^k0 0 (10)^m0], B, head last1+1. Run to first pure collapse (F at right
    extreme, single block) then on to the next B milestone; or HALT; or budget.
    Returns dict."""
    M = parse(SPEC)
    SZ = 1 << sz_pow
    tape = bytearray(SZ)
    p = SZ // 4
    for _ in range(k0):
        tape[p] = 1; p += 1
    p += 1
    for _ in range(m0):
        tape[p] = 1; p += 2
    last1 = p - 2
    lo = SZ // 4
    hi = pos = last1 + 1
    st = 1  # B
    step = 0
    mils = []          # (step, blocks) at B/right-extreme, deduped
    last_mil = None
    collapse = None    # (step, c)
    post = None        # (step, blocks) first B milestone after collapse
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return dict(k0=k0, m0=m0, halt=step, mils=mils, collapse=collapse, post=post)
        if pos >= hi and (st == 1 or st == 5):
            b = rle_blocks(tape, lo, hi)
            if st == 5 and len(b) == 1 and collapse is None:
                # pure collapse: state F, single block
                collapse = (step, b[0])
            elif st == 1 and b != last_mil:
                if collapse is not None:
                    post = (step, b)
                    return dict(k0=k0, m0=m0, halt=None, mils=mils, collapse=collapse, post=post)
                mils.append((step, b))
                last_mil = list(b)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return dict(k0=k0, m0=m0, halt=None, mils=mils, collapse=collapse, post=post, budget=True)

def summarize(res, verbose=False):
    k0 = res['k0']
    mils = res['mils']
    # decode milestones as (lead k, sea m) where possible
    dec = []
    for s, b in mils:
        if len(b) >= 2 and all(x == 1 for x in b[1:]):
            dec.append((b[0], len(b) - 1))
        elif len(b) >= 1 and all(x == 1 for x in b):
            dec.append((0, len(b)))          # pure sea, k exhausted (lead block is sea)
        else:
            dec.append(('?', b[:6]))
    tag = ""
    if res['halt'] is not None:
        tag = f"HALT@{res['halt']}"
    elif res.get('budget'):
        tag = "BUDGET"
    c = res['collapse'][1] if res['collapse'] else None
    post = res['post'][1] if res['post'] else None
    postdec = None
    if post and len(post) >= 2 and all(x == 1 for x in post[1:]):
        postdec = (post[0], len(post) - 1)
    if verbose:
        print(f"k0={k0:>4} (k0%4={k0%4})  chain={dec}  c={c}  post={postdec}  {tag}")
    return dec, c, postdec, tag

if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    rows = []
    for k0 in range(1, kmax + 1):
        res = run_epoch(k0)
        dec, c, postdec, tag = summarize(res, verbose=True)
        rows.append((k0, dec, c, postdec, tag, res))
    print()
    print("=== law extraction: c vs end-game")
    print("k0%4 | k0 -> (k_last, m_last) -> c ; candidate laws")
    for k0, dec, c, postdec, tag, res in rows:
        if c is None:
            continue
        kl, ml = dec[-1] if dec else (None, None)
        if not isinstance(kl, int):
            continue
        print(f"  k0={k0:>4} r={k0%4} last=({kl},{ml}) c={c}  c-3*ml={c-3*ml}  c-3*T(ml)={c-3*T(ml)}  post={postdec}")
    # refill map check
    ok = sum(1 for k0, dec, c, postdec, tag, res in rows
             if c is not None and postdec == (c - 2, 2))
    tot = sum(1 for k0, dec, c, postdec, tag, res in rows if c is not None)
    print(f"\nrefill map post == (c-2, 2): {ok}/{tot}")
    halts = [(k0, tag) for k0, dec, c, postdec, tag, res in rows if tag.startswith('HALT')]
    print(f"halts: {halts}")
    print("No machine decided. No label upgraded.")
