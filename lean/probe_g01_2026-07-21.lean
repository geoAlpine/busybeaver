import X2
open X2
-- Is g = 0 a generation for the §5am canonical families?
#eval ((List.range 1500).filter (fun n => 1 ≤ n && steps n (M1 0) == some (M6 0)))
-- g = 1?
#eval ((List.range 1500).filter (fun n => 1 ≤ n && steps n (M1 1) == some (M6 1)))
-- controls: g = 2 and g = 3 should be found (covered by the proven lemmas)
#eval ((List.range 1500).filter (fun n => 1 ≤ n && steps n (M1 2) == some (M6 2)))
#eval ((List.range 1500).filter (fun n => 1 ≤ n && steps n (M1 3) == some (M6 3)))
