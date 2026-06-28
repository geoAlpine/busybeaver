# certificate hunt + carry-run + o17 barrier（並行3手）（2026-06-28）

①o18/o15 に FAR-DFA certificate を探す ②(R3) sublinear carry-run o(n) を攻める ③o17 REG barrier 固め、を並行実行。
**結果: ①HOLDOUT（o18/o15 は両側から open kernel）②(R3) は illusory・equidistribution に還元 ③o17 は REG でなく
k-window floor m=8（旧 all-k 主張を撤回）。2つの健全性訂正。誤証明ゼロ。decision 主張なし。**

## ① FAR-DFA certificate hunt（`O18_CERTIFICATE_HUNT.md`）— HOLDOUT 両側 open
- far_dfa(m=2..16)・far_finder(k-tails 2..6)・far_cegar(120 round) を o18/o15 に走らせ **全 HOLDOUT**（community の stronger FAR が
  既に decide せず＝既定通り）。**controls 健全**: toolchain は positive-control counter に VERIFIED NEVER_HALTS、cryptid(Antihydra/Lucy)
  に HOLDOUT、BB4 halter に HALTS。LAYER-0 は bb_sim と 5000 step 照合。**verified certificate なし→decision なし**。
- **HOLDOUT の理由（bb_sim 照合済）**: o18 reachable は base-8/3 iteration（clean config C_N=[F]0 1^{N-1}, 幅 10→28→76→204→546→1458,
  N_{j+1}=⌊8N_j/3⌋+2）。collision 1[D]1 は 10^7 step で 0×。非停止=「carry が決して align しない」=open Erdős equidistribution。
  CEGAR の failure signature が operational proof: 「halt config が L に（too coarse）」と「receding context で closure 失敗（unbounded
  boundary 追跡要）」を振動＝regular L は too coarse(halter 混入) か too fine(non-regular counter) のどちらかに強制、FAR cert は open
  carry-alignment set を認識せねばならない。
- **synthesis**: o18 は **proven barrier も findable certificate も持たず**（両側から open kernel）。**head-local-gateable(1 step)≠
  FAR-certifiable(reachable 全体上の closure)**。o15 も同一 picture（同 HOLDOUT、同 receding-context 振動）。
  honest scope: characterization + exhaustive-search negative であって「no regular cert」の証明でない（それ自体が o18 を decide する）。

## ② (R3) sublinear carry-run o(n)（`O18_CARRYRUN.md`）— illusory・equidistribution に還元
- **厳密 recursion = 円回転**: θ_n={log_3 N_n}, θ_{n+1}={θ_n+α}, **α=log_3(8/3)=0.892789**(無理)＋summable O(1/N_n) 摂動。
  run_n=⌊−log_3 dist(θ_n,{0,1})⌋+O(1)＝回転軌道の corner への接近。realized **O(log n)**（Benford base-3 P(run≥k)≈3^{-(k-1)}, max 10@12000）。
- **[訂正・決定的] threshold はちょうど α n = 0.892789 n = k_n（base-3 桁数）**。唯一の unconditional bound は trivial `run_n ≤ k_n`
  （run は桁数を超えない）で **threshold と一致＝ZERO slack**。residual `run_n < k_n` は **alignment/halt 事象そのもの**＝「run<k_n」は
  非停止定理＝**循環**。前 O18_QUENCHED_BC の「0.9 slack / 0.98n too weak by a hair」は **natural log の誤り**（base-3 で ceiling=threshold）。
- 必要 lemma (L-carryrun)[OPEN]: dist({n log_3(8/3)+log_3 x},{0,1}) ≥ c(3/8)^n = effective inhomogeneous Diophantine/shrinking-target
  = **AEV Conj 1.6 q=3 の Archimedean/Mahler facet**。**3-adic valuation budget は無力**（trailing run を制御、halt は leading run＝
  adele の別の place、product-formula link なし、独立を検証）。
- **verdict: (R3) は equidistribution に還元、o18 を close しない**。「o18/o15 は closer to provable」は撤回。

## ③ o17 REG barrier（`O17_REG_BARRIER.md`）— REG でなく floor m=8（健全性訂正）
- **[PROVEN, 予想非依存] 2≤m≤8 で no m-window certificate**（family 0A01^k が halt 強制）。embedded family は genuinely
  Collatz-irregular（k%3∈{1,2} は trivial halt 80/80；k≡0 mod3 は 18 proven halters interleave、**delayed halter k=102@2.8×10⁷,
  k=108@6.7×10⁷**＝10⁷ で非停止に見えた＝3x+1 signature）。
- **[健全性訂正] 旧「o17 は all-k k-window/REG barrier」は over-claim・撤回**。machine-checked: all-or-nothing engine は **m≤8 で fire,
  m≥9 で停止**＝binding gram 0A01^6 が reachable から absent（A は left-0-run∈{0,∞} でのみ 0 読む、∞-frontier の right-1-run≤5）。
  5×10⁷ census で確認。LIMIT_THEOREM の「honest negative」を vindicate。
- **dichotomy は recast（binary 撤回・量的に）**: cryptid が all-k/REG barrier を得る ⟺ halt 判別子が**非有界 reachable run** に住む
  （brick-(d) counter 機構）。両 existence cryptid は finite floor で失敗: **o18 head-local floor m*=2、o17 non-local-in-block-length だが
  bounded-frontier(≤5-cell tail) floor m*=8**。o17 は o18 と brick-(d) ideal の strictly between。
- **LIMIT_THEOREM の「no REG certificate for a cryptid」は依然 OPEN**（証明は m≤8 のみ、family は m≥9 で detach）。o17 の貢献は
  **cryptid 中で最高の explicit k-window floor(m=8)** ＋ 予想非依存 Collatz-irregular halter family。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[PROVEN] o18/o15 は FAR HOLDOUT**（sound verifier、controls 健全）。**proven barrier も findable certificate も無し**＝両側から open
   kernel（AEV q=3 Erdős）。head-local-gateable ≠ FAR-certifiable。
2. **[訂正] (R3) carry-run target は illusory**（唯一の unconditional bound が threshold と一致・residual=halt 事象=循環）。
   o18 quenched も AEV q=3 Archimedean equidistribution に還元。「closer to provable」撤回。
3. **[健全性訂正] o17 は all-k/REG barrier を持たず、k-window floor m=8**（旧主張撤回）。dichotomy は量的（floor 値）＝
   all-k/REG barrier ⟺ 非有界 reachable run。**どの cryptid も proven REG barrier なし、proven no-structure-only barrier は Antihydra の
   density β>0 のみ**。
4. **[PROVEN/refined] frontier catalogue**: Antihydra/o10=AEV q=2(μ=3/2 density/composite)、o15/o18=AEV q=3(μ=8/3 Erdős existence)、
   o17=kernel-less odometer(floor m=8)。obstruction 2型(equidistribution kernel / odometer-with-Collatz-halt)。proven barrier は Antihydra のみ。

## 完全証明・限界定理の現在地（2訂正後の確定像）
- **Antihydra(density 3/2)**: 唯一 proven no-structure-only barrier(β>0)。残 OPEN=AEV q=2 Mahler density genericity。
- **o18/o15(existence 8/3)**: proven barrier なし・FAR HOLDOUT・quenched も equidistribution 還元＝**両側から open**。残 OPEN=AEV q=3
  Erdős existence(effective inhomogeneous Diophantine shrinking-target)。**「最 tractable」は誇張だった**（target は形式的に弱いが
  唯一の unconditional bound が boundary に一致）。
- **o17(odometer)**: k-window floor m=8(最高)、all-k/REG は未達、kernel-less、Collatz-irregular halter。
- **o10(composite)**: HALT 方向 OPEN、BC-II 不可、両 theorem 外。
- **共通核**: 全 cryptid（o10 除く方向）が単一軌道 effective equidistribution(AEV q=2 or q=3)に還元、proven barrier は density facet のみ。

## 次の生きた一手（候補）
1. **AEV q=3 Erdős facet を q=2 Mahler facet と統合**: o18/o15(q=3 existence/shrinking-target) と Antihydra(q=2 density) が同じ
   AEV Conj 1.6 の異 facet ＝**effective single-orbit equidistribution of ⌊x(p/q)^n⌋ for p/q∈{3/2,8/3}** に一括還元する
   1つの統一 kernel 文書（density と existence の両 facet を1つの AEV instance 族として）。
2. **non-有界-reachable-run 判定を frontier 全体に**: 各 cryptid の k-window floor を機械測定し、brick-(d)（非有界 run=REG barrier）
   との距離を catalogue（証明書階層への定量寄与）。
3. slow-width majority(o2-o16) に framework 適用（CRYPTID_CENSUS cluster 2、hand-picked milestone）。
4. 2-facet/2-axis + floor catalogue + AEV 統合を投稿文書化（BB6 frontier の named-number-theory + certificate-hierarchy 地図）。
