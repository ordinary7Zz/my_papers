% Template for ICASSP-2026 paper; to be used with:
%          spconf.sty  - ICASSP/ICIP LaTeX style file, and
%          IEEEbib.bst - IEEE bibliography style file.
% --------------------------------------------------------------------------
\documentclass{article}
\usepackage{spconf,amsmath,graphicx,hyperref}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{multirow}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{adjustbox}
\usepackage[table,xcdraw]{xcolor}

\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\centering\arraybackslash}X}

% Title.
% ------
\title{Dual-Path Cascade Framework with GT-Trained Radiomics Judge for Thyroid Ultrasound Diagnosis}
%
\name{Author(s) Name(s)\thanks{Thanks to XYZ agency for funding.}}
\address{Author Affiliation(s)}

\begin{document}
%\ninept
%
\maketitle
%
\begin{abstract}
We propose ThyroidAgent, a cascade inference framework for thyroid nodule ultrasound analysis that coordinates segmentation and classification experts through dual-path routing driven by classification consensus and a GT-trained radiomics judge. Unlike conventional approaches that rely on static pipelines, ThyroidAgent runs heterogeneous experts in parallel and splits each case into a consensus shortcut or a dispute-resolution path based on whether independent classifiers agree. A radiomics classifier trained on ground-truth masks serves as a dual-purpose judge, evaluating segmentation quality through feature-distribution distance while providing an independent malignancy signal for the selected mask. The LLM is invoked only in the hardest dispute cases, with lightweight rule-based reconciliation used otherwise, while connected-component post-processing refines segmentation masks when needed. This design improves interpretability, robustness, and adaptability across diverse ultrasound conditions.
Additionally, we curate a consolidated multi-source benchmark with aligned segmentation and classification annotations, enabling systematic cross-dataset evaluation and analysis of data factors that affect generalization.
Experimental results show that ThyroidAgent outperforms static models, demonstrating its potential for more reliable, context-aware clinical deployment.
\end{abstract}
%
\begin{keywords}
Ultrasound, Thyroid Nodule, Segmentation, Malignancy Classification, Cascade Inference
\end{keywords}
%
\section{Introduction}
\label{sec:intro}

\begin{figure*}[htb]
    \centering
    % ====== 图修改说明（Fig 1: Fig1.pdf）======
    % 需要重画为 dual-path cascade 架构图，内容应包含：
    % 1. 输入：甲状腺超声图像
    % 2. 并行专家池：上方为分割专家（DINOv3-UNet 变体 x3 + TransUNet + MedSegX + MedSAM2 + UltraFedFM），
    %    下方为独立分类专家（DINOv3-Multitask + MedSigLIP + BiomedCLIP），均不依赖 mask
    % 3. 共识检查模块：判断分类专家是否一致
    %    - 一致 → Path A（左路）：共识标签作为锚点 → 锚点指导分割选择 → CCA → 输出
    %    - 不一致 → Path B（右路）：GT-trained radiomics judge → 预筛选 → 分割选择 → CCA → AutoGluon 分类 → 规则/LLM 裁决
    % 4. GT-trained radiomics judge 用特殊图标标注（如天平/裁判符号），连接到 Path B 的分割选择和分类裁决
    % 5. LLM 模块仅出现在 Path B 最末端（最难争议时才调用）
    % 6. CCA 作为可选后处理，独立于主流程
    % 7. 整体风格：左→右数据流，Path A/B 用不同颜色区分（如绿/橙）
    % ============================================
    \includegraphics[width=1.0\linewidth]{figures/Fig1.pdf}
    \caption{Overview of the ThyroidAgent framework. While traditional systems use fixed pipelines, ThyroidAgent routes each case through a consensus shortcut or a dispute-resolution path, guided by a GT-trained radiomics judge that simultaneously assesses segmentation quality and provides an independent malignancy signal.}
    \label{fig:ThyroidAgent}
\end{figure*}

Recent advances in deep learning have greatly improved automated thyroid ultrasound analysis, with substantial progress in both nodule segmentation and malignancy classification~\cite{das2024deep}. For segmentation, prior methods have explored CNN and transformer-based designs to improve boundary delineation and robustness in noisy ultrasound images~\cite{gong2021multi,dong2024ultrasound,haribabu2025mlrt}, while recent classification models have improved malignancy prediction under data imbalance and imaging variability~\cite{gong_acl_2022,sujini2025automated}.
Nevertheless, these methods are typically developed and evaluated as separate components, leading to fixed task-specific pipelines.
This design limits the joint use of segmentation-derived structural evidence and classification confidence, which is crucial for reliable thyroid ultrasound diagnosis.

To address the limitations of task-specific pipelines, several studies have explored unified or multi-task formulations that couple nodule segmentation with malignancy classification~\cite{kang2022thyroid}. In parallel, thyroid-region priors have been incorporated via multi-task designs to improve nodule delineation under noisy ultrasound conditions~\cite{gong2021multi,gong_thyroid_2023}.
Collectively, these efforts suggest that exploiting task relatedness can improve robustness and provide more interpretable ultrasound analysis.
However, many existing formulations adopt relatively simple task coupling (e.g., ROI-based feature extraction, output concatenation, or shared encoders with task-specific heads), which may yield limited cross-task interaction and hinder effective joint optimization~\cite{he2023joint,rhanoui2025multi,wu2023multi}.
More advanced mechanisms are needed to fully leverage task correlations and optimize feature interactions.

In this work, we propose \textit{ThyroidAgent}, a cascade inference framework for thyroid ultrasound diagnosis that departs from conventional static pipelines by routing each case through a dual-path cascade driven by classification consensus and a GT-trained radiomics judge, across two coordinated tasks: segmentation and malignancy classification (Fig.~\ref{fig:ThyroidAgent}).
Instead of treating segmentation as an ROI-localization module, ThyroidAgent trains a radiomics classifier on ground-truth masks and uses it as a dual-purpose judge that simultaneously evaluates segmentation quality and provides an independent malignancy signal. Because these radiomics descriptors are extracted from image-mask pairs, their stability depends directly on segmentation quality. We therefore explicitly analyze how mask degradation propagates to downstream radiomics-based malignancy classification, rather than assuming that segmentation-derived evidence is uniformly reliable.

Motivated by the recent progress of large language models (LLMs)~\cite{dong_survey_2022} in reasoning and decision support, we explore their use in thyroid ultrasound diagnosis as a last-resort arbiter for the hardest cases~\cite{bai2025qwen3,sellergren2025medgemma}.
The LLM module receives structured evidence from multiple trained experts and performs arbitration only when independent classifiers disagree and rule-based reconciliation is ambiguous. Importantly, ThyroidAgent is not a monolithic LLM diagnosis system: task-specific segmentation and classification experts first produce candidate outputs in parallel, a GT-trained radiomics judge assesses segmentation quality and provides an independent malignancy signal, and the LLM operates only on structured evidence summaries rather than raw-image diagnosis. Connected-component analysis (CCA) is applied only as an optional mask-refinement step and is not part of the dual-path routing policy.

Related studies in thyroid CAD have also explored radiomics-assisted diagnosis, coupled segmentation-classification learning, and dynamic expert reasoning, but these lines are usually studied in isolation. Prior thyroid radiomics studies have shown that handcrafted morphology and texture descriptors can improve ultrasound malignancy assessment~\cite{park2021radiomics,shao2025multimodal}, while coupled-task frameworks have used shared supervision or interpretable constraints to connect segmentation and classification~\cite{kang2022thyroid,gong2021multi,gong_thyroid_2023}. More recent expert-routing and medical VLM systems suggest that dynamic reasoning over heterogeneous evidence can improve adaptability in complex imaging settings~\cite{she2025echovlm,bai2025qwen3,sellergren2025medgemma}. In particular, EchoVLM~\cite{she2025echovlm} introduces a universal ultrasound-specialized VLM with an internal dual-path mixture-of-experts architecture for multi-organ report generation, diagnosis, and VQA. By contrast, ThyroidAgent does not build a monolithic ultrasound VLM or perform token-level routing inside a foundation model. Instead, it targets thyroid nodule CAD specifically and performs case-level dual-path cascade routing over external segmentation and classification experts, driven by classification consensus and a GT-trained radiomics judge. In this sense, ThyroidAgent prioritizes explicit and auditable coordination between segmentation and malignancy classification, while EchoVLM prioritizes universal multimodal ultrasound understanding. Accordingly, ThyroidAgent uses the GT-trained radiomics judge not as a standalone novelty, but as the central evidence source that drives pre-filtering, segmentation selection, and classification reconciliation within a thyroid-specific cascade framework.

The key contributions of our method are summarized as below:
\textbf{1. Dual-path cascade routing with classification consensus.}
    We propose \emph{ThyroidAgent}, a cascade CAD framework that replaces the traditional static pipeline with dual-path routing. When independent classifiers reach consensus, a shortcut path uses the consensus label as an anchor to guide segmentation selection; otherwise, a dispute-resolution path invokes a GT-trained radiomics judge and lightweight rule-based or LLM-based reconciliation, enabling flexible and task-aware processing under heterogeneous acquisition conditions.
\textbf{2. GT-trained radiomics judge for joint segmentation assessment and classification.}
    We train an AutoGluon radiomics classifier on ground-truth masks and use it as a dual-purpose judge: it evaluates predicted-mask quality via feature-distribution distance (Mahalanobis) while simultaneously providing an independent malignancy probability for the selected mask. This judge drives pre-filtering, segmentation selection, and classification reconciliation, and we further quantify how segmentation-mask degradation propagates to radiomics-based classification, showing that the main impact arises from both feature distortion and train-test mask-source mismatch.
\textbf{3. Unified dataset consolidation and generalization analysis.}
    We curate a consolidated benchmark by harmonizing segmentation and classification annotations across multiple datasets, enabling cross-dataset evaluation and analysis of data factors affecting generalization in the cascade setting.

\begin{figure*}[htb]
    \centering
    % ====== 图修改说明（Fig 2: Fig2.pdf）======
    % 需要重画为 5-phase cascade workflow 图，内容应包含：
    %
    % 【离线阶段（左侧或顶部）】
    % 1. 专家池训练：DINOv3 变体（128/224/448）+ 异构架构（TransUNet/MedSegX/MedSAM2/UltraFedFM）
    %    分类专家：DINOv3-Multitask + MedSigLIP + BiomedCLIP
    % 2. GT-trained radiomics judge 训练：用 GT mask 提取 PyRadiomics 特征 → 训练 AutoGluon 分类器
    %    → 记录训练集特征均值/协方差（用于马氏距离）
    %
    % 【在线阶段（主流程，从左到右 5 个 Phase）】
    % Phase 1: 并行分割推理 — 多个分割专家各自输出 mask + confidence map
    % Phase 2: 并行分类推理 — 3 个独立分类专家各自输出 malignancy probability（无需 mask）
    % Phase 3: 共识检查 + 路径分流
    %   ├─ 共识达成（Path A）：锚点标签 → 锚点指导 SegSelect → CCA → 直接输出
    %   └─ 无共识（Path B）：进入 Phase 4
    % Phase 4: radiomics judge 评估每个 mask → 预筛选（cosine + 置信度离群过滤）
    %          → SegSelect（基于 judge + 形态学 + 一致性）→ CCA → AutoGluon 分类
    % Phase 5: 分类裁决
    %   ├─ 软投票与 AutoGluon 一致 → 采纳（规则裁决）
    %   ├─ 高置信分歧 → 信高置信方（规则裁决）
    %   └─ 模糊 → LLM 仲裁（仅此步调 LLM）
    %
    % 【标注要点】
    % - Path A 用绿色/浅色，Path B 用橙色/深色
    % - radiomics judge 用特殊图标（天平/盾牌）
    % - LLM 模块标注"仅 Path B 最难情况"
    % - 缓存/落盘节点可不画（工程细节）
    % - 每个专家用小图标表示（分割用 mask 图标，分类用概率条图标）
    % ============================================
    \includegraphics[width=1.0\linewidth]{figures/Fig2.pdf}
    \caption{Detailed workflow of the ThyroidAgent system, showing the cascade inference process with parallel expert inference, classification-consensus-driven path splitting, GT-trained radiomics judging, and rule-based or LLM-based reconciliation.}
    \label{fig:WorkFlow}
\end{figure*}

\section{Method}
\label{sec:method}

Fig.~\ref{fig:WorkFlow} illustrates the ThyroidAgent framework, which consists of parallel expert inference, a classification-consensus check that splits each case into a shortcut or dispute-resolution path, and a GT-trained radiomics judge that drives both segmentation selection and classification reconciliation.
The ThyroidAgent framework overcomes the limitations of relying on a single complex model by routing each case through a dual-path cascade that exploits classification consensus when available and falls back to multi-evidence reconciliation when experts disagree. The overall method contains five components: parallel expert prediction for the two tasks, classification-consensus check and path splitting, GT-trained radiomics judging, segmentation selection with pre-filtering, and classification reconciliation. Here, the LLM is invoked only in the hardest dispute cases, whereas CCA is used as an optional post-processing step and does not control the overall diagnostic policy.

\subsection{Toolbox for Ultrasound Analysis}
We define thyroid ultrasound analysis as a collection of tools with standardized inputs and outputs, enabling ThyroidAgent to compare expert models based on consistent evidence for reproducible results. The toolbox facilitates expert selection and improves prediction accuracy through three complementary components: a hybrid expert pool that includes DINOv3-based variants alongside heterogeneous architectures for both segmentation and classification, a GT-trained radiomics judge that simultaneously evaluates segmentation quality and provides an independent malignancy signal, and a CCA-based post-processing module that refines segmentation masks before downstream evidence aggregation when needed.

\subsubsection{Hybrid Expert Pool}
\label{sec:dinov3_models}
Our expert pool combines multiple DINOv3-based variants with heterogeneous architectures to improve robustness under cross-dataset variability. The DINOv3 variants share a common backbone with task-specific lightweight heads~\cite{simeoni2025dinov3} and are trained on stacked datasets with varying input resolutions (128, 224, 448) and dilation settings, providing a family of same-backbone experts whose diversity arises from training-condition perturbation. The pool also incorporates heterogeneous architectures that cover complementary inductive biases: for segmentation, transformer-based designs (TransUNet~\cite{chen2024transunet}), ultrasound-specific foundation models (UltraFedFM~\cite{jiang2025pretraining}), and SAM-style segmenters (MedSegX~\cite{zhang2025generalist}, MedSAM2~\cite{ma2025medsam2}); for classification, vision-language foundation models (MedSigLIP, BiomedCLIP) and lightweight convnets (ResNet-50~\cite{he2016deep}, RepViT~\cite{wang2023repvit}, LSNet~\cite{wang2025lsnet}) are included alongside the DINOv3 multitask head.
For the DINOv3 segmentation experts, we adopt a U-Net-style decoder with skip fusion to output a dense nodule mask probability map, optimized by a weighted BCE+IoU loss $\mathcal{L}_{\mathrm{seg}}$. For the DINOv3 classification experts, backbone features are summarized by global average and max pooling and fed into a compact attention-based head to output a malignancy logit, trained with a generalized logit-adjustment (GLA) loss to alleviate class imbalance.
The core weighting and logit adjustment used by $\mathcal{L}_{\mathrm{seg}}$ and GLA are:
\begin{equation}
\begin{aligned}
w &= 1 + 5 \cdot \left| \operatorname{AvgPool}_{31}(y) - y \right|,\\
z'_b &= z_b + \tau \left( y_b \log p_{\text{pos}} + (1-y_b)\log p_{\text{neg}} \right),
\end{aligned}
\label{eq:losses}
\end{equation}
where $y \in \{0,1\}^{H\times W}$ denotes the binary segmentation target, $\operatorname{AvgPool}_{31}(\cdot)$ is a $31\times31$ average-pooling operator used to emphasize boundary-aware pixels, and $w$ is the resulting spatial weight map used in $\mathcal{L}_{\mathrm{seg}}$. For classification, $y_b\in\{0,1\}$ is the binary malignancy label of sample $b$, $z_b$ is the original logit, $z'_b$ is the class-prior-adjusted logit, $p_{\text{pos}}$ and $p_{\text{neg}}$ are the empirical positive and negative class priors, and $\tau$ is the logit-adjustment coefficient. We use $\mathcal{L}_{\mathrm{bm}}$ to denote BCE-with-logits computed on $z'_b$, while the GLA objective refers to this class-prior-aware classification loss.

In recent years, the issue of dataset bias has remained a critical challenge in the development of reliable machine learning models~\cite{torralba2011unbiased}. Despite the increasing diversity and scale of modern datasets, recent studies show that neural networks can still easily capture dataset-specific biases, which may hinder generalization across diverse real-world conditions~\cite{liu2024decade}. Motivated by these findings, our design adopts a cascade paradigm that replaces static pipelines with dual-path expert routing. Specifically, independent classification experts first produce mask-free malignancy predictions; when they agree, their consensus serves as an anchor that guides segmentation selection, and when they disagree, a GT-trained radiomics judge and lightweight reconciliation resolve the conflict. This architecture is intended to explicitly mitigate cross-dataset and cross-device bias by avoiding reliance on a single fixed model whose behavior may be overly coupled to training data idiosyncrasies. As validated in Sec.~\ref{sec:effectiveness}, dual-path cascade routing offers a practical and more stable, interpretable alternative to a single fixed model, improving robustness and generalization under heterogeneous clinical acquisition conditions via context-aware decision-making.

\subsubsection{GT-Trained Radiomics Judge}
\label{sec:radiomics_judge}
A key component of ThyroidAgent is a \emph{GT-trained radiomics judge}: an AutoGluon tabular classifier trained on radiomics features extracted from ground-truth masks. Unlike mask-guided radiomics descriptors used in prior work solely as classification evidence, this judge serves a dual purpose---it simultaneously assesses segmentation quality and provides an independent malignancy signal for each predicted mask. Given an image $x$ and a mask $M$, we extract a 2D PyRadiomics feature vector $f = \phi(x, M)$ covering shape2D and texture families. Representative formulations include:
\begin{equation}
\begin{aligned}
A = \sum_{x=1}^{H} \sum_{y=1}^{W} \mathbb{I} \left[ M(x,y) = 1 \right], \\
\mathrm{Energy} = \sum_{i=1}^{N_g} \sum_{j=1}^{N_g} P(i,j)^2,
\end{aligned}
\end{equation}
where $A$ denotes the ROI area, $M(x,y) \in \{0,1\}$ is the binary ROI mask at spatial coordinate $(x,y)$, $\mathbb{I}[\cdot]$ is the indicator function, $H \times W$ is the mask resolution, $\mathrm{Energy}$ is the gray-level co-occurrence matrix (GLCM) energy, $P(i,j)$ is the normalized GLCM entry associated with gray levels $i$ and $j$, and $N_g$ is the number of discretized gray levels used in radiomics quantization. The judge $g_\theta$ is trained on $\{(f_i, y_i)\}_{i=1}^{N}$ where $f_i = \phi(x_i, M_i^{\mathrm{GT}})$ are features extracted from ground-truth masks and $y_i$ is the malignancy label. At inference time, for each predicted mask $M_k$, the judge outputs a malignancy probability $p_{\mathrm{judge}}^{(k)} = g_\theta(\phi(x, M_k))$ and a confidence $c_{\mathrm{judge}}^{(k)} = \max(p_{\mathrm{judge}}^{(k)}, 1-p_{\mathrm{judge}}^{(k)})$. The intuition is that a more accurate mask yields radiomics features closer to the GT training distribution, producing more reliable classification confidence. To quantify this deviation, we compute the Mahalanobis distance:
\begin{equation}
d_{\mathrm{mah}}^{(k)} = \sqrt{(f_k - \boldsymbol{\mu}_{\mathrm{GT}})^{\top} \boldsymbol{\Sigma}_{\mathrm{GT}}^{-1} (f_k - \boldsymbol{\mu}_{\mathrm{GT}})},
\label{eq:mahalanobis}
\end{equation}
where $\boldsymbol{\mu}_{\mathrm{GT}}$ and $\boldsymbol{\Sigma}_{\mathrm{GT}}$ are the mean and covariance of GT-mask features in the training set. A large $d_{\mathrm{mah}}^{(k)}$ indicates that mask $M_k$ produces features inconsistent with GT-trained statistics, signaling a potentially unreliable segmentation. Together, $\{p_{\mathrm{judge}}^{(k)}, c_{\mathrm{judge}}^{(k)}, d_{\mathrm{mah}}^{(k)}\}$ form the judge evidence that drives pre-filtering, segmentation selection, and classification reconciliation in the cascade.

\subsubsection{Connected Component Analysis for Mask Refinement}
We apply connected component analysis (CCA) to refine segmentation masks before downstream evidence construction when needed~\cite{liu2025shapekit}. CCA suppresses isolated noisy regions and preserves the largest anatomically plausible connected structure, improving mask consistency for subsequent radiomics judging and classification reconciliation. This refinement step is deterministic and independent of the radiomics judge and any LLM-based arbitration.

\begin{algorithm}[t]
\caption{ThyroidAgent cascade inference}
\label{alg:thyroidagent_inference}
\begin{algorithmic}[1]
\Require Image $x$; seg experts $\mathcal{E}_{seg}$; cls experts $\mathcal{E}_{cls}$; radiomics judge $g_\theta$
\Ensure Final mask $\hat{M}$, label $\hat{y}$, confidence $\hat{p}$

\Statex \textbf{Phase 1--2: Parallel expert inference}
\State $\{M_k\}_{k=1}^{K} \gets \mathrm{RunSeg}(\mathcal{E}_{seg}, x)$
\State $\{p_m\}_{m=1}^{M} \gets \mathrm{RunCls}(\mathcal{E}_{cls}, x)$ \Comment{mask-free}

\Statex \textbf{Phase 3: Consensus check \& path split}
\State consensus $\gets \big[\arg\max_m p_m \text{ all equal}\big]$
\If{consensus}
  \State $a \gets$ consensus class \Comment{classification anchor}
  \State $\hat{k} \gets \mathrm{SegSelect}(\{M_k\}, g_\theta, a)$ \Comment{anchor-guided}
  \State $\hat{M} \gets \mathrm{CCARefine}(M_{\hat{k}})$; $\hat{y} \gets a$
  \State \Return $\hat{M}, \hat{y}$ \Comment{Path A: shortcut}
\EndIf

\Statex \textbf{Phase 4: Pre-filter \& mask selection (Path B)}
\State $\{M_k\} \gets \mathrm{PreFilter}(\{M_k\}, g_\theta)$ \Comment{outlier removal}
\State $\hat{k} \gets \mathrm{SegSelect}(\{M_k\}, g_\theta, \mathrm{None})$
\State $\hat{M} \gets \mathrm{CCARefine}(M_{\hat{k}})$

\Statex \textbf{Phase 5: Classification reconciliation}
\State $p_{\mathrm{rad}} \gets g_\theta\big(\phi(x, \hat{M})\big)$ \Comment{AutoGluon on selected mask}
\State $\hat{y}, \hat{p} \gets \mathrm{Reconcile}(\{p_m\}, p_{\mathrm{rad}})$
\If{$\mathrm{softvote} \neq p_{\mathrm{rad}}$}
  \State $\hat{y}, \hat{p} \gets \mathrm{LLMArbitrate}(\{p_m\}, p_{\mathrm{rad}}, \hat{M})$
\EndIf
\State \Return $\hat{M}, \hat{y}, \hat{p}$
\end{algorithmic}
\end{algorithm}

In Algorithm~\ref{alg:thyroidagent_inference}, $\mathrm{SegSelect}(\cdot)$ denotes the segmentation selection function that consumes radiomics-judge evidence together with morphological and inter-model agreement metrics, $\mathrm{PreFilter}(\cdot)$ removes outlier masks based on cosine similarity and judge-confidence deviation with a safety floor of $\max(3, K/2)$ retained models, and $\mathrm{Reconcile}(\cdot)$ performs weighted soft voting and compares it with the AutoGluon prediction, invoking $\mathrm{LLMArbitrate}(\cdot)$ only when both signals are ambiguous. The routing LLM uses low-temperature decoding (temperature 0.3, bounded output length) and a strict JSON decision schema to ensure deterministic arbitration.

\subsection{Cascade Inference with Dual-Path Routing}
Fig.~\ref{fig:WorkFlow} overviews ThyroidAgent as a cascade workflow with offline expert construction and online dual-path routing. Multiple segmentation and classification experts are trained on stacked datasets and organized into an expert pool with a registry that records validation performance, training-set scale, and input resolution. The GT-trained radiomics judge (Sec.~\ref{sec:radiomics_judge}) is constructed offline from ground-truth masks and reused at inference for both segmentation assessment and classification.

As illustrated in Fig.~\ref{fig:WorkFlow} and Algorithm~\ref{alg:thyroidagent_inference}, during inference we first run all segmentation experts and all independent mask-free classification experts in parallel. We then check whether the independent classifiers reach consensus, i.e., whether $\arg\max_m p_m$ is identical across all $M$ classifiers. When all independent classifiers agree, the consensus class serves as a classification anchor: the segmentation selector prefers masks whose radiomics-judge prediction is consistent with the anchor, while still using morphological quality and inter-model agreement as secondary signals, and the final malignancy label is taken directly from the anchor, bypassing AutoGluon and the LLM entirely (Path~A). When the independent classifiers disagree, no anchor is available, and the system proceeds through pre-filtering, radiomics-judge-guided mask selection, AutoGluon classification on the selected mask, and rule-based or LLM-based reconciliation (Path~B).

In Path~B, a deterministic pre-filter removes candidate masks whose radiomics feature vectors are cosine-similarity outliers relative to the group or whose judge confidence deviates strongly from the group median, with a safety floor of $\max(3, K/2)$ retained models preventing over-aggressive pruning. The segmentation selector $\mathrm{SegSelect}(\cdot)$ then ranks the surviving masks using a priority order that favors radiomics-judge consistency and reasonable Mahalanobis distance, inter-model agreement, morphological plausibility, and device and dataset compatibility. When the LLM is enabled, the selector formats these structured signals into a compact JSON prompt and asks the LLM to return a single best model or a weighted top-$k$ ensemble; when disabled, a static rule selecting the highest-agreement model is used. The selected mask is optionally refined by CCA before downstream use.

Given the selected mask $\hat{M}$, the GT-trained radiomics judge produces a malignancy probability $p_{\mathrm{rad}} = g_\theta(\phi(x, \hat{M}))$, while a weighted soft-voting over the independent classifiers yields a vote-based prediction $\hat{y}_{\mathrm{sv}}$. If $p_{\mathrm{rad}}$ and $\hat{y}_{\mathrm{sv}}$ agree, the shared label is adopted with confidence boosted by agreement; if they disagree but one side is high-confidence ($>0.8$) while the other is low-confidence, the high-confidence side is preferred; if both are ambiguous, the LLM is invoked with the independent predictions, AutoGluon output, and segmentation reasoning as structured evidence, returning a final label with a strict JSON schema. This multi-tier strategy ensures that the LLM is used only on the hardest cases, while the majority of predictions are resolved by efficient rule-based reconciliation.

% TODO: 数据为随机占位，待真实实验结果替换
\begin{table*}[htbp]
    \begin{center}
    \caption{Performance comparison of segmentation models across 5 datasets.}
    \label{tab:table1_seg_blocks}
    \begin{tabular}{c|cc|cc|cc|cc|cc}
        \toprule
        \multirow{2}{*}{\textbf{Method}} &
        \multicolumn{2}{c|}{\textbf{TN3K}} &
        \multicolumn{2}{c|}{\textbf{DDTI}} &
        \multicolumn{2}{c|}{\textbf{ThyroidXL}} &
        \multicolumn{2}{c|}{\textbf{PKTN}} &
        \multicolumn{2}{c}{\textbf{TN5K}}
        \\
        & Dice & HD95 & Dice & HD95 & Dice & HD95 & Dice & HD95 & Dice & HD95\\
        \midrule
        TransUNet~\cite{chen2024transunet} & 81.84 & 14.92 & 74.43 & 24.37 & 85.75 & 27.42 & 76.89 & 36.88 & 78.54 & 32.32 \\
        MedSegX~\cite{zhang2025generalist} & 83.93 & 10.95 & 85.34 & 10.44 & 79.98 & 11.07 & 80.63 & 10.83 & 83.10 & 11.76 \\
        MedSAM2~\cite{ma2025medsam2} & 84.47 & 11.51 & 84.90 & 9.68 & 83.74 & 6.91 & 80.71 & 10.69 & 81.22 & 10.12 \\
        UltraFedFM~\cite{jiang2025pretraining} & 81.18 & 14.98 & 75.55 & 18.10 & 84.70 & 8.10 & 75.31 & 16.08 & 77.13 & 14.96 \\
        \midrule
        \rowcolor{lightgray}
        \textbf{ThyroidAgent} & \textbf{85.28} & \textbf{10.31} & \textbf{85.16} & \textbf{9.44} & \textbf{87.58} & \textbf{5.43} & \textbf{82.96} & \textbf{9.01} & \textbf{83.26} & \textbf{10.94}\\
        \bottomrule
    \end{tabular}
  \end{center}
\end{table*}

\section{Experiment}
\label{sec:experiment}
\subsection{Experimental Details}
We evaluate on a consolidated thyroid ultrasound benchmark assembled from multiple sources, including TN3K~\cite{gong2021multi}, TN5K~\cite{zhang2025tn5000}, DDTI~\cite{pedraza2015open}, ThyroidXL~\cite{duong2025thyroidxl}, and PKTN~\cite{sun2025clip}, spanning heterogeneous acquisition protocols and device settings. The segmentation task predicts a binary nodule mask, and the classification task predicts benign or malignant labels.
All splits are performed at the patient level to avoid leakage, using a 0.7/0.15/0.15 split protocol where applicable.
We then construct stacked training sets by merging the training portions across datasets, the largest stacked set contains 26,074 images.
To build a diverse expert pool, we train multiple DINOv3-based variants for each task by varying the stacked training set, dilation design, and input resolution (128, 224, and 448), and additionally include heterogeneous architectures: TransUNet~\cite{chen2024transunet}, UltraFedFM~\cite{jiang2025pretraining}, MedSegX~\cite{zhang2025generalist}, and MedSAM2~\cite{ma2025medsam2} for segmentation, and MedSigLIP and BiomedCLIP for classification.
The downstream ThyroidAgent cascade then selects and reconciles from these expert outputs during inference. A GT-trained AutoGluon radiomics judge is constructed from ground-truth masks and reused for segmentation assessment, pre-filtering, and classification reconciliation. All trainable baselines and expert models are trained under a harmonized split-and-test protocol wherever adaptation is possible, using PyTorch (v2.4.1), AdamW, a learning rate of $1e-4$, batch size 12, and 50 epochs on 3$\times$48\,GB NVIDIA RTX A6000 GPUs. For the open-source VLM baselines, MedGemma and Qwen3-VL-8B-Instruct are adapted to the binary malignancy-classification task using LoRA-based fine-tuning, while the proprietary GPT-5.1 baseline is evaluated only through prompt-based API inference. MedGemma and Qwen3-VL are implemented as image-conditioned generative classifiers with binary textual targets (0 for benign, 1 for malignant), and their malignancy scores are obtained by comparing the conditional likelihoods of the two candidate answers during inference. In the LLM arbitration module, low-temperature decoding (temperature 0.3, bounded output length) is used to stabilize JSON-form decisions, and the LLM is invoked only in Path B cases where rule-based reconciliation is ambiguous.

\paragraph{Cross-mask-source radiomics sensitivity protocol.}
To quantify how segmentation-mask errors propagate to radiomics-based classification, we conduct a dedicated cross-mask-source experiment on TN5K. We compare four ROI sources: ground-truth masks (\texttt{gt}), two GT-based synthetic perturbation settings with mild and moderate boundary noise (\texttt{gt\_mild\_perturb} and \texttt{gt\_moderate\_perturb}), and predicted masks produced by the segmentation model (\texttt{pred}). For each mask source, radiomics features are extracted under the same PyRadiomics pipeline and used to train an AutoGluon classifier. We then evaluate all $4\times4$ train/test combinations to disentangle the effects of mask degradation during training and inference. We report AUROC, AUPRC, ACC, sensitivity, and specificity. Here, the mild and moderate settings serve as controlled GT-based perturbation proxies, whereas \texttt{pred} represents real segmentation errors produced by the deployed segmentation model.

\subsection{Main Experimental Results: Segmentation and Classification}
Segmentation performance is evaluated using Dice (\%) and HD95. Table~\ref{tab:table1_seg_blocks} compares ThyroidAgent against three categories of methods: general-purpose segmenters (MedSegX~\cite{zhang2025generalist}, MedSAM2~\cite{ma2025medsam2}), a specialized ultrasound model (UltraFedFM~\cite{jiang2025pretraining}), and a recent advanced transformer-based approach (TransUNet~\cite{chen2024transunet}).
% TODO: 数据为随机占位，待真实实验结果替换
\begin{table*}[htbp]
    \begin{center}
    \caption{Performance comparison of classification models across 4 datasets.}
    \label{tab:table2_cls_blocks2}
    \begin{tabular}{c|cc|cc|cc|cc}
        \toprule
        \multirow{2}{*}{\textbf{Method}} &
        \multicolumn{2}{c|}{\textbf{TN3K}} &
        \multicolumn{2}{c|}{\textbf{DDTI}} &
        \multicolumn{2}{c|}{\textbf{ThyroidXL}} &
        \multicolumn{2}{c}{\textbf{TN5K}}
        \\
        & {\scriptsize AUROC} & {\scriptsize AUPRC} & {\scriptsize AUROC} & {\scriptsize AUPRC}
        & {\scriptsize AUROC} & {\scriptsize AUPRC} & {\scriptsize AUROC} & {\scriptsize AUPRC} \\
        \midrule
        MedSigLIP & 0.831 & 0.762 & 0.798 & 0.421 & 0.924 & 0.895 & 0.941 & 0.971 \\
        BiomedCLIP & 0.798 & 0.715 & 0.762 & 0.385 & 0.905 & 0.871 & 0.928 & 0.965 \\
        ResNet-50~\cite{he2016deep} & 0.767 & 0.687 & 0.674 & 0.248 & 0.904 & 0.888 & 0.932 & 0.967 \\
        RepViT~\cite{wang2023repvit} & 0.514 & 0.380 & 0.640 & 0.183 & 0.561 & 0.511 & 0.375 & 0.665 \\
        LSNet~\cite{wang2025lsnet} & 0.789 & 0.758 & 0.775 & 0.318 & 0.917 & 0.904 & 0.909 & 0.955 \\
        UltraFedFM~\cite{jiang2025pretraining} & 0.765 & 0.813 & 0.675 & 0.741 & 0.825 & 0.852 & 0.827 & 0.761 \\
        MedGemma~\cite{sellergren2025medgemma} & 0.849 & 0.804 & 0.825 & 0.453 & 0.937 & 0.909 & 0.944 & 0.974 \\
        Qwen3-VL-8B-Instruct~\cite{bai2025qwen3} & 0.823 & 0.761 & 0.736 & 0.311 & 0.905 & 0.878 & 0.921 & 0.963 \\
        GPT-5.1~\cite{openai2025gpt5systemcard} & 0.640 & 0.487 & 0.705 & 0.330 & 0.599 & 0.472 & 0.673 & 0.843 \\
        \midrule
        \rowcolor{lightgray}
        \textbf{ThyroidAgent} & \textbf{0.869} & 0.790 & \textbf{0.845} & 0.542 & \textbf{0.951} & \textbf{0.920} & \textbf{0.961} & \textbf{0.985}\\
        \bottomrule
    \end{tabular}
  \end{center}
\end{table*}
For malignancy classification, we evaluate AUROC and AUPRC. Table~\ref{tab:table2_cls_blocks2} compares ThyroidAgent with four categories of methods: medical vision-language models (MedSigLIP, BiomedCLIP), ultrasound-specific models (UltraFedFM~\cite{jiang2025pretraining}), general-purpose classifiers (LSNet~\cite{wang2025lsnet}, RepViT~\cite{wang2023repvit}, ResNet50~\cite{he2016deep}), and vision-language models (Qwen3-VL-8B-Instruct~\cite{bai2025qwen3}, MedGemma-4B~\cite{sellergren2025medgemma}, GPT-5.1~\cite{openai2025gpt5systemcard}).
Open-source VLM baselines are adapted to the thyroid malignancy task using LoRA-based fine-tuning and evaluated with binary image-conditioned prompts, whereas GPT-5.1 is used only through prompt-based API inference rather than task-specific adaptation.
Across datasets, ThyroidAgent achieves best or near-best performance on the test sets, demonstrating robust behavior under heterogeneous imaging conditions.

\subsection{System Analysis}
\subsubsection{Impact of Segmentation Mask Errors on Radiomics-Based Classification.}
To isolate the effect of mask quality on radiomics, we performed a $4\times4$ cross-mask-source experiment on TN5K using GT masks, two GT-based perturbation settings, and predicted masks. Table~\ref{tab:cross_mask_source_tn5k} reports the full AUROC/AUPRC matrix.

% TODO: 数据为随机占位，待真实实验结果替换
\begin{table*}[htbp]
    \centering
    \caption{Cross-mask-source analysis of radiomics-based classification on TN5K. Each cell reports AUROC / AUPRC. \textbf{gt}, \textbf{mild}, \textbf{moderate}, and \textbf{pred} denote GT masks, GT-based mild perturbations, GT-based moderate perturbations, and predicted masks, respectively.}
    \label{tab:cross_mask_source_tn5k}
    \resizebox{0.7\linewidth}{!}{%
    \begin{tabular}{c|cccc}
        \toprule
        \multirow{2}{*}{\textbf{Train source}} & \multicolumn{4}{c}{\textbf{Test source}} \\
        \cmidrule(lr){2-5}
        & \textbf{gt} & \textbf{mild} & \textbf{moderate} & \textbf{pred} \\
        \midrule
        \textbf{gt} & 0.860 / 0.923 & 0.843 / 0.914 & 0.821 / 0.909 & 0.793 / 0.892 \\
        \textbf{mild} & 0.853 / 0.917 & 0.845 / 0.914 & 0.848 / 0.924 & 0.798 / 0.897 \\
        \textbf{moderate} & 0.850 / 0.915 & 0.847 / 0.912 & 0.867 / 0.926 & 0.811 / 0.912 \\
        \textbf{pred} & 0.835 / 0.912 & 0.832 / 0.913 & 0.825 / 0.912 & 0.853 / 0.924 \\
        \bottomrule
    \end{tabular}%
    }
\end{table*}

When training is fixed on GT masks, AUROC decreases monotonically from 0.860 (\textbf{gt}$\rightarrow$\textbf{gt}) to 0.843 (\textbf{gt}$\rightarrow$\textbf{mild}), 0.821 (\textbf{gt}$\rightarrow$\textbf{moderate}), and 0.793 (\textbf{gt}$\rightarrow$\textbf{pred}), confirming that segmentation degradation directly weakens downstream radiomics classification.

A weaker degradation trend is observed when the test masks are fixed to GT and the training masks are degraded, where AUROC changes from 0.860 (\textbf{gt}$\rightarrow$\textbf{gt}) to 0.853 (\textbf{mild}$\rightarrow$\textbf{gt}), 0.850 (\textbf{moderate}$\rightarrow$\textbf{gt}), and 0.835 (\textbf{pred}$\rightarrow$\textbf{gt}). This indicates that radiomics-based classification is more sensitive to inference-time mask quality than to training-time mask degradation.

Importantly, \textbf{pred}$\rightarrow$\textbf{pred} reaches an AUROC of 0.853, close to \textbf{gt}$\rightarrow$\textbf{gt}, which suggests that predicted-mask radiomics still retain substantial diagnostic information when the classifier is trained on the same mask distribution. The large gap between \textbf{gt}$\rightarrow$\textbf{pred} and \textbf{pred}$\rightarrow$\textbf{pred} therefore indicates that much of the degradation comes from train-test mask-source mismatch, not only from absolute loss of information.

Real predicted masks also produce a larger drop than the GT-based perturbation proxies. Under GT training, \textbf{gt}$\rightarrow$\textbf{pred} performs worse than \textbf{gt}$\rightarrow$\textbf{moderate} (0.793 vs. 0.821), and specificity falls sharply from 0.602 in \textbf{gt}$\rightarrow$\textbf{gt} to 0.271 in \textbf{gt}$\rightarrow$\textbf{pred}. This suggests that real segmentation errors introduce not only boundary noise, but also a more complex structural bias that shifts radiomics feature distributions and decision thresholds.

\begin{figure*}[htb]
    \centering
    % ====== 图修改说明（Fig 3: Fig3.pdf）======
    % 需要重画为 cascade 系统分析图，包含 3 个子图：
    %
    % (a) 分类共识与路径分布（饼图或堆叠条形图）：
    %     - Path A（共识快捷）占比 vs Path B（争议裁决）占比
    %     - 可按数据集分组（TN3K/DDTI/ThyroidXL/TN5K）
    %     - 标注各路径的平均置信度
    %     - 替代原来的 "Cls vote consistency distribution"
    %
    % (b) 分割模型间分歧分布（Area-CV 直方图，保留）：
    %     - X 轴：Area-CV（面积变异系数）
    %     - Y 轴：样本数
    %     - 标注中位数（0.057）和 90th percentile（0.250）
    %     - 可叠加 Path A/B 的分布（不同颜色）
    %     - 保留原有数据
    %
    % (c) 分类性能 vs 分割质量（分组条形图，保留但调整）：
    %     - X 轴：Seg Dice-score bins（[0-0.2], [0.2-0.4], [0.4-0.6], [0.6-0.8], [0.8-1.0]）
    %     - Y 轴：AUROC
    %     - 分组条：独立分类模型 soft-voting vs radiomics judge vs ThyroidAgent full
    %     - 重点展示 [0.6, 0.8] 区间 ThyroidAgent 的优势
    %     - 标注性能差距收窄的 [0.8, 1.0] 区间
    %
    % 【整体风格】
    % - 3 个子图横排，共享标题
    % - Path A 用绿色，Path B 用橙色
    % - radiomics judge 相关数据用蓝色
    % ============================================
    \includegraphics[width=1.0\linewidth]{figures/Fig3.pdf}
    \caption{Analysis of dual-path cascade routing.
    (a) Path A/B distribution and consensus ratio across datasets.
    (b) Distribution of Seg disagreement scores (Area-CV).
    (c) Cls performance across Seg Dice-score bins.}
    \label{fig:system_analysis}
\end{figure*}

\subsubsection{Effectiveness of Dual-Path Cascade Routing.}
\label{sec:effectiveness}
The rationale for using dual-path cascade routing is supported by the fact that multi-model outputs are not trivially redundant. Both segmentation and classification experts exhibit non-negligible disagreement across samples, as illustrated by the Area-CV distribution (median = 0.057, 90th percentile = 0.250) in Fig.~\ref{fig:system_analysis}(b) and the vote-consistency pie in Fig.~\ref{fig:system_analysis}(a). This indicates that no single model consistently performs across all images, which motivates the consensus-based path split and radiomics-judge-driven selection.

Fig.~\ref{fig:system_analysis}(c) further shows that ThyroidAgent outperforms heuristics such as selecting the most confident expert or majority voting, especially in the Dice-score range of [0.6, 0.8], where radiomics features improve contour and texture characterization. Consistent with the cross-mask-source analysis above, radiomics-only classification is sensitive to mask-source shift and segmentation degradation. This sensitivity further motivates ThyroidAgent as a multi-evidence cascade framework, in which the GT-trained radiomics judge contributes as one informative but not exclusively trusted evidence source. The performance gap narrows in the [0.8, 1.0] range as segmentation quality improves and expert predictions converge.

\begin{figure*}[htb]
    \centering
    % ====== 图修改说明（Fig 4: Fig4.pdf）======
    % 需要重画为 radiomics judge 可解释性分析图，包含 3 个子图：
    %
    % (a) SHAP 全局特征重要性（水平条形图）：
    %     - 展示 GT-trained radiomics judge 的 top-10/15 特征
    %     - 分组显示：shape2D 特征（如 Sphericity, Elongation, Area）
    %                texture 特征（如 LRHGLE, SRHGLE, GLCM Energy）
    %     - 标注特征对恶性预测的方向（正/负贡献）
    %     - 替代原来的 "key features in classification"
    %
    % (b) SHAP waterfall 图（单案例，保留）：
    %     - 展示一个典型案例的 SHAP 值瀑布图
    %     - 从 base value 到最终预测值的特征贡献分解
    %     - 标注最终分类决策（如 "Malignant, p=0.82"）
    %     - 体现 radiomics judge 如何综合多个特征做决策
    %
    % (c) 分割 mask 可视化对比（保留但增强）：
    %     - 展示 2-3 个案例，每个案例一行：
    %       原图 | GT mask | Model A mask | Model B mask | Selected mask | Mahalanobis distance
    %     - 标注各 mask 的 radiomics judge 置信度和马氏距离
    %     - 体现 judge 如何区分高质量/低质量 mask
    %     - 可用热力图叠加显示 judge 关注的区域
    %
    % 【整体风格】
    % - 3 个子图竖排或横排
    % - SHAP 图用红蓝双色（正/负贡献）
    % - mask 可视化用叠加透明度
    % - 马氏距离用颜色编码（绿=近, 红=远）
    % ============================================
    \includegraphics[width=1.0\linewidth]{figures/Fig4.pdf}
    \caption{Interpretability analysis of the GT-trained radiomics judge: (a) global SHAP feature importance, (b) case-level SHAP waterfall for a malignancy prediction, (c) segmentation mask comparison with judge confidence and Mahalanobis distance.}
    \label{fig:interpretability_analysis}
\end{figure*}

\subsubsection{Interpretability Analysis.}
We analyze the model's decision-making using SHAP values from global and individual perspectives. Fig.~\ref{fig:interpretability_analysis}(a) highlights key features such as Sphericity in classification, supporting the cascade decisions made by ThyroidAgent. Fig.~\ref{fig:interpretability_analysis}(b) shows that feature contributions align with the final classification, confirming the interpretability of the radiomics-judge evidence. Fig.~\ref{fig:interpretability_analysis}(c) compares segmentation masks with ground truth, showing that ThyroidAgent focuses on spatial structure for mask reliability, unlike classification evidence which prioritizes 2D shape and texture cues.

\section{Conclusion}
\label{sec:conclusion}
We propose ThyroidAgent, a cascade inference framework for thyroid ultrasound analysis that routes each case through a consensus shortcut or a dispute-resolution path guided by a GT-trained radiomics judge. By coupling classification consensus with segmentation selection and using a GT-trained radiomics classifier as a dual-purpose judge for both segmentation quality and malignancy prediction, ThyroidAgent improves robustness, interpretability, and generalization across heterogeneous datasets while preserving task-specific modeling. The LLM is invoked only in the hardest dispute cases, whereas CCA is restricted to optional segmentation-mask post-processing refinement.
Our analysis further shows that segmentation-mask errors affect radiomics-based classification through both feature distortion and train-test mask-source mismatch: predicted-mask radiomics remain informative when training and testing use the same source, yet mismatched GT-derived and prediction-derived radiomics cause a marked performance drop. Future work will focus on expanding the dataset, validating the idealized ablation findings prospectively, and exploring additional modalities to further improve practical deployment.

% References should be produced using the bibtex program from suitable
% BiBTeX files (here: strings, refs, manuals). The IEEEbib.bst bibliography
% style file from IEEE produces unsorted bibliography list.
% -------------------------------------------------------------------------
\bibliographystyle{IEEEbib}
\bibliography{ref}

\end{document}
