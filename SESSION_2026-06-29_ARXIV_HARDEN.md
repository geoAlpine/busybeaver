# arXiv 硬化: Antihydra TM-extraction [PROVEN]・citation pin・nested-Collatz theorem（2026-06-29）

3トラック並行（Y1 nested-Collatz theorem / Y2 citation pin / Y3 TM-extraction hand-proof）。
**結果: Antihydra TM-extraction が FULL hand-proof [PROVEN] に昇格（arXiv load-bearing gap が flagship で閉）、citation ほぼ全 pin、
nested-Collatz conditional theorem 完成。誤証明ゼロ・decision なし・self-catch 1件。**

## Y3【最重要】Antihydra TM-extraction FULL hand-proof（`TM_EXTRACTION_PROOFS.md`）
- **Antihydra = FULL hand-proof [PROVEN]（conjecture-free）**: macro-config `C(a,b)=0^∞ 1^a 0 1^{b+1} 0 1[A>0]0^∞`, c:=b+6。
  3 shift lemma（A→/E→/C← sweep、各 one-transition 帰納）+ inner ×3/2 lemma（`I(a,L,R)⟹I(a,L−2,R+3)`, L≥3、10-link chain=2R+13 micro-steps 各 link が単一 table entry or shift lemma）+ 両 carry lemma（EVEN: a↦a+2 / ODD: a↦a−1 or HALT、bb_sim skeleton と cross-check）。
  **macro-step 定理: b'=⌊3b/2⌋+3 always、a は b の parity で +2/−1、c=b+6 ⟹ c'=⌊3c/2⌋（literal hydra map）**。
  **halt 基準 PROVEN: 奇-c step で balance a=0 のとき halt ⟺ balance が初めて負 ⟺ Lemma 3.1**。inner lemma 675/675、macro lockstep 15 steps bb_sim 一致（c-orbit 8,12,18,27,40,60,90,135,…）、309 generic continue + 全 a=0 halt/continue 検証。
  **→ PAPER_MAIN §3.1 Antihydra macro-structure [VERIFIED]→[PROVEN]、Theorem 1 for Antihydra は [PROVEN] outright（AEV/Mahler kernel は [OPEN] のまま不変）**。
- o18/o15: **halt 基準は table-trivially [PROVEN]**（唯一の halting transition）。macro-coordinate は [VERIFIED] のまま（o18 base-3 odometer carry 帰納 未完、o15 parity-irregular）。
- o10-inner: PARTIAL（inner ⌈3m/2⌉ orbit 再検証 exact、full chain 未転記）、[VERIFIED]/[CONDITIONAL]、o10-FULL OUT。
- **健全性: file 自身の summary 表の over-claim（o10-inner/o18 を full と誤記）を本文 partial に合わせて訂正**。

## Y1 nested-Collatz conditional theorem（`NESTED_COLLATZ_THEOREM.md`）
- **[PROVEN structural; PROVEN-instance o10] 厳密還元**: M halts ⟺ ∃ epoch e で reseeded inner orbit O_e（seed B_e）が H_e を hit。非停止 ⟺ reseed family が H を永久回避（Π⁰₁-avoidance）。direction = Σ_e p_e 上の Borel-Cantelli 二分。
- **[CONDITIONAL] direction theorem**: IF 各 reseed の effective 等分布（doubly-exp reseed family 横断で uniform rate, p_e を破る）THEN direction は Σp_e に従う。convergent Σp_e<∞ ⟹ 非停止（BC-I 独立性不要=o18 existence の Axis-2 lift, provable-ish）／divergent ⟹ 停止だが BC-II の quasi-independence を単一決定論 reseed family が供給不能=o10 壁。
- 分類: divergent/halt-leaning = **o10 のみ**（p_e≈1/3 非減衰 VERIFIED, decision [OPEN]）/ convergent/non-halt = o2,o7,o8,o11,o12,o14,o16（spontaneous-defect target, scaling 未抽出 [OPEN]）/ unclear = o13（outer halt-measure 未抽出, 前「~0」は inner safe-rate で confounded、[OPEN]）。
- **barrier 二部 inherit [PROVEN]**: halting reseed 存在（o10: m 奇 b=0 halt, inner 固定点 m=−1）だが不変**集合**は halting reseed を除外でき β-barrier 不成立 → **inner parity sub-factor は β=+1/2 を inherit、full machine の outer existence は [OPEN] over-approximation 軸**（doubly-exp family を扱う separating set 要、FAR/CEGAR HOLDOUT）。
- 数値: o10 abstract vs raw TM **0 mismatch**, halt fraction **0.33678**（doc の 33.67% 再現、旧 ~1/6 reimpl 不一致を解消）。

## Y2 citation pin（`CITATIONS.md`）— ほぼ全 VERIFIED
- **ergodic-opt**: Mañé Nonlinearity 9(1996)273-310 / Bousch Ann.IHP 36(2000)489-508 + Ann.ENS 34(2001)287-311 / Jenkinson DCDS 15(2006)197-224 + ETDS 39(2019)2593-2618(arXiv:1712.02307)。
- **2-adic Collatz**: Lagarias AMM 92(1985)3-23 / Bernstein-Lagarias Canad.J.Math.48(1996)1154-1169 / Matthews-Watts Acta Arith.43(1984)167-175（page は MathSciNet 確認推奨）。
- **Mahler/Z-number**: Mahler JAMS 8(1968)313-321 / FLP Acta Arith.70(1995)125-147 / Dubickas-Mossinghoff Math.Comp.78(2009)1837-1851（=「4/3 問題」）/ Dubickas Glasgow MJ 51(2009)243-252（subword complexity）/ AFS Israel J.Math.168(2008)53-91 / Narkiewicz(1980) / Erdős Math.Mag.52(1979)67-70。
- **arXiv:1901.03913 = Dömötör Pálvölgyi「The range of non-linear natural polynomials cannot be context-free」(2019)** VERIFIED → PAPER_HIERARCHY の authorship caveat 削除可。
- **AEV 2510.11723** conjecture 番号 VERIFIED（Conj1.2 正規性 / 1.4 no Z-number p<q² / 1.6 mod-q^k 等分布 / Thm1.5 1.2⟹1.4 / Thm1.7 1.2⟺1.6）。Eliahou-Verger-Gaugry 2504.13716 VERIFIED。
- **unpinnable（flag）**: Conze-Guivarc'h（genuinely unpublished、"unpublished" と cite）/ Matthews-Watts page（MathSciNet）/ Akiyama solo 2008（AFS でカバー、cite せず）/ Dubickas 2009 二論文 disambiguation（用途で選択）。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[PROVEN 昇格] Antihydra TM-extraction FULL hand-proof**: transition-table случай 解析 + sweep 終了論で raw TM → c'=⌊3c/2⌋ + halt 基準を hand-prove。**Theorem 1 for Antihydra は [PROVEN] outright**（arXiv load-bearing gap を flagship で閉、AEV kernel [OPEN] 不変）。
2. **[PROVEN/CONDITIONAL] nested-Collatz conditional theorem**: halt ⟺ outer orbit 上 BC、convergent/divergent 二分、9機械分類、barrier 二部 inherit。Axis-2 が theorem として完成。
3. **citation ほぼ全 pin**（VERIFIED）、1901.03913=Pálvölgyi 確定、AEV 番号確認。arXiv reference が submission-grade に。
4. **[健全性] Y3 が自身の summary over-claim を self-catch・訂正**（規律維持）。

## 完全証明・arXiv の現在地（硬化後）
- **PAPER_MAIN**: Theorem 1 Antihydra [PROVEN] outright（TM-extraction hand-proof）、citation pin 済、nested-Collatz theorem 参照可。残: o18/o15/o10-inner macro-coordinate は [VERIFIED]（誠実 flag）、AEV kernel [OPEN]。
- **PAPER_HIERARCHY**: 1901.03913 authorship 確定で caveat 削除可、citation pin 済。
- **arXiv-readiness**: 主要 gap（flagship hand-proof, citation locator）が閉、**submission-grade に大きく前進**。残機械的残務: paper 本文に label 昇格・pinned citation を反映、o18 carry 帰納の hand-proof（任意、in-scope の他3は halt 基準のみ trivial PROVEN で十分）。

## 次の生きた一手（候補）
1. **PAPER_MAIN/PAPER_HIERARCHY に今回の昇格を反映**: Antihydra [PROVEN]、pinned citations、1901.03913 caveat 削除、nested-Collatz theorem 参照＝両 paper を submission-grade 最終形に。
2. **o18 base-3 odometer carry 帰納の hand-proof**（o18 を Antihydra 並みに [PROVEN] in-scope に、任意）。
3. odometer 2体（o3,o17）保留中（ユーザ判断）。
4. 両 paper の最終 read-through + abstract 調整。
