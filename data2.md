\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Performance of methods on lymph node metastasis (LNM) prediction and follicular thyroid carcinoma versus papillary thyroid carcinoma (FTC/PTC) subtype classification. Values are reported as AUROC and AUPRC with 95\% confidence intervals. Em dashes indicate tasks not evaluated for a given method.}
\label{tab:Malignant_images_tasks_performance}

\footnotesize
\setlength{\tabcolsep}{5.5pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lcccc}
\toprule
\multirow{2}{*}{\textbf{Method}}
& \multicolumn{2}{c}{\textbf{Lymph Node Metastasis}}
& \multicolumn{2}{c}{\textbf{FTC/PTC subtype}} \\
& AUROC & AUPRC & AUROC & AUPRC \\
\midrule
RepViT~\cite{wang2023repvit}
& $0.7905 \pm 0.0676$
& $0.8152 \pm 0.0638$
& $0.6419 \pm 0.0839$
& $0.6297 \pm 0.0942$\\
LSNet~\cite{wang2025lsnet}
& $0.5878 \pm 0.0865$
& $0.6301 \pm 0.0875$
& $0.4858 \pm 0.0925$
& $0.4845 \pm 0.0908$\\
UltraFedFM~\cite{jiang2025pretraining}
& $0.7757 \pm 0.0731$
& $0.7902 \pm 0.0845$
& $0.7365 \pm 0.0744$
& $0.7582 \pm 0.0824$\\
MedGemma~\cite{sellergren2025medgemma}
& $0.8403 \pm 0.0461$
& $0.8585 \pm 0.0566$
& $0.6598 \pm 0.0824$
& $0.6142 \pm 0.1056$\\
Qwen3-VL-8B-Instruct~\cite{bai2025qwen3}
& $0.8070 \pm 0.0632$
& $0.8055 \pm 0.0800$
& $0.6056 \pm 0.0866$
& $0.5539 \pm 0.1118$\\
% 引用gpt5的system card
GPT-5.5~\cite{openai2025gpt5systemcard}
& $0.8410 \pm 0.0575$
& $0.8629 \pm 0.0533$
& $0.1604 \pm 0.0706$
& $0.3638 \pm 0.0847$\\
Gemini-3.1-Pro~\cite{comanici_gemini_2025}
& $0.5414 \pm 0.0736$
& $0.5492 \pm 0.0915$
& $0.3324 \pm 0.0872$
& $0.4187 \pm 0.0837$\\
LLNM-Net~\cite{shen2025explainable}
& $0.7665 \pm 0.0692$
& $0.7363 \pm 0.0849$
& ---
& ---\\
Tiger-Model~\cite{dai2025improving}
& ---
& ---
& $0.7136 \pm 0.0814$
& $0.7117 \pm 0.1101$\\
\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& $0.8642 \pm 0.0550$
& $0.8808 \pm 0.0537$
& $0.8053 \pm 0.0599$
& $0.7863 \pm 0.0793$\\
\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}