#!/usr/bin/env python
"""
FAR CEGAR — crack invariants that suffix-merge (k-tails) structurally cannot, e.g. a boundary-anchored
PREFIX-parity. RPNI Blue-Fringe state merging with NEGATIVE examples: a merge is allowed only if the
resulting DFA accepts no known-bad string. Negatives are produced by the SOUND verifier itself: each
failed verification yields a concrete spurious config (self.witness) that must be excluded. Loop:
build DFA -> verify -> add witness to negatives -> rebuild, until verified or budget. Soundness is the
verifier's (unchanged); CEGAR only steers the heuristic search, so it can never create a false proof.
"""
from __future__ import annotations
import sys, os
from collections import deque, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse, sim
from far_dfa import Invariant, reachable_configs, canon, STATES
from far_finder import MergedDFA, augment


def build_pta(samples):
    """root 0 = left blank-infinity (self-loop on '0'); leading 0s stripped. children[s][sym]=t."""
    children = [dict()]; accept = set()
    children[0]["0"] = 0
    def newstate():
        children.append(dict()); return len(children) - 1
    for s in samples:
        s = list(s)
        while s and s[0] == "0":
            s.pop(0)
        st = 0
        for sym in s:
            if sym not in children[st]:
                children[st][sym] = newstate()
            st = children[st][sym]
        accept.add(st)
    return children, accept


class RPNI:
    def __init__(self, children, accept):
        self.ch = [dict(c) for c in children]          # mutable per-class child maps
        self.par = list(range(len(children)))
        self.acc = [s in accept for s in range(len(children))]
        self.log = None

    def find(self, x):
        while self.par[x] != x:
            x = self.par[x]
        return x

    def _set_par(self, a, b):
        self.log.append(("par", a, self.par[a])); self.par[a] = b

    def _set_acc(self, a, v):
        if self.acc[a] != v:
            self.log.append(("acc", a, self.acc[a])); self.acc[a] = v

    def _set_ch(self, a, sym, t):
        old = self.ch[a].get(sym, None)
        self.log.append(("ch", a, sym, old)); self.ch[a][sym] = t

    def union_fold(self, a, b):
        """merge classes of a,b and determinize (fold conflicting children). uses self.log for undo."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        self._set_par(rb, ra)
        self._set_acc(ra, self.acc[ra] or self.acc[rb])
        pending = []
        for sym, ct in list(self.ch[rb].items()):
            ct = self.find(ct)
            if sym in self.ch[ra]:
                ex = self.find(self.ch[ra][sym])
                if ex != ct:
                    pending.append((ex, ct))
            else:
                self._set_ch(ra, sym, ct)
        for x, y in pending:
            self.union_fold(x, y)

    def child(self, root, sym):
        t = self.ch[root].get(sym)
        return self.find(t) if t is not None else None

    def endable(self, st):
        seen = set()
        cur = self.find(st) if st is not None else None
        while cur is not None and cur not in seen:
            if self.acc[cur]:
                return True
            seen.add(cur); cur = self.child(cur, "0")
        return False

    def accepts_neg(self, neg):
        s = list(neg)
        while s and s[0] == "0":
            s.pop(0)
        st = self.find(0)
        for sym in s:
            st = self.child(st, sym)
            if st is None:
                return False
        return self.endable(st)

    def try_merge(self, a, b, negs):
        """attempt union_fold(a,b); keep it only if NO negative becomes accepted. returns bool."""
        self.log = []
        self.union_fold(a, b)
        ok = not any(self.accepts_neg(n) for n in negs)
        if not ok:
            for entry in reversed(self.log):
                if entry[0] == "par":
                    self.par[entry[1]] = entry[2]
                elif entry[0] == "acc":
                    self.acc[entry[1]] = entry[2]
                else:
                    _, a2, sym, old = entry
                    if old is None:
                        self.ch[a2].pop(sym, None)
                    else:
                        self.ch[a2][sym] = old
        self.log = None
        return ok

    def run(self, negs, max_red=400):
        red = [self.find(0)]
        redset = {red[0]}
        while True:
            # blue = children of red not in red (representatives)
            blue = []
            for r in red:
                for sym, t in list(self.ch[r].items()):
                    ft = self.find(t)
                    if ft not in redset and ft not in blue:
                        blue.append(ft)
            blue = [b for b in blue if self.find(b) == b]
            if not blue:
                break
            b = min(blue)
            merged = False
            for r in red:
                if self.try_merge(r, b, negs):
                    merged = True; break
            if not merged:
                red.append(self.find(b)); redset.add(self.find(b))
                if len(red) > max_red:
                    break
        return self.export()

    def export(self):
        delta = {}; accept = set()
        roots = set(self.find(s) for s in range(len(self.par)))
        for r in roots:
            for sym, t in self.ch[r].items():
                delta[(r, sym)] = self.find(t)
            if self.acc[r]:
                accept.add(r)
        return delta, accept, self.find(0)


def prove(spec, N=1500, rounds=60, trail=3, verbose=False):
    markers = [q for q in STATES if q in parse(spec)]
    configs, halted = reachable_configs(spec, N)
    if halted:
        return "HALTS", N
    configs = sorted(set(configs))                     # deterministic order (no hash-seed sensitivity)
    samples = sorted(augment(configs, trail=trail))
    Pset = set(tuple(s) for s in samples)
    children, accept = build_pta(samples)
    negs = []
    for it in range(rounds):
        soln = RPNI(children, accept)
        delta, acc, start = soln.run(negs)
        dfa = MergedDFA(spec, delta, acc, start, markers)
        ok, msg = dfa.verify()
        nq = len(set([start]) | {b for (a, s), b in delta.items()})
        if verbose:
            print(f"  round {it:2d}: |negs|={len(negs)} |Q|={nq} -> {ok}  {msg[:60]}")
        if ok:
            return "NEVER_HALTS", (f"CEGAR rounds={it+1}", f"negs={len(negs)}", msg)
        w = getattr(dfa, "witness", None)
        if not w:
            return "HOLDOUT", f"no witness at round {it} ({msg[:40]})"
        wt = tuple(w)
        # if the witness is actually a real reachable config, it cannot be a negative -> bail
        if wt in Pset or tuple(canon(list(w))) in Pset:
            return "HOLDOUT", f"witness is reachable (round {it}); needs richer sample"
        if wt in [tuple(n) for n in negs]:
            return "HOLDOUT", f"witness repeats (round {it}); CEGAR stalled"
        negs.append(list(w))
    return "HOLDOUT", f"not closed in {rounds} rounds (|negs|={len(negs)})"


def main():
    spec = "1RB0LZ_1LC1RA_0RA0LC"
    print("TARGET", spec)
    print(" ->", prove(spec, verbose=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
