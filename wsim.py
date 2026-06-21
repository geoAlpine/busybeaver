#!/usr/bin/env python
"""
Word-block symbolic simulator (segment model) — for multi-symbol-repeater bouncers.

Tape = list of segments around an implicit 0^inf on both ends:
  ['c', [cells...]]            concrete run of single cells
  ['r', (W tuple), (a, b)]     a repeater: word W repeated (a*n + b) times  (n the growth variable)
head = (seg index into a 'c' segment, offset); state = letter.

Stepping: ordinary TM micro-step inside concrete segments. When the head would walk INTO a repeater
segment, it is crossed atomically by a VERIFIED word-chain (wchain.extract_chain: q steps/copy,
uniform across 3 concrete copies => sound for any count). No trace extrapolation (the v3 sin).

G1 validation (bottom): instantiate at concrete n, run the macro-sim and the trusted concrete sim
in lockstep, compare cell-for-cell. Same discipline that validated counter_prove.py.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from wchain import extract_chain


def val(exp, n):
    return exp[0] * n + exp[1]


def _cp(segs):
    """deep-copy segments (the 'c' cell lists are mutable and must not be shared)."""
    return [[x[0], list(x[1])] if x[0] == "c" else [x[0], x[1], x[2]] for x in segs]


def exps_valid(cfg, base):
    """every repeater count is >= 0 at n=base (so the symbolic derivation is valid for all n>=base)."""
    return all(val(s[2], base) >= 0 for s in cfg[1] if s[0] == "r")


def expand(segs, n):
    """-> (cells list, seg_start_index list)."""
    cells = []; starts = []
    for s in segs:
        starts.append(len(cells))
        if s[0] == "c":
            cells += list(s[1])
        else:
            cells += list(s[1]) * val(s[2], n)
    return cells, starts


def cfg_to_tape(cfg, n):
    state, segs, hi, ho = cfg
    cells, starts = expand(segs, n)
    head_abs = starts[hi] + ho
    tape = {i: c for i, c in enumerate(cells) if c}
    return tape, head_abs, state


def normalize(cfg):
    """merge adjacent 'c' segs, drop empty/zero-count segs, keep head valid. Returns new cfg."""
    state, segs, hi, ho = cfg
    # map old head to an absolute marker so we can re-find it
    # tag the head cell with a sentinel object inside the concrete seg
    segs = _cp(segs)
    # drop zero-count repeaters and empty concrete segs (but not the head seg) by rebuilding
    out = []; head_marker = ("HEAD", hi, ho)
    for idx, s in enumerate(segs):
        if s[0] == "r" and s[2] == (0, 0):
            continue
        if s[0] == "c" and len(s[1]) == 0 and idx != hi:
            continue
        out.append((idx, s))
    # merge adjacent concrete
    merged = []
    for idx, s in out:
        if s[0] == "c" and merged and merged[-1][1][0] == "c":
            # record offset shift for head if needed
            merged[-1] = (merged[-1][0] + [idx], ["c", merged[-1][1][1] + s[1]])
        else:
            merged.append(([idx], list(s)))
    # find new head seg/off
    new_segs = [m[1] for m in merged]
    new_hi = new_ho = None
    for ni, (idxs, s) in enumerate(merged):
        if hi in idxs and s[0] == "c":
            # offset = cells before in the merged seg + ho
            off = 0
            for j in idxs:
                if j == hi:
                    off += ho; break
                off += len(segs[j][1])
            new_hi, new_ho = ni, off
            break
    if new_hi is None:                       # head seg vanished (shouldn't); fallback
        return state, new_segs, hi, ho
    return state, new_segs, new_hi, new_ho


def micro(M, cfg):
    """One macro action. Returns (kind, cost_in_micro_steps) or ('HALT',0)/('STUCK',0)."""
    state, segs, hi, ho = cfg
    segs = _cp(segs)
    cur = segs[hi][1][ho]
    tr = M[state][cur]
    if tr is None:
        return cfg, ("HALT", 0)
    w, mv, ns = tr
    segs[hi][1][ho] = w
    d = 1 if mv == "R" else -1
    nho = ho + d
    if 0 <= nho < len(segs[hi][1]):
        return (ns, segs, hi, nho), ("MICRO", 1)
    # stepped off this concrete seg
    nbr = hi + d                              # neighbor index in travel direction
    if d > 0:
        if nbr >= len(segs):                  # blank to the right
            segs.append(["c", [0]]); return (ns, segs, nbr, 0), ("MICRO", 1)
        if segs[nbr][0] == "c":
            return (ns, segs, nbr, 0), ("MICRO", 1)
        res = cross(M, ns, segs, hi, nbr, +1)
        return res if res[1][0] != "STUCK" else materialize(ns, segs, nbr, +1)
    else:
        if nbr < 0:                           # blank to the left
            segs.insert(0, ["c", [0]]); return (ns, segs, 0, 0), ("MICRO", 1)
        if segs[nbr][0] == "c":
            return (ns, segs, nbr, len(segs[nbr][1]) - 1), ("MICRO", 1)
        res = cross(M, ns, segs, hi, nbr, -1)
        return res if res[1][0] != "STUCK" else materialize(ns, segs, nbr, -1)


def materialize(ns, segs, rep, d):
    """no chain crosses repeater segs[rep]=(W,exp): peel ONE concrete copy of W on the head's side so
    the head can micro-step into it (a boundary bounce). Sound: (W)^exp = (W)^(exp-1) . W. If the head
    bounces back, absorb() re-folds it. Validity (exp-1 >= 0 for n>=base) is checked by the prover."""
    W = segs[rep][1]; exp = segs[rep][2]
    segs[rep][2] = (exp[0], exp[1] - 1)
    if d > 0:                                  # head entering from the left -> copy goes left of repeater
        segs.insert(rep, ["c", list(W)])
        return (ns, segs, rep, 0), ("MICRO", 1)
    else:                                      # entering from the right -> copy goes right of repeater
        segs.insert(rep + 1, ["c", list(W)])
        return (ns, segs, rep + 1, len(W) - 1), ("MICRO", 1)


def _sim_cross(M, state, W, K, d):
    """Cross K concrete copies of W with HEAD-CONTAINMENT: the head enters (W)^K at the near boundary
    in `state` and must exit at the FAR boundary in `state`, reading ONLY cells of the K copies in
    between. If it ever reads outside [0, K|W|) (a neighbour) the crossing is context-dependent and we
    return None (SOUND: a chain is trusted only when crossing is independent of what bounds the
    repeater — the bug fix). Returns (W' tuple, total_steps) on a clean contained crossing."""
    qc = len(W); N = K * qc
    tape = {i: W[i % qc] for i in range(N)}
    head = 0 if d > 0 else N - 1
    s = state; steps = 0; cap = N * 8 + 60
    while steps < cap:
        if (d > 0 and head == N) or (d < 0 and head == -1):
            break                                  # exited the far boundary cleanly
        if head < 0 or head >= N:
            return None                            # read a neighbour -> context-dependent, reject
        tr = M[s].get(tape[head])
        if tr is None:
            return None
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; s = ns; steps += 1
    else:
        return None                                # didn't exit within cap
    if s != state:
        return None                                # must return to the same state at the far boundary
    region = [tape[i] for i in range(N)]
    Wp = tuple(region[:qc])
    if any(tuple(region[i:i + qc]) != Wp for i in range(0, N, qc)):
        return None                                # transformed word must be uniform across copies
    return Wp, steps


_CHAIN_CACHE = {}


def chain_cross(M, state, W, d):
    """Verify a SOUND contained chain by crossing K = 2,3,4 copies: same transformed word W', same
    exit state, and steps LINEAR in K through the origin (steps = K*qstep). If so the per-copy
    behaviour is uniform AND contained, so crossing (W)^m is sound for any m>=1. Returns (W', qstep).
    Memoized per (machine, state, W, d) — deterministic, so caching is sound and avoids recomputing
    on materialize-loops (a big speedup)."""
    mkey = tuple((s, sym, M[s].get(sym)) for s in M for sym in (0, 1))
    key = (mkey, state, tuple(W), d)
    if key in _CHAIN_CACHE:
        return _CHAIN_CACHE[key]
    if len(_CHAIN_CACHE) > 50000:
        _CHAIN_CACHE.clear()
    res = []
    for K in (2, 3, 4):
        r = _sim_cross(M, state, list(W), K, d)
        if r is None:
            _CHAIN_CACHE[key] = None; return None
        res.append(r)
    Wp = res[0][0]
    out = None
    s0, s1, s2 = (st for _, st in res)
    qstep = s1 - s0
    if (not any(w != Wp for w, _ in res)) and (s1 - s0 == s2 - s1) and qstep > 0 and s0 == 2 * qstep:
        out = (Wp, qstep)                          # uniform + linear-through-origin = sound chain
    _CHAIN_CACHE[key] = out
    return out


def cross(M, state, segs, from_seg, rep_seg, d):
    """head in `state` about to enter repeater segs[rep_seg]=(W,exp) from direction d. Cross via a
    CONTAINED, uniform word-chain (chain_cross); reject (STUCK) if crossing is neighbour-dependent.
    The chain op carries (exp, qstep): cost = exp*qstep micro-steps (+1 entry, in validate)."""
    _, W, exp = segs[rep_seg]
    info = chain_cross(M, state, list(W), d)
    if info is None:
        return (state, segs, from_seg, (0 if d > 0 else len(segs[from_seg][1]) - 1)), ("STUCK", 0)
    Wp, qstep = info
    segs[rep_seg] = ["r", Wp, exp]
    far = rep_seg + d
    if d > 0:
        if far >= len(segs):
            segs.append(["c", [0]]); return (state, segs, far, 0), ("CHAINR", exp, qstep)
        if segs[far][0] == "c":
            return (state, segs, far, 0), ("CHAINR", exp, qstep)
        return (state, segs, rep_seg, 0), ("STUCK", 0)
    else:
        if far < 0:
            segs.insert(0, ["c", [0]]); return (state, segs, rep_seg, 0), ("CHAINL", exp, qstep)
        if segs[far][0] == "c":
            return (state, segs, far, len(segs[far][1]) - 1), ("CHAINL", exp, qstep)
        return (state, segs, rep_seg, 0), ("STUCK", 0)


def absorb(cfg):
    """canonicalize: fold concrete W-copies that sit against a repeater into its exponent (sound
    re-bracketing: 'c'[..W] 'r'W^e == 'r'W^(e+1) with 'c'[..]). Never absorbs the head's cell."""
    state, segs, hi, ho = cfg
    segs = _cp(segs)
    changed = True
    while changed:
        changed = False
        for i, s in enumerate(segs):
            if s[0] != "r":
                continue
            W = s[1]; q = len(W)
            # left neighbor: absorb trailing copies of W
            if i - 1 >= 0 and segs[i - 1][0] == "c":
                c = segs[i - 1][1]; j = 0
                while len(c) >= (j + 1) * q and tuple(c[len(c) - (j + 1) * q: len(c) - j * q]) == W:
                    j += 1
                if i - 1 == hi:                      # don't absorb the head's cell
                    while j > 0 and ho >= len(c) - j * q:
                        j -= 1
                if j > 0:
                    segs[i][2] = (s[2][0], s[2][1] + j)
                    segs[i - 1][1] = c[:len(c) - j * q]; changed = True
            # right neighbor: absorb leading copies of W
            if i + 1 < len(segs) and segs[i + 1][0] == "c":
                c = segs[i + 1][1]; j = 0
                while len(c) >= (j + 1) * q and tuple(c[j * q:(j + 1) * q]) == W:
                    j += 1
                if i + 1 == hi:
                    while j > 0 and ho < j * q:
                        j -= 1
                if j > 0:
                    segs[i][2] = (s[2][0], s[2][1] + j)
                    segs[i + 1][1] = c[j * q:]
                    if i + 1 == hi:
                        ho -= j * q
                    changed = True
    return normalize((state, segs, hi, ho))


def step(M, cfg):
    cfg2, op = micro(M, cfg)
    if op[0] in ("HALT", "STUCK"):
        return cfg2, op
    return absorb(normalize(cfg2)), op


def cost_micro(op, exp_or_word, q, n):
    if op[0] == "MICRO":
        return 1
    if op[0] in ("CHAINR", "CHAINL"):
        return val(op[1], n) * q
    return 0


# ---------------- G1 validation ----------------
def concrete_run(M, tape, head, st, nsteps):
    for _ in range(nsteps):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return tape, head, st, True
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns
    return tape, head, st, False


def validate(spec, cfg0, ns=(3, 4, 5, 7), max_macro=200):
    M = parse(spec); checked = 0
    for n in ns:
        cfg = cfg0
        tape, head, st = cfg_to_tape(cfg, n)
        ctape, chead, cst = dict(tape), head, st
        for i in range(max_macro):
            # cost needs q of the repeater being crossed; recompute inside
            prev = cfg
            cfg, op = step(M, cfg)
            if op[0] == "HALT":
                break
            if op[0] == "STUCK":
                break
            if op[0] == "MICRO":
                cost = 1
            else:                                # CHAIN ('CHAINR'/'CHAINL', exp, qstep): 1 entry + copies*qstep
                cost = 1 + val(op[1], n) * op[2]
            ctape, chead, cst, halted = concrete_run(M, ctape, chead, cst, cost)
            stape, shead, sst = cfg_to_tape(cfg, n)
            if sst != cst:
                return False, f"n={n} op#{i} state {sst}!={cst} op={op}"
            keys = set(k for k, v in stape.items() if v) | set(k for k, v in ctape.items() if v)
            for off in range(-3, 4):
                for base in (shead, chead):
                    pass
            # compare relative to head
            allk = set(stape) | set(ctape)
            for k in range(min(allk, default=0) - 2, max(allk, default=0) + 3):
                if stape.get(shead - chead + k, 0) != ctape.get(k, 0):
                    return False, f"n={n} op#{i} tape mismatch @{k} op={op}\n  sym head={shead} {cfg}\n  con head={chead}"
            checked += 1
    return True, f"validated {len(ns)} n-values, {checked} macro-ops cell-for-cell"


def main():
    # (10)^n bouncer; C(n) = (10)^n . "10", head on the trailing 0, state B (matches the (R,B) record).
    spec = "1RB0LB_1LA0RA_0LA0LZ"
    cfg0 = ("B", [["r", (1, 0), (1, 0)], ["c", [1, 0]]], 1, 1)
    ok, detail = validate(spec, cfg0, ns=(6, 7, 8, 10), max_macro=400)
    print("=" * 70)
    print("wsim — G1 word-block simulator validation")
    print(f"  {spec}  C(n) = (10)^n 10, head on trailing 0, state B")
    print(f"  {'OK' if ok else 'FAIL'}: {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
