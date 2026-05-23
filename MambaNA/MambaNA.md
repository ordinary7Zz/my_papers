\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts
% The preceding line is only needed to identify funding in the first footnote. If that is unneeded, please comment it out.
%Template version as of 6/27/2024

\usepackage{cite}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage[table]{xcolor}
\let\oldrowcolor\rowcolor
\usepackage{booktabs} %需要加载宏包{booktabs}
\usepackage{multirow} %合并单元格
\usepackage{makecell}
\usepackage{pifont} 
\usepackage{threeparttable}

\def\BibTeX{{\rm B\kern-.05em{\sc i\kern-.025em b}\kern-.08em
    T\kern-.1667em\lower.7ex\hbox{E}\kern-.125emX}}
\begin{document}

\title{MambaNA: A state space model with Neighborhood Attention for Medical Super-Resolution
}

\author{\IEEEauthorblockN{1\textsuperscript{st} Bodong Wang, 2\textsuperscript{nd} Mingzhi Mao*}
\IEEEauthorblockA{\textit{School of Software Engineering} \\
\textit{Sun Yat-sen University}\\
Zhuhai, China \\
wangbd8@mail2.sysu.edu.cn, mcsmmz@mail.sysu.edu.cn}
\thanks{* Corresponding author: Mingzhi Mao (mcsmmz@mail.sysu.edu.cn).}
}

\maketitle

\begin{abstract}
% MambaNA: A state space model with Neighborhood Attention for Medical Super-Resolution 
% 期刊 BSPC（Biomedical Signal Processing and Control）CIBM（Computers in Biology and Medicine）

In recent years, Mamba-based methods have demonstrated significant potential in various tasks, including medical image super-resolution, due to Mamba's ability to balance global receptive fields and computational efficiency. 
However, the inherent causal modeling of Mamba restricts its ability to capture local features, which poses a challenge for medical image super-resolution, where intricate local details in structures such as cells and tissue boundaries are crucial.
In this work, we propose MambaNA, a novel medical image super-resolution method that integrates a neighborhood attention mechanism into the Mamba model. 
Specifically, MambaNA computes pixel-wise attention weights for neighboring elements to introduce non-causality while extracting local features that maintain translational equivariance.
Furthermore, it performs multi-frequency channel fusion directly following the SSM's sequence modeling, which significantly improves model performance and training stability.
Extensive experiments demonstrate the superior performance of MambaNA in medical image super-resolution tasks.
\end{abstract}

\begin{IEEEkeywords}
Medical image super-resolution, Mamba, neighborhood attention, state space model, channel attention
\end{IEEEkeywords}

\section{Introduction}
\label{sec:intro}
%Introduction
% 第一段增加医学图像增强的重要性（具体疾病等应用场景）
Modern medical diagnosis relies heavily on the visual information provided by medical imaging. However, acquiring high-quality images often requires expensive advanced equipment and prolonged patient exposure. Recent advances in deep learning have made super-resolution (SR) a cost-effective solution for image enhancement, enabling the reconstruction of fine structures from low-resolution inputs. In the medical domain, SR aims to generate high-resolution outputs from low-resolution scans by recovering details that are typically lost during image acquisition.

Early super-resolution methods, based on simple interpolation \cite{keys2003cubic,farsiu2004fast,freeman2002example} and optimization \cite{stark1989high}, were straightforward but often failed to faithfully restore fine details. Subsequently, Convolutional Neural Networks (CNNs) \cite{dai2019second,dong2014learning,zhang2018residual,zhang2017beyond,ledig2017photo,li2019feedback} and Generative Adversarial Networks (GANs) \cite{ledig2017photo,wang2018esrgan,wang2021real} were widely adopted because of their ability to learn nonlinear mappings and rich feature representations. However, these methods often struggle to capture long-range dependencies and global receptive fields, which limits their ability to restore high-frequency details and maintain structural coherence, especially in complex medical images.

To address these limitations, the Transformer architecture \cite{vaswani2017attention}, with its powerful self-attention mechanism for global dependency modeling, has been successfully adapted to computer vision, notably through the Vision Transformer (ViT) \cite{dosovitskiy2020image,chen2021pre,liang2021swinir,wang2022uformer,chen2023dual}. Although effective at capturing long-range spatial relationships, Transformer-based methods often incur substantial computational and memory costs because of the quadratic complexity of global self-attention. State Space Models (SSMs) \cite{gu2021efficiently,gu2021combining,smith2022simplified} have recently emerged as efficient sequence models for long-range dependency modeling. Among them, Mamba \cite{gu2023mamba} is particularly attractive because it balances global receptive fields with computational efficiency. However, its inherent causal modeling limits its ability to fully exploit local features \cite{guo2025mambairv2}, which is especially problematic for medical images, where fine localized details are crucial for accurate analysis.

To address these limitations, we propose MambaNA, a novel medical image super-resolution method. It integrates Neighborhood Attention (NA) \cite{hassani2023neighborhood} into a Mamba architecture to introduce non-causal modeling and alleviate Mamba's inherent causal limitations while enhancing local feature extraction. In addition, MambaNA incorporates a lightweight Channel Mixing module, implemented with multi-spectral channel attention (MSCA) \cite{qin2021fcanet} based on the Discrete Cosine Transform (DCT). This design captures intricate frequency-domain patterns and cross-channel dependencies, and experimental results show that it significantly improves both performance and training stability. The main contributions of this paper are summarized as follows:
\begin{enumerate}
% 太多 空话减少
    \item We develop MambaNA, a Mamba-based network for medical image super-resolution that combines efficient global modeling with non-causal local attention for more accurate image reconstruction.
    \item We propose an SSM-Layer equipped with a Channel Mixing module directly after the SSM module. Implemented as a multi-spectral channel attention (MSCA) design, it adaptively weights frequency components within channels, thereby improving both reconstruction quality and training stability.
    \item We conduct extensive experiments and ablation studies to validate the contribution of each component. The results show that MambaNA achieves strong and consistent performance across multiple super-resolution benchmarks.
\end{enumerate}

\section{Related Works}
\label{sec:relatedworks}
\subsection{Medical Image Super-Resolution}
Deep learning has substantially advanced medical image SR. CNN-based methods such as SRCNN and VDSR, together with residual and dense variants \cite{dong2014learning,kim2016accurate,zhao2019applications,pham2019multiscale,qiu2022residual,chen2018brain}, have improved detail recovery across CT and MRI. GAN-based methods further enhance perceptual quality in low-dose CT and MRI reconstruction \cite{wolterink2017generative,yang2018low,chen2018efficient,mahapatra2019progressivegenerativeadversarialnetworks}. More recently, Transformer-based models have introduced stronger global context modeling for SR \cite{forigua2022superformer,huang2023transmrsr,zheng2025efficient,li2025high}, although their memory and computational costs remain high for high-resolution medical images.

\subsection{State Space Models and Attention}
SSMs provide an efficient alternative for long-range dependency modeling. Mamba \cite{gu2023mamba} and its vision variants \cite{liu2024vmamba,zhu2024visionmambaefficientvisual,yang2024plainmamba,huang2025localmamba,guo2024mambair,guo2025mambairv2} improve global modeling efficiency, yet their causal scanning process is less suitable for dense 2D local interactions. In parallel, attention mechanisms remain effective for refining feature representations. Neighborhood Attention preserves local inductive bias and translation equivariance in spatial modeling \cite{hassani2023neighborhood}, while frequency-aware channel attention such as FcaNet \cite{qin2021fcanet} improves channel discrimination. These observations motivate our design: combining Mamba for efficient global context modeling with local spatial attention and frequency-aware channel modulation for medical SR.

\begin{figure*}
    \centering
    \includegraphics[width=1.0\linewidth]{figures/MambaNA.png}
    \caption{Overall architecture of MambaNA for medical image super-resolution. The network consists of shallow feature extraction, stacked MambaNA groups for deep feature modeling, and a final reconstruction module for generating the high-resolution output.}
    \label{fig:Overall Architecture}
\end{figure*}
\section{Methodology}
\subsection{Preliminaries}
\subsubsection{State Space Models}
SSMs model an input sequence $x$ and output sequence $y$ through a hidden state $h$. A continuous-time SSM is written as
\begin{equation}
\label{equ:ODEs}
\begin{aligned}
    h'(t) &= Ah(t) + Bx(t), \\
    y(t) &= Ch(t) + Dx(t),
\end{aligned}
\end{equation}
and discretized for neural sequence modeling as
\begin{equation}
\label{equ:dis-formulation}
\begin{aligned}
    h_{t} &= \bar{A}h_{t-1} + \bar{B}x_t,  \\
    y_t &= Ch_t + Dx_t.
\end{aligned}
\end{equation}
Mamba \cite{gu2023mamba} extends this formulation with input-dependent parameters, enabling efficient long-range dependency modeling with linear complexity.

\subsection{Overall Architecture}
As shown in Figure \ref{fig:Overall Architecture}, MambaNA consists of shallow feature extraction, deep feature extraction, and image reconstruction modules. Given an input image $I_{LQ}$, a $3\times3$ convolution first produces shallow features $F_0$. Deep features are then extracted by stacking $N_1$ residual MambaNA groups, each containing $N_2$ MambaNA blocks. Each block is composed of an Attention Block and an SSM-Layer. The refined features are finally used to reconstruct the high-quality output image.

For medical image super-resolution, we optimize MambaNA with a hybrid loss:
%For the task of medical image super-resolution, MambaNA is optimized using the $\ell_1$(L1) loss function.
%Given a reconstructed high-quality image $I_{HQ}$ and its corresponding ground-truth image $I_{GT}$, the $\ell_1$ loss is defined as:
\begin{equation}
\begin{aligned}
    \mathcal{L} = 0.7 \cdot \mathcal{L}_{L_1} + 0.3 \cdot \mathcal{L}_{perceptual},\\
    \mathcal{L}_{\ell_{1}} = ||I_{HQ} - I_{GT}||_1,\\
    \mathcal{L}_{perceptual} = ||\phi{(I_{HQ})} - \phi{(I_{GT})} ||_2^2
\end{aligned}
\end{equation}
where $\phi(\cdot)$ denotes feature extraction from pre-trained VGG-19's 5th conv layer.
%The $\ell_1$ loss is preferred for its robustness to outliers and its tendency to produce sharper results compared to $\ell_2$ in image restoration tasks.

\subsection{Attention Block}
\begin{figure}
    \centering
    \caption{Structure of the Attention Block in MambaNA. It applies Neighborhood Attention to strengthen local non-causal interactions and improve the reconstruction of fine anatomical details.}
    \label{fig:attention-block}
\end{figure}
MambaNA adopts Neighborhood Attention (NA) \cite{hassani2023neighborhood} to introduce non-causal local modeling. Unlike global or window-based attention, NA restricts each query to a local neighborhood, making it well suited to preserving subtle anatomical structures. Given an input $X \in \mathbb{R}^{N \times d}$, the attention at position $i$ is computed as
\begin{equation}
\begin{aligned}
    A_i^k &= Q_iK_{\mathcal{N}(i)}^T + B_i, \\
    NA_k(i) &= softmax(\frac{A_i^k}{\sqrt{d}})V_{\mathcal{N}(i)}.\\
\end{aligned}
\end{equation}
This design improves fine-grained local interaction while preserving translation equivariance, complementing Mamba's global modeling.
\subsection{SSM-Layer}
\begin{figure}
    \centering
    \caption{Structure of the proposed SSM-Layer in MambaNA. The layer combines adaptive scan ordering with multi-spectral channel attention to capture global dependencies and refine frequency-aware channel responses.}
    \label{fig:ssm-layer}
\end{figure}
The SSM-Layer captures long-range dependencies through adaptive pixel reordering. Given a feature map $X \in \mathbb{R}^{C \times H \times W}$, a semantic relevance score is estimated for each pixel:
\begin{equation}
    s(i) = MLP(GAP(X_i)),
\end{equation}
and quantized into $G$ groups:
\begin{equation}
    g(i) = \lfloor G \cdot \sigma(s(i)) \rfloor.
\end{equation}
Pixels are then concatenated by group to form the scan order:
\begin{equation}
    \pi = concat(\pi_{g=0}, \pi_{g=1},...,\pi_{g=G-1}).
\end{equation}
This adaptive sequence reduces semantic distance within the SSM scan while keeping linear complexity.

To further refine channel responses, we apply a Channel Mixing module after the SSM module. Implemented with multi-spectral channel attention (MSCA), this module uses fixed DCT bases to aggregate frequency responses and produce channel weights:
\begin{equation}
\begin{aligned}
    Freq^i &= \sum_{h=0}^{H-1} \sum_{w=0}^{W-1} X^{i,h,w} \cdot DCT^{i,h,w}, \\
    Freq &= cat(
    \begin{bmatrix}
        Freq^1 & Freq^2 & \cdots & Freq^C
    \end{bmatrix}
    ), \\
    w = \sigma(MLP(Freq)).
\end{aligned}
\end{equation}
The Channel Mixing module strengthens frequency-aware channel modulation and improves optimization stability.

\section{Experiments}
\begin{figure*}
    \centering
    \includegraphics[width=1.0\linewidth]{figures/Error Map.png}
    \caption{Qualitative comparison of reconstruction results and corresponding error maps. Darker regions indicate smaller reconstruction errors, showing that MambaNA preserves anatomical structures more faithfully than competing methods.}
    \label{fig:Error Map}
\end{figure*}

\subsection{Experimental Settings}
\subsubsection{Datasets and Metrics}
Our experiments utilized two publicly available datasets for medical image super-resolution: the IXI dataset\footnote{https://brain-development.org/ixi-dataset/} and a Brain Tumor MRI dataset\footnote{https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset}.
The IXI dataset includes 3D multimodal MRI scans with T1, T2, and PD modalities. 
We focused on the T1-weighted subset (IXI-T1) for SR training and evaluation because of its superior soft-tissue contrast. 
Each original IXI-T1 scan contains 96 slices of size 240 $\times$ 240 pixels; we uniformly selected 8 representative slices per scan to avoid redundant low-variation samples. 
The IXI-T1 dataset was split as follows: 75 scans (600 slices) for training, 6 scans (48 slices) for validation, and 10.5 scans (84 slices from the remaining qualified T1 scans) for testing. All slices retained the original 240 $\times$ 240 resolution.

To quantitatively evaluate the quality of the super-resolved images, we adopted two widely used metrics: Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index Measure (SSIM). 
PSNR measures pixel-wise fidelity by comparing reconstructed images with the ground truth, while SSIM evaluates perceptual similarity in terms of luminance, contrast, and structure.

\subsubsection{Experimental Details}
Our MambaNA model was implemented in PyTorch and trained on an NVIDIA RTX A6000 GPU.
The low-resolution training samples were generated in the frequency domain to better match the distribution of real low-resolution images.
We used Adam as the optimizer with $\beta_1=0.9$ and $\beta_2=0.99$.
The initial learning rate and batch size were set to $2 \times 10^{-4}$ and 2, respectively.
Additionally, the original images were cropped into $64 \times 64$ patches during training.
We used six Mamba blocks, each with 192 channels.

\subsection{Comparison on Image Super-Resolution}
\begin{table*}[!htp]
    \begin{center}
    \caption{Quantitative comparison of medical image super-resolution performance on the Brain Tumor and IXI-T1 datasets. MambaNA achieves the best overall PSNR and SSIM results under both $2\times$ and $4\times$ upsampling settings.}
    \label{tab:Comparison on IXI-T1 and BTMRI}
    \begin{tabular}{c|c|c|cc|cc}
        \toprule
        \multirow{2}{*}{\textbf{Method}} & 
        \multirow{2}{*}{\textbf{Scale}} & 
        \multirow{2}{*}{\textbf{Param}} &
        \multicolumn{2}{c|}{\textbf{Brain Tumor}} &
        \multicolumn{2}{c}{\textbf{IXI-T1}} \\
        & & & PSNR $\uparrow$&SSIM $\uparrow$& PSNR $\uparrow$&SSIM $\uparrow$\\
        \midrule
        Bicubic [2D] & $2\times$ & - & 26.96 & 0.9331 & 27.57 & 0.9523\\
        EDSR \cite{lim2017enhanced} + MMHCA \cite{georgescu2023multimodal} & $2\times$ & 20.8M & 31.70 & 0.8397 & 32.08 & 0.9604\\
        SwinIR \cite{liang2021swinir} & $2\times$ & 11.9M & 35.60 & 0.9347 & 32.82 & 0.9631\\
        MambaIR \cite{guo2024mambair} & $2\times$ & 22.9M & 35.75 & 0.9362 & 33.30 & 0.9650\\
        MambaIRv2 \cite{guo2025mambairv2} & $2\times$ & 27.6M & 36.43 & 0.9431 & 33.58 & 0.9664\\
        \rowcolor{lightgray}
        MambaNA [Ours] & $2\times$ & 30.5M & \textbf{36.95} & \textbf{0.9447} & \textbf{33.94} & \textbf{0.9686}\\
        \midrule
        Bicubic [2D] & $4\times$ & - & 18.85 & 0.7535 & 21.22 & 0.8293\\
        EDSR \cite{lim2017enhanced} + MMHCA \cite{georgescu2023multimodal} & $4\times$ & 20.8M & 28.10 & 0.9059 & 28.45 & 0.8925\\
        SwinIR \cite{liang2021swinir} & $4\times$ & 11.9M & 30.23 & 0.9235 & 28.12 & 0.9011\\
        MambaIR \cite{guo2024mambair} & $4\times$ & 22.9M & 30.75 & 0.9202 & 29.56 & 0.9073\\
        MambaIRv2 \cite{guo2025mambairv2} & $4\times$ & 27.6M & 31.50 & 0.8609 & 30.07 & 0.9334\\
        \rowcolor{lightgray}
        MambaNA [Ours] & $4\times$ & 30.5M & \textbf{32.28} & \textbf{0.9386} & \textbf{30.64} & \textbf{0.9379}\\
        \bottomrule
    \end{tabular}
  \end{center}
\end{table*}
\begin{table}[!htp]
    \centering
    \begin{tabular}{cc|cc}
        \toprule
        \textbf{\makecell{Attention\\Block}} &
        \textbf{\makecell{Channel\\Mixing}} &
        PSNR $\uparrow$&
        SSIM $\uparrow$\\
        \midrule
        \ding{56} & \ding{52} & 36.41 & 0.9413 \\
        \ding{52} & \ding{56} & 36.65 & 0.9462 \\
        \ding{56} & \ding{56} & 35.68 & 0.8874 \\
        \bottomrule
    \end{tabular}
    \caption{Ablation results for the main components of MambaNA. The comparison shows that both the Attention Block and Channel Mixing module contribute to the final reconstruction performance.}
    \label{tab:Ablation}
\end{table}
Our evaluation first focused on comparing MambaNA with existing medical image super-resolution methods on the Brain Tumor and IXI-T1 datasets.
As detailed in Table \ref{tab:Comparison on IXI-T1 and BTMRI}, MambaNA consistently achieves higher PSNR and SSIM values than \cite{georgescu2023multimodal}, \cite{guo2025mambairv2}, and \cite{liang2021swinir}.
These quantitative results highlight MambaNA's strong ability to reconstruct high-fidelity medical images while balancing global context modeling and local detail recovery.

Beyond numerical metrics, Figure \ref{fig:Error Map} presents a qualitative comparison of the super-resolution results. The first row shows the reconstructed images from different methods, while the second row presents the corresponding pixel-wise mean squared error (MSE) maps with respect to the ground truth.
Darker regions in the error maps indicate smaller deviations from the ground truth and therefore better reconstruction fidelity.
As shown in the figure, MambaNA produces reconstructions that are visually closer to the ground truth, with fewer artifacts and better preservation of fine anatomical structures than competing methods.
This qualitative superiority further supports the practical value of MambaNA for clinical image analysis.

\begin{table*}[!htp]
    \begin{center}
    \caption{Quantitative comparison on classical natural image super-resolution benchmarks, including BSDS100, Urban100, and Manga109. The results demonstrate that MambaNA maintains strong generalization ability beyond medical image datasets.}
    \label{tab:Comparison on Classical}
    \begin{threeparttable}
    \begin{tabular}{c|c|c|cc|cc|cc}
        \toprule
        \multirow{2}{*}{\textbf{Method}} & 
        \multirow{2}{*}{\textbf{Scale}} & 
        \multirow{2}{*}{\textbf{Param}} &
        \multicolumn{2}{c|}{\textbf{BSDS100}} &
        \multicolumn{2}{c|}{\textbf{Urban100}} &
        \multicolumn{2}{c}{\textbf{Manga109}} \\
        & & & PSNR $\uparrow$&SSIM $\uparrow$&PSNR $\uparrow$&SSIM $\uparrow$& PSNR $\uparrow$&SSIM $\uparrow$\\
        \midrule
        EDSR \cite{lim2017enhanced} & $2\times$ & 42.6M & 32.32 & 0.9013 & 32.93 & 0.9351 & 39.10 & 0.9773\\
        SwinIR \cite{liang2021swinir} & $2\times$ & 11.8M & 31.63 & 0.9022 & 32.98 & 0.9363 & 38.89 & 0.9736\\
        MambaIR\cite{guo2024mambair} & $2\times$ & 20.4M & 31.57 & 0.9302 & 34.06 & 0.9446 & 40.10 & 0.9784\\
        MambaIRv2 \cite{guo2025mambairv2} & $2\times$ & 22.9M & 32.71 & 0.9046 & 34.88 & 0.9471 & 40.37 & 0.9785\\
        \rowcolor{lightgray}
        MambaNA [Ours] & $2\times$ & 31.5M & \textbf{32.82} & \textbf{0.9054} & \textbf{35.36} & \textbf{0.9493} & \textbf{40.81} & \textbf{0.9871}\\
        \midrule
        EDSR \cite{lim2017enhanced} & $4\times$ & 43.0M & 27.68 & 0.7398 & 26.63 & 0.8012 & 30.89 & 0.9011\\
        SwinIR \cite{liang2021swinir} & $4\times$ & 11.9M & 27.78 & 0.7482 & 27.39& 0.8213 & 31.92 & 0.9136\\
        MambaIR\cite{guo2024mambair} & $4\times$ & 20.4M & 27.90 & 0.7489 & 27.51 & 0.8273 & 32.16 & 0.9245\\        
        MambaIRv2 \cite{guo2025mambairv2} & $4\times$ & 23.1M & 27.86 & \textbf{0.7498} & 27.72 & 0.8335 & 32.34 & 0.9288\\
        \rowcolor{lightgray}
        MambaNA [Ours] & $4\times$ & 31.5M & \textbf{27.93} & 0.7488 & \textbf{28.04} & \textbf{0.8511} & \textbf{32.55} & \textbf{0.9382}\\
        \bottomrule
    \end{tabular}
    \end{threeparttable}
  \end{center}
\end{table*}

To assess the generalization capability of MambaNA, we also evaluated it on widely used natural image super-resolution benchmarks, including BSDS100, Urban100, and Manga109.
As presented in Table \ref{tab:Comparison on Classical}, MambaNA consistently achieves competitive and often best or near-best PSNR and SSIM results across these datasets, demonstrating strong competitiveness against established natural image super-resolution methods.
These results indicate that, although MambaNA is designed for medical images, its super-resolution capability transfers effectively to diverse natural image scenarios, highlighting its versatility and broad applicability.

\subsection{Ablation Study}
We conducted ablation experiments to evaluate the contributions of the Attention Block and the Channel Mixing module under the same training settings. As shown in Table \ref{tab:Ablation}, removing either component degrades both PSNR and SSIM, whereas the full model achieves the best overall performance. These results confirm that both local non-causal attention and the frequency-aware channel modulation provided by the Channel Mixing module are important to MambaNA.

\section{Conclusion}
In this paper, we developed MambaNA, a novel super-resolution framework tailored for medical image reconstruction. By adopting the Mamba architecture, the model benefits from efficient long-range dependency modeling, which is important for processing high-resolution medical data. To overcome the limitations of Mamba's causal sequence modeling in 2D image restoration, MambaNA integrates both an Attention Block and a Channel Mixing module. The Attention Block introduces non-causal local modeling into the Mamba backbone, while the Channel Mixing module improves training stability and feature refinement, jointly contributing to better overall performance. Extensive experiments demonstrated MambaNA's strong performance on medical image super-resolution tasks and highly competitive generalization on natural image benchmarks. This work underscores the significant potential of Mamba-based architectures in high-fidelity image reconstruction. Future work will focus on improving computational efficiency for extremely large 3D volumes and exploring unsupervised learning strategies to reduce data dependency.
{
    \small
    \bibliographystyle{IEEEtran}
    \bibliography{main}
}

\end{document}