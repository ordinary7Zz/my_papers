\documentclass[fleqn,10pt]{wlscirep}

% Compile with XeLaTeX because this manuscript contains Chinese text.
\usepackage{ctex}

\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{multirow}
\usepackage{adjustbox}
\usepackage{subcaption}
\usepackage{pifont}
\usepackage{xr}
\usepackage{float}
\usepackage{nameref}
\usepackage{xcolor}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{array}
\usepackage{appendix}
\usepackage{hyperref}
\usepackage[nameinlink,noabbrev]{cleveref}
\usepackage{makecell}
\usepackage[table]{xcolor}
\usepackage{threeparttable}

\newcommand{\cmark}{\ding{51}}%
\newcommand{\xmark}{\ding{55}}%
\newcommand{\ph}[1]{\texttt{\textless #1\textgreater}}

\crefname{figure}{Fig.}{Figs.}
\crefname{table}{Table}{Tables}
\crefname{section}{Section}{Sections}
\crefname{appendix}{Supplementary}{Supplementary}

\title{Clinician-interactive agentic AI for thyroid ultrasound diagnosis and reporting}
% An open clinician-interactive agentic AI system for thyroid ultrasound diagnosis and reporting

\author[1,$\dagger$]{Haifan Gong}
\author[1,$\dagger$]{Shiyu Chen}
\author[2,$\dagger$]{Baidong Wang}
\author[3,$\dagger$]{Yuqi Wang}
\author[4]{Shijie Wang}
\author[5]{Guoliang You}
\author[1]{Xinyu Xiong}
\author[6]{Haowei Wang}
\author[7]{Qinghua Liu}
\author[2]{Mingzhi Mao}
\author[4]{Dexing Kong}
\author[8,*,$\ddagger$]{Wei Lou}
\author[9,*,$\ddagger$]{Fei Chen}
\author[1,*,$\ddagger$]{Guanbin Li}

\affil[1]{School of Computer Science and Engineering, Sun Yat-sen University, Guangdong, China}
\affil[2]{School of Software Engineering, Sun Yat-sen University, Guangdong, China}
\affil[3]{Duke University, Durham, USA}
\affil[4]{School of Mathematical Sciences, Zhejiang University, Hangzhou, 310058, China}
\affil[5]{School of Computer Science and Technology, University of Science and Technology of China}
\affil[6]{Department of Pathology, Zhujiang Hospital, Southern Medical University}
\affil[7]{Department of Health Management, Zhujiang Hospital, Southern Medical University}
\affil[8]{College of Mathematical Medicine, Zhejiang Normal University, Jinhua, 321004, China}
\affil[9]{Department of Thyroid Surgery, Zhujiang Hospital, Southern Medical University}

\affil[*]{\textbf{Corresponding authors:} Wei Lou~([louwei@zjnu.edu.cn](mailto:louwei@zjnu.edu.cn)), Fei Chen~([gzchenfei@126.com](mailto:gzchenfei@126.com)), and Guanbin Li~([liguanbin@mail.sysu.edu.cn](mailto:liguanbin@mail.sysu.edu.cn))}
\affil[$\dagger$]{These authors contributed equally to this work}
\affil[$\ddagger$]{These authors jointly supervised this work and contributed equally to this work}



\begin{abstract}
TODO
\end{abstract}

\begin{document}
\flushbottom
\maketitle
\thispagestyle{empty}

\section{Introduction}

Thyroid nodules are common in clinical practice and are increasingly detected during routine imaging \cite{Alexander2022Lancet}. Their management requires a balance between identifying clinically meaningful malignancy and avoiding unnecessary biopsy, surgery, or surveillance for indolent disease \cite{Grani2024NatRevEndocrinol}. Ultrasound is the first-line imaging modality for thyroid nodule assessment, and structured systems such as the Thyroid Imaging Reporting and Data System (TI-RADS) have improved the consistency of malignancy risk stratification and biopsy recommendations \cite{Tessler2017ACRTIRADS}. Nevertheless, thyroid ultrasound remains operator- and reader-dependent, with substantial variability in the assessment of margins, echogenic foci, and other sonographic descriptors \cite{Hoang2018AJRInterobserver}. Fine-needle aspiration cytology provides additional diagnostic evidence, but indeterminate Bethesda categories remain a major source of uncertainty in clinical decision-making \cite{Cibas2017Bethesda}. Thyroid nodule assessment is therefore not a single image-classification problem, but a clinical workflow that links lesion localization, measurement, sonographic characterization, risk estimation, cytology-informed management, reporting, and clinician review \cite{Alexander2022Lancet,Grani2024NatRevEndocrinol}.

Artificial intelligence has been applied to several components of thyroid ultrasound diagnosis, including nodule detection, segmentation, malignancy classification, and management support \cite{Peng2021LancetDigitalHealthThyNet}. Feature-aligned models have attempted to make thyroid AI more clinically interpretable by linking predictions to structured ultrasound descriptors and TI-RADS-related features \cite{Chen2022RadiologyTIRADS}. Multimodal systems such as ThyGPT have further reframed thyroid AI as a diagnostic and management copilot rather than a stand-alone classifier \cite{Yao2025NPJDigitMedThyGPT}. Beyond ultrasound image classification, deep learning has also been extended to thyroid fine-needle aspiration biopsy and cytology interpretation \cite{Wang2024LancetDigitalHealthFNAB}. Recent Nature Communications studies on lateral lymph-node metastasis prediction and rare thyroid cancer subtype classification show that thyroid AI is moving toward more specialized and clinically consequential tasks \cite{Shen2025NatCommunLLNM,Dai2025NatCommunThyroidSubtype}. Despite this progress, most systems are still developed as isolated predictors that produce a final probability, label, or report-like output without preserving the intermediate clinical evidence needed for audit, correction, and workflow integration \cite{Yao2025NPJDigitMedThyGPT,Qiu2024NatMachIntellAgenticSystems}.

Agentic AI offers a framework for connecting these isolated capabilities into a traceable clinical process \cite{Zou2025LancetAgenticTeammates}. In medicine, agentic systems are increasingly defined by their ability to plan, use tools, maintain intermediate state, coordinate specialized modules, and interact with clinicians or clinical environments \cite{Qiu2024NatMachIntellAgenticSystems}. Coordinated networks of specialized medical agents have been proposed as a way to organize heterogeneous AI tools across clinical and operational tasks \cite{Moritz2025NatBMECoordinatedAgents}. At the same time, emerging benchmarks such as MedAgentBench emphasize that medical agents should be evaluated in interactive environments that require information retrieval, action execution, and workflow-level reasoning rather than static question answering alone \cite{Jiang2025NEJMAIMedAgentBench}. For thyroid ultrasound, this means that an agentic system should not merely output a malignancy score; it should connect image evidence, nodule masks, measurements, sonographic descriptors, lymph-node findings, risk estimates, report statements, uncertainty signals, and clinician feedback within a single auditable workflow \cite{Tessler2017ACRTIRADS,Grani2024NatRevEndocrinol}.

Here we present ThyroidXAgent, a clinician-interactive agentic AI framework for thyroid ultrasound diagnosis and reporting. The system is designed to support the thyroid ultrasound workflow rather than to replace it with a single end-to-end model. It integrates public thyroid ultrasound datasets with large-scale institutional clinical data and organizes heterogeneous inputs into task-specific workflows for nodule localization, malignancy diagnosis, malignant-lesion characterization, and structured report generation. ThyroidXAgent coordinates segmentation models, classification models, radiomics extraction, tabular learning, measurement tools, anatomical-context parsing, report-template retrieval, and post hoc explanation modules. A planning-and-routing layer selects the relevant tools for each case, consolidates their outputs into a case-level thyroid evidence store, and exposes masks, measurements, sonographic descriptors, risk estimates, uncertainty signals, and report clauses for clinician inspection and correction.

We evaluate ThyroidXAgent along three clinically motivated axes. First, we test whether agentic orchestration improves nodule localization and malignancy diagnosis across heterogeneous ultrasound datasets. Second, we assess whether the framework extends beyond benign--malignant classification to clinically relevant malignant-lesion tasks, including ultrasound-based prediction of lymph-node metastasis and follicular versus papillary thyroid carcinoma subtype. Third, we formulate thyroid ultrasound reporting as structured evidence-to-report generation, in which image-derived findings are first converted into auditable evidence and then assembled into editable clinical reports. To evaluate clinical semantic correctness, we introduce ThyClinScore, a thyroid-ultrasound-specific metric that compares lesion-level and feature-level information rather than surface word overlap alone. By linking thyroid ultrasound data resources, domain-specific tool use, structured evidence generation, controlled report assembly, and clinician feedback, ThyroidXAgent provides a reproducible framework for developing auditable agentic AI systems in specialty medical imaging.


\section{Results}
\subsection{Segmentation, classification performance and interpretability}
Accurate lesion delineation and reliable benign--malignant classification are central to thyroid ultrasound decision-making, yet both remain challenging across datasets with different class balance and lesion geometry (Supplementary Figs.~\ref{fig:BM_Case_Counts} and~\ref{fig:Mask_Position_Size}). Across five segmentation datasets, ThyroidXAgent achieved a mean Dice of 85.24\% and a mean HD95 of 8.30, compared with 78.77\% and 14.44 for UltraFedFM~\cite{jiang2025pretraining}; exact per-dataset values and 95\% confidence intervals are reported in Supplementary Table~\ref{tab:seg_performance}. Across the four datasets that also supported benign--malignant classification, ThyroidXAgent achieved a mean AUROC of 0.9466 and a mean AUPRC of 0.8361, substantially exceeding GPT-5.5~\cite{openai2025gpt5systemcard} (0.7025 and 0.6441, respectively). Cross-dataset comparisons are summarized in Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}a--d and Supplementary Table~\ref{tab:cls_performance}. On a blinded 500-image physician comparison set, ThyroidXAgent also achieved the strongest overall discrimination, with an AUROC of 0.9256 and an AUPRC of 0.9250 (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}f,g), indicating strong performance under direct reader-level comparison.

To interpret these predictions, we next examined cohort-level SHAP profiles and representative cases. Morphology-related descriptors, particularly Sphericity and Elongation, dominated benign--malignant classification, whereas texture and intensity features provided complementary signal (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}e). Representative benign and malignant cases showed that stronger segmentation was accompanied by tighter alignment between lesion boundaries, attribution maps and downstream predictions (Supplementary Fig.~\ref{fig:BM_cases}). These signals were further exposed in an interactive review workflow for mask inspection, feature attribution and corrective annotation (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}h). In this clinician-in-the-loop setting, AI assistance shortened segmentation time across most cases while preserving Dice agreement with manual segmentation (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}i--k).

We then evaluated whether the same framework generalized beyond benign--malignant discrimination to clinically consequential malignant-lesion tasks. On lymph node metastasis prediction, ThyroidXAgent achieved an AUROC of 0.864 and an AUPRC of 0.881, corresponding to relative improvements of 12.7\% and 19.6\% over LLNM-Net~\cite{shen2025explainable}; on FTC/PTC subtype classification, it achieved an AUROC of 0.805 and an AUPRC of 0.786, corresponding to relative improvements of 12.9\% and 10.5\% over Tiger-Model~\cite{dai2025improving} (Fig.~\ref{fig:ThyroidXAgent_Malignant_Image_tasks}b and Supplementary Table~\ref{tab:Malignant_images_tasks_performance}). SHAP analyses again revealed task-specific radiomic signatures, with lymph node metastasis prediction driven mainly by intensity- and size-related features and FTC/PTC discrimination driven more strongly by texture heterogeneity and shape descriptors (Fig.~\ref{fig:ThyroidXAgent_Malignant_Image_tasks}c--f). Distinct attribution profiles were therefore observed across the two malignant-lesion tasks.


\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ThyroidXAgent_SegCls_performance.pdf}
    \caption{ThyroidXAgent improves thyroid nodule segmentation and benign--malignant classification while enabling clinician-interactive review. \textbf{a--d}, Cross-dataset segmentation and classification performance across thyroid ultrasound benchmarks. \textbf{e}, Cohort-level SHAP beeswarm analysis for benign--malignant classification. \textbf{f,g}, ROC and precision--recall curves on the 500-image physician comparison set, with clinician operating points shown before and after ThyroidXAgent support. \textbf{h}, Interactive review workflow for mask inspection, SHAP-based feature analysis and corrective annotation. \textbf{i}, Segmentation time under manual and AI-assisted workflows. \textbf{j}, Within-case time saving ranked across cases. \textbf{k}, Paired Dice distributions for manual and AI-assisted segmentation, indicating preserved segmentation quality.}
    \label{fig:ThyroidXAgent_SegCls_performance}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/Malignant_Image_tasks.pdf}
    \caption{ThyroidXAgent generalizes to clinically relevant malignant-lesion stratification tasks and provides task-specific radiomic explanations. \textbf{a}, Workflow for SHAP-based interpretation of malignant-lesion tasks. \textbf{b}, Performance comparison between ThyroidXAgent and the corresponding specialist baselines for FTC/PTC subtype classification and lymph node metastasis prediction, reported as AUROC and AUPRC; percentages denote the relative improvement of ThyroidXAgent over each baseline. \textbf{c,d}, Global and representative local SHAP analyses for lymph node metastasis prediction. \textbf{e,f}, Global and representative local SHAP analyses for FTC/PTC subtype classification, showing stronger contributions from texture heterogeneity and shape descriptors.}
    \label{fig:ThyroidXAgent_Malignant_Image_tasks}
\end{figure}

\subsection{Report generation}
We next evaluated the report-generation capability of ThyroidXAgent, a core task of the thyroid diagnostic agent. The report-generation workflow used multi-view and multi-modal thyroid ultrasound inputs to construct image priors, invoked segmentation, classification, measurement and captioning tools through an agentic planning-and-execution process, and converted the resulting structured facts into reports through BM25-based template retrieval, slot filling and clause assembly (Fig.~\ref{fig:thyroidxagent_report_generation}c--g). The auxiliary tools used by this workflow and their held-out performance are summarized in Supplementary Table~\ref{tab:auxiliary_tools}. In addition to conventional natural-language generation metrics, we constructed ThyClinScore, a thyroid-ultrasound-specific clinical semantic metric that structures ground-truth and generated reports, matches lesion entries and compares clinically relevant attributes (Fig.~\ref{fig:thyroidxagent_report_generation}b). We assessed the generated reports on an in-house dataset and the public KMVE benchmark using both metric families (Fig.~\ref{fig:thyroidxagent_report_generation}h and Supplementary Tables~\ref{tab:report_generation_nlg_ci} and~\ref{tab:report_generation_clinical_ci}).

On conventional n-gram and sequence-overlap metrics, ThyroidXAgent achieved the strongest overall performance across the two evaluation settings (Fig.~\ref{fig:thyroidxagent_report_generation}h). On the in-house dataset, it obtained the highest BLEU-1, BLEU-4 and ROUGE$_L$ scores, reaching 0.5799, 0.3291 and 0.5390, respectively, while maintaining a METEOR score of 0.3575 that was close to the best baseline value of 0.3628. On the KMVE dataset, ThyroidXAgent ranked first on all four natural-language generation metrics, with BLEU-1 of 0.6209, BLEU-4 of 0.4465, METEOR of 0.3596 and ROUGE$_L$ of 0.5826. These results indicate that grounding report generation in structured diagnostic facts preserved the surface form of expert reports while improving overlap-based agreement with reference reports.

Clinical semantic evaluation with ThyClinScore further showed that the generated reports retained clinically relevant information rather than only matching reference wording (Fig.~\ref{fig:thyroidxagent_report_generation}b,h). On the in-house dataset, ThyroidXAgent achieved the highest ThyClinScore of 0.5002, together with the highest feature accuracy (0.6102) and F1 score (0.5073). Its completeness score (0.9654) was comparable to the best-performing baseline, and its consistency score (0.4884) was close to the highest baseline value. On the KMVE dataset, ThyroidXAgent again achieved the highest ThyClinScore (0.4465), while maintaining competitive feature accuracy, completeness and consistency. Because individual submetrics emphasized different failure modes, such as false lesion detection, feature mismatch or missing structured fields, the combined ThyClinScore suggests that ThyroidXAgent provided the best overall balance between report completeness and clinical semantic alignment among the compared models.

To validate the clinical reliability of ThyClinScore, we next performed two-sided Pearson correlation analyses across evaluation metrics and against a location-aware GPT-5 judge. Conventional natural-language generation metrics were strongly correlated with one another, with pairwise correlations of 0.90--0.95 among BLEU-1, BLEU-4, METEOR and ROUGE$_L$ (Supplementary Fig.~\ref{fig:experiment_for_thyclinscore}a). This high internal correlation indicated that these overlap-based metrics were largely homogenized in their evaluation criteria. In contrast, their correlations with the proposed clinical semantic metrics were lower, indicating that lesion matching, completeness and consistency captured broader and more clinically distinct dimensions of report quality. When benchmarked against the location-aware GPT-5 judge, ThyClinScore achieved the highest correlation among all evaluated metrics (Pearson's \(r=0.696\), \(p<0.001\)), exceeding both conventional metrics and individual clinical semantic submetrics (Supplementary Fig.~\ref{fig:experiment_for_thyclinscore}b). Overall, these results show that ThyClinScore addresses an important limitation of conventional overlap-based metrics by better reflecting the clinical semantic correctness of thyroid ultrasound reports.

We then examined whether ThyroidXAgent could improve the efficiency of human report writing in a reader-study setting. Two physicians wrote reports for 151 thyroid ultrasound videos under both manual and AI-assisted workflows, with each case evaluated in both workflows but by different physicians to reduce memory bias (Fig.~\ref{fig:reader_study}a). AI-assisted report writing shortened the mean reporting time from 2.5 to 1.8 min per case, corresponding to a 27.4\% reduction, while preserving the paired case structure of the comparison (Fig.~\ref{fig:reader_study}b,c). The time-saving effect was also observed after stratification by physician, with reporting-time reductions of 28.1\% and 26.6\% for the two readers, respectively (Fig.~\ref{fig:reader_study}d). Representative cases further illustrate how the structured evidence generated by ThyroidXAgent can support clinically concordant statements on gland morphology, nodule location, measurements, sonographic features and diagnostic impression, while exposing partially correct or incorrect statements for review (Fig.~\ref{fig:reader_study}e).


\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ThyroidRGAgent_fig1(3).pdf}
    \caption[Report generation and evaluation in ThyroidXAgent]{
    Overview of report generation and evaluation in ThyroidXAgent. The figure presents its report generation pipeline and the proposed ThyClinScore metric.
    a. Data resources and experimental settings.
    b. ThyClinScore structures ground-truth and generated reports, matches lesions, and compares clinically relevant attributes.
    c. Multi-view and multi-modal thyroid ultrasound inputs.
    d. ROI cropping and context parsing produce agent-ready image priors.
    e. The planner generates a diagnostic plan from image priors and tool definitions.
    f. A ReAct-style executor invokes segmentation, classification, measurement, and captioning tools on demand.
    g. Structured evidence is converted into reports through BM25 template retrieval, slot filling, and clause combination.
    h. Comparison with baselines on the in-house dataset and the public KMVE benchmark.
    }
    \label{fig:thyroidxagent_report_generation}
\end{figure}

\begin{figure}[p]
    \centering
    \includegraphics[width=\textwidth]{imgs/ReaderStudy[TODO].pdf}
    \caption{Reader study of AI-assisted thyroid ultrasound report writing. \textbf{a}, Cross-over reader-study design comparing manual and AI-assisted workflows. \textbf{b--d}, Reporting-time analyses across 151 paired cases, showing a 27.4\% reduction overall and consistent physician-stratified time saving. \textbf{e}, Representative qualitative examples illustrating report generation for a normal thyroid case and a malignant thyroid nodule case, with clinically correct, partially correct and incorrect statements highlighted in comparison with the ground-truth reports.}
    \label{fig:reader_study}
\end{figure}

\section{Discussion}

\section{Methods}

%\subsection{Dataset} 

\noindent\textit{Dataset and task definition.} We built the benchmark from TN3K~\cite{gong2021multi}, TN5K~\cite{zhang2025tn5000}, DDTI~\cite{pedraza2015open}, ThyroidXL~\cite{duong2025thyroidxl}, and PKTN~\cite{sun2025clip}. The segmentation task predicts a binary nodule mask. The classification task was trained on binary labels from TN3K, TN5K, DDTI, and ThyroidXL, whereas PKTN provided no classification labels. To construct the expert pool, we merged the training portions across datasets into stacked training sets, with the largest stacked training set containing 18,723 images. Different DINOv3-based~\cite{simeoni2025dinov3} experts were trained under varying stacked-training compositions, dilation designs, and input resolutions of 128, 224, and 448. To compare against recent open-source and proprietary multimodal large models, we used MedGemma~\cite{sellergren2025medgemma} and Qwen3-VL-8B-Instruct~\cite{bai2025qwen3} with LoRA~\cite{hu2022lora} fine-tuning, whereas GPT-5.5~\cite{openai2025gpt5systemcard} and Gemini-3.1-Pro~\cite{comanici_gemini_2025} were evaluated with prompt-based API inference; classification scores for the VLMs were derived from the conditional likelihoods of the two output labels.

\noindent\textit{ThyroidXAgent for Segmentation and Classification.} As illustrated in Fig.~\ref{fig:ThyroidXAgent_for_seg_and_cls}, the DINOv3-based expert pool uses task-specific lightweight heads. The segmentation branch adopts a U-Net-style decoder with skip fusion to output dense mask probabilities and is optimized with a weighted BCE+IoU loss. The classification branch pools backbone features with global average and max pooling, then applies a compact attention head to predict class probabilities with generalized logit adjustment. This expert pool is intended to reduce sensitivity to dataset-specific bias and improve robustness across heterogeneous acquisition conditions~\cite{torralba2011unbiased,liu2024decade}. The radiomics branch extracts 2D PyRadiomics~\cite{van2017computational} descriptors from image-mask pairs to support downstream tabular classification, focusing on shape and texture families such as area and GLCM energy. Connected component analysis is used as an optional deterministic refinement step to remove isolated noisy regions and preserve connected anatomical structures before radiomics extraction~\cite{liu2025shapekit}. The selected lesion mask is then used to generate radiomic features, which are passed to an AutoGluon-based~\cite{erickson2020autogluon} tabular classifier. The tabular classifier is accompanied by SHAP-based post hoc interpretation to identify the most influential radiomic features for each prediction. During inference, segmentation experts first produce candidate masks and confidence scores, and classification experts produce class probabilities and confidence scores. The LLM router summarizes these outputs as structured evidence, using segmentation evidence built from mask-quality proxies, expert confidence, and inter-expert disagreement, and classification evidence built from class probabilities, classifier confidence, and radiomics descriptors. It also conditions on ultrasound metadata, including image resolution, device, and data source, to account for acquisition-related variation. The LLM operates only on these summaries rather than on raw images, uses low-temperature decoding (temperature 0.3), and emits a strict JSON decision to select the most reliable final prediction.

\noindent\textit{ThyroidXAgent for report generation.} In the report-generation branch, ThyroidXAgent took a case-level ultrasound examination as input and generated a standardized report comprising ultrasound findings and impression (Fig.~\ref{fig:thyroidxagent_report_generation}c--g). The input included all available multi-view and multi-modal images, rather than a manually selected representative frame. After ROI cropping and context parsing, ThyroidXAgent extracted image-level priors, including anatomical region, modality, view and nodule presence (Fig.~\ref{fig:thyroidxagent_report_generation}c,d). These priors conditioned a Planner--Executor workflow~\cite{wang_plan-and-solve_2023}. The planner produced a case-specific diagnostic outline from the image context and available tool definitions, specifying the major diagnostic subtasks, their approximate order and their dependency structure, without enumerating a fixed sequence of image-level operations. Guided by this outline, the executor performed ReAct-style local decision-making during tool use~\cite{yao_react:_2022}, dynamically selecting image targets according to metadata and intermediate observations (Fig.~\ref{fig:thyroidxagent_report_generation}e,f). The tools used in the preprocessing and executor stages, together with their held-out performance, are summarized in Supplementary Table~\ref{tab:auxiliary_tools}. This design was intended to reduce the rigidity of fixed serial pipelines while limiting redundant tool calls and missed findings associated with unconstrained reactive execution.

Following tool execution, gland-level, nodule-level and lymph-node evidence was consolidated into a structured clinical record. Because the diagnostic content had been extracted by specialized tools, report generation was formulated as controlled data-to-text generation~\cite{rebuff_data2text_2020}, rather than open-ended language-model decoding, which may introduce factual hallucinations in clinical text generation~\cite{ji2023survey,farquhar2024detecting}. ThyroidXAgent therefore used a training-free template retrieval and filling strategy (Fig.~\ref{fig:thyroidxagent_report_generation}g). The template library was constructed from 20,400 real-world thyroid ultrasound reports after exclusion of all test cases. Findings and impression components were stored separately, and patient-specific measurements and lesion-specific descriptors were abstracted to enable case-specific filling. During inference, templates matched to the structured evidence were retrieved and populated with the corresponding measurements, anatomical locations, ultrasound features, TI-RADS categories, CDFI findings and lymph-node status. For multi-view or multi-nodule examinations, lesion-level evidence was reconciled before report assembly, enabling the final report to describe case-level thyroid findings while preserving traceability to the supporting tool outputs.



\section{Code availability}

\section{Acknowledgments}

\section{Author Contributions}

Conceptualization: YL, HG, YW, QK, XL;
Methodology: HG, YW, QK, XL;
Investigation: HG, YW, QK, XL, LL, BW, YZ, JZ, GC, JC, YY, XY, XZ;
Visualization: HG, QK, XL, BW;
Funding acquisition: YL;
Project administration: YL, LL;
Supervision: YL, XZ, XY, YY;
Writing -- original draft: HG, QK, XL, BW;
Writing -- review \& editing: YL, YW, HG, QK.

\section{Competing Interests}

\clearpage
\begin{appendices}
\clearpage
\section*{Supplementary Information}
\clearpage
\renewcommand{\thefigure}{S\arabic{figure}}
\renewcommand{\thetable}{S\arabic{table}}
\setcounter{figure}{0}
\setcounter{table}{0}

\subsection{ThyroidXAgent for Segmentation and Classification}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ThyroidXAgent_for_seg_and_cls.pdf}
    \caption{Overview of ThyroidXAgent for segmentation and classification. The expert pool generates candidate segmentation masks and class probabilities from DINOv3-based experts, while the radiomics branch derives PyRadiomics descriptors from the selected lesion mask, feeds them to an AutoGluon-based classifier, and provides SHAP-based post hoc interpretation. An LLM router combines these candidate outputs with ultrasound metadata, including image resolution, device, and data source, to select the most reliable final prediction.}
    \label{fig:ThyroidXAgent_for_seg_and_cls}
\end{figure}

\section{Data availability}
\begin{table}[htbp]
\centering
\caption{Composition of the thyroid ultrasound benchmark across source datasets and study cohorts. Numbers indicate images contributed by each dataset to the full benchmark ((n=23{,}622)) and to the training ((n=18{,}723)), validation ((n=945)) and test ((n=3{,}954)) cohorts. Percentages indicate the proportion of each dataset within the corresponding column. PKTN contributed images for segmentation only, as classification labels were unavailable.}
\label{tab:dataset_summary}
\renewcommand{\arraystretch}{1.2}
\setlength{\tabcolsep}{8pt}
\begin{tabular}{lcccc}
\hline
\cellcolor[gray]{0.90}\textbf{DataSet} &
\cellcolor[gray]{0.90}\textbf{Total (n=23622)} &
\multicolumn{3}{c}{\cellcolor[gray]{0.90}\textbf{Cohort}} \\
\cline{3-5}
\cellcolor[gray]{0.90}\textbf{} &
\cellcolor[gray]{0.90}\textbf{} &
\cellcolor[gray]{0.90}\makecell[c]{\textbf{Train Cohort}\\\textbf{(n=18723)}} &
\cellcolor[gray]{0.90}\makecell[c]{\textbf{Valid Cohort}\\\textbf{(n=945)}} &
\cellcolor[gray]{0.90}\makecell[c]{\textbf{Test Cohort}\\\textbf{(n=3954)}} \\
\hline
\makecell[l]{TN3K~\cite{gong2021multi}} & 5347 (22.64\%) & 4633 (24.74\%) & 100 (10.58\%) & 614 (15.53\%) \\
\hline
\makecell[l]{TN5K~\cite{zhang2025tn5000}} & 5000 (21.17\%) & 3500 (18.69\%) & 500 (52.91\%) & 1000 (25.29\%) \\
\hline
\makecell[l]{ThyroidXL~\cite{duong2025thyroidxl}} & 11631 (49.26\%) & 9441 (50.42\%) & 100 (10.58\%) & 2090 (52.95\%) \\
\hline
\makecell[l]{PKTN~\cite{sun2025clip}} & 1003 (4.25\%) & 703 (3.75\%) & 150 (15.87\%) & 150 (3.79\%) \\
\hline
\makecell[l]{DDTI~\cite{pedraza2015open}} & 349 (2.70\%) & --- & --- & 349 (2.43\%) \\
\hline
\makecell[l]{Shanghai7K} & 7288 (---\%) & --- & --- & 7288 (---\%) \\
\hline
\makecell[l]{Zhujiang2K} & 1854 (---\%) & --- & --- & 1854 (---\%) \\
\hline
\end{tabular}
\end{table}



\begin{table}[htbp]
\centering
\caption{Comparison of Thyroid Ultrasound Datasets}
\label{tab:dataset_comparison}
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}llllllll@{}}
\toprule
\textbf{Dataset} & \textbf{Images} & \textbf{Train} & \textbf{Test} & \textbf{File Format} & \textbf{Task} & \textbf{Location} & \textbf{Ultrasonic Imaging Device} \\
\midrule

TGVideo~\cite{wunderling2017comparison} & 15,186 (16 cases) & 15,186 & N/A &
\begin{tabular}[c]{@{}l@{}}Image: DICOM\\Mask: DICOM\end{tabular} &
Segmentation &
Germany &
GE Logiq E9 \\

\midrule
DDTI~\cite{pedraza2015open} & 637 & N/A & 637 &
\begin{tabular}[c]{@{}l@{}}Image: PNG\\Mask: PNG\\Label: CSV\end{tabular} &
\begin{tabular}[c]{@{}l@{}}Segmentation\\Classification\end{tabular} &
Colombia &
\begin{tabular}[c]{@{}l@{}}TOSHIBA Nemio 30\\TOSHIBA Nemio MX\end{tabular} \\

\midrule
TN3K~\cite{gong2021multi,gong2022less,gong2023thyroid} & 3,493 & 2,879 & 614 &
\begin{tabular}[c]{@{}l@{}}Image: JPG\\Mask: JPG\\Label: CSV\end{tabular} &
\begin{tabular}[c]{@{}l@{}}Segmentation\\Classification\end{tabular} &
Guangzhou, China &
\begin{tabular}[c]{@{}l@{}}GE Logiq E9\\ARIETTA 850\\RESONA 70B\end{tabular} \\

\midrule
24-TMI~\cite{li2024ultrasound} &
\begin{tabular}[c]{@{}l@{}}2,460 cases\\4,920 images\end{tabular} &
3,934 & 986 &
JPEG &
Report Generation &
Beijing, China &
N/A \\

\midrule
TN5K~\cite{zhang2025tn5000} & 5,000 & 4,000 & 1,000 &
\begin{tabular}[c]{@{}l@{}}Image: JPG\\Label: XML\end{tabular} &
\begin{tabular}[c]{@{}l@{}}Detection\\Classification\end{tabular} &
Beijing, China &
\begin{tabular}[c]{@{}l@{}}GE Logiq E9\\GE S7\end{tabular} \\

\midrule
ThyUS2Path~\cite{hou2024ultrasonography} & 8,508 & 5,457 & 3,051 &
\begin{tabular}[c]{@{}l@{}}Image: JPG\\Label: CSV\end{tabular} &
Classification &
Zhejiang, China &
Esaote MyLab (Portable) \\

\midrule
Cine-clip~\cite{stanford2024thyroid} &
\begin{tabular}[c]{@{}l@{}}17,412 frames\\192 cases\\avg. 90 frames/case\end{tabular} &
N/A & N/A &
\begin{tabular}[c]{@{}l@{}}Image: HDF5\\Label: CSV\end{tabular} &
\begin{tabular}[c]{@{}l@{}}Segmentation\\Classification\end{tabular} &
California, USA &
N/A \\

\midrule
AHU~\cite{yang2025annotated} &
\begin{tabular}[c]{@{}l@{}}1,833 cases\\125,896 images\end{tabular} &
N/A & N/A &
\begin{tabular}[c]{@{}l@{}}Image: JPG\\Label: Folder-level\end{tabular} &
Classification &
China (web scraping) &
Heterogeneous \\

\midrule
ThyroidXL~\cite{duong2024thyroidxl} & 11,635 & 9,541 & 2,094 &
\begin{tabular}[c]{@{}l@{}}Image: PNG\\Mask: PNG\\Label: TXT\end{tabular} &
\begin{tabular}[c]{@{}l@{}}Segmentation\\Classification\\Detection\end{tabular} &
Vietnam &
Hitachi Aloka Arietta V70 \\

\midrule
PKTN~\cite{sun2024cliptnsegmultimodalhybridframework} & 1,005 & N/A & N/A &
\begin{tabular}[c]{@{}l@{}}Image: JPG\\Mask: JPG\end{tabular} &
Segmentation &
Beijing, China &
N/A \\

\midrule
TNVideo & 148 cases & N/A & N/A & N/A &
\begin{tabular}[c]{@{}l@{}}Segmentation\\Finding\end{tabular} &
Guangzhou, China &
N/A \\

\bottomrule
\end{tabular}%
}
\end{table}

\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Segmentation performance across multi thyroid ultrasound datasets. Upper block, Dice score; lower block, 95th percentile Hausdorff distance (HD95). Values are reported with 95\% confidence intervals.}
\label{tab:seg_performance}

\footnotesize
\setlength{\tabcolsep}{5.5pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lcccccc}
\toprule
\textbf{Model}
& \textbf{TN3K}
& \textbf{ThyroidXL}
& \textbf{PKTN}
& \textbf{TN5K}
& \textbf{Zhujiang2K}
& \textbf{Shanghai7K} \\
\midrule
TransUnet~\cite{chen2024transunet}
& $81.84 \pm 1.62$
& $85.75 \pm 0.57$
& $76.89 \pm 3.56$
& $78.54 \pm 1.51$
& $80.72 \pm 0.97$
& $84.83 \pm 0.37$ \\
MedSegX~\cite{zhang2025generalist}
& $83.93 \pm 0.79$
& $79.98 \pm 0.36$
& $80.63 \pm 0.42$
& $83.10 \pm 0.48$
& $84.06 \pm 0.39$
& $85.40 \pm 0.18$ \\
MedSAM2~\cite{ma2025medsam2}
& $84.47 \pm 1.02$
& $83.74 \pm 0.46$
& $80.71 \pm 0.98$
& $81.22 \pm 1.14$
& $90.73 \pm 0.46$
& \textbf{91.53 $\pm$ 0.01} \\
UltraFedFM~\cite{jiang2025pretraining}
& $81.18 \pm 1.46$
& $84.70 \pm 0.53$
& $75.31 \pm 1.12$
& $77.13 \pm 1.38$
& $80.64 \pm 0.84$
& $83.10 \pm 0.33$ \\
\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{85.28 $\pm$ 1.28}
& \textbf{87.58 $\pm$ 0.44}
& \textbf{82.96 $\pm$ 1.98}
& \textbf{83.26 $\pm$ 1.34}
& \textbf{96.83 $\pm$ 0.09} 
& 91.46 $\pm$ 0.14 \\

\midrule
TransUnet~\cite{chen2024transunet}
& $27.27 \pm 5.52$
& $22.42 \pm 1.34$
& $26.88 \pm 9.66$
& $22.32 \pm 3.43$
& $18.37 \pm 0.75$
& $18.81 \pm 0.74$ \\
MedSegX~\cite{zhang2025generalist}
& $10.95 \pm 0.64$
& $11.07 \pm 0.32$
& $10.83 \pm 0.70$
& $11.76 \pm 0.76$
& $10.96 \pm 0.35$
& $9.37 \pm 0.18$ \\
MedSAM2~\cite{ma2025medsam2}
& $11.51 \pm 1.53$
& $6.91 \pm 0.44$
& $10.69 \pm 2.34$
& $10.94 \pm 1.12$
& $6.79 \pm 0.57$
& $3.56 \pm 0.10$ \\
UltraFedFM~\cite{jiang2025pretraining}
& $14.98 \pm 2.10$
& $8.10 \pm 0.58$
& $16.08 \pm 1.67$
& $14.96 \pm 1.65$
& $14.57 \pm 1.09$
& $9.06 \pm 0.38$ \\
\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{10.31 $\pm$ 1.70}
& \textbf{5.43 $\pm$ 0.53}
& \textbf{9.01 $\pm$ 3.58}
& \textbf{10.12 $\pm$ 1.23}
& \textbf{0.36 $\pm$ 0.06}
& \textbf{1.92 $\pm$ 0.08} \\

\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}

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
& \textbf{Zhujiang2K} \\
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
& \textbf{0.8642 $\pm$ 0.0550}
& \textbf{0.8808 $\pm$ 0.0537}
& \textbf{0.8053 $\pm$ 0.0599}
& \textbf{0.7863 $\pm$ 0.0793}\\
\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}



\begin{table*}[!htp]
\centering
\caption{Auxiliary tools used by ThyroidXAgent and their performance on held-out test sets. The preprocessing tools include image normalization, nodule-presence triage, and anatomical context parsing. The executor-stage tools include measurement support, gland localization, lymph-node screening, gland captioning, and nodule-feature extraction. Compact tool-level results are presented using merged cells, whereas anatomical context parsing and nodule-feature extraction are further expanded at the class level. For the binary margin and shape classifiers, AUROC and AUPRC are computed at the tool level and are therefore reported once across the two class rows. AP, average precision; MAE, mean absolute error; MSE, mean squared error; MAPE, mean absolute percentage error.}
\label{tab:auxiliary_tools}
\scriptsize
\setlength{\tabcolsep}{2.3pt}
\renewcommand{\arraystretch}{1.08}
\resizebox{\textwidth}{!}{%
\begin{tabular}{|>{\raggedright\arraybackslash}p{0.085\textwidth}|>{\raggedright\arraybackslash}p{0.115\textwidth}|>{\raggedright\arraybackslash}p{0.13\textwidth}|>{\raggedright\arraybackslash}p{0.185\textwidth}|>{\centering\arraybackslash}p{0.045\textwidth}|>{\centering\arraybackslash}p{0.045\textwidth}|>{\centering\arraybackslash}p{0.045\textwidth}|>{\centering\arraybackslash}p{0.065\textwidth}|>{\centering\arraybackslash}p{0.085\textwidth}|>{\centering\arraybackslash}p{0.078\textwidth}|>{\centering\arraybackslash}p{0.078\textwidth}|>{\centering\arraybackslash}p{0.078\textwidth}|}
\hline
\textbf{Agent stage} & \textbf{Tool group} & \multicolumn{2}{c|}{\textbf{Tool}} & \multicolumn{2}{c|}{\textbf{Test set}} & \multicolumn{3}{c|}{\textbf{Primary result}} & \multicolumn{3}{c|}{\textbf{Secondary result}} \\
\hline
\multirow{10}{*}{Preprocessing}
& Image normalization & \multicolumn{2}{l|}{Ultrasound ROI cropping} & \multicolumn{2}{c|}{\(n=49\)} & \multicolumn{3}{l|}{Dice, 0.9803; IoU, 0.9625} & \multicolumn{3}{l|}{Precision, 0.9902; recall, 0.9717; pixel accuracy, 0.9816} \\
\cline{2-12}
& Case triage & \multicolumn{2}{l|}{Nodule-presence detection} & \multicolumn{2}{c|}{\(n=16{,}467\)} & \multicolumn{3}{l|}{Accuracy, 0.9830; F1, 0.9749} & \multicolumn{3}{l|}{AUROC, 0.9981; AP, 0.9961; specificity, 0.9821} \\
\cline{2-12}
& \multicolumn{11}{c|}{\textbf{Anatomical context parsing}} \\
\cline{2-12}
& \textbf{Tool} & \textbf{Class} & \textbf{Train} & \textbf{Val} & \textbf{Test} & \textbf{Total} & \textbf{Precision} & \textbf{Recall} & \textbf{F1} & \textbf{AUROC} & \textbf{AUPRC} \\
\cline{2-12}
& \multirow{6}{*}{\makecell[l]{Thyroid-region\\classification}} & Left-lobe lateral view & 780 & 110 & 159 & 1,049 & 0.6643 & 0.5975 & 0.6291 & 0.8521 & 0.7185 \\
\cline{3-12}
& & Right-lobe lateral view & 946 & 133 & 199 & 1,278 & 0.6460 & 0.7337 & 0.6871 & 0.8327 & 0.7368 \\
\cline{3-12}
& & Bilateral thyroid view & 120 & 19 & 30 & 169 & 0.8929 & 0.8333 & 0.8621 & 0.9896 & 0.8911 \\
\cline{3-12}
& & Left-lobe transverse view & 267 & 52 & 41 & 360 & 0.7045 & 0.7561 & 0.7294 & 0.9567 & 0.8198 \\
\cline{3-12}
& & Right-lobe transverse view & 272 & 61 & 79 & 412 & 0.8088 & 0.6962 & 0.7483 & 0.9553 & 0.8585 \\
\cline{3-12}
& & Neck region & 267 & 21 & 12 & 300 & 1.0000 & 0.9167 & 0.9565 & 0.9974 & 0.9524 \\
\hline
\multirow{20}{*}{Executor}
& Measurement support & \multicolumn{2}{l|}{Spacing prediction} & \multicolumn{2}{c|}{Not reported} & \multicolumn{3}{l|}{MAE, 0.0131; \(R^2\), 0.8520} & \multicolumn{3}{l|}{MSE, \(5.66\times10^{-4}\); MAPE, 21.39\%} \\
\cline{2-12}
& Gland localization & \multicolumn{2}{l|}{Gland segmentation} & \multicolumn{2}{c|}{\(n=90\)} & \multicolumn{3}{l|}{Dice, 0.8006; IoU, 0.6866} & \multicolumn{3}{l|}{Precision, 0.8025; recall, 0.8339} \\
\cline{2-12}
& Neck-region screening & \multicolumn{2}{l|}{Cervical lymph-node detection} & \multicolumn{2}{c|}{\(n=49\)} & \multicolumn{3}{l|}{Accuracy, 0.7959; F1, 0.7368} & \multicolumn{3}{l|}{AUROC, 0.8163} \\
\cline{2-12}
& Gland description & \multicolumn{2}{l|}{Gland captioning} & \multicolumn{2}{c|}{\(n=400\)} & \multicolumn{3}{l|}{BLEU-4, 0.5898; METEOR, 0.4582} & \multicolumn{3}{l|}{ROUGE$_L$, 0.7450; CIDEr, 2.7736} \\
\cline{2-12}
& \multicolumn{11}{c|}{\textbf{Nodule feature extraction}} \\
\cline{2-12}
& \textbf{Tool family} & \textbf{Feature classifier} & \textbf{Class} & \textbf{Train} & \textbf{Val} & \textbf{Test} & \textbf{Total} & \textbf{Specificity} & \textbf{Sensitivity} & \textbf{AUROC} & \textbf{AUPRC} \\
\cline{2-12}
& \multirow{14}{*}{\makecell[l]{Nodule-feature\\classification}}
& \multirow{3}{*}{Composition} & Cystic & 1,877 & 234 & 234 & 2,345 & 0.8345 & 0.8571 & 0.9189 & 0.9127 \\
\cline{4-12}
& & & Mixed cystic and solid & 893 & 111 & 111 & 1,115 & 0.9122 & 0.4324 & 0.8272 & 0.5852 \\
\cline{4-12}
& & & Solid & 1,438 & 179 & 179 & 1,796 & 0.8421 & 0.7654 & 0.9038 & 0.8164 \\
\cline{3-12}
& & \multirow{4}{*}{Echogenicity} & Anechoic & 1,745 & 218 & 218 & 2,181 & 0.8763 & 0.9167 & 0.9426 & 0.9029 \\
\cline{4-12}
& & & Hyperechoic & 222 & 27 & 27 & 276 & 0.9873 & 0.2963 & 0.8368 & 0.4152 \\
\cline{4-12}
& & & Hypoechoic & 1,453 & 181 & 181 & 1,815 & 0.8491 & 0.7127 & 0.8475 & 0.7788 \\
\cline{4-12}
& & & Isoechoic & 601 & 75 & 75 & 751 & 0.9198 & 0.5467 & 0.8925 & 0.5531 \\
\cline{3-12}
& & \multirow{3}{*}{Echogenic foci} & Macrocalcifications & 1,187 & 148 & 148 & 1,483 & 0.8343 & 0.4595 & 0.6907 & 0.5456 \\
\cline{4-12}
& & & None & 2,209 & 276 & 276 & 2,761 & 0.5342 & 0.7862 & 0.7311 & 0.7327 \\
\cline{4-12}
& & & Punctate echogenic foci & 690 & 86 & 86 & 862 & 0.9127 & 0.2209 & 0.6735 & 0.2975 \\
\cline{3-12}
& & \multirow{2}{*}{Margin} & Ill-defined & 1,191 & 148 & 148 & 1,487 & 0.8510 & 0.7568 & \multirow{2}{*}{0.8721} & \multirow{2}{*}{0.8999} \\
\cline{4-10}
& & & Smooth & 1,664 & 208 & 208 & 2,080 & 0.7568 & 0.8510 &  &  \\
\cline{3-12}
& & \multirow{2}{*}{Shape} & Taller-than-wide & 84 & 10 & 10 & 104 & 0.9750 & 0.5000 & \multirow{2}{*}{0.9337} & \multirow{2}{*}{0.9911} \\
\cline{4-10}
& & & Wider-than-tall & 642 & 80 & 80 & 802 & 0.5000 & 0.9750 &  &  \\
\hline
\end{tabular}%
}
\end{table*}

\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{NLG evaluation results on report generation with test-set bootstrap 95\% confidence intervals. Values are reported as mean$\pm$half-width of the 95\% percentile confidence interval.}
\label{tab:report_generation_nlg_ci}

\footnotesize
\setlength{\tabcolsep}{8pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lcccc}
\toprule
\textbf{Model}
& \textbf{BLEU-1}
& \textbf{BLEU-4}
& \textbf{METEOR}
& \textbf{ROUGE$_L$} \\
\midrule

\rowcolor{gray!20}
\multicolumn{5}{c}{\textbf{In-house Dataset}} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.3500$\pm$0.0100
& 0.1330$\pm$0.0057
& 0.3247$\pm$0.0047
& 0.3577$\pm$0.0077 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.3836$\pm$0.0085
& 0.1374$\pm$0.0054
& 0.3254$\pm$0.0037
& 0.3732$\pm$0.0068 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.3702$\pm$0.0094
& 0.1373$\pm$0.0063
& 0.3308$\pm$0.0038
& 0.3584$\pm$0.0071 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.4483$\pm$0.0130
& 0.2427$\pm$0.0081
& \textbf{0.3628$\pm$0.0040}
& 0.5147$\pm$0.0088 \\

Medgemma~\cite{sellergren2025medgemma}
& 0.0457$\pm$0.0072
& 0.0207$\pm$0.0035
& 0.1736$\pm$0.0051
& 0.0829$\pm$0.0075 \\

LLaVA-Med~\cite{li_llavamed_2023}
& 0.1670$\pm$0.0077
& 0.0159$\pm$0.0024
& 0.1439$\pm$0.0053
& 0.1482$\pm$0.0073 \\

KMVE~\cite{li_ultrasound_2024}
& 0.1743$\pm$0.0131
& 0.0398$\pm$0.0035
& 0.1719$\pm$0.0063
& 0.2212$\pm$0.0039 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.5799$\pm$0.0141}
& \textbf{0.3291$\pm$0.0137}
& 0.3575$\pm$0.0088
& \textbf{0.5390$\pm$0.0119} \\

\midrule

\rowcolor{gray!20}
\multicolumn{5}{c}{\textbf{KMVE Dataset}} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.4467$\pm$0.0154
& 0.2136$\pm$0.0102
& 0.2799$\pm$0.0116
& 0.3850$\pm$0.0148 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.4149$\pm$0.0073
& 0.1668$\pm$0.0062
& 0.3042$\pm$0.0070
& 0.4128$\pm$0.0089 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.5065$\pm$0.0117
& 0.2394$\pm$0.0092
& 0.2863$\pm$0.0083
& 0.4742$\pm$0.0111 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.5425$\pm$0.0135
& 0.2783$\pm$0.0120
& 0.2952$\pm$0.0084
& 0.5066$\pm$0.0118 \\

Medgemma~\cite{sellergren2025medgemma}
& 0.0374$\pm$0.0195
& 0.0219$\pm$0.0151
& 0.1075$\pm$0.0119
& 0.1862$\pm$0.0205 \\

LLaVA-Med~\cite{li_llavamed_2023}
& 0.2842$\pm$0.0149
& 0.1244$\pm$0.0088
& 0.2138$\pm$0.0101
& 0.3939$\pm$0.0127 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.6209$\pm$0.0178}
& \textbf{0.4465$\pm$0.0159}
& \textbf{0.3596$\pm$0.0102}
& \textbf{0.5826$\pm$0.0123} \\

\bottomrule
\end{tabular}

\end{threeparttable}
\end{table*}
```


\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Clinical semantic evaluation results on report generation with test-set bootstrap 95\% confidence intervals. Values are reported as mean$\pm$half-width of the 95\% percentile confidence interval. FDR with $\downarrow$ indicates that lower is better.}
\label{tab:report_generation_clinical_ci}

\footnotesize
\setlength{\tabcolsep}{5.5pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lcccccc}
\toprule
\textbf{Model}
& \textbf{FDR}\,$\downarrow$
& \textbf{Feat Acc}
& \textbf{F1 Score}
& \textbf{Complete.}
& \textbf{Consist.}
& \textbf{ThyClin} \\
\midrule

\rowcolor{gray!20}
\multicolumn{7}{c}{\textbf{In-house Dataset}} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.7189$\pm$0.0362
& 0.5555$\pm$0.0351
& 0.2526$\pm$0.0332
& 0.8208$\pm$0.0132
& 0.4023$\pm$0.0182
& 0.4105$\pm$0.0172 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.4170$\pm$0.0417
& 0.5644$\pm$0.0351
& 0.4390$\pm$0.0402
& 0.8585$\pm$0.0077
& \textbf{0.4980$\pm$0.0166}
& 0.4882$\pm$0.0182 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.6797$\pm$0.0388
& 0.5586$\pm$0.0385
& 0.2965$\pm$0.0366
& 0.8789$\pm$0.0107
& 0.4040$\pm$0.0187
& 0.4280$\pm$0.0176 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.7426$\pm$0.0295
& 0.5804$\pm$0.0373
& 0.2656$\pm$0.0290
& 0.9620$\pm$0.0063
& 0.4809$\pm$0.0142
& 0.4883$\pm$0.0137 \\

Medgemma~\cite{sellergren2025medgemma}
& 0.8943$\pm$0.0229
& 0.5784$\pm$0.0434
& 0.1027$\pm$0.0202
& \textbf{0.9657$\pm$0.0055}
& 0.3353$\pm$0.0119
& 0.3697$\pm$0.0131 \\

LLaVA-Med~\cite{li_llavamed_2023}
& \textbf{0.1625$\pm$0.0363}
& 0.4100$\pm$0.2125
& 0.2582$\pm$0.0426
& 0.4576$\pm$0.0227
& 0.1387$\pm$0.0166
& 0.1752$\pm$0.0150 \\

KMVE~\cite{li_ultrasound_2024}
& 0.4813$\pm$0.0488
& 0.5944$\pm$0.1233
& 0.2103$\pm$0.0390
& 0.5995$\pm$0.0085
& 0.2013$\pm$0.0144
& 0.2265$\pm$0.0145 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& 0.2517$\pm$0.0408
& \textbf{0.6102$\pm$0.0448}
& \textbf{0.5073$\pm$0.0448}
& 0.9654$\pm$0.0055
& 0.4884$\pm$0.0172
& \textbf{0.5002$\pm$0.0220} \\

\midrule

\rowcolor{gray!20}
\multicolumn{7}{c}{\textbf{KMVE Dataset}} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.5843$\pm$0.0427
& 0.6608$\pm$0.0691
& 0.2137$\pm$0.0350
& 0.6180$\pm$0.0113
& 0.4275$\pm$0.0231
& 0.3344$\pm$0.0188 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.4133$\pm$0.0423
& \textbf{0.6967$\pm$0.0492}
& 0.3749$\pm$0.0402
& 0.6506$\pm$0.0038
& 0.4504$\pm$0.0189
& 0.3853$\pm$0.0189 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.3211$\pm$0.0407
& 0.5093$\pm$0.0418
& \textbf{0.4648$\pm$0.0401}
& 0.6270$\pm$0.0045
& 0.4135$\pm$0.0213
& 0.3810$\pm$0.0187 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.4553$\pm$0.0422
& 0.6154$\pm$0.0448
& 0.3823$\pm$0.0397
& 0.6525$\pm$0.0050
& 0.4035$\pm$0.0230
& 0.3674$\pm$0.0193 \\

Medgemma~\cite{sellergren2025medgemma}
& 0.1877$\pm$0.0327
& 0.6820$\pm$0.0463
& 0.2868$\pm$0.0381
& \textbf{0.6622$\pm$0.0033}
& 0.5172$\pm$0.0240
& 0.3932$\pm$0.0203 \\

LLaVA-Med~\cite{li_llavamed_2023}
& \textbf{0.0000$\pm$0.0000}\tnote{*}
& N/A\tnote{*}
& 0.2541$\pm$0.0386
& 0.6508$\pm$0.0007
& \textbf{0.5669$\pm$0.0225}
& 0.3928$\pm$0.0208 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& 0.4184$\pm$0.0434
& 0.6761$\pm$0.0418
& 0.3689$\pm$0.0394
& 0.6467$\pm$0.0027
& 0.5654$\pm$0.0221
& \textbf{0.4465$\pm$0.0206} \\

\bottomrule
\end{tabular}

\begin{tablenotes}[flushleft]
\footnotesize
\item[*] On the KMVE dataset, LLaVA-Med collapsed and predicted
``no abnormality'' for all test samples. Therefore, Feat Acc is N/A
and FDR is 0 because no positive predictions were made.
\end{tablenotes}

\end{threeparttable}
\end{table*}
```

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ExperimentForThyClinScore.pdf}
    \caption{Validation of ThyClinScore for thyroid ultrasound report generation.
    \textbf{a}, Pearson correlation matrix comparing conventional natural-language generation metrics with the proposed clinical semantic metrics. Traditional overlap-based metrics showed high mutual correlations, whereas the clinical semantic metrics captured complementary report-quality dimensions.
    \textbf{b}, Pearson correlations between each metric and a location-aware GPT-5 judge. ThyClinScore achieved the highest correlation among the evaluated metrics. Asterisks indicate statistical significance: * \(p<0.05\), ** \(p<0.01\), and *** \(p<0.001\).}
    \label{fig:experiment_for_thyclinscore}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs_sup/BM_Case_Counts.pdf}
    \caption{Benign and malignant case counts across thyroid ultrasound datasets. Bar plots show the numbers of benign and malignant cases in TN3K, TN5K, ThyroidXL, DDTI and Zhujiang2K. The y axis is logarithmic. Dataset size and class balance vary substantially across cohorts.}
    \label{fig:BM_Case_Counts}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs_sup/Mask_Position_Size.pdf}
    \caption{Spatial and size distributions of lesion masks across datasets. Left, two-dimensional kernel density estimates of normalized lesion-mask centroid positions. Right, distributions of relative lesion size, defined as mask area divided by image area. Across datasets, lesion masks are predominantly concentrated near the image center, whereas lesion sizes show right-skewed distributions. For cross-dataset comparison, all size distributions are shown on a shared x-axis range and all position maps use a common density scale.}
    \label{fig:Mask_Position_Size}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs_sup/BM_cases.pdf}
    \caption{SHAP feature attribution and segmentation Grad-CAM maps in representative benign and malignant thyroid ultrasound cases. Left, SHAP values of the most influential classification features, with red indicating contributions toward malignancy and blue indicating contributions toward benignity. Right, corresponding ultrasound images with segmentation contours and Grad-CAM maps from the segmentation model. Cases with good and poor segmentation performance are shown for both benign and malignant nodules.}
    \label{fig:BM_cases}
\end{figure}

\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Segmentation performance with cumulatively stacked training data. The model was evaluated on six test sets after training on four progressively enlarged training configurations: dataset1 (TN3K), dataset2 (TN3K + ThyroidXL), dataset3 (TN3K + ThyroidXL + PKTN), and dataset4 (TN3K + ThyroidXL + PKTN + TN5K). The upper block reports the Dice coefficient (\%), and the lower block reports the 95th percentile Hausdorff distance (HD95, mm). All values are presented as the mean $\pm$ 95\% confidence interval across five independent runs.}
\label{tab:stacked_seg_performance}

\footnotesize
\setlength{\tabcolsep}{5.5pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lcccccc}
\toprule
\textbf{Dataset}
& \textbf{TN3K}
& \textbf{ThyroidXL}
& \textbf{PKTN}
& \textbf{TN5K}
& \textbf{Zhujiang2K}
& \textbf{Shanghai7K} \\
\midrule
dataset1
& 85.11 $\pm$ 1.24
& 81.76 $\pm$ 0.61
& 81.40 $\pm$ 2.44
& 77.75 $\pm$ 1.23
& ---
& --- \\
dataset2
& 84.90 $\pm$ 1.31
& 87.23 $\pm$ 0.46
& 80.28 $\pm$ 2.82
& 77.76 $\pm$ 1.23
& ---
& --- \\
dataset3
& 85.18 $\pm$ 1.21
& 87.81 $\pm$ 0.43
& 84.40 $\pm$ 1.74
& 78.05 $\pm$ 1.24
& ---
& --- \\
dataset4
& 85.22 $\pm$ 1.24
& 87.71 $\pm$ 0.44
& 84.37 $\pm$ 2.15
& 83.29 $\pm$ 1.29
& ---
& --- \\

\midrule
dataset1
& 10.97 $\pm$ 1.72
& 9.44 $\pm$ 0.57
& 11.75 $\pm$ 3.47
& 12.53 $\pm$ 1.43
& ---
& --- \\
dataset2
& 11.17 $\pm$ 2.03
& 5.73 $\pm$ 0.46
& 13.62 $\pm$ 4.07
& 12.56 $\pm$ 1.53
& ---
& --- \\
dataset3
& 10.19 $\pm$ 1.61
& 5.37 $\pm$ 0.45
& 7.48 $\pm$ 2.11
& 11.63 $\pm$ 1.36
& ---
& --- \\
dataset4
& 10.97 $\pm$ 1.78
& 5.38 $\pm$ 0.44
& 9.13 $\pm$ 3.29
& 8.46 $\pm$ 1.34
& ---
& --- \\

\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}

\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Classification performance with cumulatively stacked training data. The model was evaluated on five test sets after training on three progressively enlarged training configurations: dataset1 (TN3K), dataset2 (TN3K + ThyroidXL), and dataset3 (TN3K + ThyroidXL + TN5K). The upper block reports the area under the receiver operating characteristic curve (AUROC), and the lower block reports the area under the precision--recall curve (AUPRC). All values are presented as the mean $\pm$ 95\% confidence interval across five independent runs.}
\label{tab:stacked_cls_performance}

\footnotesize
\setlength{\tabcolsep}{5.5pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lccccc}
\toprule
\textbf{Dataset}
& \textbf{TN3K}
& \textbf{ThyroidXL}
& \textbf{TN5K}
& \textbf{DDTI}
& \textbf{Zhujiang2K} \\
\midrule
dataset1
& 0.7860 $\pm$ 0.00
& 0.8795 $\pm$ 0.00
& 0.8177 $\pm$ 0.00
& ---
& --- \\
dataset2
& 0.7576 $\pm$ 0.00
& 0.9283 $\pm$ 0.00
& 0.8083 $\pm$ 0.00
& ---
& --- \\
dataset3
& 0.7947 $\pm$ 0.00
& 0.9304 $\pm$ 0.00
& 0.9614 $\pm$ 0.00
& ---
& --- \\
\midrule
dataset1
& 0.7019 $\pm$ 0.00
& 0.8378 $\pm$ 0.00
& 0.9179 $\pm$ 0.00
& ---
& --- \\
dataset2
& 0.6886 $\pm$ 0.00
& 0.9156 $\pm$ 0.00
& 0.9023 $\pm$ 0.00
& ---
& --- \\
dataset3
& 0.7301 $\pm$ 0.00
& 0.9201 $\pm$ 0.00
& 0.9853 $\pm$ 0.00
& ---
& --- \\
\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}

\end{appendices}

\clearpage
\bibliography{ref}

\end{document}