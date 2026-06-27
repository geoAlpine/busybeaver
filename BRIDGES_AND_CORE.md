# endogeneity defect の同型概念調査 — 大部分は既存理論への「橋」、核1つだけが genuinely new（2026-06-27）
3つの並列文献調査の統合。問い：「endogeneity defect」は新数学か、既存理論への橋か。**答え：分解すると、ほとんどの
ピースは既存の名前付き概念に対応し（橋＝道具を借りられる）、genuinely new なのは1つの核だけ——その難しさは
ちょうどマーラー 3/2。** これは専門家が期待した「新数学でなく既存理論を結ぶ橋」がかなり当たっていたことを示す。
引用は verified/unverified を明記（PDF 未確認は要確認）、捏造ゼロ。

---
## 1. 橋（既存概念に対応＝道具・名前を借りられる、citable）
| 我々のピース | 既存の名前付き概念 | 借りる道具/名前 | 検証 |
|---|---|---|---|
| 再帰 `Def(k+1)≤ρDef(k)+Inj(k)`, ρ<1 | **Lasota–Yorke 二ノルム不等式** ＋ **離散 affine Grönwall/Bellman** ＋ Keller–Liverani 摂動 ＋ Nagaev–Guivarc'h | quasi-compactness/spectral gap の標準機構；`Def(k)≤ρ^k Def(0)+Σρ^{k-1-j}Inj(j)` | 構造 verified |
| annealed vs quenched 比較 | **surrogate-data testing**（Theiler 1992）＋ **closed-loop identification bias**（Söderström–Stoica 1983） | 我々の defect の**正直な名前＝閉ループ同定バイアス**；annealed=shuffle surrogate | verified |
| B_k conditional-bias operator | **Yao の next-bit test** | B_k≈0＝「B_k という1テストに対し pseudorandom」 | verified |
| 障害（一方向 character sum/自己相関） | **van der Corput 差分 ＋ Mauduit–Rivat carry lemma ＋ Gowers ノルム**（automatic 列） | 「自身の carry 生成関数と相関する列」の**まさにその機械**；Inj(k)＝Gowers/additive-energy 増分 | verified（carry lemma の逐語は要確認） |
| 自己生成 disorder | **"self-induced quenched disorder" / 決定論的スピングラス**（Bouchaud–Mézard 1994；Marinari–Parisi–Ritort；LABS/merit-factor） | **最も近い概念的 home**：単一決定論対象が自分の disorder を生成、replica surrogate は高温で可解・低温/基底状態で**OPEN**＝我々の defect の near-exact 像 | verified（逐語要確認） |
| 「指定軌道は a.e. が成功する所で失敗」 | **effective ergodic theory / algorithmic randomness**（Gács–Hoyrup–Rojas：Schnorr random ⇔ Birkhoff-typical；computable⇒never ML-random⇒a.e. genericity から除外）＋ **open normality / finite-state dimension** | 「computable ⇒ a.e. が効かない」の厳密な名前；π/e の normality 未解決と同型 | verified |
| 自己feeding 桁 ＝ マーラー | **base-3/2 odometer**（Akiyama–Frougny–Sakarovitch 2008）＋ **AEV 正規性予想**（arXiv:2510.11723, 2025）＋ 「1の割合→1/2」予想（arXiv:2504.13716, Conj 4.2） | 我々の問題は**既に名前付き open 予想**；k-kernel test で carry が automaticity を破ることを certify | verified |

**⇒ 「engine（Lasota-Yorke/Grönwall）」「障害解析（Mauduit-Rivat carry lemma + Gowers）」「framing（surrogate/
closed-loop ID、self-induced disorder）」「formalization（open normality/algorithmic randomness）」「prior art
（AEV/AFS）」は全て借りられる citable な既存理論。**

---
## 2. genuinely new な核（既存の home なし、これが我々の貢献）
> **単一の指定された決定論的軌道の、ENDOGENOUS（自己生成・閉ループ）cocycle に対する unique ergodicity /
> effective equidistribution——annealed（i.i.d. surrogate）から Dirac（決定論）quenched 極限への transfer。**
- あらゆる既存枠組みは「a.e. のランダム realization」で止まる（RDS の quenched＝a.e. 環境）、またはランダム測度上
  に住む（Malliavin/anticipating）、または automatic/bounded-carry・高温の場合だけ解く（Mauduit-Rivat/spin glass）。
- 唯一の先例は (T,T⁻¹)/random walk in random scenery——自身の軌道に沿って cocycle を読む唯一の場所——だが
  そこでは **UE/transfer-operator の道具を捨てて確率的極限定理に切り替える**。**その切替えこそが我々の
  endogeneity defect**。endogenous-cocycle の UE 理論は存在しない。
- **その核の難しさ ＝ ちょうどマーラー 3/2。**

---
## 3. 重要な訂正（これらに頼ってはいけない、エージェントが明示）
- **Anashin の p-adic ergodic 理論は適用不可**：⌊3x/2⌋ は Z_2 上で 1-Lipschitz でない（奇数の半分は Z_2 で未定義）、
  かつ「orbit の充填」であって「桁の normality」でない。**頼るな。**
- **FCSR は PARTIAL のみ**：loop が閉じていない（入力は過去 cell であって出力 parity でない）、modulus も違う（×3 mod 2^k
  vs ×2⁻¹ mod 奇 q）。equidistribution 定理を主張するな。
- **「log₂3 を instrument に」は IV exogeneity を満たさない**（log₂3 は軌道を生成、完全相関）＝類推であって transfer でない。
- **「自身の力学に対し pseudorandom」は普遍命題として証明可能に不可能**（次ビットを embed する distinguisher）＝
  普遍 phrasing を捨てよ。

---
## 4. これが意味すること（戦略・kernel/community-feedback への含意）
- **専門家の見立てがかなり当たった**：endogeneity defect は「新数学を1から」でなく、**大部分が既存理論への橋**
  （engine・障害解析・framing・formalization・prior art を借りられる）。**残る genuinely new な核は narrow で locatable**
  （endogenous-cocycle equidistribution / annealed→Dirac-quenched transfer）＝マーラー。
- **community-feedback（A）が劇的に強くなる**：もう「我々の新概念 endogeneity defect」でなく、**既存の語彙で語れる**——
  「closed-loop identification bias を surrogate-data testing で測り、障害は Mauduit-Rivat carry lemma 型の自己相関、
  これは self-induced quenched disorder（merit-factor 級の難問）と同型、formalization は open normality、prior art は
  AEV 予想」。専門家は自分の道具が刺さるか即判断できる。
- **最も有望な借り先 ＝ 統計物理の「self-induced quenched disorder」**（決定論スピングラス/merit-factor/LABS）。
  同じ構造的理由で数十年 open ＝ 難しさを validate し、disordered systems の道具体系と community を与える。
- **新数学 vs 橋の最終判定**：**橋が主**（多数の既存理論から道具を借りる）、**新核は1つ**（endogenous-cocycle UE
  = マーラー）。だから「ゼロから全く新しい概念の発明」ではなく、「既存の engine/障害/framing を組み、唯一の新核
  （= 既存 open 問題）を埋める」——これが正確な姿。

---
## 5. 正直な caveat
- いくつかの逐語的定理文（Mauduit-Rivat carry lemma、Bouchaud-Mézard 1994、Keller-Liverani 全文、AEV subalphabet
  文言、FLP 定理番号、Lasota-Yorke 年）は PDF 未 render で **UNVERIFIED**——論文引用前に要確認。著者・arXiv ID・
  構造的対応は VERIFIED。
- 「FCSR↔マーラー橋」「r_n は非 2-automatic」は文献に**無い**——主張するなら自分で証明（cite でなく）。
- 「quenched/annealed = endogeneity」の同一視は我々の original framing（既存でない、だが apt）。
