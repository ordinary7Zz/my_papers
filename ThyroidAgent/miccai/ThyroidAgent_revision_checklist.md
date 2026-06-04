# ThyroidAgent 论文修改清单

本文档根据 `ThyroidAgentReviews.md` 中三位 reviewer 的意见，结合当前 `ThyroidAgent.md` 的内容整理而成，用于后续 rebuttal 与改稿。

## 一、必须优先修改

### 1. 明确界定 agent 的方法定义
**核心问题：** 当前论文对 agent、LLM、PPO 三者的角色定义不清，导致方法主线模糊。

**需要修改的位置：**
- `ThyroidAgent.md:117-119`
- `ThyroidAgent.md:141-147`
- `ThyroidAgent.md:190-194`
- `ThyroidAgent.md:217-224`
- `ThyroidAgent.md:204-212`

**需要修改的内容：**
- 明确区分：
  - **LLM-based agent**：负责 segmentation/classification expert 的选择或聚合。
  - **PPO-based RL module**：如果只用于 CCA 超参数优化，需要与主 agent 明确分开。
- 说明整个系统中“agent”到底指什么，避免 reviewer 理解为整个 ThyroidAgent 都由 PPO 训练。
- 正式定义：
  - state / input
  - action / output
  - evidence 的构成
  - selection 与 aggregation 的区别
  - JSON decision 的字段
- 说明 metadata 缺失时如何处理。

**建议：**
- 在 Method 中新增专门小节，例如：
  - `Formal Definition of the Agent Policy`
  - `Distinction Between LLM Routing and PPO-based CCA Optimization`

---

### 2. 补全公式和符号定义
**核心问题：** 方程中的变量定义不完整，影响可复现性和可读性。

**需要修改的位置：**
- `ThyroidAgent.md:157-166`（Eq. 1）
- `ThyroidAgent.md:181-188`（Eq. 2）

**需要修改的内容：**
- 对 Eq. (1) 明确定义：
  - `y`
  - `y_b`
  - `z_b`
  - `p_pos`
  - `p_neg`
  - `tau`
  - `AvgPool31`
- 不仅说明这些量用于 `L_seg` 和 `GLA loss`，还应给出完整损失定义，或在正文/附录中明确公式。
- 对 Eq. (2) 明确定义：
  - `N_g`
  - `P(i,j)`
  - `I[·]`
  - ROI mask 与灰度离散化方式

---

### 3. 把 Fig. 2 对应的 pipeline 讲清楚
**核心问题：** pipeline 组件多，但正文对每个组件角色和输入输出说明不足。

**需要修改的位置：**
- `ThyroidAgent.md:139-147`
- `ThyroidAgent.md:217-224`

**需要修改的内容：**
- 按顺序解释整条流程：
  1. offline expert training
  2. metadata registry 构建
  3. segmentation expert candidate generation
  4. segmentation evidence construction
  5. expert selection / aggregation
  6. radiomics extraction
  7. classification evidence construction
  8. final classification decision
- 明确 `SegEvidence` 与 `ClsEvidence` 分别包含哪些信号：
  - confidence
  - disagreement
  - radiomics
  - metadata
  - device/source information
- 每个模块写清楚输入与输出，而不是只保留模块名称。

---

### 4. 增强消融实验，证明 agent 的必要性
**核心问题：** 当前 Table 3 只能说明系统整体更好，不能说明 agent 为什么必要。

**当前相关位置：**
- `ThyroidAgent.md:303-320`

**需要补充的实验：**
1. **LLM routing vs heuristic**
   - max confidence
   - majority vote
   - rule-based selection
2. **有无 radiomics**
   - image only
   - mask + handcrafted radiomics
   - raw mask feature vs radiomics feature
3. **有无 metadata**
   - image only
   - image + metadata
4. **expert 数量的影响**
   - 1 / 3 / 6 / 12 experts
5. **有无 RL-CCA**
6. **selection accuracy**
   - agent 有多大比例选中了正确或最优专家

---

### 5. 重新说明 baseline fairness
**核心问题：** 当前 baseline 对比容易被认为不够公平，尤其是 foundation model 和 VLM 的使用方式。

**需要修改的位置：**
- `ThyroidAgent.md:266-300`

**需要修改的内容：**
- 说明 segmentation baselines 是否：
  - fine-tune
  - 使用统一训练协议
  - 采用官方推荐设置
- 明确 VLM baselines 是 prompt-only 还是 fine-tuned。
- 如果是 prompt inference，需要在文中明确写为：
  - `zero-shot/prompted VLM baselines`
- 解释为什么这种比较仍然具有参考意义。
- 说明为什么不直接用 pretrained foundation models 构建 expert pool，或将其作为 future work。

---

### 6. 增加 segmentation error propagation 分析
**核心问题：** radiomics 依赖 segmentation mask，但当前没有系统分析 segmentation 误差如何影响 classification。

**需要修改的位置：**
- `ThyroidAgent.md:178-188`
- `ThyroidAgent.md:324-345`

**需要补充的内容：**
- 分析 segmentation 质量下降时 classification 性能如何变化。
- 增加 mask perturbation / noise sensitivity 实验，例如：
  - erosion / dilation
  - boundary perturbation
  - random hole / contour shift
- 分析 radiomics 对 mask 误差的敏感性。

---

### 7. 补充临床相关指标
**核心问题：** 仅报告 AUROC 和 AUPRC 不足以支持临床可用性。

**需要修改的位置：**
- `ThyroidAgent.md:269-300`

**建议补充指标：**
- sensitivity
- specificity
- accuracy
- F1
- precision / recall（可选）
- operating point / threshold 的设定方式

---

### 8. 增加 cost / latency / stability 分析
**核心问题：** 当前论文缺少系统复杂度、推理开销和稳定性报告。

**需要修改的位置：**
- `ThyroidAgent.md:217-224`
- `ThyroidAgent.md:260-261`
- `ThyroidAgent.md:343-345`

**需要补充的内容：**
- inference latency
- 每张图运行多少个 expert
- LLM token / API cost 或近似计算成本
- 训练 12 个 experts 的成本
- 不同随机种子或不同 decoding 设置下的性能方差

---

## 二、建议补强

### 9. 调整创新点表述，弱化 radiomics 本身的新颖性
**核心问题：** radiomics 本身不是新的方法，不应作为主要创新点单独突出。

**需要修改的位置：**
- `ThyroidAgent.md:121-128`

**建议修改方向：**
- 将创新点从“提出 radiomics”改为“将 radiomics 作为结构化 evidence 纳入 agent routing / aggregation”。
- 强调真正创新在于：
  - dynamic expert orchestration
  - segmentation-derived structured evidence
  - explainable evidence aggregation

---

### 10. 增补 related work，并明确差异
**核心问题：** reviewer 认为相关工作覆盖不足，尤其是动态 expert routing 和联合 segmentation-classification 方向。

**需要修改的位置：**
- `ThyroidAgent.md:95-112`

**需要补充的内容：**
- dynamic expert routing / mixture-of-experts / VLM in ultrasound 的相关工作
- thyroid segmentation + classification 联合建模工作
- 明确本文与这些工作的差异和新增价值

---

### 11. 补充 reproducibility 细节
**核心问题：** 三位 reviewer 都认为当前可复现信息不足。

**需要修改的位置：**
- `ThyroidAgent.md:257-261`

**需要补充的内容：**
- 每个数据集的样本数、类别比例、标签来源
- stacked datasets 的构造方式
- 12 experts 的形成方式和彼此差异
- prompt template
- LLM model/version
- decoding 参数（temperature、top-p、max tokens 等）
- metadata 字段清单
- CCA 参数空间
- PPO 配置
- 随机种子设置

---

### 12. 统一命名，避免品牌不一致
**核心问题：** 系统、模块和实验名不统一，影响论文专业感。

**需要修改的位置：**
- `ThyroidAgent.md:248`
- `ThyroidAgent.md:291`

**需要修改的内容：**
- 统一以下命名：
  - `ThyroidAgent`
  - `ThyAgent-Seg`
  - `ThyAgent-Cls`
- 建议使用统一规则，例如：
  - system: `ThyroidAgent`
  - module: `ThyroidAgent-Seg`, `ThyroidAgent-Cls`

---

### 13. 修正文中的图表引用和排版细节
**核心问题：** 图表引用格式和排版存在细节问题，影响 reviewer 阅读体验。

**需要修改的位置：**
- `ThyroidAgent.md:343-345`
- `ThyroidAgent.md:360`
- 以及全文所有 `Fig.~\ref{...}.(a)` 的写法

**需要修改的内容：**
- 将 `Fig.~\ref{fig:system_analysis}.(a)` 改为 `Fig.~\ref{fig:system_analysis}(a)`
- 在正文中显式引用 Table 1 和 Table 2
- 修正 typo，例如 reviewer 提到的 `Generalizatior`
- 统一 subfigure notation 和 figure reference 风格

---

### 14. 增加 limitations 段落
**核心问题：** 当前论文没有主动交代系统边界和未完成问题。

**建议补充内容：**
- 尚未进行 radiologist-in-the-loop study
- 尚未进行 prospective validation
- foundation model expert pool 尚未探索
- 训练和推理成本仍需进一步优化

---

## 三、建议的修改优先级

### 第一优先级
1. 重新定义 agent / LLM / PPO 的角色
2. 补全公式和符号定义
3. 重写 pipeline 叙述
4. 扩展 Table 3 的机制消融
5. 重新说明 baseline fairness

### 第二优先级
6. segmentation → classification error propagation 分析
7. 临床相关指标
8. latency / cost / stability 分析

### 第三优先级
9. 补 related work
10. 补 reproducibility 细节
11. 统一命名、修正图表引用和 typo
12. 增加 limitations 段落

---

## 四、总评
当前论文最需要修改的不是继续堆叠结果，而是：
- 把核心方法讲严谨
- 用消融证明 agent 的必要性
- 补齐公平性、成本和临床可用性分析
- 修复公式、命名和写作层面的可复现性问题

这些修改点是三位 reviewer 意见中的高度共识部分，应优先处理。