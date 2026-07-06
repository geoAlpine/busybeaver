# o15 fixed-point hunt, part 4: the FATAL BUFFER LANGUAGE.
# State [2,2] + buffer + [V]. Question: is the set of fatal buffers a REGULAR language?
# Hypothesis from part 3: over alphabet {1,2}, fatal (V==1 mod 3) <=> buffer avoids factor "11".
# Exact concrete runs (run_gen), zero acceleration.
import sys, itertools
from o15_template_scan import run_gen

def land(blocks):
    status, out, steps, unsafe, mg, toks, bad0 = run_gen(blocks, record=False)
    assert status in ('HALT', 'LAND'), (blocks, status)  # a BUDGET must never pass as 'safe'
    return status, out, steps

print("== fatal buffer language over {1,2}, lengths 0..5, head [2,2], V in {52,100} (==1 mod 3) ==")
mism = 0
for L in range(0, 6):
    for buf in itertools.product((1, 2), repeat=L):
        has11 = any(buf[i] == 1 and buf[i + 1] == 1 for i in range(L - 1))
        verdicts = []
        for V in (52, 100):
            status, out, steps = land([2, 2] + list(buf) + [V])
            verdicts.append(status == 'HALT')
        assert verdicts[0] == verdicts[1], (buf, verdicts)
        fatal = verdicts[0]
        pred = not has11
        tag = "" if fatal == pred else "  *** HYPOTHESIS MISMATCH"
        if fatal != pred:
            mism += 1
        print(f"  buf={list(buf)}: fatal={fatal} pred(no-11)={pred}{tag}")
print(f"hypothesis 'fatal <=> no 11 factor' over {{1,2}}^0..5: mismatches = {mism}")

print("\n== buffers with one digit >=3 inserted (protection depth), V=52 ==")
for buf in ([3], [4], [5], [6], [3, 2], [2, 3], [5, 2], [2, 5], [2, 5, 2], [5, 2, 5],
            [2, 2, 3], [3, 2, 2], [2, 3, 2], [5, 1], [1, 5], [2, 1, 5], [5, 1, 2]):
    status, out, steps = land([2, 2] + buf + [V := 52])
    print(f"  buf={buf}: {status}" + (f" -> {out}" if status == 'LAND' else ""))

print("\n== V==0 mod 3 fatal buffers over {1,2} lengths 0..4 + selected, V in {51,99} ==")
for L in range(0, 5):
    for buf in itertools.product((1, 2), repeat=L):
        verdicts = []
        for V in (51, 99):
            status, out, steps = land([2, 2] + list(buf) + [V])
            verdicts.append(status == 'HALT')
        assert verdicts[0] == verdicts[1], (buf, verdicts)
        if verdicts[0]:
            print(f"  FATAL buf={list(buf)}")
for buf in ([5], [8], [5, 1], [1, 5], [5, 2], [2, 5], [5, 5], [8, 2], [3], [6], [4], [7]):
    status, out, steps = land([2, 2] + buf + [51])
    print(f"  buf={buf}: {'FATAL' if status == 'HALT' else 'safe'}")

print("\n== head-side extension: [x, 2, 2, buf*, V=52] -- which heads protect fatal buffers? ==")
for head in ([1], [2], [1, 1], [2, 1], [1, 2], [3], [1, 1, 1], [4]):
    for buf in ([], [1]):
        status, out, steps = land(head + [2, 2] + buf + [52])
        print(f"  head={head} buf={buf}: {'FATAL' if status == 'HALT' else 'safe'}")
