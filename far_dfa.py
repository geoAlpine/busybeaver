#!/usr/bin/env python
"""
FAR LAYER 1+2 — guess a regular invariant L (m-gram automaton) from reachable configs, then
SOUNDLY VERIFY it is an inductive non-halting invariant. Soundness lives only in verify(): a wrong
guess fails verification, never a false proof. Built on the trusted LAYER-0 step (far.step_str).

L (the m-gram automaton), no boundary symbols — blank-invariance is intrinsic:
  config string = U q c_h V  (U,V tape symbols over {0,1}; q one state-marker; c_h the head cell).
  The bi-infinite tape is 0-extended, so we read with the window initialised to 0^(m-1) (left blank
  infinity) and "flush" with 0^(m-1) at the end (right blank infinity). A string is ACCEPTED iff it
  has exactly one marker and every length-m window (over 0^(m-1)+config+0^(m-1)) is in the gram set G.

verify checks, with finite DFA operations only:
  (S) the blank start  0 A 0  is accepted;
  (C) closure: for every accepted x and its trusted one-step successor x', x' is accepted -- reduced
      to suffix-language inclusions L(pre) ⊆ L(post) over reachable left-context states (a TM step
      rewrites O(1) cells next to the marker; the unchanged suffix must stay acceptable);
  (H) no accepted config is a halt (marker q on a cell c with M[q][c] is None).
If all three pass, reachable(start) ⊆ L and L has no halt  =>  the TM never halts. SOUND.
"""
from __future__ import annotations
import sys, os
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from far import step_str, trim, STATES


def canon(s):
    """ensure explicit tape neighbours on both sides of the marker."""
    s = list(s)
    j = next(k for k, ch in enumerate(s) if ch in STATES)
    if j + 1 >= len(s):
        s = s + ["0"]
    if j == 0:
        s = ["0"] + s
    return s


def reachable_configs(spec, steps):
    M = parse(spec)
    s = ["A"]; out = []
    for _ in range(steps):
        out.append(tuple(canon(trim(s))))
        s, halted = step_str(M, s)
        if halted:
            return out, True
        s = trim(s)
    return out, False


class Invariant:
    """Base class holding the SOUND verifier. Subclasses provide: self.M, self.markers, self.alpha,
    self.START, step(state,sym)->state|None, endable(state)->bool. The verifier is decider-agnostic:
    it checks (S) start in L, (C) succ(L) subset L, (H) no halt in L on whatever DFA the subclass
    defines. A wrong DFA fails verification; it can never produce a false NEVER_HALTS."""
    tag = "invariant"

    def feed(self, st, seq):
        for sym in seq:
            st = self.step(st, sym)
            if st is None:
                return None
        return st

    def endable(self, st):
        raise NotImplementedError

    def accepts(self, cfg):
        st = self.feed(self.START, list(cfg))
        return self.endable(st)

    def reachable_context_states(self):
        """all DFA states reachable from START reading tape-only (non-marker) prefixes -- exactly the
        possible left-context states p (after reading U) of an accepted config U q c_h V."""
        seen = {self.START}; dq = deque([self.START]); out = [self.START]
        while dq:
            st = dq.popleft()
            for sym in ["0", "1"]:                       # U is tape-only (no marker read yet)
                nx = self.step(st, sym)
                if nx is not None and nx not in seen:
                    seen.add(nx); dq.append(nx); out.append(nx)
        return out

    def suffix_includes(self, a, b, witness=False):
        """True iff every continuation acceptable from state a is acceptable from state b
        (L(a) ⊆ L(b)). A continuation = tape/marker symbols then the right-blank flush.
        If witness=True, returns (False, bad_continuation) on failure."""
        if a is None:
            return (True, None) if witness else True
        seen = {(a, b)}; dq = deque([(a, b, [])])
        while dq:
            x, y, path = dq.popleft()
            if self.endable(x) and not self.endable(y):
                return (False, path) if witness else False
            for sym in self.alpha:
                nx = self.step(x, sym)
                if nx is None:
                    continue
                ny = self.step(y, sym) if y is not None else None
                key = (nx, ny)
                if key not in seen:
                    seen.add(key); dq.append((nx, ny, path + [sym]))
        return (True, None) if witness else True

    def shortest_prefix(self, target):
        """shortest {0,1}* string driving START to `target` (the U context). None if unreachable."""
        seen = {self.START: ()}; dq = deque([self.START])
        while dq:
            st = dq.popleft()
            if st == target:
                return seen[st]
            for sym in ("0", "1"):
                nx = self.step(st, sym)
                if nx is not None and nx not in seen:
                    seen[nx] = seen[st] + (sym,); dq.append(nx)
        return None

    def _completion(self, st):
        """shortest continuation (over alpha) from st reaching an endable state; () if st endable."""
        seen = {st: ()}; dq = deque([st])
        while dq:
            x = dq.popleft()
            if self.endable(x):
                return seen[x]
            for sym in self.alpha:
                nx = self.step(x, sym)
                if nx is not None and nx not in seen:
                    seen[nx] = seen[x] + (sym,); dq.append(nx)
        return None

    def verify(self):
        self.witness = None
        # (S) start accepted
        if not self.accepts(canon(["A"])):
            return False, "start not in L"
        ctx = self.reachable_context_states()
        for q in self.markers:
            for c in (0, 1):
                tr = self.M[q].get(c)
                cs = str(c)
                for p in ctx:
                    pq = self.step(p, q)
                    pqc = self.step(pq, cs) if pq is not None else None
                    if pqc is None:
                        continue                         # this (context, q, c) not in L; nothing to preserve
                    # is there an accepted config U q c V with this context p? only if pqc can finish
                    reachable_here = pqc is not None
                    if tr is None:
                        # (H) halt: must be NO accepted config with q reading c here
                        if self._can_finish(pqc):
                            U = self.shortest_prefix(p); V = self._completion(pqc)
                            if U is not None and V is not None:
                                self.witness = list(U) + [q, cs] + list(V)
                            return False, f"halt config in L: state {q} reads {c} (context {p})"
                        continue
                    w, d, ns = tr
                    if d == "R":
                        post = self.step(self.step(p, str(w)), ns)
                        ok, vwit = self.suffix_includes(pqc, post, witness=True)
                        if not ok:
                            U = self.shortest_prefix(p)
                            if U is not None and vwit is not None:
                                self.witness = list(U) + [q, cs] + list(vwit)
                            return False, f"closure R fails: {q},{c}->{w}{d}{ns} ctx {p}"
                    else:
                        # L move needs the left neighbour c_L; p already includes it as last window sym.
                        # Re-derive: context here is the state BEFORE c_L. Handle via per-(c_L) below.
                        pass
        # L moves handled separately (need the cell left of the marker)
        for q in self.markers:
            for c in (0, 1):
                tr = self.M[q].get(c)
                if tr is None or tr[1] != "L":
                    continue
                w, d, ns = tr
                cs = str(c)
                for p in ctx:                            # p = state BEFORE the left neighbour c_L
                    for cL in ("0", "1"):
                        pre = self.feed(p, [cL, q, cs])
                        if pre is None:
                            continue
                        post = self.feed(p, [ns, cL, str(w)])
                        ok, vwit = self.suffix_includes(pre, post, witness=True)
                        if not ok:
                            U = self.shortest_prefix(p)
                            if U is not None and vwit is not None:
                                self.witness = list(U) + [cL, q, cs] + list(vwit)
                            return False, f"closure L fails: {q},{c}->{w}{d}{ns} ctx {p} cL {cL}"
        return True, f"VERIFIED inductive invariant ({self.tag}, {len(ctx)} ctx states)"

    def _can_finish(self, st):
        """is any accepted config completable from state st? (st has mc==1 already)"""
        if st is None:
            return False
        seen = {st}; dq = deque([st])
        while dq:
            x = dq.popleft()
            if self.endable(x):
                return True
            for sym in self.alpha:
                nx = self.step(x, sym)
                if nx is not None and nx not in seen:
                    seen.add(nx); dq.append(nx)
        return False


class FAR(Invariant):
    """m-gram invariant: config in L iff every length-m window of 0^(m-1)+config+0^(m-1) is in G.
    state = (window of last m-1 symbols, marker_count)."""
    def __init__(self, spec, configs, m):
        self.M = parse(spec)
        self.m = m
        self.markers = [q for q in STATES if q in self.M]
        self.alpha = ["0", "1"] + self.markers
        self.tag = f"m-gram m={m}"
        pad = ["0"] * (m - 1)
        G = set()
        for cfg in configs:
            seq = pad + list(cfg) + pad
            for i in range(len(seq) - m + 1):
                G.add(tuple(seq[i:i + m]))
        self.G = G
        self.START = (tuple(["0"] * (m - 1)), 0)

    def step(self, st, sym):
        if st is None:
            return None
        w, mc = st
        if sym in self.markers:
            mc += 1
            if mc > 1:
                return None
        gram = w + (sym,)
        if len(gram) == self.m and gram not in self.G:
            return None
        nw = (w + (sym,))[-(self.m - 1):] if self.m > 1 else ()
        return (nw, mc)

    def endable(self, st):
        if st is None:
            return False
        end = self.feed(st, ["0"] * (self.m - 1))
        return end is not None and end[1] == 1


def prove(spec, samples=(400, 1000, 3000, 8000), ms=(2, 3, 4, 5, 6, 7, 8)):
    for N in samples:
        configs, halted = reachable_configs(spec, N)
        if halted:
            return "HALTS", N
        for m in ms:
            far = FAR(spec, configs, m)
            ok, msg = far.verify()
            if ok:
                return "NEVER_HALTS", (f"FAR m={m}", f"N={N}", msg)
    return "HOLDOUT", "no verified invariant in range"


def main():
    targets = ["1RB0LZ_1LC1RA_0RA0LC", "1RB1LC_0LA0RB_1LA0LZ"]
    gates = [("Antihydra", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
             ("Lucy", "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
             ("BB4-halter", "1RB1LB_1LA0LC_1RZ1LD_1RD0RA")]
    for spec in targets:
        print("TARGET", spec, "->", prove(spec))
    for n, s in gates:
        print("GATE ", n, "->", prove(s, samples=(400, 1500), ms=(2, 3, 4, 5))[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
