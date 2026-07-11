# Sub3 评价：skill 合规性 + TissueLab 风格对比

> 评价对象：`\subsection{Segmentation, classification and radiomics}`
> 评价日期：2026-07-11
> 评价依据：nature-writing skill（method.md / workflow.md / en.md / nature.md）+ TissueLab 论文 Methods 风格（2509.20279v1, 1475–1597 行）

---

## 一、当前 sub3 结构概览

| 段 | 行 | 主题 | 句数 | 设计含义句 |
|---|---|------|------|-----------|
| P1 | 207 | 专家池设计（动机→变异维度→含义） | 5 | ✅ "This heterogeneity exposes..." |
| P2 | 209–217 | 分割+分类分支（motivation→架构→loss→产出） | 6 + 2 公式 | 隐含（产出定义收束，过渡到 P3） |
| P3 | 219 | 质量评估+router+ensemble（评估→选择→含义） | 4 | ✅ "This routing design allows..." |
| P4 | 221 | radiomics+解释+复用（motivation→提取→解释→复用→含义） | 9 | ✅ "This reuse allows..." |

---

## 二、Skill 合规性检查

### 2.1 三要素模式（method.md 核心要求）

每个模块应回答：Motivation（解决什么问题）→ Mechanism（具体做什么）→ Evidence/role（在整体中的贡献）。

| 模块 | Motivation | Mechanism | Evidence/role | 状态 |
|------|-----------|-----------|--------------|------|
| 专家池 (P1) | ✅ "To reduce sensitivity to dataset bias" | ✅ DINOv3, 三维度变异, dilation | ✅ "so that the router can select..." | 完整 |
| 分割分支 (P2) | ✅ "to preserve fine boundary detail" + "balances pixel-level...with region-level" | ✅ U-Net + loss 公式 | ⚠️ 隐含（$m^*$ 被 P4 复用） | 基本完整 |
| 分类分支 (P2) | ✅ "To mitigate class imbalance" | ✅ pooling + GLA 公式 | ⚠️ 隐含（$p_i$, $c_i$ 被 P3 router 使用） | 基本完整 |
| Router (P3) | ✅ "rather than by simple confidence maximization" | ✅ 质量评估 + LLM 推理 + ensemble | ✅ "This routing design allows..." | 完整 |
| Radiomics (P4) | ✅ "To provide a classification signal independent of..." | ✅ 连通域 + PyRadiomics + AutoGluon | ✅ "complementary interpretive signal" | 完整 |
| 解释模块 (P4) | ✅ "To explain the predictions" | ✅ SHAP + Grad-CAM | ✅ "complementary attribution modalities" | 完整 |
| 跨任务复用 (P4) | ✅ "Importantly, the same...is reused" | ✅ "only task-specific...are changed" | ✅ "This reuse allows..." | 完整 |

**结论**：7 个模块中 5 个完全满足三要素，2 个（seg/cls）的 evidence/role 为隐含。Methods 中不强制写 ablation hook，隐含通过文本流体现是可以接受的。

### 2.2 段落流检查（workflow step 7）

| 段 | 主题 | 首句是否为 topic/claim | 后续句是否有显式关系 | 评估 |
|---|------|----------------------|---------------------|------|
| P1 | 专家池设计 | ✅ "To reduce sensitivity...is designed as..." | ✅ elaboration → restriction → implication | 通过 |
| P2 | 分割+分类分支 | ✅ "Within the expert pool, the segmentation branch uses..." | ✅ seg → cls（并列）→ per-expert outputs（过渡） | 通过 |
| P3 | Router 选择 | ✅ "Before routing, task-specific quality metrics..." | ✅ metrics → selection → fallback → implication | 通过 |
| P4 | Radiomics+解释+复用 | ✅ "To provide a classification signal...the radiomics branch processes..." | ✅ motivation → refinement → extraction → classification → explanation → reuse → implication | 通过 |

### 2.3 语言规则（en.md）

| 规则 | 状态 | 说明 |
|------|------|------|
| 句长 10–30 词 | ⚠️ | P3 第 1 句 ~40 词（质量评估句），P3 第 2 句 ~35 词。其余在范围内 |
| 每句一个命题 | ✅ | 长句均为列表结构，仍是单一命题 |
| 避免介词堆叠 | ✅ | |
| 避免 em dash | ⚠️ | P3、P4 使用 `---`。但全文（Introduction、Results）均使用 em dash，属于论文级一致性 issue |
| 动词校准 | ✅ | `is designed`, `uses`, `selects`, `may instead select` — 适当 |
| 无营销动词 | ✅ | 无 `leverages`/`enables`/`empowers` |
| 无全称断言 | ✅ | 无 `always`/`never`/`comprehensive` |

### 2.4 禁止模糊短语（method.md）

无 `under standard conditions`、`using routine methods`、`the method was validated` 等。✅

---

## 三、TissueLab Methods 风格对比

以 TissueLab 的 "Tissue segmentation and classification" 子节（1575–1597 行）和 "Adaptive and extensible agentic system" 子节（1477–1489 行）为参照：

| 维度 | TissueLab | 当前 sub3 | 一致性 |
|------|-----------|-----------|--------|
| **问题先行开场** | "In pathology, there is currently no single universal model..." | "To reduce sensitivity to dataset bias..." | ✅ |
| **"To address/reduce..." 转折** | "To address this limitation, TissueLab adopts..." | "To reduce sensitivity..., the image expert pool is designed as..." | ✅ |
| **每段末设计含义句** | "This design ensures that..." / "This abstraction ensures..." | P1: "This heterogeneity exposes..." ✅; P3: "This routing design allows..." ✅; P4: "This reuse allows..." ✅; P2: 无（以定义收束，过渡到 P3） | ✅ 可接受 |
| **段间显式过渡** | "In contrast to...", "Building on this...", "Importantly,..." | "Within the expert pool," ✅; "Before routing," ✅; "To provide..." ✅; "Importantly,..." ✅ | ✅ |
| **公式 + where 从句** | "Mathematically, let $\mathcal{M}_t$ denote..." / "Formally, let..." | seg loss + GLA 两个 display formula，均带 where 从句 | ✅ |
| **工具引用 + 功能定位** | 每工具一句 + 引用号 | PyRadiomics, AutoGluon, SHAP, Grad-CAM 均有 | ✅ |
| **每段主题数** | 1–2 | P2: 2（seg+cls）; P4: 3（radiomics+解释+复用）| ⚠️ P4 略密 |
| **句长** | 15–30 词为主 | P3 有 2 句超 30 词 | ⚠️ 略长 |
| **段落数（同等内容量）** | 5 段 | 4 段 | ✅ 可比 |
| **模块黑箱化** | "internal implementation remains a black box" | 工具以引用+功能描述提及，不展开内部 | ✅ |

---

## 四、总体判断

### 与 skill 要求的符合度：高

- 三要素模式基本满足（5/7 完整，2/7 隐含）
- 段落流清晰（4 段均通过 paragraph-flow check）
- 无禁止用语
- 语言规则基本遵守（2 句偏长，em dash 为论文级 issue）

### 与 TissueLab 风格的相似度：高

- 问题先行、设计含义回扣、公式+where、工具引用、段间过渡等核心风格特征均已对齐
- 段落数和主题密度可比

### 剩余可优化项（均为低优先级）

1. **P3 质量评估句偏长（~40 词）**：可将 `---morphological plausibility...for classification---` 拆为独立句。但这会增加总句数，需权衡。
2. **P1 "progressively broader data distributions"**：分辨率和预训练改变的是模型容量/特征空间，不是"更广的分布"。可改为 "complementary generalization profiles"（与同段前文一致）。
3. **P4 三个主题**：radiomics + 解释 + 复用。TissueLab 同等内容会拆成 2 段。但三者耦合紧密（解释依赖 radiomics，复用依赖两者），合并是合理的。
4. **Em dash**：论文级 issue，不建议在 sub3 单独修改。

### 结论

当前 sub3 已达到可投稿质量。剩余项为打磨级别，不影响审稿人对方法的理解和复现。
