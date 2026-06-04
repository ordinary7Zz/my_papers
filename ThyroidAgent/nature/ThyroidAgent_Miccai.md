这个文档记录了ThyroidAgent论文（投稿在miccai会议）中的method的内容，ThyroudXAgent中关于分割和分类的子方法就是使用了这个论文的方法。注意：ThyroidXAgent是想要发表在nature子刊中的论文的名称，即ThyroidAgent = ThyroidXAgent for Segmentation and Classification。

\section{Method}
% 引用Fig2
Fig.~\ref{fig:WorkFlow} illustrates the ThyroidAgent framework, which consists of training and inference stages. During inference, the agent dynamically selects the most appropriate expert output based on contextual information and evidence signals, replacing static pipelines.
% 动机：动态选择单个简单模型的方式比训练一个复杂模型的性能更稳健；近两年来llm在多个领域得到广泛应用，利用llm的动态选择能力，同时也探索llm如何应用在甲状腺超声图像诊断领域
The agent-based framework overcomes the limitations of relying on a single complex model by dynamically selecting from multiple simpler expert models, improving flexibility and generalization across diverse datasets. Motivated by the recent advancements in large language models (LLMs), which excel in dynamic decision-making, we integrate their reasoning capabilities to perform expert selection and aggregation based on structured evidence. This dynamic orchestration allows ThyroidAgent to adapt to varying clinical scenarios and enhance decision-making in thyroid ultrasound diagnosis.

\subsection{Toolbox for Ultrasound Analysis}
%We define thyroid ultrasound analysis as a set of callable tools with standardized inputs and outputs, allowing the agent to compare expert models based on consistent evidence signals for reproducible results. The toolbox is designed to facilitate expert selection and enhance the accuracy of predictions through complementary components. 
We define thyroid ultrasound analysis as a collection of tools with standardized inputs and outputs, enabling the agent to compare expert models based on consistent evidence for reproducible results. The toolbox facilitates expert selection and improves prediction accuracy through complementary components.
% It includes: (i) a deep expert family for segmentation and classification, based on DINOv3 with varying training conditions, (ii) a radiomics tool for extracting complementary morphology and texture features, and (iii) reinforcement learning for optimizing connected component analysis (CCA) hyperparameters to refine segmentation mask quality.

\subsubsection{DINOv3-Based Expert Models}
\label{sec:dinov3_models}
Our models share a DINOv3-based backbone with task-specific lightweight heads~\cite{simeoni2025dinov3}. 
For segmentation, we adopt a U-Net-style decoder with skip fusion to output a dense nodule mask probability map, optimized by a weighted BCE+IoU loss $\mathcal{L}_{\mathrm{seg}}$. 
%For classification, the backbone features are summarized by global average/max pooling and passed to a compact attention-based classification head to produce malignancy probabilities. 
% 添加两个任务的损失函数说明
For classification, backbone features are summarized by global average and max pooling and fed into a compact attention-based head to output, trained with a GLA loss to alleviate class imbalance. 
The core weighting and logit adjustment used by $\mathcal{L}_{\mathrm{seg}}$ and GLA are:
\begin{equation}
\begin{aligned}
w &= 1 + 5 \cdot \left| \operatorname{AvgPool}_{31}(y) - y \right|,\\
z'_b &= z_b + \tau \left( y_b \log p_{\text{pos}} + (1-y_b)\log p_{\text{neg}} \right),
\end{aligned}
\label{eq:losses}
\end{equation}
where $\mathcal{L}_{\mathrm{bm}}$ is BCE-with-logits computed on the adjusted logits $z'_b$.

%Rather than designing increasingly complex single models, we construct a diverse expert pool to improve robustness under cross-dataset variability. 
% 引用databias论文，写明动机
In recent years, the issue of dataset bias has remained a critical challenge in the development of reliable machine learning models~\cite{torralba2011unbiased}. 
Despite the increasing diversity and scale of modern datasets, recent studies show that neural networks can still easily capture dataset-specific biases, which may hinder generalization across diverse real-world conditions~\cite{liu2024decade}. 
Motivated by these findings, our design adopts an agent-based paradigm to replace static pipelines with dynamic expert orchestration.
Specifically, the agent leverages ultrasound images together with contextual metadata to adaptively select or aggregate the most suitable segmentation and classification experts on a per-sample basis. This architecture is intended to explicitly mitigate cross-dataset and cross-device bias by avoiding reliance on a single fixed model whose behavior may be overly coupled to training data idiosyncrasies. 
As validated in Sec.~\ref{sec:effectiveness}, dynamic expert selection offers a practical and more stable, interpretable alternative to a single fixed model, improving robustness and generalization under heterogeneous clinical acquisition conditions via context-aware decision-making.

% Specifically, we train multiple models on stacked datasets with different input resolutions and dilation settings, and then use the agent to select or aggregate the most suitable expert model output for each case based on evidence signals.  
% This design is empirically validated in Sec.~\ref{sec:effectiveness} to provide more stable and interpretable performance than relying on a single fixed model to generalize across all imaging conditions.

\subsubsection{Radiomics Tool for Feature Extraction}
%Radiomics extracts interpretable features from an image and an ROI mask to complement deep learning predictions. We adopt a 2D PyRadiomics setup, enabling standard feature families such as shape2D and texture, consistent with our observation that morphology and texture features are dominant in predicting outcomes. We report representative formulations for these families:
Radiomics extracts interpretable features from images and ROI masks to complement deep learning predictions. Using a 2D PyRadiomics setup, we focus on feature families such as shape2D, which are dominant in predicting outcomes. Representative formulations include:
\begin{equation}
\begin{aligned}
A = \sum_{x=1}^{H} \sum_{y=1}^{W} \mathbb{I} \left[ M(x,y) = 1 \right], \\
\mathrm{Energy} = \sum_{i=1}^{N_g} \sum_{j=1}^{N_g} P(i,j)^2,
\end{aligned}
\end{equation}
%where $A$ denotes the ROI area, $M(x,y) \in {0,1}$ is the binary ROI mask, $\mathbb{I}[\cdot]$ is the indicator function, $H \times W$ is the mask resolution, $\mathrm{Energy}$ is the GLCM energy, $P(i,j)$ is the normalized gray-level co-occurrence matrix, and $N_g$ is the number of discretized gray levels.
where $A$ is the ROI area, $M(x,y) \in \{0,1\}$ is the binary ROI mask, $\mathrm{Energy}$ is the GLCM energy and $P(i,j)$ is the normalized gray-level co-occurrence matrix.

\begin{algorithm}[t]
\caption{ThyroidAgent inference process}
\label{alg:thyroidagent_inference}
\begin{algorithmic}[1]
\Require Image $x$, optional context $c$; expert pools $\mathcal{E}_{seg},\mathcal{E}_{cls}$; metadata registry $\mathcal{R}$
\Ensure Final mask $\hat{M}$, label $\hat{y}$ with confidence $\hat{p}$, decision log $\mathcal{L}$

\State $x' \gets \mathrm{Preprocess}(x)$; $\mathcal{L}\gets\emptyset$
\State $\{M_k,s_k\}_{k=1}^{K} \gets \mathrm{RunSeg}(\mathcal{E}_{seg},x',\mathcal{R})$ 
\State $E_{seg}\gets \mathrm{SegEvidence}(\{M_k,s_k\},c,\mathcal{R})$ 
\State $\hat{k}\gets \mathrm{PolicySelect}(E_{seg})$; $\hat{M}\gets M_{\hat{k}}$; $\mathcal{L}\gets\mathcal{L}\cup\{\hat{k},E_{seg}\}$
\State $r\gets \mathrm{PyRadiomics2D}(x',\hat{M})$ 
\State $\{p_m,\gamma_m\}_{m=1}^{M} \gets \mathrm{RunCls}(\mathcal{E}_{cls},x',\mathcal{R})$ 
\State $E_{cls}\gets \mathrm{ClsEvidence}(\{p_m,\gamma_m\},r,c,\mathcal{R})$ 
\State $\hat{m}\gets \mathrm{PolicySelect}(E_{cls})$; $\hat{y} \gets \mathbb{I}[p_{\hat{m}}\ge 0.5]$; $\hat{p}\gets p_{\hat{m}}$
\State $\mathcal{L}\gets\mathcal{L}\cup\{\hat{m},E_{cls}\}$; \Return $\hat{M},\hat{y},\hat{p},\mathcal{L}$
\end{algorithmic}
\end{algorithm}

% 把对图和算法的引用提到前面，在Method开始已经引用了Fig2，这里结合算法1，再简单介绍一下
\subsection{Agentic Inference Workflow}
%Fig.~\ref{fig:WorkFlow} summarizes ThyroidAgent as a policy-driven workflow with offline expert construction and online inference. In the offline stage, multiple segmentation and classification experts are trained from stacked datasets and organized into an experts zoo with a metadata registry. 
%In the online stage, a test ultrasound image is processed by multiple candidate experts, whose outputs are summarized as compact evidence signals and passed to ThyroidAgent for a strict JSON decision that drives expert selection or aggregation and final prediction. 
%As formalized in Algorithm~\ref{alg:thyroidagent_inference}, the process proceeds from segmentation-side candidate generation and evidence-based mask selection, to mask-guided radiomics extraction, and then to classification-side evidence construction and policy selection using expert predictions, radiomics evidence, context, and metadata, thereby replacing a single static forward pass with evidence-aware orchestration across experts.
Fig.~\ref{fig:WorkFlow} overviews ThyroidAgent as a policy-driven pipeline with expert construction and agentic inference. 
Multiple segmentation and classification experts are trained on stacked datasets and organized into an expert pool with a metadata registry that records imaging device provenance of the training data, validation performance, training-set scale, and input resolution.
As illustrated in Fig.~\ref{fig:WorkFlow} and Algorithm~\ref{alg:thyroidagent_inference}, during inference we execute candidate experts and summarize their predictions into compact evidence signals, together with context and metadata cues. 
ThyroidAgent then outputs a strict JSON decision to select or aggregate experts, producing the final mask and label. This workflow replaces a single fixed forward pass with evidence-aware orchestration across experts.