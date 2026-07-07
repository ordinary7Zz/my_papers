# `ThyroidXAgent` Results 写作模板（更准确的文献风格总结版）

## 文件定位

这份文档分成 **两层**：

- **第 1 层：文献风格总结**
  - 尽量只保留能从 3 篇参考文献 `Results` 中直接观察到的写法特征。
- **第 2 层：对 `ThyroidXAgent` 的应用建议**
  - 明确标注哪些内容是**基于文献风格做出的定制改稿方案**，而不是三篇论文的原样复刻。

这样做的目的，是避免把“参考文的真实共性”和“针对当前稿件的最佳改写路径”混在一起。

---

## 参考文献范围

本模板基于以下 3 篇文献的 `Results` 部分：

- `2509.20279v1.pdf`
- `25-NC-Thyroid-Explainable Metasis Analysis.pdf`
- `25-NC-RareThyroid Cancer.pdf`

---

## 一、先给总判断

如果严格从这 3 篇文献本身出发，它们并不是同一种 `Results` 写法，而是 3 种不同但可迁移的组织模式：

- **`LLNM-Net`**：更像**临床证据阶梯**
  - 数据描述 → 主性能 → 解释性/机制线索 → 更临床的风险分层 → 临床应用价值。
- **`Tiger Model`**：更像**模块验证 + 医生评估 + 下游任务 + 外部泛化**
  - 先证明中间模块本身成立，再证明它对诊断任务有帮助。
- **`TissueLab`**：更像**capability showcase / 任务模块展示**
  - 每个 subsection 围绕一个能力模块展开，强调 workflow、工具调用、任务完成率和与 baseline 的差异。

因此，更准确的表述不是“3 篇论文共同给出同一条固定链条”，而是：

**这 3 篇论文分别提供了 3 种可迁移的 `Results` 组织方式；它们在写法上有交集，但并不存在一个可以机械套用到所有论文上的统一模板。**

---

## 二、三篇参考论文各自的 `Results` 组织特征

## 1. `25-NC-Thyroid-Explainable Metasis Analysis.pdf`：临床证据阶梯最完整

### `Results` 的实际顺序

- `Data description`
- `Prediction performance of models and human experts`
- `Qualitative and quantitative analysis for predicting LLNM`
- `Predicting high-risk lymph node metastasis patients`
- `Application of LLNM-Net in clinical practice`

### 这篇文献最值得抓住的写法

- **先交代队列与任务场景**，让后面的结果有落点。
- **主性能是第一层证据**，而且紧跟 human experts / model baselines 对比。
- **解释性结果不是只展示图**，而是会压缩成一个可复述的临床观察。
- **结果会向更高层级的临床问题推进**，比如从是否转移，推进到高风险分层。
- **最后落回 clinical practice**，形成完整说服链。

### 代表性句式

> “Figure 3a shows that LLNM-Net exhibits significantly superior predictive performance...”

> “When the minimum distance is less than 0.25 cm, the average probability of LLNM occurrence exceeds 72%.”

> “The model is capable of predicting the stage of lateral lymph node metastasis.”

### 对它的准确概括

这篇文献最适合概括为：

**数据与任务背景明确、主性能先行、解释性要能转成临床观察、后段再走向更具体的临床决策与实践价值。**

---

## 2. `25-NC-RareThyroid Cancer.pdf`：先验证模块，再验证任务收益

### `Results` 的实际顺序

- `Overview of the Tiger Model`
- `Data collection and experimental design`
- `Quantitative analysis of image generation quality`
- `Doctor assessment of image generation quality`
- `Diagnoses for rare thyroid cancer subtype - downstream task`
- `External evaluation of the Tiger Model on public datasets`

### 这篇文献最值得抓住的写法

- **不是一上来就报下游分类结果**，而是先解释系统/模型在做什么。
- **中间模块先独立验证**，例如先验证生成图像质量，再去谈对诊断的帮助。
- **医生评估被单独作为证据层**，不混在主性能段里。
- **下游 rare subtype diagnosis 放在后面**，形成“模块有效 → 人看起来也合理 → 下游任务受益”的顺序。
- **最后做外部评估**，把泛化能力作为后段收束，而不是开头主卖点。

### 代表性句式

> “In Table 2, we utilize a comprehensive set of metrics to evaluate the performance of our generative network...”

> “We conducted three Turing test experiments with medical professionals...”

### 对它的准确概括

这篇文献最适合概括为：

**先证明方法中的中间机制可靠，再引入医生评估，最后说明它确实改善了下游任务并具备外部泛化。**

---

## 3. `2509.20279v1.pdf`：按能力模块组织的 `Results`

### `Results` 的实际顺序

- `2.1 Creating a co-evolving agentic AI system for medical imaging`
- `2.2 Co-evolving agentic AI accelerates expert-level assessment of tissue measurement`
- `2.3 TissueLab enables guideline-aligned diagnosis using an effectively infinite medical knowledge database`
- `2.4 TissueLab enables high-dimensional radiology image analysis`
- `2.5 TissueLab interactive ecosystem enables customized tool development`
- `2.6 TissueLab enables multi-modal integration of spatial omics and histology to improve accuracy in pathology analysis`

### 这篇文献最值得抓住的写法

- **一个 subsection 对应一个能力模块或一个任务场景**。
- **workflow 可以写进 `Results`**，而不是只能放在 `Methods`。
- **模型为什么强，会通过流程结构来解释**，不是只报数字。
- **baseline 不可靠时，会明确解释原因**，例如任务失败、输入限制、表面指标好但不具区分性。
- **human feedback / interactive loop** 可以作为结果的一部分呈现，而不是只能在系统设计里说。

### 代表性句式

> “We first evaluated TissueLab on predicting tumor invasion depth from whole-slide pathology images.”

> “As illustrated in Figure 2b, TissueLab agent (TLAgent) designs a structured workflow...”

> “As a result, the predicted invasion depths were strongly correlated with pathologist annotated ground truth...”

### 对它的准确概括

这篇文献最适合概括为：

**按能力模块拆解 `Results`，每节都让读者同时看到任务、workflow、关键指标和与 baseline 的结构性差异。**

---

## 三、真正可以跨文献归纳的共同规律

下面这些规律，有比较充分的跨文献支撑。

## 规则 1：小标题往往承担“证据推进”功能，而不只是内容清单

- `LLNM-Net` 的小标题本身就在推动证据层级：数据 → 性能 → 解释 → 风险分层 → 临床应用。
- `Tiger Model` 的小标题体现的是验证顺序：overview → 模块质量 → 医生评估 → downstream task → external evaluation。
- `TissueLab` 的小标题体现的是能力边界：每节只围绕一个能力模块展开。

**可迁移结论**：
`Results` 的小标题最好不仅说“写了什么内容”，还要反映“证据在往哪里推进”。

---

## 规则 2：段首常常先给 judgement，再给数字

这 3 篇文献虽然风格不同，但都经常采用 **conclusion-first** 的段首组织：

- 先说 `significantly superior predictive performance`
- 再说具体 `AUC`、`accuracy` 或其他指标
- 或先说某个能力成立，再给图和数字支撑

**可迁移结论**：
段落开头最好先告诉读者“这一段的主判断是什么”，而不是先平铺实验动作。

---

## 规则 3：headline claim 后面通常很快跟上图表锚点

这 3 篇文献里，强 claim 往往很快就会落到 `Fig.`、`Table` 或 `Supplementary` 上，而不是把图表引用拖到很后面。

**可迁移结论**：
强结论出现后，应尽快给出支撑它的图表位置，避免读者需要回头找证据。

---

## 规则 4：强 claim 通常带比较对象或操作性意义

这 3 篇文献都不太满足于只写：

- `performed well`
- `showed robust performance`
- `was useful`

更常见的是：

- **相对 baseline / human experts 更强**
- **能完成 baseline 常失败的任务**
- **能推进到更高层级的临床判断**
- **能进入可操作的工作流或医生反馈环**

**可迁移结论**：
强结果最好不仅有数字，还要有比较对象、失败对照或实际意义。

---

## 规则 5：解释性结果最好压缩成“可复述的发现”

这一点在 `LLNM-Net` 最典型：解释性分析并不止于“给一张热图”，而是会提炼成一句能被临床读者复述的规律。

**可迁移结论**：
如果写 SHAP、attention、attribution 或 case analysis，尽量把它变成：

- 哪类特征主导判断
- 哪个任务依赖哪些特征
- 有什么 clinically meaningful observation

而不是只写“见图”。

---

## 规则 6：clinical / practical value 往往出现在后段收束

三篇论文都不是一开始就把“临床价值”当主句，而是通常在：

- 核心能力已经被证明之后
- 或中间模块已经被验证之后
- 再去谈 clinical practice、doctor assessment、human feedback、workflow benefit

**可迁移结论**：
临床或应用价值通常更适合作为后段证据，而不是在最前面替代核心结果。

---

## 四、不宜过度概括为“三篇共同规律”的几点

下面这些说法，在原模板里比较强，但如果严格按文献本身来讲，应该弱化或改写。

## 1. 不能把三篇论文都概括成同一条固定链条

原先那种：

**数据/任务背景 → 核心性能 → 解释性/机制线索 → 扩展任务/泛化 → 新指标验证 → 临床工作流价值**

更适合看作一种**改稿时的理想证据顺序**，而不是 3 篇论文共同共享的原始结构。

更准确的说法是：

- `LLNM-Net` 更接近线性临床证据链
- `Tiger Model` 更接近模块验证链
- `TissueLab` 更接近能力模块展示链

---

## 2. “一段只做一个 job”是很好的编辑原则，但不是三篇论文的严格共同事实

这个原则对改稿非常有帮助，但它更像**写作优化建议**，而不是三篇参考文全都严格遵守的真实规律。

更准确的表述应是：

**高质量 `Results` 往往会让每段的主功能比较清楚，但并不意味着每段都绝对只承担一种功能。**

---

## 3. “新 metric 必须独立成块”不是三篇共同特征，而是面向 `ThyClinScore` 的定制建议

`Tiger Model` 确实体现了“先证明模块，再证明下游收益”的思路；
但三篇文献并没有共同展示一个“新 report metric 独立验证”的固定结构。

更准确的表述应是：

**如果你的稿件中存在一个需要单独建立合理性的指标，例如 `ThyClinScore`，那么把它独立成节会更清楚；但这是一项针对当前稿件的写作决策，不是三篇参考文共同复现的结构。**

---

## 4. “6 个 subsection 最像两篇 NC 文”这个说法应改成“基于参考文风格的实用改稿方案”

原模板里的 6-subsection 结构是**实用且合理的**，但更准确的定位应是：

**这是综合 3 篇参考文的风格后，为 `ThyroidXAgent` 量身定制的一种推荐写法，而不是参考文原样结构的直接翻版。**

---

## 五、基于上述文献风格，对 `ThyroidXAgent` 的应用建议

这一节开始，不再是“文献本身如何写”，而是“基于这些风格，`ThyroidXAgent` 最适合怎么写”。

## 推荐结构（应用建议，不是文献原样）

```text
\section{Results}

\subsection{Cross-dataset segmentation and benign--malignant classification}
\subsection{Interpretable predictions and clinician-interactive review}
\subsection{Generalization to clinically consequential malignant-lesion tasks}
\subsection{Evidence-grounded report generation from thyroid ultrasound}
\subsection{Clinical semantic validation of ThyClinScore}
\subsection{AI-assisted reporting improves efficiency while preserving clinical utility}
```

### 为什么这个结构对 `ThyroidXAgent` 合理

- **前 3 节** 更接近 `LLNM-Net` 的临床证据推进逻辑
  - 核心性能
  - 解释性与可审阅性
  - 更临床相关的恶性任务泛化
- **后 3 节** 借用了 `Tiger Model` 的“模块先成立，再验证中间证据，再落到实际工作流”的思路
  - report generation 本身是否成立
  - `ThyClinScore` 是否值得相信
  - AI-assisted reporting 是否带来真实工作流收益
- **workflow 写进 `Results`** 的合法性，则可从 `TissueLab` 得到支持

### 这套结构的准确定位

这套结构应表述为：

**一种综合三篇参考文风格后形成的 `ThyroidXAgent` 专用改稿骨架。**

而不是：

**三篇参考文共同展示出的标准答案。**

---

## 六、对 `ThyroidXAgent` 最值得迁移的 6 条写作规则

## 1. 小标题要体现证据推进，而不是只列内容

比起：

- `Segmentation, classification performance and interpretability`
- `Report generation`

更好的写法是把不同层级的证据拆开，让标题本身有推进感。

---

## 2. subsection 开头先交代这一节要回答的问题

可直接复用的起句包括：

- `We first evaluated whether ...`
- `We next asked whether ...`
- `We then examined whether ...`
- `To interpret these predictions, we next examined ...`
- `To assess ..., we evaluated ...`

---

## 3. 第一段先报 headline finding，再给图和数字

尽量避免先堆实验动作、最后才给判断。

更稳的方式是：

- 先说 `ThyroidXAgent achieved ...`
- 紧接着给 `Fig.` / `Table`
- 再展开指标与比较对象

---

## 4. 解释性段落要回答“模型到底看到了什么”

不要只写：

- `SHAP analysis is shown in Fig. X`

更好的写法是：

- 哪些特征主导
- representative cases 是否与这些特征一致
- 这些解释信号能否进入 review / correction workflow

---

## 5. workflow 可以写进 `Results`，但必须服务于结果解释

`TissueLab` 提供了重要启发：workflow 不是不能写进 `Results`，关键在于它必须解释为什么结果成立。

因此对 `ThyroidXAgent` 来说：

- interactive review workflow
- report-generation workflow
- reader-study workflow

都可以写进 `Results`，但要避免只做流程描述而没有对应结果判断。

---

## 6. 每节结尾最好有一句 roll-up sentence

常用句型包括：

- `Together, these results establish ...`
- `Overall, these findings indicate that ...`
- `Collectively, these analyses support ...`
- `These results position ThyroidXAgent as ...`

其作用是：

- 收束本节主判断
- 防止段落停在数字上
- 让 6 个 subsection 更像一条完整证据链

---

## 七、`ThyroidXAgent` 的最小可复用骨架

如果你接下来要按这份模板改稿，最稳的骨架可以是：

```text
\section{Results}

\subsection{Cross-dataset segmentation and benign--malignant classification}
[核心任务重要性 + cross-dataset headline performance]
[baseline / physician comparison + short roll-up]

\subsection{Interpretable predictions and clinician-interactive review}
[cohort-level SHAP + representative cases]
[interactive review workflow + corrective annotation + efficiency / auditability]

\subsection{Generalization to clinically consequential malignant-lesion tasks}
[malignant-lesion tasks headline results + baseline comparison]
[task-specific signatures / interpretation]

\subsection{Evidence-grounded report generation from thyroid ultrasound}
[workflow + structured evidence design]
[NLG metrics / report-generation headline performance]

\subsection{Clinical semantic validation of ThyClinScore}
[ThyClinScore headline result]
[submetrics and failure modes]
[correlation / external validation of metric meaning]

\subsection{AI-assisted reporting improves efficiency while preserving clinical utility}
[reader-study design + time reduction]
[physician-stratified benefit + representative cases + closing sentence]
```

---

## 八、建议保留、但要明确属于“应用建议”的内容

下面这些内容仍然建议保留，因为对 `ThyroidXAgent` 很有用；只是它们应该被明确标为**应用层建议**，而不是“文献共性事实”：

- **把当前两个过宽的 subsection 拆成 6 个 subsection**
- **把 `ThyClinScore` 单独成节**
- **把解释性与 interactive review 放在同一节**
- **把 report generation 主性能与 reader study 分开**
- **把 `Results` 写成两大块**
  - 核心影像任务
  - 报告生成与临床工作流

这些建议之所以合理，不是因为三篇文献都“原样这样写”，而是因为它们分别提供了：

- 证据推进方式
- 模块验证顺序
- workflow 写入 `Results` 的写法合法性

---

## 九、最短结论版心法

如果只保留最重要的判断，可以记住下面 5 句：

1. **三篇文献不是一个模板，而是三种可迁移的 `Results` 组织模式。**
2. **真正稳定的共性，是结论先行、图表紧跟、比较对象明确、解释性要能转成可复述发现。**
3. **`LLNM-Net` 最像临床证据阶梯，`Tiger Model` 最像模块验证链，`TissueLab` 最像能力模块展示。**
4. **`ThyroidXAgent` 的 6-subsection 结构是合理的应用方案，但不是参考文原样复刻。**
5. **写 `Results` 时，应先区分“文献真实共性”和“面向自己稿件的最佳改稿策略”。**

---

## 十、你接下来如何使用这份模板

建议按以下顺序使用：

1. **先按第五节确定结构**
   - 先拆 subsection，不先改数字。
2. **再按第六节统一段落写法**
   - 先把每一节的主判断写清楚。
3. **最后再做语言层面的 NC 化**
   - 压缩重复表达
   - 统一 `show / indicate / demonstrate / suggest` 的证据强度
   - 让 figure call 更及时

如果后续继续改 `ThyroidXAgent.md`，这份文档应优先被当作：

**“文献风格校准器 + 应用层骨架说明书”**，而不是“可以无差别机械套用的唯一模板”。
