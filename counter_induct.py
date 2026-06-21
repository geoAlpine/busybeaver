#!/usr/bin/env python
"""
Counter prover — STEP 2, the nested-induction engine. PIECE 1: the macro-machine substrate.

The bouncer provers build a repeater seg by hand from a record. A COUNTER's interior is a binary
counter (not one uniform run), so to accelerate it we must (a) AUTO-COMPRESS uniform runs into
repeaters and (b) cross them with wsim's verified chains. This file builds and G1-VALIDATES that
substrate. The rule-detection + proof-by-induction layers come next (PIECE 2/3).

`compress` is a SOUND re-bracketing: a run of k identical cells in a concrete segment becomes a
repeater (sym,)^k. It never touches the head's cell. With it, the counter's left/right sweeps
(self-loop chains: here state A sweeps left over 1s unchanged, state B sweeps right over 1s -> 0)
become single macro-steps, so the simulator reaches k carry-outs in ~poly(k) macro-steps with the
SAME tape as the trusted simulator (validated below).
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from wsim import step, val, cfg_to_tape, _cp, normalize


def merge_reps(cfg):
    """merge adjacent repeaters of the SAME word into one (sound: (W)^a (W)^b = (W)^(a+b)).
    Adjusts the head index. Concrete-segment merging is left to normalize."""
    state, segs, hi, ho = cfg
    segs = _cp(segs)
    out = []; old2new = {}
    for idx, s in enumerate(segs):
        if s[0] == "r" and out and out[-1][1][0] == "r" and tuple(out[-1][1][1]) == tuple(s[1]):
            e0 = out[-1][1][2]; out[-1][1][2] = (e0[0] + s[2][0], e0[1] + s[2][1])
            old2new[idx] = out[-1][0]
        else:
            old2new[idx] = len(out); out.append([idx, list(s)])
    new_segs = [o[1] for o in out]
    return normalize((state, new_segs, old2new.get(hi, hi), ho))


def compress(cfg, T=2):
    """fold maximal single-symbol runs (length >= T) in concrete segments into (sym,)^len repeaters,
    then merge adjacent same-word repeaters. NEVER folds the head's cell. The head position is tracked
    LOCALLY (seg index + offset) — never via absolute positions (those depend on the symbolic n)."""
    state, segs, hi, ho = cfg
    new_segs = []; nhi = nho = None
    for idx, s in enumerate(_cp(segs)):
        if s[0] != "c":
            if idx == hi:                             # head can't be in a repeater, but guard anyway
                nhi, nho = len(new_segs), ho
            new_segs.append(s); continue
        cells = s[1]; is_head = (idx == hi)
        i = 0
        while i < len(cells):
            j = i
            while j < len(cells) and cells[j] == cells[i]:
                j += 1
            head_in_run = is_head and i <= ho < j
            if j - i >= T and not head_in_run:
                new_segs.append(["r", (cells[i],), (0, j - i)])
            else:
                if head_in_run:
                    nhi, nho = len(new_segs), ho - i   # head lands in this concrete piece
                new_segs.append(["c", list(cells[i:j])])
            i = j
    if nhi is None:                                   # head seg was empty/edge; fall back
        nhi, nho = hi, ho
    return merge_reps(normalize((state, new_segs, nhi, nho)))


def macro_run(spec, start, max_ops=4000, T=2):
    """accelerated macro-sim: compress then step, repeatedly. Returns list of (op, cfg)."""
    M = parse(spec); cfg = start; trace = []
    for _ in range(max_ops):
        cfg = compress(cfg, T)
        cfg, op = step(M, cfg)
        trace.append((op, cfg))
        if op[0] in ("HALT", "STUCK"):
            break
    return trace


# ---------------- G1 validation: accelerated sim vs trusted concrete sim ----------------
def concrete_run(M, tape, head, st, nsteps):
    for _ in range(nsteps):
        tr = M[st][tape.get(head, 0)]
        if tr is None:
            return tape, head, st, True
        w, mv, ns = tr; tape[head] = w; head += 1 if mv == "R" else -1; st = ns
    return tape, head, st, False


def micro_cost(op, n):
    if op[0] == "MICRO":
        return 1
    if op[0] in ("CHAINR", "CHAINL"):
        return 1 + val(op[1], n) * op[2]
    return 0


def validate(spec, max_ops=300):
    """run the accelerated sim from the blank tape and the trusted sim in lockstep, cell-for-cell."""
    M = parse(spec)
    cfg = ("A", [["c", [0]]], 0, 0)
    ctape, chead, cst = {}, 0, "A"
    for i in range(max_ops):
        cfg = compress(cfg, 2)
        cfg, op = step(M, cfg)
        if op[0] in ("HALT", "STUCK"):
            break
        cost = micro_cost(op, 0)                       # exps are concrete here (n unused) -> val(,0)
        ctape, chead, cst, halted = concrete_run(M, ctape, chead, cst, cost)
        stape, shead, sst = cfg_to_tape(cfg, 0)
        if sst != cst:
            return False, f"op#{i} state {sst}!={cst} op={op}"
        allk = set(k for k, v in stape.items() if v) | set(k for k, v in ctape.items() if v)
        for k in range(min(allk, default=0) - 2, max(allk, default=0) + 3):
            if stape.get(shead - chead + k, 0) != ctape.get(k, 0):
                return False, f"op#{i} tape@{k} op={op}\n sym={cfg}"
    return True, f"validated {max_ops} accelerated macro-ops cell-for-cell"


def shape(cfg):
    """structural signature: state, (seg-kind, word) per seg, head — exps abstracted away."""
    st, segs, hi, ho = cfg
    return (st, tuple((s[0], tuple(s[1])) for s in segs), hi, ho)


def detect_rules(spec, max_ops=600, min_occ=4):
    """PIECE 2 (sound: detection only). Run the accelerated macro-sim and find shapes that RECUR
    with a repeater exponent growing monotonically -> candidate rules S(v) -> S(v+d). Returns
    [(count, shape, [(op_index, exps)...])]. (Detection is heuristic; the PROOF is PIECE 3.)"""
    tr = macro_run(spec, ("A", [["c", [0]]], 0, 0), max_ops=max_ops)
    groups = {}
    for i, (op, cfg) in enumerate(tr):
        exps = tuple(val(s[2], 0) for s in cfg[1] if s[0] == "r")
        groups.setdefault(shape(cfg), []).append((i, exps))
    cands = []
    for sh, occ in groups.items():
        if len(occ) < min_occ:
            continue
        seq = [e for _, e in occ if e]
        if not seq:
            continue
        for pos in range(len(seq[0])):
            vals = [e[pos] for e in seq if len(e) > pos]
            if len(vals) >= min_occ and all(vals[k + 1] > vals[k] for k in range(len(vals) - 1)):
                cands.append((len(occ), sh, occ[:6])); break
    cands.sort(reverse=True)
    return cands


def validate_symbolic(spec, start_template, ns=(4, 5, 6, 8, 11, 20), max_ops=120):
    """G1 for a SYMBOLIC start config: instantiate at concrete n, run the symbolic accelerated sim
    and the trusted sim in lockstep cell-for-cell, ONLY while exponents stay valid at that n.
    This is the guard that caught the compress head-tracking bug (absolute positions depend on n)."""
    from wsim import exps_valid
    M = parse(spec); total = 0
    for n in ns:
        cfg = start_template
        tp, hd, st = cfg_to_tape(cfg, n); ct, ch, cs = dict(tp), hd, st
        for i in range(max_ops):
            cfg = compress(cfg)
            if not exps_valid(cfg, n):
                break
            cfg, op = step(M, cfg)
            if op[0] in ("HALT", "STUCK") or not exps_valid(cfg, n):
                break
            ct, ch, cs, _ = concrete_run(M, ct, ch, cs, micro_cost(op, n))
            stape, sh, ss = cfg_to_tape(cfg, n)
            if ss != cs:
                return False, f"n={n} op#{i} state"
            allk = set(k for k, v in stape.items() if v) | set(k for k, v in ct.items() if v)
            for k in range(min(allk, default=0) - 2, max(allk, default=0) + 3):
                if stape.get(sh - ch + k, 0) != ct.get(k, 0):
                    return False, f"n={n} op#{i} tape"
            total += 1
    return True, f"{total} symbolic ops cell-for-cell across n={ns}"


def d_window(cfg):
    """Is the head at a D-form '... 1 (0)^m B> 0' window? Return (rep_seg_index, exp_tuple) or None.
    D-form: state B, head on a concrete [0] cell (offset 0), the seg just left is (0,)^m, and the seg
    left of THAT ends in 1."""
    st, segs, hi, ho = cfg
    if st != "B" or ho != 0:
        return None
    if hi < 2 or segs[hi][0] != "c" or not segs[hi][1] or segs[hi][1][0] != 0:
        return None
    r = segs[hi - 1]; L = segs[hi - 2]
    if r[0] == "r" and tuple(r[1]) == (0,) and L[0] == "c" and L[1] and L[1][-1] == 1:
        return hi - 1, r[2]
    return None


def lt_var(exp, base):
    """is the linear exponent exp = a*k+b provably < k (the induction variable) for all k>=base?"""
    a, b = exp
    if a == 0:
        return b < base                      # constant m < k  iff  m < base (<= smallest k)
    if a == 1:
        return b <= -1                       # k+b < k  iff  b<0
    return False


def prove_counter(spec, base=3, max_ops=4000):
    """‼ WIP / NOT VALIDATED — never returns a trusted proof yet. ‼
    BREAKTHROUGH (sound, confirmed by the faithful simulator): the canonical counter obeys the
    SELF-RECURSIVE rule  R: D(k)->D(k+1)  (D(k)='1 0^k B>', the 0-block grows by 1), and R for all k
    => unbounded tape => never halts. R is provable by induction.

    BUT the inductive STEP here is WRONG and INCOMPLETE: sligocki's method applies the IH D(k-1)->D(k)
    a CONSTANT number of times (twice — that is the f(n+1)=2f(n)+... doubling), to the SYMBOLIC k-1.
    This draft instead applies R(m) to CONCRETE inner windows (m=2,3,4,...) — exponentially many, and
    it mishandles the window CONTEXT (head-containment is not verified). So it does NOT close, and its
    IH application is unsound in general. It is kept as a documented WIP. To finish: recognise the
    symbolic D(k-1) sub-structure, apply R(k-1) twice with head-containment verified, gate on the
    cryptids + a self-consistency check on f(k). DO NOT trust a NEVER_HALTS from this until then."""
    M = parse(spec)

    def D(kexp):
        return ("B", [["c", [1]], ["r", (0,), kexp], ["c", [0]]], 2, 0)

    # ---- base case: D(base) -> D(base+1) concretely (no IH), no halt ----
    cfg = D((0, base)); ok_base = False
    for _ in range(max_ops):
        cfg = compress(cfg); cfg, op = step(M, cfg)
        if op[0] == "HALT":
            return "HALTS-base", None
        st, segs, hi, ho = cfg
        if (st, hi, ho) == ("B", 2, 0) and len(segs) == 3 and segs[0] == ["c", [1]] \
           and segs[1][0] == "r" and tuple(segs[1][1]) == (0,) and segs[2] == ["c", [0]]:
            if val(segs[1][2], 0) == base + 1:
                ok_base = True
            break
    if not ok_base:
        return "HOLDOUT", "base case did not reach D(base+1)"

    # ---- inductive step: D(k) symbolic -> D(k+1), applying R(m) on inner windows (m<k) ----
    cfg = D((1, 0))                            # D(k), k symbolic
    applied = 0
    for _ in range(max_ops):
        w = d_window(cfg)
        # apply the IH on an inner window whose exponent is provably < k, and is NOT the whole start
        if w and lt_var(w[1], base) and not (cfg == D((1, 0))):
            ridx, mexp = w
            st, segs, hi, ho = cfg
            segs = _cp(segs)
            segs[ridx][2] = (mexp[0], mexp[1] + 1)   # R(m): D(m) -> D(m+1)  (0-block + 1)
            cfg = compress((st, segs, hi, ho)); applied += 1
            continue
        cfg = compress(cfg)
        # closure: reached D(k+1)?
        st, segs, hi, ho = cfg
        if (st, hi, ho) == ("B", 2, 0) and len(segs) == 3 and segs[0] == ["c", [1]] \
           and segs[1][0] == "r" and tuple(segs[1][1]) == (0,) and segs[2] == ["c", [0]] \
           and segs[1][2] == (1, 1):           # exp = k+1
            # ‼ IH logic NOT validated -> NEVER claim a proof here yet (avoid the v3 sin)
            return "WIP-CLOSED-UNTRUSTED", ("D(k)->D(k+1)", f"base={base}", f"IH-applied={applied}")
        cfg, op = step(M, cfg)
        if op[0] == "HALT":
            return "‼ HALT-in-step", None
        if op[0] == "STUCK":
            return "HOLDOUT", "step stuck"
    return "HOLDOUT", "step did not close to D(k+1)"


def main():
    spec = "1RB1LA_0LA0RB_0LA0LZ"
    ok, detail = validate(spec)
    Csym = ("A", [["c", [0]], ["r", (1,), (1, 0)], ["c", [0]]], 0, 0)
    oks, dets = validate_symbolic(spec, Csym)
    print("=" * 70)
    print("counter_induct — accelerated macro-machine (compress + chains)")
    print(f"  {spec}")
    print(f"  PIECE 1 (G1 from blank):  {'OK' if ok else 'FAIL'}: {detail}")
    print(f"  PIECE 3 (G1 symbolic C(n)): {'OK' if oks else 'FAIL'}: {dets}")
    print(f"  PIECE 2 (rule detection): candidate self-similar shapes (recur with growing exponent):")
    for cnt, sh, occ in detect_rules(spec)[:6]:
        st, kinds, hi, ho = sh
        desc = " ".join(("".join(map(str, w)) if k == "c" else "(" + "".join(map(str, w)) + ")^*")
                        for k, w in kinds)
        print(f"    x{cnt}  {st} [{desc}] h=({hi},{ho})  e.g. {occ[:4]}")
    print("  PIECE 3 (window-rule nested-induction proof) = the next build (the hard sligocki core).")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
