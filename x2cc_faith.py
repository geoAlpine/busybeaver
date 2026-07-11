#!/usr/bin/env python3
"""x2cc_faith.py -- CARRY CALCULUS step 3: the faithfulness induction, mechanized.

Proves milestone-to-milestone transports of the x2 machine on PARAMETERIZED
configurations using the certified symbolic executor (x2cc_symb).  The prover:

  * runs the symbolic executor; whenever a comparison is undecidable (Split), it
    case-splits automatically: for a single-parameter affine expression it branches
    into finitely many concrete small cases plus a shifted general case (param := param'+k)
    -- an exhaustive, sound case analysis;
  * detects LOOPS: if the current config equals an earlier config under a uniform
    parameter shift (p := p - d), the segment between them is a PROVEN inductive step
    (it was derived symbolically, i.e. for every parameter value satisfying the
    assumptions), so the loop may be accelerated: config(p) ->* config(p mod d ...)
    with the segment's event multiset repeated.  Only d=1 accelerations are used here
    (then the loop closes at p=0 exactly);
  * collects every E-met gap event (length >= 2); the executor HALTS on any gap of
    length exactly 3 (the proven halt gate), so a completed derivation IS a proof that
    the transport emits no fatal event.

Every completed transport is therefore a machine-checked induction: micro-steps are
the raw TM; macro-rules are the certified closed forms; splits are exhaustive; loop
acceleration is induction on the shifted parameter.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import (E, ZERO, ONE, Config, Machine, Split, Halted, merge,
                       runs_concrete, check_rules)


def T(spec, **params):
    """template DSL -> run list.  spec: space-separated tokens pat^cnt, cnt an int,
    param name, or 'param+int' / 'int*param+int'."""
    runs = []
    for tok in spec.split():
        if '^' in tok:
            pat, c = tok.split('^')
        else:
            pat, c = tok, '1'
        runs.append((pat, parse_cnt(c, params)))
    return merge(runs)


def parse_cnt(c, params):
    c = c.strip()
    if c.lstrip('-').isdigit():
        return E(int(c))
    # forms: p | p+3 | 4p+1 | p-2
    import re
    m = re.fullmatch(r'(?:(\d+)\*?)?([A-Za-z]\w*)(?:([+-]\d+))?', c)
    assert m, c
    coef = int(m[1]) if m[1] else 1
    const = int(m[3]) if m[3] else 0
    return E.var(m[2], coef, const)


class Prover:
    """Depth-first exhaustive case analysis with loop acceleration."""

    def __init__(self, name, verbose=True):
        self.name = name
        self.verbose = verbose
        self.results = []   # (case-desc, final config, events)
        self.failed_loops = set()
        self.ok = True

    def log(self, *a):
        if self.verbose:
            print(' ', *a, flush=True)

    def prove(self, cfg, goal, case='', depth=0, events=None, max_ops=200000,
              allow_loops=True):
        """run cfg until it matches goal (a Goal object, substituted along with the
        config on every case split), splitting and loop-accelerating."""
        if depth > 60:
            raise RuntimeError("split depth exceeded")
        m = Machine(cfg.copy(), guard_r=True)
        m.events = list(events or [])
        history = []
        ops = 0
        while ops < max_ops:
            ops += 1
            if goal.matches(m.cfg):
                self.results.append((case, m.cfg.copy(), list(m.events)))
                self.log(f"[{case or 'base'}] reached target: {m.cfg}")
                ev = [(str(e[2]) if e[1] == 'gap' else f"loop:{e[2]}") for e in m.events]
                self.log(f"    events: {ev}")
                return
            if allow_loops:
                hit = None
                ck = m.cfg.key()
                for (pcfg, pevents) in history:
                    if (pcfg.key(), ck) in self.failed_loops:
                        continue
                    r = self.match_general(pcfg, m.cfg)
                    if r:
                        hit = (pcfg, pevents, r)
                        break
                if hit:
                    pcfg, pevents, (p, deltas) = hit
                    body_events = m.events[len(pevents):]
                    for (_, kind, L) in body_events:
                        if kind == 'gap' and not L.is_const():
                            raise RuntimeError(f"loop body event symbolic {L}")
                    self.log(f"[{case}] LOOP candidate on {p}, accumulators at runs "
                             f"{sorted(deltas)}; body events {[str(e[2]) for e in body_events if e[1]=='gap']}")
                    fin = self.accelerate(pcfg, p, deltas, case, depth)
                    if fin is None:
                        self.failed_loops.add((pcfg.key(), ck))
                    if fin is not None:
                        nevents = list(pevents) + [
                            (E(0), 'loop', (str(p), tuple(le[2].c for le in body_events
                                                          if le[1] == 'gap')))]
                        self.prove(fin, goal, case=f"{case}|loop({p})",
                                   depth=depth + 1, events=nevents,
                                   max_ops=max_ops - ops)
                        return
                history.append((m.cfg.copy(), list(m.events)))
            try:
                m.step()
            except Split as s:
                expr = s.expr
                if expr is None or expr.is_const():
                    raise
                # choose a positive-coef param to split on
                p = None
                for q, coef in sorted(expr.m.items()):
                    if coef > 0:
                        p = q
                        break
                if p is not None:
                    self.log(f"[{case}] split on {p} (expr {expr}): {p}=0 | {p}>=1")
                    c0 = self.subst_config(m.cfg, p, E(0))
                    ev0 = self.subst_events(m.events, p, E(0))
                    self.prove(c0, goal.subst(p, E(0)), case=f"{case}|{p}=0",
                               depth=depth + 1, events=ev0, max_ops=max_ops - ops)
                    c1 = self.subst_config(m.cfg, p, E.var(p, 1, 1))
                    ev1 = self.subst_events(m.events, p, E.var(p, 1, 1))
                    self.prove(c1, goal.subst(p, E.var(p, 1, 1)), case=f"{case}|{p}+",
                               depth=depth + 1, events=ev1, max_ops=max_ops - ops)
                    return
                raise
        raise RuntimeError(f"max_ops exceeded in case {case}; cfg={m.cfg}")

    def accelerate(self, pcfg, p, deltas, case, depth):
        """Certify the loop: generalize accumulator runs with fresh param J, prove the
        body INV(p+1, J) ->* INV(p, J+1) symbolically, then return INV[p:=0, J:=p].
        deltas: dict {(side, idx): +k} of runs whose counts grow by const k per round.
        Sound: the body proof holds for every p>=0, J>=0; iterating from the current
        (p, J=0) down to p=0 accumulates J=p."""
        JP = f"J{depth}"
        gen = pcfg.copy()

        def adjust(runs, side):
            out = []
            for i, (pat, cnt) in enumerate(runs):
                k = deltas.get((side, i))
                if k:
                    if k < 0:
                        return None
                    out.append((pat, cnt + E.var(JP, k)))
                else:
                    out.append((pat, cnt))
            return out
        gl = adjust(gen.left, 'L')
        gr = adjust(gen.right, 'R')
        if gl is None or gr is None:
            self.log(f"[{case}] negative accumulator; loop not certified")
            return None
        inv = Config(gl, gen.state, gr, E(0))
        inv1 = self.subst_config(inv, p, E.var(p, 1, 1))     # p := p+1
        tgt = self.subst_config(inv, JP, E.var(JP, 1, 1))    # J := J+1 (p stays)
        sub = Prover(f"{self.name}/body({p})", verbose=self.verbose)
        try:
            sub.prove(inv1, GoalConfig(tgt), case='body', depth=depth + 1,
                      allow_loops=False, max_ops=20000)
        except Exception as ex:
            self.log(f"[{case}] body proof FAILED: {ex}")
            return None
        if len(sub.results) < 1:
            return None
        # all body branches must have reached the target (prove raises otherwise)
        self.log(f"[{case}] loop body PROVEN: INV({p}+1,{JP}) ->* INV({p},{JP}+1), "
                 f"{len(sub.results)} branch(es)")
        fin = self.subst_config(inv, p, E(0))        # p := 0 (loop exhausted)
        fin = self.subst_config(fin, JP, E.var(p))   # J := p (rounds executed)
        return fin

    @staticmethod
    def match_general(c1, c2):
        """c2 == c1 with p := p-1 for one param, allowing some runs' counts to differ
        by positive integer consts (accumulators).  returns (p, {(side,idx): k}) or None."""
        if c1.state != c2.state:
            return None
        if len(c1.left) != len(c2.left) or len(c1.right) != len(c2.right):
            return None
        pairs = []
        for side, (r1, r2) in (('L', (c1.left, c2.left)), ('R', (c1.right, c2.right))):
            for i, ((p1, e1), (p2, e2)) in enumerate(zip(r1, r2)):
                if p1 != p2:
                    return None
                pairs.append((side, i, e1, e2))
        params = set()
        for _, _, e1, e2 in pairs:
            params |= set(e1.m) | set(e2.m)
        for p in params:
            deltas = {}
            good = True
            used = False
            for side, i, e1, e2 in pairs:
                e1s = e1.subst(p, E.var(p, 1, -1))
                if p in e1.m:
                    used = True
                d = e2 - e1s
                if d.is_const():
                    if d.c > 0:
                        deltas[(side, i)] = d.c
                    elif d.c < 0:
                        good = False
                        break
                else:
                    good = False
                    break
            if good and used:
                return (p, deltas)
        return None

    @staticmethod
    def subst_config(cfg, p, val):
        def s(runs):
            return merge([(pat, c.subst(p, val)) for pat, c in runs])
        return Config(s(cfg.left), cfg.state, s(cfg.right), E(0))

    @staticmethod
    def subst_events(events, p, val):
        return [(st, k, (L.subst(p, val) if isinstance(L, E) else L))
                for st, k, L in events]

    @staticmethod
    def match_shift(c1, c2):
        """does c2 == c1 with every param p := p-1 for exactly one param?  returns
        {p: 1} or None.  (c1 earlier, c2 later)"""
        if c1.state != c2.state:
            return None
        if len(c1.left) != len(c2.left) or len(c1.right) != len(c2.right):
            return None
        pairs = list(zip(c1.left, c2.left)) + list(zip(c1.right, c2.right))
        cand = None
        for (p1, e1), (p2, e2) in pairs:
            if p1 != p2:
                return None
        # find single param p, shift 1: e2 == e1.subst(p, p-1) for all runs
        params = set()
        for (p1, e1), (p2, e2) in pairs:
            params |= set(e1.m) | set(e2.m)
        for p in params:
            good = True
            for (pp1, e1), (pp2, e2) in pairs:
                if e2 != e1.subst(p, E.var(p, 1, -1)):
                    good = False
                    break
            if good:
                # exclude trivial no-op (p absent everywhere)
                if any(p in e1.m for (pp1, e1), _ in pairs):
                    return {p: 1}
        return None


class GoalRight:
    """goal: state E, no 1s left of head, right side semantically equal to template."""

    def __init__(self, runs):
        self.runs = merge(list(runs))

    def subst(self, p, val):
        return GoalRight([(pat, c.subst(p, val)) for pat, c in self.runs])

    def matches(self, cfg):
        if cfg.state != 'E':
            return False
        for pat, c in cfg.left:
            if '1' in pat and c.ge(1) is not False:
                return False
        return semantically_equal(cfg.right, self.runs)


class GoalConfig:
    """goal: full config equality (state + left + right, semantic)."""

    def __init__(self, cfg):
        self.cfg = cfg

    def subst(self, p, val):
        return GoalConfig(Prover.subst_config(self.cfg, p, val))

    def matches(self, cfg):
        return (cfg.state == self.cfg.state
                and semantically_equal(cfg.left, self.cfg.left)
                and semantically_equal(cfg.right, self.cfg.right))


def semantically_equal(r1, r2):
    """exact equality of the denoted cell sequences.  Fast path: tuple equality of
    canonical forms.  Slow path: align by peeling one cell at a time symbolically;
    to stay decidable we compare the canonical forms after expanding every CONCRETE
    pattern run; symbolic runs must match up to pattern-rotation-free equality."""
    a, b = merge(list(r1)), merge(list(r2))
    if tuple(a) == tuple(b):
        return True
    # expand concrete pattern runs to plain runs and re-canonicalize
    def flat(runs):
        out = []
        for pat, c in runs:
            if len(pat) > 1 and c.is_const():
                for _ in range(c.c):
                    for ch in pat:
                        out.append((ch, ONE))
            else:
                out.append((pat, c))
        return merge(out)
    fa, fb = flat(a), flat(b)
    if tuple(fa) == tuple(fb):
        return True
    # final resort: expand SMALL symbolic-free prefixes cell by cell
    return False
