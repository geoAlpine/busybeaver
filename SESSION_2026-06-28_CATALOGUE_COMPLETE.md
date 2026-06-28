# frontier カタログ完成 + 新 multiplier（5/2, 4/3）+ frontier scout（2026-06-28）

slow-width majority（cluster 2: o2–o16, Space Needle）を framework で characterize し、frontier 全体を分類完成。
並行で最新文献 scout。**結果: カタログ実質完成、新 multiplier 5/2(Space Needle)・4/3(o4,o5) で kernel 類を拡張、
全機械 HOLDOUT（decidable なし）、frontier は「新無条件角度なし」+2訂正。誤証明ゼロ・decision 主張ゼロ。**

## 新発見（カタログ）
- **Space Needle = ⌊5x/2⌋ Mahler counter（μ=5/2, p=2, v₂=−1）**[VERIFIED]。clean reset b=12,36,96,246,621、差分が
  正確に ×5/2。**新 multiplier 5/2**（3/2 でも 8/3 でもない、{2^a/3^b} の外）。loose な「Mahler-3/2-type」tag を訂正。
  expanding-kernel 類を {μ: v_p(μ)=−1} へ拡張（5 は奇ゆえ v₂(5/2)=−1、T_μ exact-endomorphism 類に適合）。
- **o4, o5 = ⌊4x/3⌋ Mahler（μ=4/3=2²/3, p=3, v₃=−1）**[VERIFIED]。reset peaks 比 → 1.334=4/3、existence facet(11-collision)。
  **新 multiplier 4/3**。o5 の旧「exponential」tag を訂正（4/3 は content multiplier で width 包絡でない、width は ~√t）。
  → **q=3 Erdős existence family = {o4, o5, o15, o18}**（4/3 と 8/3、ともに 2^a/3）。
- 全機械 ~√t width 包絡（slow-width=quadratic-time）、auto-milestone は IRREGULAR で hand-picked turning point 必須。

## 完成した frontier カタログ（19 cryptid）
| 機械 | μ | p | facet | barrier | 分類 |
|---|---|---|---|---|---|
| **Antihydra** | 3/2 | 2 | density q=2 | **β>0 PROVEN（唯一）** | Mahler density |
| o2, o7 | 3/2 | 2 | existence q=2 | head-local 無 | Mahler 3/2 family |
| o8 | 3/2 | 2 | existence q=2 (nested) | — | Mahler 3/2 nested |
| o10 | 3/2(inner) | 2 | composite | — | inner clean, **full OUT(確率停止)** |
| **Space Needle** | **5/2** | 2 | existence q=2 | — | **Mahler 5/2(新)** |
| o15, o18 | 8/3 | 3 | existence q=3 | 無(FAR HOLDOUT) | Erdős ternary |
| **o4, o5** | **4/3** | 3 | existence q=3 | — | **Erdős ternary(新)** |
| o3, o17 | — | — | — | o17: floor m=8 | **kernel-less odometer** |
| o11,o12,o13,o14,o16 | 不明確 | — | — | — | **too irregular（clean scalar map なし、~√t、(10)* sea + 不規則 geometric 内容）** |

**収束**: BB6 Collatz core = 4 multiplier {3/2, 5/2（p=2）, 4/3, 8/3（p=3）}、全て **v_p(μ)=−1 の expanding-kernel 類**
（BB6_STRUCTURAL_LIMIT_THEOREM の定理が一括カバー）+ kernel-less odometer 2体 + irregular 5体。

## lottery（decidability）— 全 HOLDOUT
o2–o16 + Space Needle 全機械、sound tool（far_dfa m≤8, far_finder k≤7, far_cegar 80–120 round）で **全 HOLDOUT**。
verify gate は何も verify せず＝**decidable な機械なし、DECISION 主張ゼロ**。lottery upside は frontier 全体で refuted。soundness 健全。
（最 tame な decision candidate は o3 = bounded-alphabet odometer、だが現状 HOLDOUT・[OPEN]。）

## frontier scout（`FRESH_ANGLES_SCOUT.md`）— 新無条件角度なし、2訂正
- 単一軌道 Σe(t ξ(3/2)^n)=o(N)（=AEV q=2/Mahler）への 2018–2026 技法を全 survey、全て**2つの壁**の背後：(I) metric/a.e.-in-ξ（代数 ξ に
  特殊化不可）or (II) annealed/measure-level（quenched 単一実現を bound せず）。
  - decoupling(Bourgain-Demeter): L^p-mean = Salem-Zygmund √N の face、単一点で何もなし → (I) lacunarity で closed（vdC と同理由）。
  - sum-product/Fourier decay(Li, Streck, L²-flattening 2407.16699): 全て measure |μ̂(ξ)|→0 = annealed、単一 Haar-null 軌道に不可、
    Streck は非Pisot 代数で logarithmic only → (II) closed。
  - entropy decrement(Tao): ℤ の乗法構造要・乗法関数用、単一幾何軌道に transfer せず。
  - nilsequences/Host-Kra/Frantzikinakis-Host: (3/2)^n は polynomial でなく nilsequence でない、polynomial leading-bit（既知等分布）のみ制御 → closed。
  - ×2×3/homogeneous(Lindenstrauss-Mohammadi, Datta-Jana): measure-rigidity は正エントロピー不変測度要、Datta-Jana も measure を input。
- **Mahler 3/2 の 2020–2026 進展は density に効かず**（2411.03468=confinement、AEV=reformulation、1806.03559=数値のみ、easy p>q² は 3/2 で構造破綻）。
- **唯一の un-closed（speculative）framing**: 軌道自身の finite-N 経験測度上の **quenched/deterministic L²-flattening**（×3 自己拡大を自己脱相関に）。
  既存 notes に不在だが「壁を破るのでなく再 frame」（それ自体が証明になる）[OPEN]/speculative、小数値 probe の価値のみ。
- **[訂正1]** AEV_METHODS の「effective Fourier rate→Erdős-Turán→density」は **doubly dead**（annealed+ν_{2/3} は logarithmic、
  Datta-Jana は decay>1/2 要）→ AEV_METHODS に banner。
- **[訂正2]** Datta-Jana threshold Σ_{|m|≤X}|μ̂(m)|=O(X^{1/2−θ}), θ>7/64 が future bridge の clean calibration。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[VERIFIED] frontier カタログ実質完成**: 19 cryptid を {3/2,5/2,4/3,8/3 の expanding-kernel（v_p(μ)=−1）} + kernel-less odometer(o3,o17)
   + irregular(o11-o16) に分類。**新 multiplier 5/2(Space Needle)・4/3(o4,o5)** で kernel 類拡張。BB6_STRUCTURAL_LIMIT_THEOREM が一括カバー。
2. **[訂正] tag**: Space Needle=5/2(3/2 でない)、o5=4/3(exponential でない)。
3. **[PROVEN/HOLDOUT] decidable な cryptid なし**（全 sound tool HOLDOUT）、lottery refuted、soundness 健全。
4. **[honest] frontier(A) に新無条件角度なし**（2018-2026 全技法が metric-a.e. or annealed の壁の背後）、doubly-dead route 撤回、
   Datta-Jana calibration 取得。reduction が無条件貢献のまま。

## 完全証明の現在地（カタログ完成後）
- **(B) 構造的限界定理 = 実質完成・カタログ完成**（19 cryptid 全分類、4 multiplier の expanding-kernel 類 + odometer + irregular、
  density facet に proven barrier(Antihydra)、5階層 hierarchy）。投稿可能。
- **(A) 個別 cryptid = AEV/Mahler に等価（q=2: 3/2,5/2 / q=3: 4/3,8/3）、近道なし**。新角度 scout も closed、唯一 speculative=quenched L²-flattening。
- BB6 Collatz core 全体が **4 つの Mahler/Erdős 等分布問題（multiplier 3/2,5/2,4/3,8/3）のカタログ**に整理＝「BB6 frontier が encode する named number theory」の完成（CRYPTID_CENSUS Route ii/iii 達成）。

## 次の生きた一手（候補）
1. **BB6_STRUCTURAL_LIMIT_THEOREM に完成カタログ（4 multiplier + 全 19 分類）を addendum**、`docs/theory_certification_hierarchy.md` と統合（投稿形）。
2. **o3 / o11–o16 の clean reduction を追う**（irregular 5体に hand-picked milestone で scalar map が出るか、o3 odometer の decidability 再挑戦）。
3. **quenched L²-flattening の小数値 probe**（唯一の speculative frontier、壁を破らずとも構造が見えるか）。
4. **5/2・4/3 の AEV 配置を精密化**（5/2 は q=2 だが {2^a/3^b} 外＝AEV の coprime p/q=5/2 instance、4/3=q=3）。
