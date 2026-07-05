# `ThyroidXAgent` Results 写作模板（按 3 篇参考论文风格提炼）

## 文件目的

这不是泛泛的“写作建议”，而是一份**可直接拿来改稿**的 `Results` 模板。

它整合了 3 篇参考论文的共同套路：

- `2509.20279v1.pdf`：**系统展示型 / capability showcase**
- `25-NC-Thyroid-Explainable Metasis Analysis.pdf`：**临床转化型 / Nature Communications 标准链条**
- `25-NC-RareThyroid Cancer.pdf`：**方法验证型 / evidence ladder**

这份模板的目标是：

1. 把 `ThyroidXAgent` 当前偏拥挤的 `Results`，拆成**更像 NC 风格**的证据阶梯。
2. 让每个 subsection 只承担**一个主要 job**。
3. 给出**可直接替换的英文句型模板**。
4. 在合适的地方放入**参考原文示例**，帮助你把语气和节奏拉到更接近目标风格。

---

## 一句话总原则

把 `Results` 从“把所有强结果都塞进两个 subsection”改成：

**数据/任务背景 → 核心性能 → 解释性/机制线索 → 扩展任务/泛化 → 新指标验证 → 临床工作流价值**

也就是说，`Results` 不是结果堆叠，而是**说服顺序**。

---

## 一、先给 `ThyroidXAgent` 的推荐 Results 新目录

## 推荐版本（最建议，6 个 subsection）

```text
\section{Results}

\subsection{Cross-dataset segmentation and benign--malignant classification}
\subsection{Interpretable predictions and clinician-interactive review}
\subsection{Generalization to clinically consequential malignant-lesion tasks}
\subsection{Evidence-grounded report generation from thyroid ultrasound}
\subsection{Clinical semantic validation of ThyClinScore}
\subsection{AI-assisted reporting improves efficiency while preserving clinical utility}
```

这是最接近你当前材料强项、也最像两篇 `Nature Communications` 参考文的写法。

### 为什么要这样拆

因为你当前版本有两个核心问题：

- **第一个 subsection 太挤**：分割、分类、解释性、交互式 review、恶性病灶任务泛化都塞在一起。
- **第二个 subsection 太满**：报告生成流程、文本指标、临床语义指标、指标有效性验证、reader study 都塞在一起。

拆开后，每个 subsection 的功能就会更清楚：

- **Subsection 1**：证明模型在核心影像任务上真的强
- **Subsection 2**：证明模型不是黑箱，而且能进入 clinician-in-the-loop workflow
- **Subsection 3**：证明不是只会做良恶性二分类，还能外延到更临床相关的恶性任务
- **Subsection 4**：证明 agent 能把结构化证据转成报告
- **Subsection 5**：证明 `ThyClinScore` 不是随便造的 metric，而是值得相信的 metric
- **Subsection 6**：证明系统在真实工作流里有时间收益和临床实用性

---

## 二、三篇参考论文里最值得迁移的 `Results` 套路

## 1. 参考论文 A：`2509.20279v1.pdf` 的可迁移套路

### 核心特征

- 按**能力模块**拆 subsection，而不是把所有实验混写。
- 每个 subsection 都遵循：
  - 任务为什么重要
  - 这个任务怎么设置
  - agent / workflow 做了什么
  - 关键数字结果
  - 与 baseline 或人工对比
  - 必要时解释为什么 baseline 看起来还行但其实不可靠

### 可直接借鉴的原文示例

> “We first evaluated TissueLab on predicting tumor invasion depth from whole-slide pathology images.”

> “As illustrated in Figure 2b, TissueLab agent (TLAgent) designs a structured workflow…”

> “As a result, the predicted invasion depths were strongly correlated with pathologist annotated ground truth…”

### 你该学什么

- `We first evaluated...` 这类句子特别适合用作 subsection 开头
- `As illustrated in Figure X...` 很适合在结果里快速交代 workflow，而不是让 workflow 悬空
- `As a result...` 适合在给数字前做结果起句

---

## 2. 参考论文 B：`LLNM-Net` 的可迁移套路

### Results 小标题顺序

- `Data description`
- `Prediction performance of models and human experts`
- `Qualitative and quantitative analysis for predicting LLNM`
- `Predicting high-risk lymph node metastasis patients`
- `Application of LLNM-Net in clinical practice`

### 这个顺序为什么好

因为它是非常稳的临床 AI 说服链：

1. 先交代数据
2. 再证明模型准
3. 再解释模型为什么这样判
4. 再把任务往更细粒度临床决策推进
5. 最后落到真实 clinical workflow

### 可直接借鉴的原文示例

> “Figure 3a shows that LLNM-Net exhibits significantly superior predictive performance…”

> “When the minimum distance is less than 0.25 cm, the average probability of LLNM occurrence exceeds 72%.”

> “The model is capable of predicting the stage of lateral lymph node metastasis.”

### 你该学什么

- **小标题本身就是证据阶梯**
- 结果段先报**headline finding**，再给图和数字
- 解释性分析不是单独炫图，而是要给出一个**可复述的 clinically relevant observation**

---

## 3. 参考论文 C：`Tiger Model` 的可迁移套路

### Results 小标题顺序

- `Overview of the Tiger Model`
- `Data collection and experimental design`
- `Quantitative analysis of image generation quality`
- `Doctor assessment of image generation quality`
- `Diagnoses for rare thyroid cancer subtype - downstream task`
- `External evaluation of the Tiger Model on public datasets`

### 这个顺序为什么好

它特别适合你的第二个大块，也就是 `report generation + ThyClinScore + reader study` 这一组内容。

它的套路是：

1. 先说明系统/方法在干什么
2. 再证明中间环节本身成立
3. 再做人工评估
4. 最后才说“对下游任务真的有帮助”

### 可直接借鉴的原文示例

> “In Table 2, we utilize a comprehensive set of metrics to evaluate the performance of our generative network…”

> “We conducted three Turing test experiments with medical professionals…”

### 你该学什么

- **新指标或新模块不要和主任务性能写在同一段里**
- 先证明“这个中间机制本身有效”，再证明“它提升了最终任务”
- 人工评估单独成段，甚至单独成 subsection，会更像高水平论文

---

## 三、把这三篇套路压缩成一套 `ThyroidXAgent` 专用骨架

## `ThyroidXAgent` 的建议总结构

### Block A：核心影像任务

- `Cross-dataset segmentation and benign--malignant classification`
- `Interpretable predictions and clinician-interactive review`
- `Generalization to clinically consequential malignant-lesion tasks`

### Block B：报告生成与临床工作流

- `Evidence-grounded report generation from thyroid ultrasound`
- `Clinical semantic validation of ThyClinScore`
- `AI-assisted reporting improves efficiency while preserving clinical utility`

这个拆法有两个好处：

- 更像 `LLNM-Net`：从核心性能一路走到 clinical use
- 也更像 `Tiger Model`：把“report metric validity”单独拉出来做中间证据验证

---

## 四、逐 subsection 模板：每节该写什么

下面这部分是本文件最重要的内容。

每个 subsection 我都给你：

- **该节的 job**
- **推荐段落数**
- **每段该放什么**
- **英文模板句**
- **和你现有内容的映射关系**

---

## Subsection 1
## `Cross-dataset segmentation and benign--malignant classification`

### 这一节的 job

只做一件事：

**证明 ThyroidXAgent 在核心影像任务上跨数据集表现强，而且这种强不是单一数据集偶然现象。**

### 不要在这一节里做的事

- 不要展开 SHAP 解释性
- 不要展开 clinician-in-the-loop time saving
- 不要展开恶性病灶泛化
- 不要展开 report generation

### 推荐段落数

**2 段** 或 **3 段**。

### 段落功能分配

- **P1**：任务重要性 + 跨数据集 headline performance
- **P2**：与 baseline / physician comparison 的关键对照
- **P3（可选）**：一句短的 roll-up，收束成“robust base capability”

### 英文模板

#### P1 模板

```text
Accurate lesion delineation and reliable benign--malignant classification are central to thyroid ultrasound decision-making, yet both remain challenging across heterogeneous datasets with different lesion geometry and class balance. Across [N] segmentation datasets, ThyroidXAgent achieved a mean Dice of [X] and a mean HD95 of [Y], compared with [baseline values] for [baseline] (Fig. Xa and Supplementary Table X). Across the [N] datasets supporting benign--malignant classification, ThyroidXAgent achieved a mean AUROC of [X] and a mean AUPRC of [Y], exceeding [baseline/model] ([X], [Y]) (Fig. Xb--d and Supplementary Table X).
```

#### P2 模板

```text
This advantage was also preserved under direct reader-level comparison. On a blinded [N]-image physician comparison set, ThyroidXAgent achieved an AUROC of [X] and an AUPRC of [Y], outperforming [comparison group] (Fig. Xf,g). Together, these results establish ThyroidXAgent as a robust cross-dataset foundation for thyroid nodule delineation and malignancy discrimination.
```

### 可借鉴的句法节奏

- 开头先说重要性：`Accurate X and reliable Y are central to ...`
- 第二句立刻给总体性能：`Across [N] datasets...`
- 然后给对照：`compared with...`, `exceeding...`
- 收束句不要过长：`Together, these results establish...`

### 你现有内容如何迁移

你当前 `Results` 第一个 subsection 的第一段基本已经是这个 subsection 的主体。

可以直接保留大部分数字，只需要：

- 去掉后面 SHAP 和 malignant tasks 的内容
- 把这一节的标题从宽泛标题改成更聚焦的标题
- 增强最后一句的 roll-up 功能

---

## Subsection 2
## `Interpretable predictions and clinician-interactive review`

### 这一节的 job

只做一件事：

**证明 ThyroidXAgent 的预测不是黑箱，并且这种解释性可以进入可审阅、可纠正的人机交互流程。**

### 推荐段落数

**2 段**。

### 段落功能分配

- **P1**：cohort-level SHAP + representative cases，说明模型关注什么
- **P2**：interactive review + corrective annotation + time saving

### 英文模板

#### P1 模板

```text
To interpret these predictions, we next examined cohort-level SHAP profiles together with representative benign and malignant cases. Morphology-related descriptors, particularly [feature 1] and [feature 2], contributed most strongly to benign--malignant discrimination, whereas [feature family] provided complementary signal (Fig. Xe). Representative cases further showed close alignment between lesion boundaries, attribution maps and downstream predictions (Supplementary Fig. X), supporting the interpretability of the decision process.
```

#### P2 模板

```text
We then asked whether these explanatory signals could support clinician-interactive review. In an interactive workflow for mask inspection, feature attribution and corrective annotation (Fig. Xh), AI assistance shortened segmentation time across most cases while preserving agreement with manual segmentation (Fig. Xi--k). These results suggest that ThyroidXAgent can expose auditable evidence for review while improving annotation efficiency.
```

### 参考原文示例

> `LLNM-Net` 风格：先给解释性图，再提炼一个临床上能复述的规律
>
> “When the minimum distance is less than 0.25 cm, the average probability of LLNM occurrence exceeds 72%.”

> `TissueLab` 风格：先写 workflow 可视化，再写它如何进入专家反馈环
>
> “With TissueLab platform, user can further provide additional feedback…”

### 这一节的关键写作要求

- 不要把它写成单纯“有 SHAP 图所以可解释”
- 要强调：
  - **what features dominate**
  - **whether representative cases align with those features**
  - **whether clinicians can inspect or correct them**

### 你现有内容如何迁移

你当前 `Results` 第一个 subsection 的第二段，基本就是这个 subsection 的原料。

要做的只是：

- 把它从“夹在性能段中间”改成独立 subsection
- 让第二段结尾明确写到 **auditable review workflow** 或 **clinician-interactive review**

---

## Subsection 3
## `Generalization to clinically consequential malignant-lesion tasks`

### 这一节的 job

只做一件事：

**证明 ThyroidXAgent 不仅能做良恶性分类，还能迁移到更临床相关的恶性病灶任务。**

### 推荐段落数

**2 段**。

### 段落功能分配

- **P1**：两个 malignant tasks 的 headline metrics + baseline comparison
- **P2**：task-specific SHAP signatures，说明不同任务学到的不是同一种模式

### 英文模板

#### P1 模板

```text
We next evaluated whether the same framework generalized beyond benign--malignant discrimination to clinically consequential malignant-lesion tasks. On lymph node metastasis prediction, ThyroidXAgent achieved an AUROC of [X] and an AUPRC of [Y], corresponding to relative improvements of [X]% and [Y]% over [baseline]. On FTC/PTC subtype classification, it achieved an AUROC of [X] and an AUPRC of [Y], exceeding [baseline] by [X]% and [Y]%, respectively (Fig. X and Supplementary Table X).
```

#### P2 模板

```text
SHAP analyses further revealed task-specific radiomic signatures rather than a single shared decision pattern. Whereas [task 1] was driven mainly by [feature family], [task 2] depended more strongly on [feature family] (Fig. Xc--f). These distinct attribution profiles indicate that ThyroidXAgent can adapt to clinically different malignant-lesion tasks while retaining interpretable task-specific evidence.
```

### 参考原文思路

- 这节最接近 `LLNM-Net` 的 `Predicting high-risk lymph node metastasis patients`
- 同时借用了 `Tiger Model` 的“不是只在主任务有效，还要看泛化/外部任务”的结构思维

### 写作提醒

- 这里的关键词是 **clinically consequential**，不是 `additional tasks`
- 要写成“向更重要任务推进”，而不是“顺手又做了两个实验”

### 你现有内容如何迁移

你当前第一个 subsection 的第三段，几乎完整可迁移到这里。

重点只是：

- 把这段从“大杂烩 subsection”里解救出来
- 让标题和开头句更明确地对准 “generalization”

---

## Subsection 4
## `Evidence-grounded report generation from thyroid ultrasound`

### 这一节的 job

只做一件事：

**证明 ThyroidXAgent 能把多视图超声输入和结构化事实转成高质量报告。**

### 推荐段落数

**2 段**。

### 段落功能分配

- **P1**：report-generation workflow + why structured evidence matters
- **P2**：NLG metrics 上的 headline result

### 英文模板

#### P1 模板

```text
We next evaluated evidence-grounded report generation, a core task of the thyroid diagnostic agent. Given multi-view and multimodal thyroid ultrasound inputs, ThyroidXAgent constructed image priors, invoked segmentation, classification, measurement and captioning tools through an agentic planning-and-execution workflow, and converted the resulting structured findings into editable reports through [retrieval / slot filling / clause assembly] (Fig. Xc--g). To assess performance, we evaluated the generated reports on [dataset 1] and [dataset 2] using both conventional natural-language-generation metrics and a thyroid-specific clinical semantic metric, ThyClinScore (Fig. Xh and Supplementary Tables X--Y).
```

#### P2 模板

```text
On conventional overlap-based metrics, ThyroidXAgent achieved the strongest overall performance across both evaluation settings (Fig. Xh). On the in-house dataset, it reached [BLEU-1], [BLEU-4] and [ROUGE_L], while maintaining a competitive METEOR score. On the public benchmark, it ranked first on all four evaluated natural-language-generation metrics. These results indicate that grounding report generation in structured diagnostic facts improves agreement with reference reports while preserving the surface form of expert-written ultrasound reports.
```

### 可借鉴的参考思路

这一节的结构最像 `Tiger Model` 里的：

- `Overview of the Tiger Model`
- `Quantitative analysis of image generation quality`

也就是说，先说系统如何工作，再说其在第一层指标上的表现。

### 这一节最重要的写法要求

- 先写 **evidence-grounded report generation**，不要一上来就写 BLEU/ROUGE
- 指标必须放在 workflow 之后，不然读者不知道你在评价什么
- 收束句要强调 “structured diagnostic facts” 的价值

### 你现有内容如何迁移

你当前 `Report generation` subsection 的第一段和第二段，基本就是这里的主体。

调整时只需要：

- 把指标验证和 reader study 后移
- 让这一节只负责“report generation works”

---

## Subsection 5
## `Clinical semantic validation of ThyClinScore`

### 这一节的 job

只做一件事：

**证明 `ThyClinScore` 不是附带指标，而是比传统文本重叠指标更贴近临床语义正确性。**

### 推荐段落数

**2 段** 或 **3 段**。

### 段落功能分配

- **P1**：先报 `ThyClinScore` 在两个数据集上的 headline result
- **P2**：解释 submetrics 捕捉的是哪些 failure modes
- **P3**：相关性分析，证明它比传统 NLG metric 更接近 clinical semantic correctness

### 英文模板

#### P1 模板

```text
Clinical semantic evaluation further showed that ThyroidXAgent retained clinically relevant information rather than only matching reference wording. On the in-house dataset, it achieved the highest ThyClinScore of [X], together with the highest [feature accuracy / F1 / ...], while maintaining competitive completeness and consistency. On the public benchmark, ThyroidXAgent again achieved the highest ThyClinScore, indicating the strongest overall clinical semantic alignment among the compared methods (Fig. Xb,h).
```

#### P2 模板

```text
Because the individual submetrics captured different failure modes, including [false lesion detection], [feature mismatch] and [missing structured fields], the combined ThyClinScore provided a more balanced assessment than any single submetric alone. This design was intended to distinguish reports that were lexically similar from those that were clinically correct at the lesion and attribute levels.
```

#### P3 模板

```text
To validate this interpretation, we next compared ThyClinScore with conventional overlap-based metrics and with a location-aware [judge / expert reference]. Conventional NLG metrics were strongly correlated with one another, indicating substantial redundancy in their evaluation criteria, whereas their correlations with ThyClinScore and its submetrics were lower. When benchmarked against the location-aware [judge], ThyClinScore achieved the highest correlation among all evaluated metrics ([statistic]), supporting its value as a clinically oriented report-quality measure (Supplementary Fig. X).
```

### 参考论文上的对应套路

这一节本质上是在借 `Tiger Model` 的“先证明中间环节有效，再证明它支撑最终任务”逻辑。

### 关键写作提醒

- 这节必须与 report generation 主性能分开
- 不要把 `ThyClinScore` 和 BLEU/ROUGE 混写在同一段里
- 这里写的是 **metric validation**，不是再重复 report generation result

### 你现有内容如何迁移

你当前 `Report generation` subsection 的第三、第四段，基本可直接搬到这里。

最重要的是：

- 把 `ThyClinScore` 作为一个独立科学对象来写
- 让这节的结尾强调 `clinical semantic correctness`，而不是泛泛说“better metric”

---

## Subsection 6
## `AI-assisted reporting improves efficiency while preserving clinical utility`

### 这一节的 job

只做一件事：

**证明 ThyroidXAgent 在 reader study / 临床工作流里不是只会自动生成报告，而是真的能帮助医生更高效地工作。**

### 推荐段落数

**2 段**。

### 段落功能分配

- **P1**：reader-study design + time reduction
- **P2**：physician-stratified result + representative examples + clinical utility closing sentence

### 英文模板

#### P1 模板

```text
We then examined whether ThyroidXAgent could improve human report-writing efficiency in a reader-study setting. [N] physicians wrote reports for [N] thyroid ultrasound videos under both manual and AI-assisted workflows, with [paired / crossover design detail] to reduce memory bias (Fig. Xa). AI-assisted report writing shortened the mean reporting time from [X] to [Y] min per case, corresponding to a [X]% reduction (Fig. Xb,c).
```

#### P2 模板

```text
This time-saving effect was preserved after stratification by physician, with reductions of [X]% and [Y]% for the two readers, respectively (Fig. Xd). Representative cases further showed that the structured evidence generated by ThyroidXAgent supported clinically concordant statements on [location / size / morphology / impression], while exposing partially correct or incorrect statements for review (Fig. Xe). Together, these findings indicate that ThyroidXAgent can accelerate thyroid ultrasound reporting while preserving clinically reviewable evidence.
```

### 参考论文上的对应套路

- 这节对应 `LLNM-Net` 的 `Application ... in clinical practice`
- 也借用了 `Tiger Model` 的医生人工评估逻辑

### 写法提醒

- 先报 workflow benefit，再给定性案例
- 结尾不要只写 “improves efficiency”
- 更好的句子是：`while preserving clinically reviewable evidence` 或 `while maintaining clinical utility`

### 你现有内容如何迁移

你当前 `Report generation` subsection 的最后一段，几乎完整可迁移到这里。

---

## 五、给你一个可直接套的 LaTeX/Markdown 版骨架

下面这个骨架可以直接拿去改你的 `Results`：

```text
\section{Results}

\subsection{Cross-dataset segmentation and benign--malignant classification}
[Paragraph 1: why segmentation + benign/malignant matter; headline cross-dataset metrics]
[Paragraph 2: baseline comparison + physician comparison + short roll-up]

\subsection{Interpretable predictions and clinician-interactive review}
[Paragraph 1: cohort-level SHAP + representative cases]
[Paragraph 2: interactive review workflow + corrective annotation + time saving]

\subsection{Generalization to clinically consequential malignant-lesion tasks}
[Paragraph 1: LLNM and FTC/PTC performance + baseline comparison]
[Paragraph 2: task-specific SHAP signatures + interpretation]

\subsection{Evidence-grounded report generation from thyroid ultrasound}
[Paragraph 1: workflow + structured evidence design]
[Paragraph 2: NLG metric results on in-house and public benchmarks]

\subsection{Clinical semantic validation of ThyClinScore}
[Paragraph 1: ThyClinScore headline performance]
[Paragraph 2: submetrics and failure modes]
[Paragraph 3: correlation with conventional metrics and external judge]

\subsection{AI-assisted reporting improves efficiency while preserving clinical utility}
[Paragraph 1: reader-study design + time reduction]
[Paragraph 2: physician-stratified benefit + representative cases + closing meaning sentence]
```

---

## 六、`Results` 段落层面的硬规则

下面这些规则是三篇参考文的共同底层规律。

## 规则 1：一段只做一个 job

每段只能承担这几类工作中的一种：

- context
- result
- comparison
- mechanism / interpretability
- implication

不要在一段里同时做 2–3 件事。

### 对 `ThyroidXAgent` 的直接提醒

你当前第一个 subsection 的第一段还算稳，但第二段和第三段已经进入别的 job；
你当前第二个 subsection 基本是一段接一段地切换 job，所以读起来会更累。

---

## 规则 2：段首先给 judgement，再给数字

也就是典型的 **conclusion-first**。

### 不够像 NC 的写法

```text
We evaluated the model on two datasets. The AUROC was 0.94. The AUPRC was 0.83.
```

### 更像 NC 的写法

```text
ThyroidXAgent achieved the strongest overall discrimination across both datasets, with an AUROC of 0.94 and an AUPRC of 0.83.
```

---

## 规则 3：headline claim 后面立刻接 figure 或 table 支撑

不要让读者等到段末才知道你在靠哪张图。

### 建议句型

- `... (Fig. 2a--d and Supplementary Table 3).`
- `... (Fig. 3b,c).`
- `... as summarized in Fig. 4.`

---

## 规则 4：每个强 claim 都要带一个比较对象

不要只写：

- `performed well`
- `showed robust performance`
- `was clinically useful`

最好写成：

- `achieved [metric], compared with [baseline]`
- `outperformed [baseline/human experts]`
- `reduced reporting time from [X] to [Y]`

---

## 规则 5：解释性结果必须变成“可复述的规律”

不要只写：

- `SHAP analysis is shown in Fig. X`

要写成：

- 哪类特征主导
- 两个任务是否学到不同特征
- 有没有一个 clinically meaningful observation

### 你可以参考的写法

> “When the minimum distance is less than 0.25 cm, the average probability of LLNM occurrence exceeds 72%.”

它厉害的地方在于：不是说“看了热图”，而是把解释性结果压缩成了一个**可讲给临床读者听的发现**。

---

## 规则 6：新 metric 要独立成块，不要混在主性能段里

这点对 `ThyClinScore` 尤其重要。

### 为什么

因为一旦混写，读者会分不清：

- 你是在证明 report generation 很强
- 还是在证明 `ThyClinScore` 很合理

而高水平论文会把这两件事拆开。

---

## 七、建议直接替换的 subsection 标题

## 当前标题 1

`Segmentation, classification performance and interpretability`

### 问题

这个标题一次说了 3 件事，范围太宽。

### 建议拆成

- `Cross-dataset segmentation and benign--malignant classification`
- `Interpretable predictions and clinician-interactive review`
- `Generalization to clinically consequential malignant-lesion tasks`

---

## 当前标题 2

`Report generation`

### 问题

太宽，无法体现：

- workflow
- report quality
- metric validation
- clinical workflow benefit

这 4 件事并不是同一层逻辑。

### 建议拆成

- `Evidence-grounded report generation from thyroid ultrasound`
- `Clinical semantic validation of ThyClinScore`
- `AI-assisted reporting improves efficiency while preserving clinical utility`

---

## 八、可直接复用的句型库

## 1. subsection 开头句

- `We first evaluated whether ...`
- `We next asked whether ...`
- `We then examined whether ...`
- `To assess ..., we evaluated ...`
- `To interpret these predictions, we next examined ...`

## 2. headline result 句

- `ThyroidXAgent achieved the strongest overall performance across ...`
- `This advantage was preserved in ...`
- `Across heterogeneous datasets, ThyroidXAgent achieved ...`
- `On the external benchmark, ThyroidXAgent ranked first on ...`

## 3. 对比句

- `..., compared with [baseline]`
- `..., exceeding [baseline] by [X]% and [Y]%, respectively`
- `..., outperforming both [baseline] and [baseline]`

## 4. 解释性句

- `SHAP analyses revealed task-specific radiomic signatures ...`
- `Representative cases showed close alignment between ...`
- `These attribution profiles indicate that ...`

## 5. roll-up 句

- `Together, these results establish ...`
- `Overall, these findings indicate that ...`
- `Collectively, these analyses support ...`
- `These results position ThyroidXAgent as ...`

---

## 九、不要写成什么样

## 不要 1：一个 subsection 同时讲 4 条证据链

比如：

- 核心性能
- 解释性
- 泛化
- 人机协同

全在一个 subsection 里。

这就是你当前第一节的问题。

## 不要 2：同一段里既报数字又解释 metric 合理性又讲临床意义

尤其第二节里要避免这种段落过载。

## 不要 3：只给 “best overall balance” 这类抽象总结，不给紧邻的数字和比较对象

## 不要 4：把 `Results` 写成 mini-Discussion

比如：

- `addresses an important limitation`
- `offers a promising avenue`
- `highlights the broad clinical potential`

这些可以写，但应该出现在段尾或小结，不要整段都在抒情。

---

## 十、给 `ThyroidXAgent` 的直接改稿路线图

如果你接下来要真正改稿，最稳的顺序是：

### Step 1
先只改结构，不改数字

也就是先把当前两个 subsection 拆成六个 subsection。

### Step 2
把每一段重新分配 job

建议映射如下：

- 当前第一节第一段 → 新 `Subsection 1`
- 当前第一节第二段 → 新 `Subsection 2`
- 当前第一节第三段 → 新 `Subsection 3`
- 当前第二节第一段 + 第二段 → 新 `Subsection 4`
- 当前第二节第三段 + 第四段 → 新 `Subsection 5`
- 当前第二节最后一段 → 新 `Subsection 6`

### Step 3
再做句法 NC 化

重点改：

- 段首更结论先行
- figure call 更及时
- 每节结尾多一个 roll-up sentence
- 避免 broad laundry-list title

### Step 4
最后再压字数和统一语气

也就是最后一轮再做：

- 去掉重复 `achieved the highest...`
- 去掉多余修饰词
- 统一 `show / indicate / demonstrate / suggest` 的证据强度

---

## 十一、给你一个可直接抄用的 Results 总起句模板

如果你想给整个 `Results` 开头加一个更稳的总起，也可以参考下面这个写法：

```text
We evaluated ThyroidXAgent along two clinically motivated axes. First, we tested whether the framework improves thyroid nodule delineation, malignancy discrimination and malignant-lesion stratification across heterogeneous ultrasound datasets while providing interpretable and reviewable evidence. Second, we assessed whether the same framework supports evidence-grounded report generation, clinically meaningful report evaluation and more efficient physician reporting workflows.
```

这个句子有两个作用：

- 先把 `Results` 总体逻辑告诉读者
- 避免后面 6 个 subsection 看起来像彼此无关

---

## 十二、最后给一个“最像 NC 风格”的最短心法

如果你只记 4 件事，就记下面这 4 件：

1. **小标题就是证据阶梯，不是内容清单**
2. **每段开头先给 judgement，再给数字和图**
3. **新 metric、新 workflow、人类评估，都要单独成块**
4. **每一节最后都要回答：所以这说明了什么**

---

## 十三、你下一步怎么用这份模板

建议你按下面方式使用：

- 先把当前 `Results` 结构按本模板拆开
- 再逐节改写，每次只改一个 subsection
- 改的时候先保留原数字和图号，不先动数据
- 等结构稳了，再做语言润色

如果你愿意，下一步我可以继续直接做：

1. **按这份模板，帮你把 `ThyroidXAgent.md` 的 `Results` 直接重组改写一版**
2. **先只改 subsection 标题和段落顺序，尽量少动原句**
3. **再进一步改成更像 `Nature Communications` 的英文 prose**
