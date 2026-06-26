# 新数学・第一歩：endogeneity defect の枠組みと、スケール遷移の決定的測定（2026-06-27）
会議の決定（まず (d) の器を作り、後で (a) の燃料を入れる）を実行。最小の新概念「endogeneity defect」を定義し、
「step 2 で足りるか決まる」と言われたスケール遷移の収縮率 ρ を測定。`endogeneity_defect.py`。誤証明ゼロ。

## 定義（最小の新しい対象、ルート(d)）
- **Def_k(N)** ＝ scale k の endogeneity defect ＝ 非自明 ψ mod 2ᵏ に対する `|(1/N)Σ_{n<N,odd} ψ(c_n)|` の sup
  ＝ quenched（実軌道）の mod-2ᵏ 分布と annealed（Haar、Def=0）の差。
- **ρ(k)** ＝ annealed 遷移作用素（×3 mixing エンジン）の spectral gap 因子 ＝ scale k から**繰り越された**
  defect の収縮率。
- **Inj(k)** ＝ 注入 ＝ scale k での「次ビットの不均衡」`|P(next bit=1|context)−1/2|` ＝ 自己feeding が各
  スケールで注入する defect。
- **再帰**：`Def(k+1) ≲ ρ(k)·Def(k) + Inj(k)`。ρ<1 なら `Def_∞ ≤ Inj_sup/(1−ρ)`：壁が cumulative Def から
  local Inj へ移る。

## 決定的測定の結果
1. **ρ(k) < 1 が全スケールで成立**（0.0001, 0.030, 0.105, 0.175, 0.223, 0.300, 0.340、k=1..7）。
   **会議が望んだ contraction は存在する**——それは annealed spectral gap（材料 A・C の ×3 エンジン）。
2. **再帰 `Def(k+1) ≤ ρ·Def(k) + Inj(k)` は全 k で成立**、かつ **injection 支配**（ρ·Def は ~0.0003 で無視可、
   Inj が ~0.005-0.03）。繰り越し defect は contraction で消え、全ては注入。
3. **注入 Inj(k) は i.i.d. control と全スケールで一致**（max・重み付き RMS 両方、`endogeneity_defect.py` の
   control）。⇒ Inj(k) の見かけの増加は **2ᵏ context の最大値による extreme-value artifact**で、**真の注入は
   ゼロ**。実軌道の新鮮ビットは**各スケールで本当に新鮮**（規律：artifact を control で捕捉）。

## 第一の成果（ルート(d) は器の構築に成功）
> **枠組みは、累積的な壁（Def(k)→0）を、per-scale の局所量（Inj(k)~0）に局在化した。**
ρ<1（contraction、現存）＋ Inj~0（control 確認）⇒ Def→0。**機構は完成している。** 残る open core は
「**Inj(k)~0 を証明する**」——一ビット・各スケール・i.i.d. 比較の**局所**標的で、累積 equidistribution より
strictly tractable。これが endogeneity-defect 枠組みの最初の payoff。

## 正直な限界（「step 2 で足りるか」への答え）
- **ρ<1 は必要かつ現存**だが**十分でない**：再帰の閉包は Inj に依存し、Inj~0 の証明が局在化した壁。
- ルート(a)（log₂3 燃料）を Inj に注入する問題：foothold（log₂3）は**上位**桁を制御するが、Inj(k) は**低位**
  scale の新鮮ビット——**両者は c_n の逆端**。だから foothold は低位 Inj を直接制御しない。log₂3 を低位 Inj に
  効かせる機構は、結局 moving-middle-digit ＝ マーラー core。
- **結論**：枠組み(d)は **genuine な局在化（reframing）**で、contraction ρ<1 が現存することを確定した。だが
  **まだ closure（完全証明）ではない**。壁は消えず、累積から局所へ**移動**した（より tractable な形で）。

## 次の決定的問い（ユーザー案1の精密化）
**Inj(k) 自身は収縮するか、それとも既約な壁か？** 経験的には i.i.d.-ゼロ（control 一致）なので、問いは純粋に
「**局所新鮮さを証明する**」こと。これが局在化したマーラー core。枠組みの価値は、それを「累積測度の
equidistribution」から「**一ビットの局所新鮮さ**」へ縮めたこと——証明の標的が初めて per-scale・local になった。

## 会議の判断への対応
ユーザーの「(d) で器、(a) で燃料、step 2 が決める」は正しかった：
- (d) の器は**できた**（再帰＋ρ<1＋局在化）。
- step 2 の答え：**ρ<1 は存在する（良い兆候）が、十分でない**——壁は局所 Inj へ移っただけ。
- (a) の燃料注入は、foothold が逆端なので**そのままでは効かない**＝次に「低位 Inj を log₂3 で制御する新機構」
  を発明する必要（これが本当の新数学の核）。
honest verdict：**新数学の正しい第一歩。器は完成。だが完全証明に足りるかは、局所注入 Inj(k) を制御する
（まだ存在しない）機構次第——会議の直感どおり、defect の収縮機構の発明が鍵。**
