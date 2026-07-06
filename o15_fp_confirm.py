# o15 fixed-point hunt, part 5: PREDICT-AND-CONFIRM for the refined fatal-buffer law.
# Refined law (fitted on lengths 0..5, after the no-11 hypothesis was REFUTED):
#   milestone [2,2] + buf + [V], V==1 mod 3, buf over {1,2}:
#     SAFE <=> buf starts with [1,1] AND buf contains no factor [2,2]
#   V==0 mod 3, buf over {1,2}:
#     FATAL <=> buf has a 2 among its first two digits (prefix 2* or 12*)
# A-priori predictions on UNSEEN length-6 (V==1) and length-5 (V==0) buffers, then exact runs.
import itertools
from o15_template_scan import run_gen

def land(blocks):
    status, out, steps, unsafe, mg, toks, bad0 = run_gen(blocks, record=False)
    assert status in ('HALT', 'LAND'), (blocks, status)
    return status

print("== predict-and-confirm, V==1 (V=52), ALL 64 length-6 buffers over {1,2} ==")
ok = bad = 0
for buf in itertools.product((1, 2), repeat=6):
    starts11 = buf[0] == 1 and buf[1] == 1
    has22 = any(buf[i] == 2 and buf[i + 1] == 2 for i in range(5))
    pred_fatal = not (starts11 and not has22)
    fatal = land([2, 2] + list(buf) + [52]) == 'HALT'
    if fatal == pred_fatal:
        ok += 1
    else:
        bad += 1
        print(f"  MISS buf={list(buf)}: fatal={fatal} predicted={pred_fatal}")
print(f"  length-6 grid: {ok} confirmed, {bad} misses")

print("\n== predict-and-confirm, V==0 (V=51), ALL 32 length-5 buffers over {1,2} ==")
ok = bad = 0
for buf in itertools.product((1, 2), repeat=5):
    pred_fatal = buf[0] == 2 or buf[1] == 2
    fatal = land([2, 2] + list(buf) + [51]) == 'HALT'
    if fatal == pred_fatal:
        ok += 1
    else:
        bad += 1
        print(f"  MISS buf={list(buf)}: fatal={fatal} predicted={pred_fatal}")
print(f"  length-5 grid: {ok} confirmed, {bad} misses")
