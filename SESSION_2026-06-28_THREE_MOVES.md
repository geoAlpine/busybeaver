# existence facet の3手（①barrier ②quenched BC ③o10 halter）（2026-06-28）

> **⚠ 訂正 2026-06-28（後続 `SESSION_2026-06-28_CERT_HUNT.md`, P2/P3 で判明）。** 本 doc の2点を訂正：
> (a) **「o17 は proven barrier / o18,o15 は無し」の binary は REFUTED**。正しくは**量的 floor 差**：all-k/REG barrier は
> 「halt 判別子が**非有界 reachable run** に住む（brick-(d) counter 機構）」とき**のみ**。o17 は k-window floor **m=8 まで**
> proven だが m≥9 で binding gram `0A01^6` が reachable から detach＝**all-k/REG barrier は無い**（旧主張は over-claim・撤回）。
> o18 は floor **m=2**。**どの cryptid も proven REG barrier を持たず**、proven な no-structure-only barrier は **Antihydra の
> density β>0 のみ**。 (b) **②の「o18/o15 は closer to provable（weaker target）」は (R3) が illusory（上記 O18_QUENCHED_BC 訂正）
> ゆえ撤回** — quenched target も AEV q=3 equidistribution に還元。以下は (a)(b) で amend して読むこと。

前 session の次手①②③を順に並列実行。**結果: existence facet の barrier は machine-dependent（o17 は proven, o18/o15 は head-local で無し）、
o18/o15 の quenched target は Antihydra より厳密に WEAK（closer to provable）、o10 は HALT 方向で OPEN（BC-II 適用不可）。
全て�some健全（false claim ゼロ、harness バグを self-catch）。**

## ① o18 の no-certificate barrier（`O18_NO_CERTIFICATE.md`）— machine-dependent と判明
- **[PROVEN] no 2-window（SLT）certificate**: reachable の 2-gram は (1,D)（D が 0 読む左隣 1, 8274×）と (D,1)（D が block 左端で 1 読む, 9×）を含むが
  collision「D が 1 読む・左 1」は 0×（8×10⁷ step）。任意 2-window G⊇reachable は 1[D]1 を accept→2 step で halt→step-closure が halt 強制→2-window 証明書なし。far_dfa も m=2 でここで失敗。
- **だが m≥3 は OPEN**: o18 の halt 判別子は **head-local（threshold ちょうど 3）**＝3-window が collision (1,D,1) を reachable look-alike (1,D,0) と区別。
  embedded-family 非正則論法は **o18 に transfer しない**（clean reachable family C_N=[F]0 1^{N-1} は一様非停止→pumping で非停止が出る、EQ/REG engine 失敗）。
- **β>0 と parallel な barrier を establish しない**（誠実な negative）: Antihydra の β>0 は強い（max over μ が halting atom を必ず含む→全 density 証明書 block）。
  o18 の existence barrier は bottom rung（no 2-window）のみ proven、意味ある class は全 open——不変**集合**は halting 軌道を除外でき、head-local collision は window で gate 可能（EXISTENCE_META §2b の予言通り）。
- **o17 との鋭い対比**: o17 の reachable 0A01^k は irregular に halt（**non-local** mod-3 block-length 判別子）→ **o17 は genuine k-window/REG barrier を持つ**、o18 はそれを欠く。
  → **existence facet の no-structure-only barrier は machine-dependent**: non-local halt(o17)=proven barrier、head-local halt(o18/o15)=barrier なし（むしろ certificate が存在しうる）。

## ② o18/o15 の quenched Borel-Cantelli（`O18_QUENCHED_BC.md`）— 厳密に WEAKER target
- bad event 精密化（[PROVEN] 遷移表から）。o18 を 10^10 step（epoch 0-11）, o15 を 1.3×10⁹ step（epoch 0-12）、**両者 0 collision**。
- **realized margin は binary**: ∞ ほぼ全域、carry-defect epoch（epoch7）でちょうど 1、**0 になることも grow することもない**（c·n 成長の逆）。
- annealed budget Σ1/N_n 幾何（ratio ちょうど 3/8）summable（1.54e-4）。quenched halt count は observably 0、genericity probe は summable rate と consistent（[OBSERVED] 未証明）。
- **最小 effective input**: (R2) mod 3^{k_n}（k_n≈0.893n）の effective 等分布で **累積絶対 discrepancy < 1** → count < ΣHaar+Err < 1 ⟹ =0（BC-I strength）；
  または (R3) **sublinear carry-run bound run_n=o(n)**（< 0.893n 必要、realized は O(log n) で factor~0.9 slack）。
- **Antihydra より厳密に WEAK**: BC-I（ΣP<∞⟹有限）< SLLN；summable tiny budget(1.5e-4) に対する**絶対 <1 error** < constant density に対する**相対 o(N) error を永久に**。
  summable budget が BC-I strength を「required ZERO count」に変換＝Antihydra の density には無い助け。
- **誠実な difficulty 比較**: lower bar・same wall（両者 AEV: o18=q=3 Erdős, Antihydra=q=2 Mahler）・現状 crack なし。**o18/o15 は genuinely closer to provable**（証明された訳でなく bar が低い）。
  honest trap: realized geometric near-miss（margin≤1）は O(1)/defect 事象で 1/N_n 事象でない、summable rate は1段下の「margin=0」。

## ③ o10 を halter として decide（`O10_HALTER.md`）— [OPEN]、BC-II 適用不可
- **status「o10 halts」= [OPEN]**。heuristic は HALT だが decidable でなく、Antihydra と同じ a.e.-vs-specific 壁に逆方向で当たる。**decision 主張なし**。
- [PROVEN, raw-TM 照合 0 mismatch B=1..15]: per-epoch halt 条件（countdown が奇 m で b=0 着地）、refill map（(m,1) m奇→B_next=3(m−2)；(m,0) m偶→3m−7、B=5→57 が実機再現）。
  単一軌道: B_1=5(refill)→B_2=57(refill)→B_3≈2.1×10⁸。**epoch 1-2 のみ simulable**（両非停止、≥40M holdout）。**epoch 3 は infeasible**（~1.4×10⁸ 内側 step, m が 2470万桁）。
- **Borel-Cantelli II は適用不可（proven negative）**: 33.667% は **ensemble** 統計、決定論軌道は各 epoch 0/1 で ΣP なし；BC-II は **random 事象＋独立性**要、単一固定軌道は確率空間も独立性もなし。
  （BC-I=convergence 側＝o18/o15 が得るもの；o10 は divergence 側＝単一軌道が欠く独立性を要する。）
- **open kernel（divergence 側 analog）**: doubly-exp-sparse refill 軌道 B_e が奇 m で b=0 に着地する epoch を生むか＝動的に決まる underflow index での m-parity 等分布。Antihydra より厳密に harder。両 unified theorem の外。
- **健全性 self-catch**: 最初の harness が 8 spurious halt-mismatch（内側 milestone を refill と誤判定）→ 正しい refill 条件で 0/15。SOUNDNESS_INCIDENT 教訓を measurement tool に適用、reduction は stand。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN] existence facet の barrier は machine-dependent**: o17（non-local halt 判別子）= genuine k-window/REG barrier；
   **o18/o15（head-local halt）= barrier なし**（不変集合が halting 軌道除外可、3-window が collision を gate）。
   → existence facet は「barrier 一律 open」でなく「o17 proven barrier / o18,o15 barrier 無し（certificate が存在しうる）」と細分。
2. **[PROVEN] o18 no 2-window certificate**（collision 1[D]1 が halt 強制）。m≥3 は open（head-local ゆえ certificate plausible）。
3. **[PROVEN 構造] o18/o15 quenched target は Antihydra より厳密に WEAK**（BC-I vs SLLN、summable budget→zero count、2つの具体 sufficient input R2/R3）。
   **o18/o15 が core で最も tractable** candidate（head-local halt + summable target + BC-I strength）。
4. **[PROVEN negative] o10 は BC-II 適用不可**（単一決定論軌道、独立性なし）。「o10 halts」= [OPEN]、open kernel = divergence-side 等分布、Antihydra より harder。
5. **[健全性] harness バグを self-catch・訂正**（reduction は健全）、decision 主張ゼロ。

## 完全証明・限界定理の現在地（更に refine）
- **Antihydra（density, 3/2）**: no-structure-only **PROVEN（β>0）**、残 OPEN = q=2 density genericity（Mahler）。core で barrier が最強・target が最 tight。
- **o18/o15（existence, 8/3）**: no-structure-only barrier は **head-local ゆえ弱い/無し**（certificate plausible）、だが quenched target は **strictly weaker**（BC-I, summable）＝**core で最も provable に近い**。残 OPEN = q=3 existence genericity（Erdős）＋ ≥3-window certificate 有無。
- **o17（odometer）**: no-structure-only **barrier あり**（non-local, k-window/REG で proven 方向）、kernel-less、別問題。
- **o10（composite）**: HALT 方向で OPEN、BC-II 不可、両 theorem の外。

## 次の生きた一手（候補）
1. **o18/o15 に ≥3-window / FAR-DFA certificate を本気で探す**（head-local halt ゆえ存在しうる）: far_finder/far_cegar を o18 reachable に走らせ、3-window 以上で
   forward-invariant halt-free L が構成できるか。**もし見つかれば o18/o15 を DECIDE = 真の BB6 貢献**（最も現実的な lottery upside、core で最 tractable）。
2. **(R3) sublinear carry-run bound を攻める**: o18 の leading base-3 carry-run が o(n)（< 0.893n）であることの unconditional 証明（realized O(log n)）＝quenched BC-I を closing する最弱 input。
3. o17 の REG barrier を proven として固め（certificate hierarchy への寄与）、non-local vs head-local の二分を catalogue 化。
4. 2-facet/2-axis + barrier-machine-dependence を投稿文書に統合。
