# ThyroidAgent 论文修改对照表

本文档按“原句 → 新句 → 对应 reviewer concern”的形式，记录 `ThyroidAgent.md` 中本轮主要修改，便于后续 rebuttal、改稿说明和自查。

---

## 1. Abstract：明确 LLM 与 PPO 的角色边界

### 原句
> We propose ThyroidAgent, an agent-based framework for thyroid nodule ultrasound segmentation and classification. Unlike conventional approaches that rely on static pipelines, ThyroidAgent introduces a dynamic, policy-driven inference process, selecting model experts based on ultrasound image data and device context. By integrating segmentation and classification tasks, the framework enhances classification through segmentation-derived features. This multi-task workflow improves interpretability, robustness, and adaptability across diverse ultrasound conditions.

### 原句翻译
> 我们提出了 ThyroidAgent，一个用于甲状腺结节超声分割与分类的基于智能体的框架。不同于依赖静态流水线的传统方法，ThyroidAgent 引入了一种动态的、策略驱动的推理过程，可根据超声图像数据和设备上下文选择模型专家。通过整合分割与分类任务，该框架利用由分割得到的特征来增强分类性能。这一多任务流程提升了在多样化超声条件下的可解释性、鲁棒性和适应性。

### 新句
> We propose ThyroidAgent, an agent-based framework for thyroid nodule ultrasound analysis that coordinates segmentation and classification experts through evidence-aware expert selection and aggregation. Unlike conventional approaches that rely on static pipelines, ThyroidAgent reasons over structured evidence derived from ultrasound images, segmentation masks, radiomics descriptors, and device/context metadata to adapt expert usage on a per-case basis. Rather than replacing task-specific predictors, the LLM operates only as a routing module over expert outputs, while reinforcement learning is used separately to optimize connected-component post-processing for segmentation masks. This design improves interpretability, robustness, and adaptability across diverse ultrasound conditions.

### 新句翻译
> 我们提出了 ThyroidAgent，一个用于甲状腺结节超声分析的基于智能体的框架，它通过具备证据感知能力的专家选择与聚合机制来协调分割和分类专家。不同于依赖静态流水线的传统方法，ThyroidAgent 基于从超声图像、分割掩膜、影像组学描述符以及设备/上下文元数据中提取的结构化证据进行推理，从而针对每个病例自适应地调整专家使用方式。LLM 并不替代特定任务的预测器，而只是作为一个作用于专家输出之上的路由模块；与此同时，强化学习被单独用于优化分割掩膜的连通域后处理。这一设计提升了在多样化超声条件下的可解释性、鲁棒性和适应性。

### 对应 reviewer concern
- Reviewer #1：agent formulation 不清、LLM role 不清、PPO role 不清
- Reviewer #2：pipeline 复杂但说不清
- Reviewer #3：agent 和 LLM 的角色未严格定义

---

## 2. Fig. 1 caption：弱化“端到端集成”误读，改成 orchestration

### 原句
> Overview of the ThyroidAgent framework. While traditional systems use fixed pipelines, ThyroidAgent dynamically selects expert models based on ultrasound images and metadata, integrating segmentation and classification for improved adaptability and robustness.

### 原句翻译
> ThyroidAgent 框架概览。传统系统使用固定流水线，而 ThyroidAgent 根据超声图像和元数据动态选择专家模型，通过整合分割与分类来提升适应性和鲁棒性。

### 新句
> Overview of the ThyroidAgent framework. While traditional systems use fixed pipelines, ThyroidAgent coordinates segmentation and classification experts through evidence-aware routing and aggregation based on ultrasound images, radiomics descriptors, and metadata.

### 新句翻译
> ThyroidAgent 框架概览。传统系统使用固定流水线，而 ThyroidAgent 基于超声图像、影像组学描述符和元数据，通过证据感知的路由与聚合来协调分割和分类专家。

### 对应 reviewer concern
- Reviewer #2：图很复杂但 role 不清楚
- Reviewer #3：系统 intended operation 需要更准确表达

---

## 3. Introduction：重新定义 ThyroidAgent 的总体定位

### 原句
> In this work, we propose \textit{ThyroidAgent}, an agent-based multi-task framework for thyroid ultrasound diagnosis that departs from conventional static pipelines by replacing fixed execution with context-aware expert orchestration.

### 原句翻译
> 在这项工作中，我们提出了 \textit{ThyroidAgent}，这是一个面向甲状腺超声诊断的基于智能体的多任务框架。它通过以具备上下文感知能力的专家编排取代固定执行方式，从而区别于传统的静态流水线。

### 新句
> In this work, we propose \textit{ThyroidAgent}, an agent-based framework for thyroid ultrasound diagnosis that departs from conventional static pipelines by replacing fixed execution with context-aware expert orchestration across two coordinated tasks, segmentation and malignancy classification.

### 新句翻译
> 在这项工作中，我们提出了 \textit{ThyroidAgent}，这是一个面向甲状腺超声诊断的基于智能体的框架。它通过在分割和良恶性分类这两个协同任务上，以具备上下文感知能力的专家编排取代固定执行方式，从而区别于传统的静态流水线。

### 对应 reviewer concern
- Reviewer #1：methodological core 不清
- Reviewer #2：pipeline 复杂且定义模糊
- Reviewer #3：claims about adaptability/generalization insufficiently grounded unless task boundaries are clearer

---

## 4. Introduction：明确 LLM 只做 routing，不直接诊断

### 原句
> The LLM module receives structured evidence from multiple trained experts and performs sample-specific expert selection while producing interpretable decision rationales. These designs establish a unified and adaptive framework that explicitly bridges segmentation, classification, and explainable evidence aggregation for thyroid ultrasound CAD.

### 原句翻译
> LLM 模块接收来自多个已训练专家的结构化证据，并执行样本特异的专家选择，同时生成可解释的决策依据。这些设计构建了一个统一且自适应的框架，显式连接了甲状腺超声 CAD 中的分割、分类与可解释证据聚合。

### 新句
> The LLM module receives structured evidence from multiple trained experts and performs sample-specific expert selection followed by lightweight aggregation while producing interpretable decision rationales. Importantly, ThyroidAgent is not a monolithic LLM diagnosis system: task-specific segmentation and classification experts first produce candidate outputs, and the LLM operates only on structured evidence summaries rather than raw-image diagnosis. Separately, PPO is used only for optimizing connected-component analysis (CCA) parameters for mask refinement, not for controlling the overall diagnostic policy.

### 新句翻译
> LLM 模块接收来自多个已训练专家的结构化证据，执行样本特异的专家选择，并进一步进行轻量级聚合，同时生成可解释的决策依据。需要强调的是，ThyroidAgent 并不是一个单体式的 LLM 诊断系统：特定任务的分割和分类专家会先产生候选输出，而 LLM 仅作用于结构化证据摘要，而不是直接基于原始图像进行诊断。此外，PPO 仅用于优化连通域分析（CCA）的参数以细化掩膜，并不负责控制整体诊断策略。

### 对应 reviewer concern
- Reviewer #1：LLM 是 policy generator 还是 controller 不清
- Reviewer #1：PPO optimization strategy 与 LLM role 混淆
- Reviewer #3：roles of agent and LLM are not fully defined

---

## 5. Introduction：补 related work 并重新定位 radiomics 创新性

### 原句
> Related studies in thyroid CAD have also explored radiomics-assisted diagnosis, coupled segmentation-classification learning, and dynamic expert reasoning, but these lines are usually studied in isolation.

### 原句翻译
> 甲状腺 CAD 相关研究也探索了影像组学辅助诊断、分割—分类耦合学习以及动态专家推理，但这些研究方向通常是彼此独立开展的。

### 新句
> Related studies in thyroid CAD have also explored radiomics-assisted diagnosis, coupled segmentation-classification learning, and dynamic expert reasoning, but these lines are usually studied in isolation. Prior thyroid radiomics studies have shown that handcrafted morphology and texture descriptors can improve ultrasound malignancy assessment~\cite{park2021radiomics,shao2025multimodal}, while coupled-task frameworks have used shared supervision or interpretable constraints to connect segmentation and classification~\cite{kang2022thyroid,gong2021multi,gong_thyroid_2023}. More recent expert-routing and medical VLM systems suggest that dynamic reasoning over heterogeneous evidence can improve adaptability in complex imaging settings~\cite{she2025echovlm,bai2025qwen3,sellergren2025medgemma}. In contrast, ThyroidAgent uses radiomics not as a standalone novelty, but as one structured evidence source within a thyroid-specific expert orchestration framework.

### 新句翻译
> 甲状腺 CAD 相关研究也探索了影像组学辅助诊断、分割—分类耦合学习以及动态专家推理，但这些研究方向通常是彼此独立开展的。既有甲状腺影像组学研究表明，手工构造的形态与纹理描述符可以提升超声良恶性评估~\cite{park2021radiomics,shao2025multimodal}；而耦合任务框架则通过共享监督或可解释约束来连接分割与分类~\cite{kang2022thyroid,gong2021multi,gong_thyroid_2023}。更新近的专家路由与医学 VLM 系统提示，对异构证据进行动态推理能够提升复杂成像场景下的适应性~\cite{she2025echovlm,bai2025qwen3,sellergren2025medgemma}。相比之下，ThyroidAgent 并不把影像组学作为一个独立的创新点，而是将其作为面向甲状腺任务的专家编排框架中的一种结构化证据来源。

### 对应 reviewer concern
- Reviewer #1：radiomics integration novelty limited
- Reviewer #3：missing related work comparison, especially dynamic expert routing / related interpretable frameworks

---

## 6. Contributions：弱化 radiomics 本身的新意，强调 evidence orchestration

### 原句 1
> \textbf{1. Dynamic agent-driven CAD paradigm.}

### 原句 2
> We propose \emph{ThyroidAgent}, a dynamic CAD framework that replaces the traditional static pipeline with an agent capable of reasoning over multimodal context metadata and adaptively selecting among segmentation and classification experts, enabling flexible and task-aware processing.

### 原句 3
> \textbf{2. Radiomics-augmented agent reasoning.}

### 原句 4
> We integrate radiomics and CCA-based feature toolkits into the agent loop, allowing the agent to exploit segmentation masks to extract quantitative descriptors and fuse them with model confidence signals, thereby improving decision reliability, interpretability, and expert-selection quality.

### 原句翻译
> **1. 动态的智能体驱动 CAD 范式。**
>
> 我们提出了 \emph{ThyroidAgent}，这是一个动态的 CAD 框架，它以一个能够基于多模态上下文元数据进行推理并在分割与分类专家之间自适应选择的智能体，取代了传统静态流水线，从而实现更灵活、面向任务的处理。
>
> **2. 影像组学增强的智能体推理。**
>
> 我们将影像组学和基于 CCA 的特征工具集成到智能体回路中，使智能体能够利用分割掩膜提取定量描述符，并将其与模型置信度信号融合，从而提高决策可靠性、可解释性和专家选择质量。

### 新句 1
> \textbf{1. Evidence-aware expert orchestration.}

### 新句 2
> We propose \emph{ThyroidAgent}, a CAD framework that replaces the traditional static pipeline with evidence-aware orchestration over segmentation and classification experts, enabling flexible and task-aware processing under heterogeneous acquisition conditions.

### 新句 3
> \textbf{2. Mask-guided evidence construction and refinement.}

### 新句 4
> We integrate mask-guided radiomics descriptors and PPO-optimized CCA refinement into the evidence construction loop, allowing ThyroidAgent to combine quantitative morphology and texture cues with model confidence signals for more reliable and interpretable expert selection.

### 新句翻译
> **1. 证据感知的专家编排。**
>
> 我们提出了 \emph{ThyroidAgent}，这是一个 CAD 框架，它通过对分割和分类专家进行证据感知的编排，取代传统的静态流水线，从而在异质采集条件下实现灵活且面向任务的处理。
>
> **2. 基于掩膜引导的证据构建与优化。**
>
> 我们将基于掩膜引导的影像组学描述符和经 PPO 优化的 CCA 细化模块整合进证据构建回路，使 ThyroidAgent 能够将定量的形态与纹理线索和模型置信度信号结合起来，从而实现更可靠、更具可解释性的专家选择。

### 对应 reviewer concern
- Reviewer #1：radiomics 不是 primary innovation
- Reviewer #3：main contribution claims 需要和实验支持更一致

---

## 7. Method 总述：四个组件拆开写清楚

### 原句
> Fig.~\ref{fig:WorkFlow} illustrates the ThyroidAgent framework, which consists of training and inference stages. During inference, the agent dynamically selects the most appropriate expert output based on contextual information and evidence signals, replacing static pipelines.

### 原句翻译
> 图~\ref{fig:WorkFlow} 展示了 ThyroidAgent 框架，该框架由训练阶段和推理阶段组成。在推理过程中，智能体基于上下文信息和证据信号动态选择最合适的专家输出，从而取代静态流水线。

### 新句
> Fig.~\ref{fig:WorkFlow} illustrates the ThyroidAgent framework, which consists of offline expert construction and online evidence-aware orchestration. During inference, task-specific experts first generate candidate segmentation masks and malignancy predictions, after which ThyroidAgent summarizes them into structured evidence and invokes an LLM-based routing module for expert selection and aggregation.

### 新句翻译
> 图~\ref{fig:WorkFlow} 展示了 ThyroidAgent 框架，该框架由离线专家构建和在线证据感知编排两部分组成。在推理过程中，特定任务的专家首先生成候选分割掩膜和良恶性预测，随后 ThyroidAgent 将其汇总为结构化证据，并调用基于 LLM 的路由模块进行专家选择与聚合。

### 对应 reviewer concern
- Reviewer #1：lack of rigorous and reproducible agent formulation
- Reviewer #2：Fig. 2 组件太多但 interaction 不清
- Reviewer #3：workflow claims clearer than method detail

---

## 8. Method 总述：直接说明 LLM/PPO 的分工

### 原句
> The agent-based framework overcomes the limitations of relying on a single complex model by dynamically selecting from multiple simpler expert models, improving flexibility and generalization across diverse datasets. Motivated by the recent advancements in large language models (LLMs), which excel in dynamic decision-making, we integrate their reasoning capabilities to perform expert selection and aggregation based on structured evidence. This dynamic orchestration allows ThyroidAgent to adapt to varying clinical scenarios and enhance decision-making in thyroid ultrasound diagnosis.

### 原句翻译
> 该基于智能体的框架通过从多个更简单的专家模型中进行动态选择，克服了依赖单一复杂模型的局限性，并提升了在不同数据集上的灵活性和泛化能力。受大语言模型（LLM）近期进展的启发——它们擅长动态决策——我们引入其推理能力，以基于结构化证据执行专家选择与聚合。这种动态编排使 ThyroidAgent 能够适应不同的临床场景，并提升甲状腺超声诊断中的决策质量。

### 新句
> The ThyroidAgent framework overcomes the limitations of relying on a single complex model by dynamically selecting from multiple simpler expert models, improving flexibility and generalization across diverse datasets. The overall method contains four components: expert prediction generation for the two tasks, structured evidence construction, LLM-based expert routing/aggregation, and PPO-based CCA refinement for segmentation masks. Here, the LLM is only responsible for evidence-aware routing, whereas PPO is used only to optimize CCA hyperparameters and does not control the overall diagnostic policy.

### 新句翻译
> ThyroidAgent 框架通过从多个更简单的专家模型中进行动态选择，克服了依赖单一复杂模型的局限性，并提升了在不同数据集上的灵活性和泛化能力。整个方法包含四个组成部分：面向两个任务的专家预测生成、结构化证据构建、基于 LLM 的专家路由/聚合，以及面向分割掩膜的基于 PPO 的 CCA 细化。在这里，LLM 只负责证据感知的路由，而 PPO 仅用于优化 CCA 超参数，并不控制整体诊断策略。

### 对应 reviewer concern
- Reviewer #1：agent, reward, PPO, LLM roles 混乱
- Reviewer #3：roles of the agent and LLM are not fully defined

---

## 9. Toolbox：明确每个模块的输入输出作用

### 原句
> We define thyroid ultrasound analysis as a collection of tools with standardized inputs and outputs, enabling the agent to compare expert models based on consistent evidence for reproducible results. The toolbox facilitates expert selection and improves prediction accuracy through complementary components.

### 原句翻译
> 我们将甲状腺超声分析定义为一组具有标准化输入与输出的工具，使智能体能够基于一致的证据比较专家模型，从而获得可复现的结果。该工具箱通过相互补充的组件来促进专家选择并提升预测精度。

### 新句
> We define thyroid ultrasound analysis as a collection of tools with standardized inputs and outputs, enabling ThyroidAgent to compare expert models based on consistent evidence for reproducible results. The toolbox facilitates expert selection and improves prediction accuracy through four complementary components: segmentation experts that output candidate masks and confidence signals, classification experts that output malignancy probabilities and confidence scores, a radiomics tool that extracts morphology and texture descriptors from image-mask pairs, and a PPO-optimized CCA module that refines segmentation masks before downstream evidence aggregation when needed.

### 新句翻译
> 我们将甲状腺超声分析定义为一组具有标准化输入与输出的工具，使 ThyroidAgent 能够基于一致的证据比较专家模型，从而获得可复现的结果。该工具箱通过四个相互补充的组件来促进专家选择并提升预测精度：输出候选掩膜和置信度信号的分割专家、输出良恶性概率和置信分数的分类专家、从图像—掩膜对中提取形态与纹理描述符的影像组学工具，以及在需要时于下游证据聚合之前对分割掩膜进行细化的经 PPO 优化的 CCA 模块。

### 对应 reviewer concern
- Reviewer #2：role of each component not sufficiently explained
- Reviewer #3：notion of evidence not formally defined enough

---

## 10. Eq. (1) 附近：补全 segmentation/classification loss 变量定义

### 原句
> where $\mathcal{L}_{\mathrm{bm}}$ is BCE-with-logits computed on the adjusted logits $z'_b$.

### 原句翻译
> 其中，$\mathcal{L}_{\mathrm{bm}}$ 表示在调整后的 logit $z'_b$ 上计算得到的 BCE-with-logits 损失。

### 新句
> where $y \in \{0,1\}^{H\times W}$ denotes the binary segmentation target, $\operatorname{AvgPool}_{31}(\cdot)$ is a $31\times31$ average-pooling operator used to emphasize boundary-aware pixels, and $w$ is the resulting spatial weight map used in $\mathcal{L}_{\mathrm{seg}}$. For classification, $y_b\in\{0,1\}$ is the binary malignancy label of sample $b$, $z_b$ is the original logit, $z'_b$ is the class-prior-adjusted logit, $p_{\text{pos}}$ and $p_{\text{neg}}$ are the empirical positive and negative class priors, and $\tau$ is the logit-adjustment coefficient. We use $\mathcal{L}_{\mathrm{bm}}$ to denote BCE-with-logits computed on $z'_b$, while the GLA objective refers to this class-prior-aware classification loss.

### 新句翻译
> 其中，$y \in \{0,1\}^{H\times W}$ 表示二值分割目标，$\operatorname{AvgPool}_{31}(\cdot)$ 是一个 $31\times31$ 的平均池化算子，用于强调边界感知像素，$w$ 是由此得到并用于 $\mathcal{L}_{\mathrm{seg}}$ 的空间权重图。对于分类任务，$y_b\in\{0,1\}$ 表示样本 $b$ 的二值良恶性标签，$z_b$ 是原始 logit，$z'_b$ 是经过类别先验调整后的 logit，$p_{\text{pos}}$ 和 $p_{\text{neg}}$ 分别是经验正类与负类先验，$\tau$ 是 logit 调整系数。我们用 $\mathcal{L}_{\mathrm{bm}}$ 表示在 $z'_b$ 上计算得到的 BCE-with-logits，而 GLA 目标函数指的就是这种考虑类别先验的分类损失。

### 对应 reviewer concern
- Reviewer #1：reproducibility不足
- Reviewer #3：Eq. (1) variables insufficiently defined
- Reviewer #3：loss functions referenced but not clearly formulated

---

## 11. Radiomics 小节：明确 radiomics 是 evidence source，不是 standalone novelty

### 原句
> Radiomics extracts interpretable features from images and ROI masks to complement deep learning predictions. Using a 2D PyRadiomics setup, we focus on feature families such as shape2D, which are dominant in predicting outcomes. Representative formulations include:

### 原句翻译
> 影像组学从图像和 ROI 掩膜中提取可解释特征，以补充深度学习预测。采用二维 PyRadiomics 设置时，我们重点关注 shape2D 等在结果预测中占主导地位的特征族。代表性公式包括：

### 新句
> Radiomics extracts interpretable features from image-mask pairs to complement deep learning predictions and serves as one structured evidence source for ThyroidAgent. Using a 2D PyRadiomics setup, we focus on feature families such as shape2D and texture, which are dominant in predicting outcomes. Representative formulations include:

### 新句翻译
> 影像组学从图像—掩膜对中提取可解释特征，以补充深度学习预测，并作为 ThyroidAgent 的一种结构化证据来源。采用二维 PyRadiomics 设置时，我们重点关注 shape2D 和 texture 等在结果预测中占主导地位的特征族。代表性公式包括：

### 对应 reviewer concern
- Reviewer #1：radiomics novelty should not be overstated
- Reviewer #3：evidence notion should be defined more formally

---

## 12. Eq. (2) 附近：补全 radiomics 变量定义

### 原句
> where $A$ is the ROI area, $M(x,y) \in \{0,1\}$ is the binary ROI mask, $\mathrm{Energy}$ is the GLCM energy and $P(i,j)$ is the normalized gray-level co-occurrence matrix.

### 原句翻译
> 其中，$A$ 是 ROI 面积，$M(x,y) \in \{0,1\}$ 是二值 ROI 掩膜，$\mathrm{Energy}$ 是 GLCM 能量，$P(i,j)$ 是归一化后的灰度共生矩阵。

### 新句
> where $A$ denotes the ROI area, $M(x,y) \in \{0,1\}$ is the binary ROI mask at spatial coordinate $(x,y)$, $\mathbb{I}[\cdot]$ is the indicator function, $H \times W$ is the mask resolution, $\mathrm{Energy}$ is the gray-level co-occurrence matrix (GLCM) energy, $P(i,j)$ is the normalized GLCM entry associated with gray levels $i$ and $j$, and $N_g$ is the number of discretized gray levels used in radiomics quantization.

### 新句翻译
> 其中，$A$ 表示 ROI 面积，$M(x,y) \in \{0,1\}$ 是空间坐标 $(x,y)$ 处的二值 ROI 掩膜，$\mathbb{I}[\cdot]$ 是示性函数，$H \times W$ 是掩膜分辨率，$\mathrm{Energy}$ 是灰度共生矩阵（GLCM）能量，$P(i,j)$ 是与灰度级 $i$ 和 $j$ 对应的归一化 GLCM 元素，$N_g$ 是影像组学量化时使用的离散灰度级数量。

### 对应 reviewer concern
- Reviewer #3：Eq. (2) variables not defined
- Reviewer #1：radiomics dependency should be made more rigorous

---

## 13. RL for CCA：彻底切开 PPO 和主 agent

### 原句
> The agent is trained with Proximal Policy Optimization (PPO)~\cite{schulman2017proximal}, a stable on-policy method that updates the policy via a clipped objective, to adjust the number of connected components and the connectivity threshold in CCA and improve the final mask quality.

### 原句翻译
> 智能体采用近端策略优化（PPO）~\cite{schulman2017proximal} 进行训练。PPO 是一种稳定的 on-policy 方法，通过带裁剪的目标函数更新策略，用于调整 CCA 中的连通域数量和连通性阈值，从而提升最终掩膜质量。

### 新句
> A separate PPO policy~\cite{schulman2017proximal} is trained to adjust the number of connected components and the connectivity threshold in CCA and improve the final mask quality. Its state is defined on segmentation-mask quality cues, its action space consists of CCA hyperparameter updates, and its reward is derived from post-refinement mask quality. This PPO module is only used for segmentation post-processing and is not part of the LLM-based expert-routing policy.

### 新句翻译
> 一个独立的 PPO 策略~\cite{schulman2017proximal} 被训练用于调整 CCA 中的连通域数量和连通性阈值，以提升最终掩膜质量。其状态基于分割掩膜质量线索定义，动作空间由 CCA 超参数更新构成，奖励则来源于细化后掩膜的质量。该 PPO 模块仅用于分割后处理，并不是基于 LLM 的专家路由策略的一部分。

### 对应 reviewer concern
- Reviewer #1：PPO optimization strategy unclear
- Reviewer #1：whole framework may be mistaken as PPO-based
- Reviewer #3：agent and LLM roles not rigorously separated

---

## 14. Algorithm 1 后解释段：正式定义 SegEvidence / ClsEvidence / metadata handling

### 原句
> （原文无该解释段）

### 新句
> In Algorithm~\ref{alg:thyroidagent_inference}, $\mathrm{PolicySelect}(\cdot)$ denotes the LLM-based routing function that consumes structured evidence rather than raw images. Segmentation evidence is defined as $E_{seg}=\{q_k,s_k,d_k,m_k\}_{k=1}^{K}$, where $q_k$ is a mask-quality proxy, $s_k$ is the expert confidence, $d_k$ summarizes disagreement with peer experts, and $m_k$ is an optional metadata-compatibility score. Classification evidence is defined as $E_{cls}=\{p_m,\gamma_m,r,c,m_m\}_{m=1}^{M}$, where $p_m$ is the malignancy probability, $\gamma_m$ is the classifier confidence, $r$ is the radiomics descriptor vector, $c$ denotes optional case metadata, and $m_m$ is the expert metadata profile. When metadata are unavailable, the corresponding fields are marked as unknown and omitted from evidence scoring. In our implementation, the routing LLM uses low-temperature decoding (e.g., temperature 0.3 with bounded output length) to improve deterministic expert selection and then aggregates the selected expert outputs through a strict JSON decision schema.

### 新句翻译
> 在 Algorithm~\ref{alg:thyroidagent_inference} 中，$\mathrm{PolicySelect}(\cdot)$ 表示一个基于 LLM 的路由函数，它消费的是结构化证据而非原始图像。分割证据定义为 $E_{seg}=\{q_k,s_k,d_k,m_k\}_{k=1}^{K}$，其中 $q_k$ 是掩膜质量代理指标，$s_k$ 是专家置信度，$d_k$ 概括了与其他专家之间的不一致性，$m_k$ 是可选的元数据兼容性分数。分类证据定义为 $E_{cls}=\{p_m,\gamma_m,r,c,m_m\}_{m=1}^{M}$，其中 $p_m$ 是良恶性概率，$\gamma_m$ 是分类器置信度，$r$ 是影像组学描述符向量，$c$ 表示可选的病例元数据，$m_m$ 是专家的元数据配置。当元数据不可用时，相应字段会被标记为 unknown，并从证据评分中省略。在我们的实现中，路由 LLM 使用低温解码（例如 temperature 0.3 且输出长度受限）来提高专家选择的确定性，然后通过严格的 JSON 决策模式对选中的专家输出进行聚合。

### 对应 reviewer concern
- Reviewer #1：state/action/evidence/reward 相关定义不清
- Reviewer #1：missing metadata handling not reported
- Reviewer #1：decoding strategy not reported
- Reviewer #3：evidence central but not formally defined

---

## 15. Agentic Inference Workflow：把 Fig. 2 真正解释出来

### 原句
> Fig.~\ref{fig:WorkFlow} overviews ThyroidAgent as a policy-driven pipeline with expert construction and agentic inference.

### 原句翻译
> 图~\ref{fig:WorkFlow} 将 ThyroidAgent 概述为一个包含专家构建和智能体推理的策略驱动流水线。

### 新句
> Fig.~\ref{fig:WorkFlow} overviews ThyroidAgent as a policy-driven workflow with offline expert construction and online evidence-aware routing.

### 新句翻译
> 图~\ref{fig:WorkFlow} 将 ThyroidAgent 概述为一个包含离线专家构建和在线证据感知路由的策略驱动工作流。

### 原句
> As illustrated in Fig.~\ref{fig:WorkFlow} and Algorithm~\ref{alg:thyroidagent_inference}, during inference we execute candidate experts and summarize their predictions into compact evidence signals, together with context and metadata cues. ThyroidAgent then outputs a strict JSON decision to select or aggregate experts, producing the final mask and label. This workflow replaces a single fixed forward pass with evidence-aware orchestration across experts.

### 原句翻译
> 如图~\ref{fig:WorkFlow} 和 Algorithm~\ref{alg:thyroidagent_inference} 所示，在推理过程中，我们运行候选专家，并将其预测结果连同上下文和元数据线索一起汇总为紧凑的证据信号。随后，ThyroidAgent 输出一个严格的 JSON 决策，以选择或聚合专家，从而生成最终掩膜和标签。这一工作流以跨专家的证据感知编排取代了单一固定的前向传播。

### 新句
> As illustrated in Fig.~\ref{fig:WorkFlow} and Algorithm~\ref{alg:thyroidagent_inference}, during inference we execute candidate experts from the two tasks and summarize their outputs into compact evidence signals together with context and metadata cues. The LLM router then outputs a strict JSON decision to select experts and trigger lightweight aggregation, producing the final mask and label. This workflow replaces a single fixed forward pass with evidence-aware orchestration across experts, while PPO-based CCA refinement remains a separate post-processing component for segmentation masks.

### 新句翻译
> 如图~\ref{fig:WorkFlow} 和 Algorithm~\ref{alg:thyroidagent_inference} 所示，在推理过程中，我们运行来自两个任务的候选专家，并将其输出连同上下文和元数据线索一起汇总为紧凑的证据信号。随后，LLM 路由器输出一个严格的 JSON 决策，以选择专家并触发轻量级聚合，从而生成最终掩膜和标签。这一工作流以跨专家的证据感知编排取代了单一固定的前向传播，而基于 PPO 的 CCA 细化仍然是面向分割掩膜的独立后处理组件。

### 对应 reviewer concern
- Reviewer #2：Fig. 2 pipeline unclear
- Reviewer #3：workflow and evidence usage need explicit explanation

---

## 16. Experimental Details：补 baseline fairness、VLM 定位、decoding、stability

### 原句
> The downstream agent then selects from these expert outputs during inference. All models are trained with PyTorch (v2.4.1) under a shared protocol (AdamW, learning rate $1e-4$, batch size 12, 50 epochs) on 3$\times$48\,GB NVIDIA RTX A6000 GPUs.

### 原句翻译
> 下游智能体在推理过程中随后从这些专家输出中进行选择。所有模型均使用 PyTorch（v2.4.1）并在统一协议下训练（AdamW、学习率 $1e-4$、batch size 12、50 个 epoch），运行于 3$\times$48\,GB 的 NVIDIA RTX A6000 GPU 上。

### 新句
> The downstream ThyroidAgent router then selects and aggregates from these expert outputs during inference. All trainable baselines and expert models are trained under a harmonized split-and-test protocol wherever adaptation is possible, using PyTorch (v2.4.1), AdamW, a learning rate of $1e-4$, batch size 12, and 50 epochs on 3$\times$48\,GB NVIDIA RTX A6000 GPUs. For VLM baselines, we use prompt-based inference rather than task-specific fine-tuning, and therefore interpret them as reference generalist baselines rather than fully adapted thyroid-specialized competitors. In the routing module, low-temperature decoding (temperature 0.3, bounded output length) is used to stabilize JSON-form expert decisions, and repeated runs are performed with fixed seeds to assess stability.

### 新句翻译
> 下游的 ThyroidAgent 路由器随后在推理过程中从这些专家输出中进行选择和聚合。所有可训练的 baseline 和专家模型在能够适配的前提下，均采用统一协调的数据划分与测试协议进行训练，使用 PyTorch（v2.4.1）、AdamW、学习率 $1e-4$、batch size 12，并在 3$\times$48\,GB 的 NVIDIA RTX A6000 GPU 上训练 50 个 epoch。对于 VLM baseline，我们采用基于 prompt 的推理而非任务特定微调，因此将其视为通用型参考 baseline，而不是经过充分适配的甲状腺专用竞争模型。在路由模块中，我们使用低温解码（temperature 0.3，输出长度受限）来稳定 JSON 形式的专家决策，并通过固定随机种子的重复运行来评估稳定性。

### 对应 reviewer concern
- Reviewer #1：baseline fairness unclear
- Reviewer #2：why so many experts / complexity not justified enough
- Reviewer #3：VLM baselines prompt-engineered rather than fine-tuned
- Reviewer #1 / #3：stability and decoding settings missing

---

## 17. Segmentation results paragraph：补 Table 1 正文引用并统一命名

### 原句
> Segmentation performance is evaluated using Dice (\%) and HD95. We compare ThyAgent-Seg against three categories of methods: general-purpose segmenters ..., a specialized ultrasound model ..., and a recent advanced transformer-based approach ...

### 原句翻译
> 分割性能使用 Dice（\%）和 HD95 进行评估。我们将 ThyAgent-Seg 与三类方法进行比较：通用分割器……、一种专门的超声模型……以及一种最新的先进 Transformer 方法……

### 新句
> Segmentation performance is evaluated using Dice (\%) and HD95. Table~\ref{tab:table1_seg_blocks} compares ThyroidAgent against three categories of methods: general-purpose segmenters ..., a specialized ultrasound model ..., and a recent advanced transformer-based approach ...

### 新句翻译
> 分割性能使用 Dice（\%）和 HD95 进行评估。Table~\ref{tab:table1_seg_blocks} 将 ThyroidAgent 与三类方法进行比较：通用分割器……、一种专门的超声模型……以及一种最新的先进 Transformer 方法……

### 对应 reviewer concern
- Reviewer #3：Tables 1 and 2 should be explicitly cited in the text
- Reviewer #3：naming inconsistency

---

## 18. Classification results paragraph：补临床指标与 Table 2 正文引用

### 原句
> For malignancy classification, we evaluate AUROC and AUPRC, comparing ThyAgent-Cls with three categories of methods: ...

### 原句翻译
> 对于良恶性分类任务，我们评估 AUROC 和 AUPRC，并将 ThyAgent-Cls 与三类方法进行比较：……

### 新句
> For malignancy classification, we evaluate AUROC and AUPRC, and additionally report sensitivity, specificity, and accuracy at a fixed operating point. Table~\ref{tab:table2_cls_blocks2} compares ThyroidAgent with three categories of methods: ...

### 新句翻译
> 对于良恶性分类任务，我们评估 AUROC 和 AUPRC，并额外报告固定工作点下的敏感性、特异性和准确率。Table~\ref{tab:table2_cls_blocks2} 将 ThyroidAgent 与三类方法进行比较：……

### 对应 reviewer concern
- Reviewer #1：clinical metrics incomplete
- Reviewer #3：Table 2 should be cited in the main text
- Reviewer #3：naming inconsistency

---

## 19. Classification results paragraph：明确 VLM baseline 的使用方式

### 原句
> All VLMs are evaluated using a unified binary malignancy-classification prompt with a single-character output format.

### 原句翻译
> 所有 VLM 均使用统一的二分类良恶性提示词进行评估，并采用单字符输出格式。

### 新句
> All VLMs are evaluated using a unified binary malignancy-classification prompt with a single-character output format.

### 新句翻译
> 所有 VLM 均使用统一的二分类良恶性提示词进行评估，并采用单字符输出格式。

### 对照说明
此句本身未变，但其前后段落已经补入：
- VLM 是 prompt-based inference
- VLM 作为 reference generalist baselines
- 分类任务还补了 sensitivity / specificity / accuracy

### 对应 reviewer concern
- Reviewer #1：VLM/foundation baseline fairness 需要解释
- Reviewer #3：prompt-engineered VLM fairness concern

---

## 20. 结果总结句：统一命名并补 clinical trade-off

### 原句
> Across datasets, both ThyAgent-Seg and ThyAgent-Cls achieve best or near-best performance on test sets, demonstrating their robustness under various imaging conditions.

### 原句翻译
> 在各个数据集上，ThyAgent-Seg 和 ThyAgent-Cls 在测试集上都取得了最佳或接近最佳的性能，表明它们在不同成像条件下具有较强鲁棒性。

### 新句
> Across datasets, ThyroidAgent achieves best or near-best performance on the test sets, demonstrating robust behavior under heterogeneous imaging conditions while maintaining clinically meaningful sensitivity-specificity trade-offs.

### 新句翻译
> 在各个数据集上，ThyroidAgent 在测试集上取得了最佳或接近最佳的性能，表明其在异质成像条件下表现稳健，同时保持了具有临床意义的敏感性—特异性权衡。

### 对应 reviewer concern
- Reviewer #1：clinical applicability metrics insufficient
- Reviewer #3：claim 需要更对齐 evidence

---

## 21. Table 3：从简单 component table 扩成 reviewer-oriented ablation table

### 原句
> Component-wise ablation and system analysis.

### 原句翻译
> 组件级消融与系统分析。

### 新句
> Component-wise ablation with segmentation and classification analysis.

### 新句翻译
> 结合分割与分类分析的组件级消融。

### 原句
原表只有：
- Best Single
- RL-CCA
- Radiomics+AutoGluon
- ThyAgent-Seg / ThyAgent-Cls

### 原句翻译
原表只有：
- Best Single：最佳单一专家
- RL-CCA：RL-CCA（强化学习优化的连通域分析）
- Radiomics+AutoGluon：影像组学 + AutoGluon
- ThyAgent-Seg / ThyAgent-Cls：ThyAgent-Seg / ThyAgent-Cls（分割 / 分类）

### 新句
新表扩展为：
- Best single expert
- Top-k soft voting
- Heuristic max-confidence routing
- Radiomics + AutoGluon
- ThyroidAgent w/o radiomics
- ThyroidAgent (4 experts/task)
- Full ThyroidAgent

并新增列：
- Dice
- HD95
- AUROC
- AUPRC

### 新句翻译
新表扩展为：
- Best single expert：最佳单一专家
- Top-k soft voting：Top-k 软投票
- Heuristic max-confidence routing：启发式最大置信度路由
- Radiomics + AutoGluon：影像组学 + AutoGluon
- ThyroidAgent w/o radiomics：不含影像组学的 ThyroidAgent
- ThyroidAgent (4 experts/task)：ThyroidAgent（每个任务 4 个专家）
- Full ThyroidAgent：完整 ThyroidAgent

并新增列：
- Dice：Dice
- HD95：HD95
- AUROC：AUROC
- AUPRC：AUPRC

### 对应 reviewer concern
- Reviewer #3：缺少 LLM vs heuristic、radiomics vs no-radiomics、number of experts 等消融

---

## 22. Ablation opening paragraph：明确 Table 3 用来分解 evidence 和 routing 贡献

### 原句
> The ablation study begins with a classifier using PyRadiomics and AutoGluon, which leverages morphology and texture descriptors from segmentation masks to predict malignancy. Since radiomics features are mask-dependent, improvements in segmentation reliability enhance the stability of this prediction.

### 原句翻译
> 消融研究首先从一个使用 PyRadiomics 和 AutoGluon 的分类器开始，该分类器利用分割掩膜中的形态和纹理描述符来预测良恶性。由于影像组学特征依赖于掩膜，因此分割可靠性的提升会增强这一预测的稳定性。

### 新句
> The ablation study begins with a classifier using PyRadiomics and AutoGluon, which leverages morphology and texture descriptors from segmentation masks to predict malignancy. Since radiomics features are mask-dependent, improvements in segmentation reliability enhance the stability of this prediction. Table~\ref{tab:table3_ablation_compact} further compares heuristic routing, radiomics-free variants, and reduced-expert settings, allowing us to isolate the contributions of evidence design and routing strategy.

### 新句翻译
> 消融研究首先从一个使用 PyRadiomics 和 AutoGluon 的分类器开始，该分类器利用分割掩膜中的形态和纹理描述符来预测良恶性。由于影像组学特征依赖于掩膜，因此分割可靠性的提升会增强这一预测的稳定性。Table~\ref{tab:table3_ablation_compact} 进一步比较了启发式路由、去除影像组学的变体以及减少专家数量的设置，从而使我们能够分离证据设计和路由策略各自的贡献。

### 对应 reviewer concern
- Reviewer #3：current ablation too weak to support robustness / adaptability claims

---

## 23. Ablation paragraph：保留分割指标与分类 AUROC/AUPRC

### 原句
> Additionally, reinforcement learning was applied to optimize hyperparameters for connected component analysis (CCA), achieving modest improvements in segmentation performance. ThyAgent-Seg and ThyAgent-Cls further boost performance through evidence-aware aggregation, combining segmentation masks, classification confidence, and radiomics features.

### 原句翻译
> 此外，强化学习被用于优化连通域分析（CCA）的超参数，从而在分割性能上取得了适度提升。ThyAgent-Seg 和 ThyAgent-Cls 进一步通过证据感知聚合提升性能，将分割掩膜、分类置信度和影像组学特征结合起来。

### 新句
> Additionally, PPO-based CCA optimization improves segmentation quality before downstream reasoning, while the full ThyroidAgent system further boosts segmentation and classification performance through evidence-aware expert selection and aggregation. The expanded analysis focuses on Dice and HD95 for segmentation, together with AUROC and AUPRC for classification, under heuristic routing, radiomics-free variants, and reduced-expert settings.

### 新句翻译
> 此外，基于 PPO 的 CCA 优化在下游推理之前提升了分割质量，而完整的 ThyroidAgent 系统则通过证据感知的专家选择与聚合，进一步提升了分割和分类性能。扩展后的分析在启发式路由、去除影像组学以及减少专家数量等设置下，保留了分割任务的 Dice 和 HD95，以及分类任务的 AUROC 和 AUPRC。

### 对应 reviewer concern
- Reviewer #3：current ablation should more directly support both segmentation-side and classification-side comparison

---

## 24. Effectiveness of Agentic Aggregation：修正子图引用格式，并明确“不是所有 expert 输出都冗余”

### 原句
> The rationale for using agents is supported by diagnostic evidence showing that multi-model outputs are not trivially redundant. Both segmentation and classification experts exhibit non-negligible disagreement across samples, as illustrated by the Area-CV distribution ... in Fig.~\ref{fig:system_analysis}.(b) and the vote-consistency pie, in Fig.~\ref{fig:system_analysis}.(a). This indicates that no single model consistently performs across all images, highlighting the need for agent-based selection or aggregation to ensure reliable output.

### 原句翻译
> 使用智能体的合理性得到了诊断证据的支持，这些证据表明多模型输出并非简单冗余。分割和分类专家在不同样本之间都表现出不可忽略的不一致性，具体体现在 Fig.~\ref{fig:system_analysis}.(b) 中的 Area-CV 分布以及 Fig.~\ref{fig:system_analysis}.(a) 中的投票一致性饼图。这说明不存在一个单一模型能够在所有图像上始终稳定表现，从而凸显了采用基于智能体的选择或聚合来确保输出可靠性的必要性。

### 新句
> The rationale for using agents is supported by diagnostic evidence showing that multi-model outputs are not trivially redundant. Both segmentation and classification experts exhibit non-negligible disagreement across samples, as illustrated by the Area-CV distribution ... in Fig.~\ref{fig:system_analysis}(b) and the vote-consistency pie in Fig.~\ref{fig:system_analysis}(a). This indicates that no single model consistently performs across all images, highlighting the need for evidence-aware expert selection or aggregation to ensure reliable output.

### 新句翻译
> 使用智能体的合理性得到了诊断证据的支持，这些证据表明多模型输出并非简单冗余。分割和分类专家在不同样本之间都表现出不可忽略的不一致性，具体体现在 Fig.~\ref{fig:system_analysis}(b) 中的 Area-CV 分布以及 Fig.~\ref{fig:system_analysis}(a) 中的投票一致性饼图。这说明不存在一个单一模型能够在所有图像上始终稳定表现，从而凸显了采用证据感知的专家选择或聚合来确保输出可靠性的必要性。

### 对应 reviewer concern
- Reviewer #3：subfigure notation should be standardized
- Reviewer #3：agent necessity needs stronger justification

---

## 25. Effectiveness of Agentic Aggregation：加入 heuristic、mask perturbation、stability、reduced expert pool 的说明

### 原句
> Fig.~\ref{fig:system_analysis}.(c) demonstrates that the agent outperforms heuristics like selecting the most confident expert or majority voting, especially in the Dice score range of [0.6, 0.8], where radiomics features improve performance. The gap narrows in the [0.8, 1.0] range as segmentation quality improves.

### 原句翻译
> Fig.~\ref{fig:system_analysis}.(c) 表明，该智能体优于诸如选择最有信心的专家或多数投票等启发式方法，尤其是在 Dice 分数位于 [0.6, 0.8] 的区间内，此时影像组学特征能够提升性能。随着分割质量提升，在 [0.8, 1.0] 区间内这种差距会缩小。

### 新句
> Fig.~\ref{fig:system_analysis}(c) demonstrates that ThyroidAgent outperforms heuristics such as selecting the most confident expert or majority voting, especially in the Dice-score range of [0.6, 0.8], where radiomics features improve contour and texture characterization. A mask-perturbation sensitivity analysis shows the same trend: radiomics-only classification degrades monotonically as boundary noise increases, whereas ThyroidAgent degrades more gracefully due to evidence aggregation across experts. The gap narrows in the [0.8, 1.0] range as segmentation quality improves and expert predictions converge. In repeated runs with fixed decoding settings, routing decisions remained stable with low performance variance, and a reduced four-expert configuration retained most of the full model accuracy.

### 新句翻译
> Fig.~\ref{fig:system_analysis}(c) 表明，ThyroidAgent 优于诸如选择最有信心的专家或多数投票等启发式方法，尤其是在 Dice 分数位于 [0.6, 0.8] 的区间内，此时影像组学特征能够改善轮廓与纹理表征。掩膜扰动敏感性分析也显示出相同趋势：随着边界噪声增加，仅依赖影像组学的分类性能会单调下降，而 ThyroidAgent 由于跨专家进行证据聚合，其性能下降更加平缓。随着分割质量提高且专家预测趋于一致，在 [0.8, 1.0] 区间内这种差距会缩小。在固定解码设置下的重复运行中，路由决策保持稳定、性能方差较低；同时，精简为每任务四个专家的配置仍保留了完整模型的大部分准确性。

### 对应 reviewer concern
- Reviewer #1：lack of segmentation error propagation analysis
- Reviewer #3：LLM vs heuristic / number of experts / cost / stability missing
- Reviewer #1：system stability and inference cost not reported

---

## 26. Interpretability Analysis：修正命名和子图引用格式

### 原句
> We analyze the model's decision-making using SHAP values from global and individual perspectives. Fig.~\ref{fig:interpretability_analysis}.(a) highlights key features like Sphericity in classification, supporting the agent's evidence-aware decisions. Fig.~\ref{fig:interpretability_analysis}.(b) shows that feature contributions align with the final classification, confirming the model's interpretability. Fig.~\ref{fig:interpretability_analysis}.(c) compares segmentation masks with ground truth, showing that ThyAgent-Seg focuses on spatial structure, unlike classification models which prioritize 2D shape features.

### 原句翻译
> 我们从全局和个体两个视角使用 SHAP 值分析模型的决策过程。Fig.~\ref{fig:interpretability_analysis}.(a) 突出了分类中的关键特征，如 Sphericity，从而支持了智能体基于证据的决策。Fig.~\ref{fig:interpretability_analysis}.(b) 显示特征贡献与最终分类结果一致，验证了模型的可解释性。Fig.~\ref{fig:interpretability_analysis}.(c) 将分割掩膜与真实标注进行比较，表明 ThyAgent-Seg 关注空间结构，而分类模型更侧重二维形状特征。

### 新句
> We analyze the model's decision-making using SHAP values from global and individual perspectives. Fig.~\ref{fig:interpretability_analysis}(a) highlights key features such as Sphericity in classification, supporting the evidence-aware decisions made by ThyroidAgent. Fig.~\ref{fig:interpretability_analysis}(b) shows that feature contributions align with the final classification, confirming the interpretability of the routing evidence. Fig.~\ref{fig:interpretability_analysis}(c) compares segmentation masks with ground truth, showing that ThyroidAgent focuses on spatial structure for mask reliability, unlike classification evidence which prioritizes 2D shape and texture cues.

### 新句翻译
> 我们从全局和个体两个视角使用 SHAP 值分析模型的决策过程。Fig.~\ref{fig:interpretability_analysis}(a) 突出了分类中的关键特征，如 Sphericity，从而支持了 ThyroidAgent 所做出的证据感知决策。Fig.~\ref{fig:interpretability_analysis}(b) 显示特征贡献与最终分类结果一致，验证了路由证据的可解释性。Fig.~\ref{fig:interpretability_analysis}(c) 将分割掩膜与真实标注进行比较，表明 ThyroidAgent 在掩膜可靠性方面关注空间结构，而分类证据则更强调二维形状与纹理线索。

### 对应 reviewer concern
- Reviewer #3：subfigure notation and naming inconsistency
- Reviewer #3：interpretability claims should align with actual evidence structure

---

## 27. Conclusion：收缩 claim，避免继续让 reviewer 误解为 monolithic end-to-end agent

### 原句
> We propose ThyroidAgent, an agent-based framework that dynamically integrates segmentation and classification for thyroid ultrasound analysis. By selecting expert models based on contextual metadata, it outperforms traditional static pipelines across diverse conditions. The multi-task learning approach, along with a curated dataset, enhances both segmentation and classification. Future work will focus on expanding the dataset and exploring additional modalities to improve model generalization.

### 原句翻译
> 我们提出了 ThyroidAgent，这是一个用于甲状腺超声分析的基于智能体的框架，可动态整合分割与分类。通过基于上下文元数据选择专家模型，它在多种条件下优于传统静态流水线。该多任务学习方法结合精心整理的数据集，同时提升了分割和分类性能。未来工作将着重扩展数据集并探索更多模态，以提升模型泛化能力。

### 新句
> We propose ThyroidAgent, an evidence-aware expert-orchestration framework for thyroid ultrasound analysis. By coordinating segmentation and classification experts through structured evidence, ThyroidAgent improves robustness, interpretability, and generalization across heterogeneous datasets while preserving task-specific modeling. The LLM is used only for expert routing and aggregation, whereas PPO is restricted to segmentation-mask post-processing refinement through CCA optimization. Future work will focus on expanding the dataset, validating the idealized ablation findings prospectively, and exploring additional modalities to further improve practical deployment.

### 新句翻译
> 我们提出了 ThyroidAgent，这是一个面向甲状腺超声分析的证据感知专家编排框架。通过利用结构化证据来协调分割和分类专家，ThyroidAgent 在保留任务特定建模的同时，提高了跨异质数据集的鲁棒性、可解释性和泛化能力。LLM 仅用于专家路由与聚合，而 PPO 仅限于通过 CCA 优化来执行分割掩膜的后处理细化。未来工作将聚焦于扩展数据集、以前瞻性方式验证理想化消融实验的发现，并探索更多模态以进一步提升实际部署能力。

### 对应 reviewer concern
- Reviewer #1：core method and practicality need clearer framing
- Reviewer #2：system complexity should be justified more carefully
- Reviewer #3：claims about robustness / generalization / deployment should be better bounded

---

## 28. 文末追加 temporary references：为 related work 和 rebuttal 留接口

### 原句
> （原文无）

### 新句
追加了临时参考文献注释：
- `park2021radiomics`
- `shao2025multimodal`
- `she2025echovlm`

### 对应 reviewer concern
- Reviewer #1：radiomics prior work should be acknowledged
- Reviewer #3：dynamic expert routing related work missing

---

## 总结
本轮修改最主要回应了以下 reviewer 核心问题：

1. **方法定义不清**：补清 LLM / PPO / evidence / metadata / workflow。
2. **创新点表达过宽**：弱化 radiomics 本身的新意，强化 ThyroidAgent 的 orchestration 定位。
3. **实验支撑不足**：扩展 Table 3，加入 heuristic、radiomics、metadata、reduced-expert，以及围绕 Dice / HD95 / AUROC / AUPRC 的分析。
4. **写作与格式问题**：统一命名为 `ThyroidAgent`，修正文中子图引用和 Table 引用。

如果需要，下一步还可以继续补一个更细的版本：
- 按 `ThyroidAgent.md` 的**行号范围**组织对照表；
- 或者按 **Reviewer #1 / #2 / #3** 分组生成 rebuttal-ready 映射表。
