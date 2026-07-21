#!/usr/bin/env python3
"""Locate M1(5): unique E-on-0 config with leading (0,21) & big block, near ~45M.
Enlarge SPAN (module global, looked up at call time) so K=13 tape fits. Machine
logic is untouched. First re-confirm the M1(3) anchor with the enlarged tape."""
import x2t7_lib
x2t7_lib.SPAN = 1 << 18
x2t7_lib.ORIGIN = x2t7_lib.SPAN
from x2t7_lib import run, rle_right

# anchor re-check with enlarged tape
_, st, pos, tape, _ = run(2852091)
rle = rle_right(tape, pos, limit=40000)
mb = max((l for b, l in rle if b == 1), default=0)
assert st == 4 and tape[pos] == 0 and rle[0] == (0, 21) and mb == 2039, "ANCHOR FAILED"
print("anchor M1(3)@2852091 re-confirmed with enlarged tape: bigblock=2039 OK")

LO, HI = 44_000_000, 47_000_000
hits = []
def hook(step, st, pos, tape):
    if step < LO: return
    if st == 4 and tape[pos] == 0:
        rle = rle_right(tape, pos, limit=40000)
        if rle and rle[0] == (0, 21):
            mb = max((l for b, l in rle if b == 1), default=0)
            if mb >= 8000:
                hits.append((step, mb, tuple(rle[:12])))

run(HI, hook=hook, hook_from=LO)
print(f"{len(hits)} candidate(s) with leading (0,21) & bigblock>=8000 in [{LO},{HI}]")
for x in hits:
    print("   step=%d bigblock=%d" % (x[0], x[1]))
    print("      pref=", x[2])
