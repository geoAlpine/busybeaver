#!/usr/bin/env python
"""
FAR finder — auto-construct a memory-DFA invariant by RPNI-style k-tails state merging on the
reachable-config sample, then hand it to the SOUND verifier (far_dfa.Invariant.verify). The merge
generalises the finite sample to an infinite regular language (folding the counter's loop); soundness
is NOT assumed from the merge -- a wrong DFA simply fails verify(). So the finder can be heuristic
while the result stays rigorous (the v3 lesson: trust the verifier, not the guess).

DFA model: explicit states (ints), delta[(state,sym)] -> state, an accept set. endable = accept.
Blank-invariance is fed in by augmenting each sample config with a few extra leading/trailing 0s.
"""
from __future__ import annotations
import sys, os
from collections import deque, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from far_dfa import Invariant, reachable_configs, canon, STATES


class MergedDFA(Invariant):
    def __init__(self, spec, delta, accept, start, markers):
        self.M = parse(spec)
        self.markers = markers
        self.alpha = ["0", "1"] + markers
        self.tag = f"merged-DFA |Q|={len(set([start]) | {b for (a, s), b in delta.items()})}"
        self._delta = delta
        self._accept = accept
        self.START = start

    def step(self, st, sym):
        if st is None:
            return None
        return self._delta.get((st, sym))

    def endable(self, st):
        """can the tape legally end here? a config is 0-extended to the right, so follow the
        deterministic '0'-chain: endable iff some state along it is accepting (trailing-blank flush)."""
        seen = set()
        cur = st
        while cur is not None and cur not in seen:
            if cur in self._accept:
                return True
            seen.add(cur)
            cur = self._delta.get((cur, "0"))
        return False


def build_pta(samples):
    """prefix-tree acceptor. state 0 = root = the LEFT blank-infinity; it self-loops on '0' so any
    number of leading blanks is absorbed (left blank-invariance). Leading 0s of each sample are
    stripped accordingly before insertion."""
    delta = {(0, "0"): 0}; accept = set(); nxt = 1
    for s in samples:
        s = list(s)
        while s and s[0] == "0":                       # absorbed by the root's '0' self-loop
            s.pop(0)
        st = 0
        for sym in s:
            if (st, sym) not in delta:
                delta[(st, sym)] = nxt; nxt += 1
            st = delta[(st, sym)]
        accept.add(st)
    return delta, accept, nxt


def ktails(delta, accept, nstates, k):
    """signature of each state = set of accepted suffixes up to length k (incl '' if accepting)."""
    # children adjacency
    children = defaultdict(list)
    for (st, sym), t in delta.items():
        children[st].append((sym, t))
    sig = {}
    for st in range(nstates):
        acc = set()
        dq = deque([(st, ())])
        while dq:
            cur, word = dq.popleft()
            if cur in accept:
                acc.add(word)
            if len(word) < k:
                for sym, t in children[cur]:
                    dq.append((t, word + (sym,)))
        sig[st] = frozenset(acc)
    return sig


class UF:
    def __init__(self, n):
        self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb); return True
        return False


def merge(delta, accept, nstates, k):
    """k-tails partition, then determinising union-find closure -> a deterministic quotient DFA."""
    sig = ktails(delta, accept, nstates, k)
    uf = UF(nstates)
    bysig = defaultdict(list)
    for st in range(nstates):
        bysig[sig[st]].append(st)
    for group in bysig.values():
        for s in group[1:]:
            uf.union(group[0], s)
    # determinise: same class + same symbol must go to same class
    changed = True
    while changed:
        changed = False
        out = defaultdict(dict)                       # root -> {sym: child-root}
        for (st, sym), t in delta.items():
            r = uf.find(st); ct = uf.find(t)
            if sym in out[r] and out[r][sym] != ct:
                if uf.union(out[r][sym], ct):
                    changed = True
                out[r][sym] = uf.find(out[r][sym])
            else:
                out[r][sym] = ct
    # build merged delta/accept/start
    mdelta = {}
    for (st, sym), t in delta.items():
        mdelta[(uf.find(st), sym)] = uf.find(t)
    maccept = set(uf.find(a) for a in accept)
    return mdelta, maccept, uf.find(0)


def augment(configs, trail=3):
    """leading blanks are handled by the root '0' self-loop (build_pta); add a few TRAILING blanks
    so the right blank-infinity is represented (endable also follows the '0'-chain)."""
    S = set()
    for cfg in configs:
        for b in range(trail + 1):
            S.add(tuple(cfg) + ("0",) * b)
    return S


def prove(spec, Ns=(800, 2000, 5000), ks=(2, 3, 4, 5, 6), verbose=False):
    markers = [q for q in STATES if q in parse(spec)]
    for N in Ns:
        configs, halted = reachable_configs(spec, N)
        if halted:
            return "HALTS", N
        configs = list(set(configs))
        samples = augment(configs)
        delta, accept, nstates = build_pta(samples)
        for k in ks:
            mdelta, maccept, start = merge(delta, accept, nstates, k)
            dfa = MergedDFA(spec, mdelta, maccept, start, markers)
            ok, msg = dfa.verify()
            if verbose:
                print(f"   N={N} k={k} |Q|={len(set([start])|{b for (a,s),b in mdelta.items()})} -> {ok}  {msg}")
            if ok:
                return "NEVER_HALTS", (f"merged-DFA", f"N={N}", f"k={k}", msg)
    return "HOLDOUT", "no verified invariant"


def main():
    targets = ["1RB0LZ_1LC1RA_0RA0LC", "1RB1LC_0LA0RB_1LA0LZ"]
    for spec in targets:
        print("TARGET", spec)
        print("  ->", prove(spec, verbose=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
