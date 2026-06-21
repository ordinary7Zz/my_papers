\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Classification performance across multi thyroid ultrasound datasets. Upper block, area under the receiver operating characteristic curve (AUROC); lower block, area under the precision--recall curve (AUPRC). Values are reported with 95\% confidence intervals.}
\label{tab:cls_performance}

\footnotesize
\setlength{\tabcolsep}{5.5pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lccccc}
\toprule
\textbf{Method}
& \textbf{TN3K}
& \textbf{ThyroidXL}
& \textbf{TN5K}
& \textbf{DDTI}
& \textbf{FinalData} \\
\midrule
ResNet-50~\cite{he2016deep}
& $0.7674 \pm 0.0394$
& $0.9044 \pm 0.0118$
& $0.9322 \pm 0.0168$
& $0.6704 \pm 0.0842$
& $0.6704 \pm 0.0842$ \\
RepViT~\cite{wang2023repvit}
& $0.5556 \pm 0.0463$
& $0.7774 \pm 0.0188$
& $0.6603 \pm 0.0375$
& $0.6162 \pm 0.0804$
& $0.8538 \pm 0.0185$\\
LSNet~\cite{wang2025lsnet}
& $0.8095 \pm 0.0333$
& $0.9178 \pm 0.0114$
& $0.9091 \pm 0.0201$
& $0.7581 \pm 0.0658$
& $0.8631 \pm 0.0201$\\
UltraFedFM~\cite{jiang2025pretraining}
& $0.8461 \pm 0.0697$
& $0.9239 \pm 0.0104$
& $0.9298 \pm 0.0175$
& $0.7518 \pm 0.1712$
& $0.9115 \pm 0.0140$\\
MedGemma~\cite{sellergren2025medgemma}
& $0.8492 \pm 0.0305$
& $0.9371 \pm 0.0095$
& $0.9442 \pm 0.0156$
& \textbf{0.8255 $\pm$ 0.0650}
& $0.8976 \pm 0.0166$\\
Qwen3-VL-8B-Instruct~\cite{bai2025qwen3}
& $0.8237 \pm 0.0328$
& $0.9050 \pm 0.0115$
& $0.9214 \pm 0.0187$
& $0.7361 \pm 0.0692$
& $0.8659 \pm 0.0189$\\
% 引用gpt5的system card
GPT-5.5~\cite{openai2025gpt5systemcard}
& $0.6924 \pm 0.0421$
& $0.7059 \pm 0.0469$
& $0.7737 \pm 0.0996$
& $0.6346 \pm 0.0914$
& $0.6109 \pm 0.0515$\\
Gemini-3.1-Pro~\cite{comanici_gemini_2025}
& $0.6587 \pm 0.0455$
& $0.6246 \pm 0.0640$
& $0.6873 \pm 0.0691$
& $0.6156 \pm 0.1308$
& $0.6493 \pm 0.0516$\\
\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.8692 $\pm$ 0.0349}
& \textbf{0.9676 $\pm$ 0.0066}
& \textbf{0.9472 $\pm$ 0.0152}
& $0.7991 \pm 0.0741$
& \textbf{0.9175 $\pm$ 0.0167}\\
\midrule
ResNet-50~\cite{he2016deep}
& $0.6882 \pm 0.0632$
& $0.8882 \pm 0.0174$
& $0.9674 \pm 0.0268$
& $0.3755 \pm 0.1176$
& $0.2755 \pm 0.1167$ \\
RepViT~\cite{wang2023repvit}
& $0.4275 \pm 0.0528$
& $0.7161 \pm 0.0276$
& $0.8403 \pm 0.0216$
& $0.3924 \pm 0.0933$
& $0.9486 \pm 0.0078$\\
LSNet~\cite{wang2025lsnet}
& $0.7581 \pm 0.0452$
& $0.9040 \pm 0.0142$
& $0.9551 \pm 0.0134$
& $0.4180 \pm 0.1410$
& $0.9449 \pm 0.0113$\\
UltraFedFM~\cite{jiang2025pretraining}
& $0.8531 \pm 0.0284$
& $0.9354 \pm 0.0114$
& $0.8422 \pm 0.0421$
& $0.4487 \pm 0.1452$
& $0.9669 \pm 0.0084$\\
MedGemma~\cite{sellergren2025medgemma}
& $0.8047 \pm 0.0430$
& $0.9201 \pm 0.0139$
& $0.9747 \pm 0.0084$
& $0.5537 \pm 0.1663$
& $0.9589 \pm 0.0096$\\
Qwen3-VL-8B-Instruct~\cite{bai2025qwen3}
& $0.7617 \pm 0.0511$
& $0.8787 \pm 0.0379$
& $0.9636 \pm 0.0106$
& $0.4112 \pm 0.1415$
& $0.9498 \pm 0.0096$\\
% 引用gpt5的system card
GPT-5.5~\cite{openai2025gpt5systemcard}
& $0.6627 \pm 0.0633$
& $0.6237 \pm 0.0666$
& $0.8920 \pm 0.0316$
& $0.3578 \pm 0.1089$
& $0.8311 \pm 0.0377$\\
Gemini-3.1-Pro~\cite{comanici_gemini_2025}
& $0.6205 \pm 0.0587$
& $0.4914 \pm 0.0841$
& $0.8462 \pm 0.0446$
& $0.3924 \pm 0.1527$
& $0.8403 \pm 0.0362$\\
\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.8545 $\pm$ 0.0600}
& \textbf{0.9653 $\pm$ 0.0078}
& \textbf{0.9752 $\pm$ 0.0089}
& \textbf{0.5863 $\pm$ 0.1380}
& \textbf{0.9711 $\pm$ 0.0006}\\
\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}