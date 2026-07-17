#!/usr/bin/env python3
"""x2au_phantom.py -- claim audit probe #1 for lean/X2.lean.

Extracts every backticked identifier appearing in PROSE (docstrings /-! ... -/ and
`--` comments) and checks whether it resolves to a real declaration in X2.lean.

Unresolved names are reported with line numbers for manual triage (many will be
Lean core / Mathlib names; the probe prints the context line so a human can judge).
"""
import re, sys, subprocess, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lean", "X2.lean")

DECL = re.compile(r'^\s*(?:private\s+|protected\s+|noncomputable\s+)*'
                  r'(def|theorem|lemma|abbrev|structure|inductive|instance)\s+'
                  r'([A-Za-z_][A-Za-z0-9_\'\.]*)')

def declared(lines):
    d = {}
    for i, l in enumerate(lines, 1):
        m = DECL.match(l)
        if m:
            d.setdefault(m.group(2), []).append(i)
            # also record last dotted component & namespace-stripped form
            short = m.group(2).split('.')[-1]
            d.setdefault(short, []).append(i)
    return d

def prose_regions(lines):
    """yield (lineno, text) for prose: docstring blocks and -- comments."""
    out = []
    in_doc = False
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith('/-!') or s.startswith('/--') or s.startswith('/-'):
            in_doc = True
        if in_doc:
            out.append((i, l))
            if '-/' in l:
                in_doc = False
            continue
        if s.startswith('--'):
            out.append((i, l))
    return out

IDENT = re.compile(r'`([^`\n]+)`')
# identifier-shaped: letters/digits/underscore/prime/dot, must contain a letter
IDSHAPE = re.compile(r"^[A-Za-z_][A-Za-z0-9_'\.]*$")

def main():
    lines = open(SRC).read().split('\n')
    decls = declared(lines)
    hits = {}
    for ln, text in prose_regions(lines):
        for tok in IDENT.findall(text):
            tok = tok.strip()
            if not IDSHAPE.match(tok):
                continue
            hits.setdefault(tok, []).append(ln)

    unresolved = {}
    for tok, lns in hits.items():
        if tok in decls:
            continue
        # also accept if it appears anywhere in CODE (non-prose) as a used symbol
        unresolved[tok] = lns

    print(f"# X2.lean prose-identifier audit")
    print(f"# declarations found: {len(set(decls))}")
    print(f"# distinct backticked prose identifiers: {len(hits)}")
    print(f"# unresolved (no declaration in X2.lean): {len(unresolved)}\n")
    for tok in sorted(unresolved, key=lambda t: unresolved[t][0]):
        lns = unresolved[tok]
        print(f"{tok}\tlines={lns[:8]}")

if __name__ == '__main__':
    main()
