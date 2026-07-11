#!/usr/bin/env python3
"""x2cc_symb.py -- symbolic RLE executor for the x2 machine
`1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE` (CARRY-CALCULUS faithfulness prover).

A configuration is  (left, state, right):
  left  = list of runs, leftmost first (top of stack = last element)
  right = list of runs, head is at the FIRST character of right[0]
A run is (pat, cnt): pat a nonempty 01-string, cnt an affine expression in named
parameters (all parameters assumed integer >= 0).  (pat,cnt) denotes pat repeated cnt
times.  Canonical form merges adjacent runs with equal pat.

Execution:
  * micro-step: exact TM transition on the head character.  If the head run's count
    cannot be proven >= 1, a Split exception is raised and the caller must case-split.
  * three macro-rules (each is the closed form of a 2-transition self-loop; each is
    PROVEN by induction on the run length -- see check_rules(), which verifies the
    closed form against brute micro-stepping for all small lengths, the standard
    campaign certification of sweep lemmas):
      R-cycle  E over (01)^n            -> 1^(2n), state E, +2n steps
      L-cycle  E@1 with 1^a to the left -> converts to (10)-comb leftward (parity split)
      D-loop   D@1 with 1^a to the left -> crosses leftward, +a steps
  * events: every E@0 whose maximal 0-run has length >= 2 and is bounded left by 1 is
    reported with its exact length (the halt gate: length exactly 3 = HALT).  Length-1
    E@0 entries (comb separators) are proven safe by the gate and not reported.
    HALT (B@1) raises Halted.

Soundness: run() applies macro-rules only when their preconditions are PROVEN under the
current assumptions; anything unprovable raises Split (with a suggested split) rather
than guessing.  All arithmetic is exact.
"""
import sys
from fractions import Fraction

TRANS = {  # state -> (write, dir, newstate); dir +1 = R
    ('A', '0'): ('1', 1, 'B'), ('A', '1'): ('0', 1, 'E'),
    ('B', '0'): ('1', 1, 'C'), ('B', '1'): None,  # HALT
    ('C', '0'): ('0', -1, 'D'), ('C', '1'): ('1', -1, 'E'),
    ('D', '0'): ('0', 1, 'E'), ('D', '1'): ('1', -1, 'D'),
    ('E', '0'): ('1', 1, 'F'), ('E', '1'): ('0', -1, 'C'),
    ('F', '0'): ('0', 1, 'A'), ('F', '1'): ('1', 1, 'E'),
}


class Halted(Exception):
    pass


class Split(Exception):
    """raised when a comparison is undecidable; .param/.expr describe what to split on"""
    def __init__(self, msg, expr=None):
        super().__init__(msg)
        self.expr = expr


# ---------------- affine expressions ----------------
class E:
    """affine expr: const + sum coef*param.  Params assumed >= 0 (integers)."""
    __slots__ = ('c', 'm')

    def __init__(self, c=0, m=None):
        self.c = c
        self.m = dict(m) if m else {}

    @staticmethod
    def of(x):
        if isinstance(x, E):
            return x
        return E(x)

    @staticmethod
    def var(name, coef=1, const=0):
        return E(const, {name: coef})

    def __add__(self, o):
        o = E.of(o)
        m = dict(self.m)
        for k, v in o.m.items():
            m[k] = m.get(k, 0) + v
            if m[k] == 0:
                del m[k]
        return E(self.c + o.c, m)

    def __sub__(self, o):
        o = E.of(o)
        return self + E(-o.c, {k: -v for k, v in o.m.items()})

    def __mul__(self, k):
        assert isinstance(k, int)
        return E(self.c * k, {p: v * k for p, v in self.m.items()})

    def __eq__(self, o):
        o = E.of(o)
        return self.c == o.c and self.m == o.m

    def __hash__(self):
        return hash((self.c, tuple(sorted(self.m.items()))))

    def is_const(self):
        return not self.m

    def subst(self, name, val):
        """substitute param name := val (an E or int)"""
        if name not in self.m:
            return self
        coef = self.m[name]
        rest = E(self.c, {k: v for k, v in self.m.items() if k != name})
        return rest + E.of(val) * coef

    def parity(self):
        """0/1 if parity provable (all coefs even => parity of const), else None"""
        if all(v % 2 == 0 for v in self.m.values()):
            return self.c % 2
        return None

    def half_down(self):
        """floor((e-1)/2) for ODD e with even coefs: (e-1)/2 exact"""
        assert self.parity() == 1
        return E((self.c - 1) // 2, {k: v // 2 for k, v in self.m.items()})

    def half(self):
        """e/2 for EVEN e with even coefs"""
        assert self.parity() == 0
        return E(self.c // 2, {k: v // 2 for k, v in self.m.items()})

    def ge(self, k):
        """provably >= k under param >= 0?  True / False(provably <) / None(unknown)"""
        if all(v >= 0 for v in self.m.values()):
            if self.c >= k:
                return True
            if not self.m:
                return False
            return None
        # some negative coef: cannot bound below
        if all(v <= 0 for v in self.m.values()) and self.c < k:
            return False
        return None

    def __repr__(self):
        parts = []
        for p, v in sorted(self.m.items()):
            parts.append(f"{'' if v == 1 else v}{p}")
        if self.c or not parts:
            parts.append(str(self.c))
        return '+'.join(parts).replace('+-', '-')


ZERO, ONE = E(0), E(1)


# ---------------- runs / configs ----------------
def merge(runs):
    out = []
    for pat, cnt in runs:
        g = cnt.ge(1)
        if g is False or (cnt.is_const() and cnt.c == 0):
            continue
        if out and out[-1][0] == pat:
            out[-1] = (pat, out[-1][1] + cnt)
        else:
            out.append((pat, cnt))
    # normalize single-char string patterns of length>1 that are uniform: '00'->'0' x2 etc.
    out2 = []
    for pat, cnt in out:
        if len(pat) > 1 and len(set(pat)) == 1:
            pat, cnt = pat[0], cnt * len(pat)
        if out2 and out2[-1][0] == pat:
            out2[-1] = (pat, out2[-1][1] + cnt)
        else:
            out2.append((pat, cnt))
    return fold(out2)


def fold(runs):
    """fold stretches of small concrete runs into (2-char pattern, k) runs where the
    cell sequence is 2-periodic.  Exact: preserves the concrete cell sequence (and
    leaves symbolic-count runs untouched).  Unit-tested by check_fold()."""
    out = []
    i = 0
    n = len(runs)
    while i < n:
        pat, cnt = runs[i]
        # window of consecutive fully-concrete short runs
        if cnt.is_const() and cnt.c * len(pat) <= 2:
            j = i
            chars = []
            while j < n:
                p2, c2 = runs[j]
                if c2.is_const() and c2.c * len(p2) <= 4:
                    chars.append(p2 * c2.c)
                    j += 1
                else:
                    break
            s = ''.join(chars)
            if len(s) >= 6:
                out.extend(encode2(s))
                i = j
                continue
        out.append((pat, cnt))
        i += 1
    # edge-peel: a pattern run must not abut a neighbor whose adjacent char equals the
    # pattern's edge char (that would hide a maximal-run boundary).  peel one period.
    for _pass in range(6):
        changed = False
        out2 = []
        i = 0
        while i < len(out):
            pat, cnt = out[i]
            if len(pat) > 1 and cnt.is_const() and cnt.c >= 1:
                nxt = out[i + 1] if i + 1 < len(out) else None
                prv = out2[-1] if out2 else None
                peel_r = nxt is not None and nxt[0][0] == pat[-1] and nxt[1].ge(1)
                peel_l = prv is not None and prv[0][-1] == pat[0] and prv[1].ge(1)
                if peel_l and cnt.c >= 1:
                    # move first period out as unit runs
                    for ch in pat:
                        out2.append((ch, ONE))
                    out2.append((pat, cnt - 1))
                    changed = True
                    i += 1
                    continue
                if peel_r and cnt.c >= 1:
                    out2.append((pat, cnt - 1))
                    for ch in pat:
                        out2.append((ch, ONE))
                    changed = True
                    i += 1
                    continue
            out2.append((pat, cnt))
            i += 1
        # merge equal adjacent + drop zero
        out = []
        for pat, cnt in out2:
            if cnt.is_const() and cnt.c == 0:
                continue
            if out and out[-1][0] == pat:
                out[-1] = (pat, out[-1][1] + cnt)
            else:
                out.append((pat, cnt))
        if not changed:
            break
    return fold_units(out)


def fold_units(runs):
    """run-level periodic fold: (1^a 0^b) repeated >= 2 times (2 <= a <= 8, 1 <= b <= 8,
    a+b >= 4) becomes ('1'*a+'0'*b, k).  Also absorbs adjacent existing unit runs and a
    trailing (1^a, 0^b') with b' > b (leftover ('0', b'-b)).  Exact and deterministic
    (leftmost-start greedy); unit-tested by check_fold()."""
    out = []
    i = 0
    n = len(runs)
    while i < n:
        pat, cnt = runs[i]
        unit = None
        if (pat == '1' and cnt.is_const() and 2 <= cnt.c <= 8 and i + 1 < n
                and runs[i + 1][0] == '0' and runs[i + 1][1].is_const()
                and 1 <= runs[i + 1][1].c <= 8 and cnt.c + runs[i + 1][1].c >= 4):
            a, b = cnt.c, runs[i + 1][1].c
            unit = '1' * a + '0' * b
        elif len(pat) > 2 and set(pat) == {'0', '1'} and pat[0] == '1' and pat.rstrip('0').count('0') == 0:
            # existing unit run '1^a 0^b'
            a = len(pat.rstrip('0'))
            b = len(pat) - a
            if 2 <= a <= 8 and 1 <= b <= 8:
                unit = pat
        if unit:
            a = len(unit.rstrip('0'))
            b = len(unit) - a
            total = E(0)
            j = i
            leftover = None
            while j < n:
                pj, cj = runs[j]
                if pj == unit:
                    total = total + cj
                    j += 1
                    continue
                if (pj == '1' and cj.is_const() and cj.c == a and j + 1 < n
                        and runs[j + 1][0] == '0'):
                    b2 = runs[j + 1][1]
                    if b2.is_const() and b2.c == b:
                        total = total + 1
                        j += 2
                        continue
                    if b2.is_const() and b2.c > b:
                        total = total + 1
                        leftover = ('0', E(b2.c - b))
                        j += 2
                        break
                break
            tg = total.ge(2)
            if tg is True or (total.is_const() and total.c >= 2) or (not total.is_const()):
                if total.ge(1) is not False:
                    out.append((unit, total))
                    if leftover:
                        out.append(leftover)
                    i = j
                    continue
        out.append((pat, cnt))
        i += 1
    # absorb exact adjacent periods into 2-char pattern runs (works for symbolic counts):
    #   ('01',n) ('0',1) ('1',1)  ->  ('01',n+1)   and the mirrored/leading variants
    changed = True
    guard = 0
    while changed and guard < 10:
        changed = False
        guard += 1
        out_n = []
        i = 0
        while i < len(out):
            pat, cnt = out[i]
            if (len(pat) == 2 and pat[0] != pat[1] and i + 2 <= len(out) - 1
                    and out[i + 1][0] == pat[0] and out[i + 1][1].is_const()
                    and out[i + 1][1].c == 1 and out[i + 2][0] == pat[1]
                    and out[i + 2][1].is_const() and out[i + 2][1].c == 1):
                out_n.append((pat, cnt + 1))
                out_n.extend(out[i + 3:])
                out = out_n + []
                out_n = []
                i = 0
                changed = True
                continue
            if (len(pat) == 2 and pat[0] != pat[1] and i >= 2
                    and out[i - 2][0] == pat[0] and out[i - 2][1].is_const()
                    and out[i - 2][1].c == 1 and out[i - 1][0] == pat[1]
                    and out[i - 1][1].is_const() and out[i - 1][1].c == 1):
                out_n = out_n[:-2]
                out_n.append((pat, cnt + 1))
                out_n.extend(out[i + 1:])
                out = out_n + []
                out_n = []
                i = 0
                changed = True
                continue
            out_n.append((pat, cnt))
            i += 1
        out = out_n
    # canonical: an isolated unit run with count exactly 1 expands back to plain runs
    out1 = []
    for pat, cnt in out:
        if (len(pat) > 2 and set(pat) <= {'0', '1'} and pat[0] == '1'
                and pat.rstrip('0').count('0') == 0 and cnt.is_const() and cnt.c == 1):
            a = len(pat.rstrip('0'))
            out1.append(('1', E(a)))
            out1.append(('0', E(len(pat) - a)))
        else:
            out1.append((pat, cnt))
    # merge equal adjacent again
    out2 = []
    for pat, cnt in out1:
        if cnt.is_const() and cnt.c == 0:
            continue
        if out2 and out2[-1][0] == pat:
            out2[-1] = (pat, out2[-1][1] + cnt)
        else:
            out2.append((pat, cnt))
    return out2


def encode2(s):
    """re-encode a concrete 01-string as runs, preferring 2-periodic pattern runs."""
    res = []
    i = 0
    L = len(s)
    while i < L:
        # uniform run
        j = i
        while j < L and s[j] == s[i]:
            j += 1
        if j - i >= 2:
            res.append((s[i], E(j - i)))
            i = j
            continue
        # alternating stretch starting at i
        k = i
        while k + 1 < L and s[k + 1] != s[k]:
            k += 1
        # s[i..k] alternates; use pairs
        alen = k - i + 1
        if alen >= 4:
            npairs = alen // 2
            res.append((s[i:i + 2], E(npairs)))
            i = i + 2 * npairs
        else:
            res.append((s[i], ONE))
            i += 1
    return res


def check_fold(trials=2000):
    import random
    for t in range(trials):
        runs = []
        for _ in range(random.randint(1, 12)):
            pat = random.choice(['0', '1', '01', '10', '1000000', '1111100'])
            runs.append((pat, E(random.randint(0, 5))))
        want = runs_concrete(runs, {})
        got = runs_concrete(merge(runs), {})
        assert want == got, (runs, want, got)
    print(f"check_fold: {trials} random round-trips exact")


def runs_concrete(runs, env):
    """expand runs to a concrete string using env for params"""
    s = []
    for pat, cnt in runs:
        n = cnt.c + sum(v * env.get(k, 0) for k, v in cnt.m.items())
        assert n >= 0, (pat, cnt, env)
        s.append(pat * n)
    return ''.join(s)


class Config:
    def __init__(self, left, state, right, steps=E(0)):
        self.left = merge(left)
        self.state = state
        self.right = merge(right)
        self.steps = steps

    def copy(self):
        return Config([r for r in self.left], self.state, [r for r in self.right], self.steps)

    def key(self):
        return (tuple(self.left), self.state, tuple(self.right))

    def __repr__(self):
        def rr(runs):
            return ' '.join(f"{p}^{c}" if not (c.is_const() and c.c == 1) else p
                            for p, c in runs)
        return f"{rr(self.left)}  [{self.state}]  {rr(self.right)}"


def pop_front(runs):
    """remove first char from runs; return (char, rest).  Split if count unprovable."""
    if not runs:
        return None, runs
    pat, cnt = runs[0]
    g = cnt.ge(1)
    if g is False:
        return pop_front(runs[1:])
    if g is None:
        raise Split(f"count {cnt} of run {pat} may be 0", cnt)
    ch = pat[0]
    rest = []
    if len(pat) > 1:
        rest.append((pat[1:], ONE))
    rest.append((pat, cnt - 1))
    return ch, merge(rest + runs[1:])


def pop_back(runs):
    """remove last char from runs; return (char, rest)."""
    if not runs:
        return None, runs
    pat, cnt = runs[-1]
    g = cnt.ge(1)
    if g is False:
        return pop_back(runs[:-1])
    if g is None:
        raise Split(f"count {cnt} of run {pat} may be 0", cnt)
    ch = pat[-1]
    rest = list(runs[:-1])
    rest.append((pat, cnt - 1))
    if len(pat) > 1:
        rest.append((pat[:-1], ONE))
    return ch, merge(rest)


def push_front(runs, ch):
    return merge([(ch, ONE)] + runs)


def push_back(runs, ch):
    return merge(runs + [(ch, ONE)])


# ---------------- the executor ----------------
class Machine:
    def __init__(self, cfg, name='', trace=False, guard_l=False, guard_r=True):
        self.cfg = cfg
        self.events = []      # (steps, kind, payload)
        self.name = name
        self.trace = trace
        self.guard_l = guard_l  # if True, running off the left end is an error
        self.guard_r = guard_r  # if True, running off the right end is an error

    def head_char(self):
        c = self.cfg
        if not c.right:
            if self.guard_r:
                raise Split("head reached right guard")
            return '0'
        pat, cnt = c.right[0]
        g = cnt.ge(1)
        if g is None:
            raise Split(f"head run count {cnt} may be 0", cnt)
        if g is False:
            self.cfg = Config(c.left, c.state, c.right[1:], c.steps)
            return self.head_char()
        return pat[0]

    def gap_probe(self):
        """head at E@0: length of maximal 0-run at head if bounded-left-by-1; None if
        left neighbor is 0 or tape start (leading gap -- not a gapmeet event)."""
        c = self.cfg
        # left neighbor
        ln = None
        for pat, cnt in reversed(c.left):
            g = cnt.ge(1)
            if g is False:
                continue
            if g is None:
                raise Split(f"left neighbor run {pat}^{cnt} may be empty", cnt)
            ln = pat[-1]
            break
        if ln != '1':
            return None
        # gap length: count 0s from head rightward
        L = E(0)
        bounded = False
        for pat, cnt in c.right:
            g1 = cnt.ge(1)
            if g1 is False:
                continue
            if set(pat) == {'0'}:
                L = L + cnt * len(pat)
                continue
            if g1 is None:
                raise Split(f"gap run {pat}^{cnt} may be empty", cnt)
            # pattern starting with 0s then a 1
            nz = 0
            while nz < len(pat) and pat[nz] == '0':
                nz += 1
            L = L + E(nz)
            bounded = True
            break
        if not bounded:
            if self.guard_r:
                raise Split("gap extends to right guard")
            return None  # gap runs into infinite 0 background: not an event, never ==3
        return L

    def micro(self):
        c = self.cfg
        ch = self.head_char()
        if c.state == 'E' and ch == '0':
            L = self.gap_probe()
            if L is not None:
                g2 = L.ge(2)
                if g2 is None:
                    raise Split(f"gap length {L} vs 2 undecidable", L)
                if g2:
                    # HALT gate: length-3 fatal
                    if L.is_const() and L.c == 3:
                        raise Halted(f"E meets gap 3 at steps={c.steps}")
                    if not L.is_const():
                        # must prove != 3: only lengths with const>=4 min or ==2
                        if L.ge(4) is not True:
                            raise Split(f"gap length {L} not provably != 3", L)
                    self.events.append((c.steps, 'gap', L))
        t = TRANS[(c.state, ch)]
        if t is None:
            raise Halted(f"B@1 HALT at steps={c.steps}")
        w, d, ns = t
        _, rrest = pop_front(c.right)
        if d == 1:
            nl = push_back(c.left, w)
            nr = rrest
        else:
            if not c.left and self.guard_l:
                raise Split("head reached left guard")
            lc, nl = pop_back(c.left) if c.left else ('0', [])
            nr = merge([(lc, ONE), (w, ONE)] + rrest)
        self.cfg = Config(nl, ns, nr, c.steps + 1)
        if self.trace:
            print(f"    {self.cfg}")

    # ---- macro-rules ----
    def try_R_cycle(self):
        """E @ (01)^n ...  or E @ 0 (10)^n ...: repack to 1^(2n)."""
        c = self.cfg
        if c.state != 'E' or not c.right:
            return False
        r = c.right
        # form A: leading ('01', n)
        if r[0][0] == '01':
            n = r[0][1]
            if n.ge(1):
                self.cfg = Config(merge(c.left + [('1', n * 2)]), 'E', r[1:],
                                  c.steps + n * 2)
                return True
        # form B: ('0',1) ('10', n) ...  == (01)^n 0 ...
        if r[0][0] == '0' and len(r) >= 2 and r[1][0] == '10':
            one0 = r[0][1]
            n = r[1][1]
            if one0.is_const() and one0.c == 1 and n.ge(1):
                self.cfg = Config(merge(c.left + [('1', n * 2)]), 'E',
                                  merge([('0', ONE)] + r[2:]), c.steps + n * 2)
                return True
        return False

    def try_L_cycle(self):
        """E @ 1 with left ending ('1', a), a>=2: unpack leftward.
        Closed forms (verified by check_rules):
          head cell f=1; left 1-run length a; below-run char X (must be 0; if the run
          below is '1' the run would have merged).
          a = 2m   (m>=1): after 2m+2 steps state D, head on X's left neighbor:
                   left loses ('1',2m) and X; right becomes X? -- see check_rules;
                   we implement only the SAFE cases proven there:
            a even = 2m:  [.. Y 0 1^2m | E | 1 R] -> [.. Y | D | 0 0 (10)^m R']
                          where R' = R with head 1-cell consumed (f written 0..):
                          precisely right' = ('0',2)('10',m) + (R minus leading 1)
                          steps +2m+2
            a odd = 2m+1: [.. 0 1^(2m+1) | E | 1 R] -> [.. 0 | E | 0 (10)^(m+1) R-1]
                          steps +2m+2
        """
        c = self.cfg
        if c.state != 'E' or not c.right or not c.left:
            return False
        # head char must be 1
        pat0, cnt0 = c.right[0]
        if pat0[0] != '1' or cnt0.ge(1) is not True:
            return False
        # left top must be a 1-run
        lp, lc = c.left[-1]
        if lp != '1':
            return False
        # need to know parity of lc and value: require lc const OR even-by-construction
        a = lc
        # consume head cell (write 0 -> it becomes part of right pattern)
        _, r_rest = pop_front(c.right)
        if a.is_const():
            av = a.c
            if av < 1:
                return False
            m = av // 2
            if av % 2 == 0:
                # a = 2m: ends C@X reading 0 (X below run), writes 0, lands D on Y (below X)
                nl = c.left[:-1]
                if not nl:
                    if self.guard_l:
                        raise Split("L-cycle even case hits left guard (X)")
                    X = '0'
                else:
                    X, nl = pop_back(nl)
                if X != '0':
                    raise Split(f"L-cycle even: below-run char {X} != 0 unexpected")
                if not nl:
                    if self.guard_l:
                        raise Split("L-cycle even case hits left guard (Y)")
                    Ych = '0'
                else:
                    Ych, nl = pop_back(nl)
                nr = merge([(Ych, ONE), ('0', E(2)), ('10', E(m))] + r_rest)
                self.cfg = Config(nl, 'D', nr, c.steps + 2 * m + 2)
            else:
                # a = 2m+1: ends E on X (=0, below run)
                nl = c.left[:-1]
                if not nl:
                    if self.guard_l:
                        raise Split("L-cycle odd case hits left guard (X)")
                    X = '0'
                else:
                    X, nl = pop_back(nl)
                if X != '0':
                    raise Split(f"L-cycle odd: below-run char {X} != 0 unexpected")
                nr = merge([('0', ONE), ('10', E(m + 1))] + r_rest)
                self.cfg = Config(nl, 'E', nr, c.steps + 2 * m + 2)
            return True
        # symbolic a with provable parity (all coefs even): same closed forms
        par = a.parity()
        if par is None:
            raise Split(f"L-cycle with symbolic 1-run length {a}: split parity/value", a)
        if par == 1:
            if a.ge(1) is not True:
                raise Split(f"L-cycle odd symbolic: {a} not provably >= 1", a)
            m = a.half_down()          # a = 2m+1
            nl = c.left[:-1]
            if not nl:
                if self.guard_l:
                    raise Split("L-cycle odd case hits left guard (X)")
                X = '0'
            else:
                X, nl = pop_back(nl)
            if X != '0':
                raise Split(f"L-cycle odd: below-run char {X} != 0 unexpected")
            nr = merge([('0', ONE), ('10', m + 1)] + r_rest)
            self.cfg = Config(nl, 'E', nr, c.steps + m * 2 + 2)
            return True
        else:
            if a.ge(2) is not True:
                raise Split(f"L-cycle even symbolic: {a} not provably >= 2", a)
            m = a.half()               # a = 2m
            nl = c.left[:-1]
            if not nl:
                if self.guard_l:
                    raise Split("L-cycle even case hits left guard (X)")
                X = '0'
            else:
                X, nl = pop_back(nl)
            if X != '0':
                raise Split(f"L-cycle even: below-run char {X} != 0 unexpected")
            if not nl:
                if self.guard_l:
                    raise Split("L-cycle even case hits left guard (Y)")
                Ych = '0'
            else:
                Ych, nl = pop_back(nl)
            nr = merge([(Ych, ONE), ('0', E(2)), ('10', m)] + r_rest)
            self.cfg = Config(nl, 'D', nr, c.steps + m * 2 + 2)
            return True

    def try_D_loop(self):
        """D @ 1: cross left 1-run.  [.. ('1',a) | D | 1^b R] -> [.. | D | 1^(a+b) R]"""
        c = self.cfg
        if c.state != 'D' or not c.right or not c.left:
            return False
        pat0, cnt0 = c.right[0]
        if pat0[0] != '1' or cnt0.ge(1) is not True:
            return False
        lp, lc = c.left[-1]
        if lp != '1' or lc.ge(1) is not True:
            return False
        nl = c.left[:-1]
        nr = merge([('1', lc)] + c.right)
        self.cfg = Config(nl, 'D', nr, c.steps + lc)
        return True

    def step(self):
        if self.try_R_cycle():
            return
        if self.try_L_cycle():
            return
        if self.try_D_loop():
            return
        self.micro()

    def run(self, until=None, max_ops=100000):
        """run until predicate until(cfg) is True (checked before each step)"""
        for _ in range(max_ops):
            if until and until(self.cfg):
                return True
            self.step()
        raise RuntimeError(f"max_ops exceeded; cfg={self.cfg}")


# ---------------- rule certification ----------------
def brute(tape, pos, state, nsteps=None, until_state_pos=None):
    """exact micro simulation on a python list; returns (tape,pos,state,steps)"""
    tape = list(tape)
    steps = 0
    while True:
        if until_state_pos and (state, pos) == until_state_pos:
            return tape, pos, state, steps
        if nsteps is not None and steps >= nsteps:
            return tape, pos, state, steps
        ch = tape[pos] if 0 <= pos < len(tape) else '0'
        t = TRANS[(state, ch)]
        if t is None:
            raise Halted("brute halt")
        w, d, ns = t
        if 0 <= pos < len(tape):
            tape[pos] = w
        pos += d
        state = ns
        steps += 1


def check_rules():
    """certify the three macro closed forms against brute micro-stepping, all small n.
    (This is the mechanical counterpart of the 2-transition-induction proofs.)"""
    ok = True
    # R-cycle: 0? tape = X (01)^n S, E at first 0, S in {'1','0'} suffix char
    for n in range(1, 30):
        for sc in ('1', '0'):
            tape = list('1') + list('01' * n) + [sc, '1']
            t2, p2, s2, st = brute(tape, 1, 'E', until_state_pos=('E', 1 + 2 * n))
            exp = list('1') + ['1'] * 2 * n + [sc, '1']
            assert (t2, s2, st) == (exp, 'E', 2 * n), (n, sc, t2, s2, st)
    # L-cycle even a=2m: tape = Y 0 1^2m [E@f:1] R ; head at f = index 2+2m
    for m in range(1, 20):
        tape = list('1' + '0' + '1' * (2 * m) + '1' + '10')
        f = 2 + 2 * m
        t2, p2, s2, st = brute(tape, f, 'E', nsteps=2 * m + 2)
        exp = list('1') + list('0') + list('0' + '10' * m) + list('10')
        assert t2 == exp and s2 == 'D' and p2 == 0, (m, t2, s2, p2, st)
    # L-cycle odd a=2m+1: tape = 0 1^(2m+1) [E:1] R
    for m in range(0, 20):
        tape = list('0' + '1' * (2 * m + 1) + '1' + '10')
        f = 1 + 2 * m + 1
        t2, p2, s2, st = brute(tape, f, 'E', nsteps=2 * m + 2)
        exp = list('0') + list('10' * (m + 1)) + list('10')
        assert t2 == exp and s2 == 'E' and p2 == 0, (m, t2, s2, p2, st)
    # D-loop: 0 1^a [D:1] -> crosses
    for a in range(1, 20):
        tape = list('0' + '1' * a + '1')
        t2, p2, s2, st = brute(tape, a + 1, 'D', nsteps=a)
        assert t2 == tape and s2 == 'D' and p2 == 1, (a, t2, s2, p2)
    print("check_rules: R-cycle, L-cycle(even/odd), D-loop closed forms all verified")
    return ok


if __name__ == '__main__':
    check_rules()
    check_fold()
