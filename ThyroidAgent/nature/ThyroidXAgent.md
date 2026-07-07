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
\author[2,$\dagger$]{Bodong Wang}
\author[3,$\dagger$]{Yuqi Wang}
\author[4]{Shijie Wang}
\author[5]{Guoliang You}
\author[1]{Xinyu Xiong}
\author[6]{Haowei Wang}
\author[7]{Qinghua Liu}
\author[2]{Mingzhi Mao}
\author[4]{Dexing Kong}
\author[8,*]{Wei Lou}
\author[9,*]{Fei Chen}
\author[1,*]{Guanbin Li}

\affil[1]{School of Computer Science and Engineering, Sun Yat-sen University, Guangdong, China}
\affil[2]{School of Software Engineering, Sun Yat-sen University, Guangdong, China}
\affil[3]{Duke University, Durham, USA}
\affil[4]{School of Mathematical Sciences, Zhejiang University, Hangzhou, 310058, China}
\affil[5]{School of Computer Science and Technology, University of Science and Technology of China}
\affil[6]{Department of Pathology, Zhujiang Hospital, Southern Medical University}
\affil[7]{Department of Health Management, Zhujiang Hospital, Southern Medical University}
\affil[8]{College of Mathematical Medicine, Zhejiang Normal University, Jinhua, 321004, China}
\affil[9]{Department of Thyroid Surgery, Zhujiang Hospital, Southern Medical University}

\affil[*]{\textbf{Corresponding authors:} Wei Lou~(\href{mailto:louwei@zjnu.edu.cn}{louwei@zjnu.edu.cn}), Fei Chen~(\href{mailto:gzchenfei@126.com}{gzchenfei@126.com}), and Guanbin Li~(\href{mailto:liguanbin@mail.sysu.edu.cn}{liguanbin@mail.sysu.edu.cn})}
\affil[$\dagger$]{These authors contributed equally to this work}



\begin{abstract}
Thyroid ultrasound diagnosis is not solved by a single malignancy score. In routine practice, clinicians must localize and measure lesions, characterize sonographic features, stratify malignancy risk and translate this evidence into structured reports. Here we present ThyroidXAgent, a clinician-interactive agentic framework built on OpenThyroidDB, a multitask thyroid ultrasound database comprising more than 0.3 million ultrasound images, 24,000 paired reports and 32,000 pixel-annotated images from seven centers, with validation in more than 10,000 individuals from 40 centers worldwide. ThyroidXAgent coordinates segmentation, benign--malignant classification, radiomics extraction, tabular prediction, structured evidence parsing and template-based report generation within an auditable case-level evidence store. Across heterogeneous public and institutional datasets, ThyroidXAgent improved cross-dataset nodule segmentation and classification, achieving a mean Dice score of 85.24\% and a mean AUROC of 0.9466. The same workflow generalized to opportunistic diagnostic tasks, including lateral lymph-node metastasis prediction and follicular versus papillary thyroid carcinoma subtype classification, while providing task-specific radiomic explanations. For reporting, ThyroidXAgent generated evidence-grounded reports that outperformed multimodal language-model baselines on conventional and clinically oriented semantic metrics. In reader studies, AI assistance reduced segmentation and reporting time while preserving editable intermediate evidence. These results support agentic orchestration as a practical route toward auditable, clinician-correctable thyroid ultrasound AI.
\end{abstract}

\begin{document}
\flushbottom
\maketitle
\thispagestyle{empty}


\begin{figure}[p]
    \centering
    \includegraphics[width=\textwidth]{imgs/Introduction3.pdf}
    %\caption{Overview of OpenThyroidDB and ThyroidXAgent. \textbf{a}, OpenThyroidDB integrates curated public thyroid ultrasound resources and newly collected institutional datasets into a full-spectrum database for lesion segmentation, benign--malignant classification, report generation and advanced malignant-lesion analysis across heterogeneous scanners and acquisition settings. \textbf{b}, The clinician-in-the-loop self-evolving workflow enables physicians to review and correct AI-generated masks, predictions and reports. The resulting expert-refined outputs shorten diagnostic workflows and are stored as high-quality feedback for continual model updating. \textbf{c}, ThyroidXAgent supports four downstream workflows: expert-refined nodule segmentation, clinician-verified malignancy classification, expert-edited structured report generation, and advanced diagnosis for lymph-node metastasis assessment and PTC/FTC subtype analysis. \textbf{d}, Multicentre validation design, with model development and internal validation across 10 centers followed by external validation across 35 independent centers.}
    \caption{Overview of OpenThyroidDB and ThyroidXAgent. \textbf{a}, OpenThyroidDB integrates curated public thyroid ultrasound resources and newly collected institutional datasets into a full-spectrum database for segmentation, benign--malignant classification, report generation and advanced malignant-lesion analysis across diverse scanners and acquisition settings. \textbf{b}, The clinician-in-the-loop self-evolving workflow enables physicians to review and correct AI-generated masks, predictions and reports; expert-refined outputs streamline diagnosis and provide high-quality feedback for continual model updating. \textbf{c}, ThyroidXAgent supports four workflows: expert-refined nodule segmentation, clinician-verified malignancy classification, expert-edited structured reporting, and advanced diagnosis for lymph-node metastasis assessment and PTC/FTC subtype analysis. \textbf{d}, Multicentre validation design, with model development and internal validation across 10 centers followed by external validation across 35 independent centers.}
    \label{fig:introduction_overview}
\end{figure}

\section{Introduction}

The central challenge in thyroid ultrasound is not simply to classify a nodule. A clinically useful examination requires a sequence of decisions: identifying and measuring the lesion, characterizing sonographic features, assigning risk using systems such as the Thyroid Imaging Reporting and Data System (TI-RADS), deciding whether fine-needle aspiration is indicated, integrating uncertain cytology and communicating the evidence in a structured report \cite{Alexander2022Lancet,Grani2024NatRevEndocrinol,Tessler2017ACRTIRADS,Cibas2017Bethesda}. This sequence is vulnerable to variation. Descriptors such as margins and echogenic foci show substantial reader dependence, and small changes in these features can alter biopsy or follow-up recommendations \cite{Hoang2018AJRInterobserver}. The clinically important question is therefore not whether artificial intelligence can output a malignancy probability, but whether it can support a complete thyroid ultrasound workflow that is accurate, inspectable and correctable.

Most thyroid ultrasound AI systems have addressed only fragments of this workflow~\cite{zhang2025tn5000,gong2021multi,gong2022less,gong2023thyroid}. Multicentre thyroid AI systems and feature-aligned multimodal models have further connected image predictions to TI-RADS-like descriptors or management recommendations \cite{Peng2021LancetDigitalHealthThyNet,Chen2022RadiologyTIRADS,Yao2025NPJDigitMedThyGPT}. Recent work has extended thyroid AI to fine-needle aspiration cytology, lateral lymph-node metastasis prediction and rare thyroid cancer subtype classification \cite{Wang2024LancetDigitalHealthFNAB,Shen2025NatCommunLLNM,Dai2025NatCommunThyroidSubtype}. Despite these advances, most systems still return an endpoint---a probability, mask, label or report-like output---without preserving the intermediate evidence that clinicians need to review, correct and reuse. This weakens trust and makes it difficult to determine whether a model reached the right conclusion for the right reasons.

This gap reflects a broader limitation in medical AI. High-impact clinical AI studies increasingly emphasize that useful systems should improve workflow, support human--AI collaboration, move beyond retrospective performance and be reported transparently \cite{Topol2019NatMedHighPerformance,Rajpurkar2022NatMedAIHealth,Liu2020NatMedCONSORTAI,Vasey2022NatMedDECIDEAI}. Generalist medical AI and multimodal foundation models extend this ambition to flexible inputs and outputs across tasks \cite{Moor2023NatureGMAI,Zhou2026NEJMAIMedVersa}. However, generality alone does not solve the specialty-specific requirements of thyroid ultrasound: lesion-level measurement, sonographic feature attribution, anatomical context, guideline-aligned management and auditable reporting. Thyroid ultrasound is therefore a useful test case for whether general medical-AI principles can be instantiated as a traceable clinical workflow rather than a single model prediction.

Agentic AI offers a practical route to such workflows. Instead of compressing a case into one opaque output~\cite{gong2021cmsa,gong2022vqamix,li_ultrasound_2024}, an agentic system can plan, call specialized tools, maintain intermediate state, coordinate modules and expose evidence for human review \cite{Qiu2024NatMachIntellAgenticSystems,Zou2025LancetAgenticTeammates,Moritz2025NatBMECoordinatedAgents}. Emerging medical-agent benchmarks similarly emphasize interactive settings that require information retrieval, action execution and workflow-level reasoning \cite{Jiang2025NEJMAIMedAgentBench}. In medical imaging, this principle is beginning to shape systems that standardize tool inputs and outputs, reveal intermediate results and incorporate expert feedback \cite{Li2025TissueLab}. For thyroid ultrasound, this means linking images, masks, measurements, radiomic descriptors, risk estimates, report clauses, uncertainty signals and clinician corrections into a single evidence trace.

Here we present ThyroidXAgent, a clinician-interactive agentic AI framework for thyroid ultrasound diagnosis and reporting. ThyroidXAgent is not designed as another end-to-end classifier. It coordinates segmentation models, image classifiers, radiomics extraction, tabular prediction, measurement tools, anatomical-context parsing, report-template retrieval and post hoc explanation modules. A planning-and-routing layer selects the tools required for each case, consolidates their outputs into a case-level evidence store and exposes masks, measurements, sonographic descriptors, risk estimates, uncertainty signals and report clauses for clinician inspection and correction.

We evaluate ThyroidXAgent across the main tasks encountered in thyroid ultrasound practice. First, we assess nodule segmentation and benign--malignant classification across heterogeneous public and institutional datasets. Second, we test whether the same workflow generalizes to malignant-lesion stratification, including lateral lymph-node metastasis prediction and follicular versus papillary thyroid carcinoma subtype classification. Third, we formulate report generation as evidence-to-report assembly rather than unconstrained language generation, and introduce ThyClinScore to evaluate lesion-level and feature-level clinical semantic correctness. Across these settings, ThyroidXAgent improves cross-dataset performance, provides radiomic explanations, reduces segmentation and report-writing time in reader studies, and produces editable evidence traces. Together, these results show how agentic orchestration can turn thyroid ultrasound AI from isolated prediction into an auditable specialty workflow, where traceability matters as much as accuracy.


\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ThyroidXAgent_SegCls_performance.pdf}
    \caption{ThyroidXAgent improves thyroid nodule segmentation and benign--malignant classification while enabling clinician-interactive review. \textbf{a}, Interactive review workflow for mask inspection, SHAP-based feature analysis and corrective annotation. \textbf{b--e}, Cross-dataset summaries of segmentation and classification performance, reported as Dice coefficient, HD95, AUROC and AUPRC, respectively, across heterogeneous thyroid ultrasound benchmarks. \textbf{f}, Cohort-level SHAP beeswarm analysis for benign--malignant classification. \textbf{g,h}, ROC and precision--recall curves on the 500-image physician comparison set, with clinician operating points shown before and after ThyroidXAgent support. \textbf{i}, Segmentation time under manual and AI-assisted workflows. \textbf{j}, Within-case time saving ranked across cases. \textbf{k}, Paired Dice distributions for manual and AI-assisted segmentation, showing preserved segmentation quality with improved efficiency.}
    \label{fig:ThyroidXAgent_SegCls_performance}
\end{figure}

\section{Results}
\subsection{ThyroidXAgent reshapes the thyroid ultrasound diagnostic workflow}

A thyroid ultrasound examination is not solved when an algorithm predicts a single label. In routine practice, clinicians must localize the thyroid gland and nodules, delineate lesion boundaries, measure size, inspect grayscale and colour Doppler findings, assess sonographic risk features, decide whether biopsy or follow-up is warranted, and translate these observations into a structured report. Errors or omissions at any step can propagate into downstream management. ThyroidXAgent was designed around this clinical reality: instead of treating thyroid ultrasound diagnosis as an isolated image-classification problem, it decomposes the examination into tool-callable subtasks and preserves intermediate evidence for clinician review (Fig.~\ref{fig:introduction_overview}).

OpenThyroidDB provides the data foundation for this workflow-level formulation. It integrates seven public and institutional ultrasound sources comprising 32,472 images, including 18,277 training images, 850 validation images and 13,345 test images, with independent external cohorts for classification (DDTI), segmentation (RJH-7K) and both segmentation and classification (ZJH-2K) (Supplementary Table~\ref{tab:dataset_summary}). These resources cover heterogeneous acquisition settings, file formats, annotation types and clinical tasks, including nodule segmentation, benign--malignant classification, report generation and advanced malignant-lesion analysis (Fig.~\ref{fig:introduction_overview}a and Supplementary Table~\ref{tab:dataset_comparison}). This breadth allows ThyroidXAgent to be evaluated not only as a predictive model, but as an integrated diagnostic workflow spanning image interpretation, structured evidence extraction and report writing.

Built on this database, ThyroidXAgent coordinates four workflow branches: expert-refined nodule segmentation, clinician-verified malignancy classification, expert-edited report generation and opportunistic advanced diagnosis for lateral lymph-node metastasis and PTC/FTC subtype analysis (Fig.~\ref{fig:introduction_overview}b). Each branch contributes structured evidence to the same case-level record, including masks, measurements, class probabilities, radiomic descriptors, feature attributions, uncertainty signals and report clauses. This design makes intermediate outputs reusable across tasks: a corrected mask can support radiomics extraction, a classification result can inform report impressions, and structured report evidence can be reviewed rather than accepted as free text.

This structure changes the role of AI from an isolated predictor to an interactive diagnostic assistant. Clinicians can inspect generated masks, correct segmentation errors, review SHAP- or Grad-CAM-based explanations, edit report statements and return corrected outputs to the evidence store (Fig.~\ref{fig:introduction_overview}c). The workflow therefore reduces repeated manual work while preserving the ability to verify and revise each diagnostic step. More importantly, it reframes thyroid ultrasound AI around traceable clinical work: the system is judged not only by final performance metrics, but by whether it produces evidence that clinicians can understand, correct and reuse.

\subsection{Agentic workflow improves conventional thyroid segmentation and classification}
We first evaluated whether the agentic workflow benefits the two conventional thyroid ultrasound tasks: nodule segmentation and benign--malignant classification. The benchmark comprised 32,472 images from seven source datasets, including independent external test cohorts for segmentation and classification (Supplementary Table~\ref{tab:dataset_summary} and Supplementary Figs.~\ref{fig:BM_Case_Counts} and~\ref{fig:Mask_Position_Size}). For each case, ThyroidXAgent collected candidate masks and class probabilities from DINOv3-based experts, extracted radiomic features from the selected lesion mask and consolidated confidence, disagreement and tabular predictions into structured evidence (Supplementary Fig.~\ref{fig:ThyroidXAgent_for_seg_and_cls}). This design tests whether orchestration across complementary tools can improve robustness in a setting where dataset bias remains a major source of performance degradation~\cite{liu2024decade}.

On six segmentation test sets, including the independent RJH-7K and ZJH-2K cohorts, ThyroidXAgent achieved a mean Dice coefficient of 85.24\% and a mean 95th-percentile Hausdorff distance (HD95) of 8.30~mm (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}b,c and Supplementary Table~\ref{tab:seg_performance}). It obtained the highest Dice score on five of six test sets and the lowest HD95 on all test sets, indicating that the ensemble-and-selection workflow improved boundary robustness across heterogeneous acquisition conditions.

For benign--malignant classification, ThyroidXAgent achieved a mean AUROC of 0.9466 and a mean AUPRC of 0.8361 across five test sets, including the independent DDTI and ZJH-2K cohorts (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}d,e and Supplementary Table~\ref{tab:cls_performance}). Specialized image models showed weaker cross-dataset consistency; for example, RepViT~\cite{wang2023repvit} reached AUROC of 0.777 on ThyroidXL but 0.556 on TN3K. General-purpose vision-language models also underperformed the agentic workflow, supporting the need for domain-specific image and radiomics tools rather than direct prompting alone.

The benefit was not limited to automatic prediction. Cohort-level SHAP profiles~\cite{lundberg2017unified} showed that morphology-related radiomic descriptors, especially Sphericity and Elongation, dominated benign--malignant classification, whereas texture and intensity features contributed complementary information (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}f). Representative benign and malignant cases showed alignment between SHAP attributions, segmentation Grad-CAM maps~\cite{selvaraju2017gradcam} and visible nodule appearance (Supplementary Fig.~\ref{fig:BM_cases}). In a blinded 500-image physician comparison set, ThyroidXAgent achieved AUROC of 0.9256 and AUPRC of 0.9250 (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}g,h). With ThyroidXAgent support, accuracy increased from 79.2\% to 85.6\% for clinician 1 and from 74.0\% to 82.0\% for clinician 2; F1 scores increased from 0.778 to 0.851 and from 0.734 to 0.815, respectively.

The same evidence representation supported clinician-interactive segmentation review. Clinicians inspected the predicted mask and SHAP-based feature attribution, corrected segmentation when needed and returned the corrected output to the case-level evidence store (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}a). AI assistance reduced mean segmentation time from 14.21~s to 9.11~s per image, a 1.6-fold speedup, while preserving segmentation quality (Fig.~\ref{fig:ThyroidXAgent_SegCls_performance}i--k). AI-assisted Dice (0.903) matched or exceeded manual Dice (0.879) in approximately two-thirds of paired cases. Thus, the workflow improved conventional segmentation and classification while keeping intermediate evidence available for correction.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/Malignant_Image_tasks.pdf}
    \caption{ThyroidXAgent generalizes to clinically relevant malignant-lesion stratification tasks and provides task-specific radiomic explanations. \textbf{a}, Workflow for SHAP-based interpretation of malignant-lesion tasks. \textbf{b}, Performance comparison between ThyroidXAgent and the corresponding specialist baselines for FTC/PTC subtype classification and lymph node metastasis prediction, reported as AUROC and AUPRC; percentages denote the relative improvement of ThyroidXAgent over each baseline. \textbf{c,d}, Global and representative local SHAP analyses for lymph node metastasis prediction. \textbf{e,f}, Global and representative local SHAP analyses for FTC/PTC subtype classification, showing stronger contributions from texture heterogeneity and shape descriptors.}
    \label{fig:ThyroidXAgent_Malignant_Image_tasks}
\end{figure}

\subsection{Opportunistic classification tasks and rapid clinical insight generation}
We next tested whether ThyroidXAgent could be redirected to opportunistic classification tasks that arise after the primary thyroid nodule assessment. Lateral lymph-node metastasis (LNM) prediction informs surgical planning, whereas follicular (FTC) versus papillary (PTC) thyroid carcinoma subtype discrimination informs treatment strategy and follow-up. In a conventional development pipeline, each task would require a separate workflow for preprocessing, feature extraction, prediction, interpretation and reporting. In ThyroidXAgent, the same segmentation, radiomics extraction, tabular classification and routing logic could be reused, with only task-specific classifier fine-tuning and task instructions changed.

This reuse enabled rapid generation of clinically interpretable task-specific evidence. ThyroidXAgent achieved AUROC of 0.864 for LNM prediction (338 cases from two centres) and 0.805 for FTC/PTC subtype classification (696 images) (Fig.~\ref{fig:ThyroidXAgent_Malignant_Image_tasks}b and Supplementary Table~\ref{tab:Malignant_images_tasks_performance}). It outperformed the compared task-specific baselines, including LLNM-Net for LNM prediction. These results suggest that the agentic workflow can extend beyond the primary benign--malignant question and support additional clinically relevant classification tasks without rebuilding the full diagnostic pipeline.

The explanatory profiles also changed with the clinical task (Fig.~\ref{fig:ThyroidXAgent_Malignant_Image_tasks}a,c--f). LNM prediction relied more on lymph-node position and size features, including distance to the thyroid capsule and lesion area. FTC/PTC subtype classification relied more on texture heterogeneity and shape descriptors. These task-dependent attribution patterns suggest that ThyroidXAgent did not simply reuse the benign--malignant decision rule, but generated new radiomic insight according to the requested clinical question.


\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ThyClinScore.pdf}
    \caption{ThyClinScore for clinical semantic evaluation of thyroid ultrasound reports. \textbf{a}, ThyClinScore first structures the ground-truth and predicted reports into lesion-level entries, matches corresponding lesions, and scores clinically relevant attributes, including size, vascularity, morphology, lesion-level F1 and completeness. \textbf{b}, Pearson correlation matrix comparing conventional natural-language generation metrics with clinical semantic metrics. Overlap-based metrics were highly correlated with one another, whereas the clinical semantic metrics captured complementary report-quality dimensions. \textbf{c}, Pearson correlations between each metric and a location-aware LLM judge. ThyClinScore showed the strongest correlation among the evaluated metrics; asterisks denote statistical significance (* \(p<0.05\), ** \(p<0.01\), *** \(p<0.001\)). \textbf{d}, Qualitative comparison showing that reports with similar wording overlap can differ in clinically important lesion attributes, which is reflected by ThyClinScore.}
    \label{fig:thyclinscore}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=\textwidth]{imgs/ReportGen.pdf}
    \caption[Interactive report generation and evaluation in ThyroidXAgent]{
    Interactive report generation and evaluation in ThyroidXAgent. \textbf{a}, Case-level thyroid ultrasound input, including video or image sequences, multiple views and anatomical regions, and grayscale and CDFI modalities. \textbf{b}, Input-preparation skills crop regions of interest, parse image context, detect CDFI information, classify nodules and anatomical regions, and convert the resulting preprocessing outputs into agent-ready image priors. \textbf{c}, Diagnostic planning combines the skill instructions, preprocessing information and tool contract with an LLM planner to generate a staged diagnostic task graph. \textbf{d}, A ReAct-style execution loop iteratively observes intermediate evidence, reasons over the next step and calls tools through an MCP server that exposes the public workflow API, including case initialization, input preparation, plan approval, status checking, evidence retrieval and report generation. \textbf{e}, Structured evidence is transformed into report text through query construction, template retrieval, slot filling and clause combination, producing an editable ultrasound report. \textbf{f}, Report-generation performance on SMU-HMC, KMVE and ZJH-TS, comparing ThyroidXAgent with multimodal language-model baselines using ROUGE-L and ThyClinScore. \textbf{g}, Radar plots comparing ThyroidXAgent with the static pipeline across lexical and clinical semantic metrics, including BLEU, METEOR, lesion-level F1 and ThyClinScore.
    }
    \label{fig:thyroidxagent_report_generation}
\end{figure}

\subsection{Clinical report evaluation and human--AI cooperative reporting}
We then addressed the reporting component of thyroid ultrasound diagnosis. Because conventional natural-language generation metrics reward surface overlap, they can miss clinically important disagreements in lesion location, size, vascularity, morphology or impression. We therefore developed ThyClinScore, a clinical semantic metric that structures ground-truth and generated reports, matches lesion entries and scores clinically relevant attributes rather than wording similarity alone (Fig.~\ref{fig:thyclinscore}a).

ThyClinScore captured complementary dimensions of report quality. Overlap-based metrics were strongly correlated with one another, whereas the clinical semantic metrics captured distinct lesion-level and feature-level information (Fig.~\ref{fig:thyclinscore}b). ThyClinScore showed the strongest correlation with a location-aware LLM judge among the evaluated metrics (Pearson's \(r=0.696\), \(p<0.001\); Fig.~\ref{fig:thyclinscore}c). Qualitative examples further show that reports with similar wording overlap can differ in clinically important attributes, which is reflected by the ThyClinScore components (Fig.~\ref{fig:thyclinscore}d).

For report generation, ThyroidXAgent used multi-view and multimodal thyroid ultrasound inputs to construct image priors, invoked diagnostic tools through planning and execution, and converted structured facts into reports by BM25 template retrieval, slot filling and clause assembly (Fig.~\ref{fig:thyroidxagent_report_generation}a--g). Auxiliary tool performance is summarized in Supplementary Table~\ref{tab:auxiliary_tools}. This workflow makes report writing interactive: clinicians can review the structured evidence, edit generated statements and return corrected report content to the case-level evidence store.

On conventional natural-language generation metrics, ThyroidXAgent achieved the strongest overall performance across the in-house dataset and the public KMVE benchmark~\cite{li_ultrasound_2024} (Fig.~\ref{fig:thyroidxagent_report_generation}f and Supplementary Table~\ref{tab:report_generation_nlg_ci}). On the in-house dataset, BLEU-1, BLEU-4 and ROUGE$_L$ reached 0.5799, 0.3291 and 0.5390, respectively. On KMVE, ThyroidXAgent ranked first on all reported overlap metrics, with BLEU-1 of 0.6209, BLEU-4 of 0.4465, METEOR of 0.3596 and ROUGE$_L$ of 0.5826.

Clinical semantic evaluation showed that the reports retained clinically relevant information beyond wording similarity (Fig.~\ref{fig:thyclinscore} and Supplementary Table~\ref{tab:report_generation_clinical_ci}). ThyroidXAgent achieved the highest ThyClinScore on the in-house dataset (0.5002) and KMVE (0.4465), while maintaining competitive feature accuracy, completeness and consistency. The metric-ablation analysis confirmed that clinical semantic scoring captured information not represented by conventional overlap metrics (Supplementary Fig.~\ref{fig:experiment_for_thyclinscore}).

Finally, we assessed human--AI cooperation in a cross-over reader study. Two physicians wrote reports for 151 thyroid ultrasound videos under manual and AI-assisted workflows, with each case evaluated in both workflows by different physicians to reduce memory bias (Fig.~\ref{fig:reader_study}a). AI assistance reduced mean reporting time from 2.5 to 1.8 min per case, a 27.4\% reduction, with similar time savings for both readers (Fig.~\ref{fig:reader_study}b--d). Representative cases show that the structured evidence could support concordant statements on gland morphology, nodule location, measurements, sonographic features and diagnostic impression, while leaving partially correct or incorrect statements available for clinician review (Fig.~\ref{fig:reader_study}e).

\begin{figure}[p]
    \centering
    \includegraphics[width=\textwidth]{imgs/ReaderStudy.pdf}
    \caption{Reader study of AI-assisted thyroid ultrasound reporting. \textbf{a}, Cross-over reader-study design. Each ultrasound video was interpreted under both manual and AI-assisted conditions by different physicians, reducing recall bias while enabling paired case-level comparisons. \textbf{b}, Representative malignant thyroid nodule case comparing reports generated by Qwen 3.5, GPT-5 and ThyroidXAgent with the reference report. Text spans are annotated as correct, partially correct or incorrect according to medical-semantic concordance; ThyroidXAgent shows closer agreement with the reference. \textbf{c}, Annotation-based diagnostic-direction consistency of manual and AI-assisted reports, shown overall and stratified by benign and malignant cases. \textbf{d}, Case-level reporting-time reduction, defined as manual minus AI-assisted reporting time and ranked across paired cases. \textbf{e}, Physician-level reporting time under the manual and AI-assisted conditions.}
    \label{fig:reader_study}
\end{figure}



\section{Discussion}

ThyroidXAgent reframes thyroid ultrasound AI as a workflow-level problem. The central finding is that coordinating specialized tools through an auditable evidence store can improve segmentation, classification, malignant-lesion stratification and report generation while preserving clinician oversight. This differs from the prevailing pattern of isolated predictors, in which a model produces a mask, class probability or free-text report without exposing the intermediate evidence required for clinical review. In ThyroidXAgent, masks, radiomic descriptors, confidence estimates, report clauses and clinician corrections are explicit objects in the workflow, making the system easier to audit and easier to improve.

The results also clarify where agentic orchestration is most useful. General-purpose vision-language models remained weak on thyroid ultrasound classification and report generation, whereas ThyroidXAgent benefited from domain-specific image models, radiomics and controlled report assembly. This does not imply that large language models should replace medical-imaging models. Instead, the LLM component is most valuable as a router and coordinator that operates on structured evidence, leaving image interpretation and measurement to tools designed for those tasks. This design is consistent with emerging agentic medical-imaging systems that emphasize standardized tool interfaces, persistent intermediate state and expert feedback rather than unconstrained end-to-end reasoning \cite{Li2025TissueLab}.

A second contribution is the evaluation of reporting as a clinical semantic task. Conventional natural-language metrics reward surface overlap, but thyroid ultrasound reports can share similar wording while differing in lesion location, size, echogenicity, vascularity or TI-RADS-relevant descriptors. ThyClinScore addresses this by matching lesion-level entries and scoring clinically meaningful attributes. Its stronger correlation with a location-aware LLM judge suggests that clinical report evaluation should move beyond n-gram overlap, although expert adjudication remains necessary before such metrics can be used as substitutes for clinical review.

Several limitations remain. The evaluations are retrospective, and although multiple external cohorts were included, prospective deployment in real ultrasound reporting environments is still required. The reader studies involved a limited number of physicians and should be expanded to include different experience levels, institutions and workflow settings. The quality of ThyroidXAgent depends on the quality of its component tools; routing cannot fully compensate for poor segmentation, biased training data or incomplete metadata, which remain central concerns for responsible medical AI \cite{Wiens2019NatMedDoNoHarm,Obermeyer2019ScienceBias}. The report-generation module is intentionally conservative and template-based, which reduces hallucination risk but may limit linguistic flexibility and local reporting-style adaptation. Finally, the framework stores clinician corrections as reusable evidence, but continual learning in clinical practice will require governance for data quality, privacy, versioning, model drift and regulatory review. These limitations define the next step: prospective, multi-centre evaluation of agentic thyroid ultrasound AI as a clinician-supervised workflow rather than a standalone diagnostic product.

\section{Methods}

\subsection{Datasets and task definitions}
We built the thyroid ultrasound benchmark from seven source datasets. TN3K~\cite{gong2021multi}, TN5K~\cite{zhang2025tn5000}, ThyroidXL~\cite{duong2025thyroidxl} and PKTN~\cite{sun2025clip} served as internal training and validation cohorts. DDTI~\cite{pedraza2015open} was used as an independent external test set for classification. ZJH-2K, collected at Zhujiang Hospital, Southern Medical University, contained 1,854 images and was used as an independent external test set for both segmentation and classification. RJH-7K, from the TN-SCUI 2020 challenge~\cite{zhou2020thyroid}, contained 7,288 images and was used exclusively as an independent external test set for segmentation. The segmentation task predicted a binary nodule mask. The benign--malignant classification task used binary labels from TN3K, TN5K and ThyroidXL; PKTN and DDTI did not contribute classification training labels. To construct the expert pool, we merged training portions across datasets into stacked training sets, with the largest stacked set containing 18,723 images.

Two additional datasets were used for malignant-lesion stratification. The LNM dataset comprised 338 cervical lymph-node ultrasound images from a multicentre open-access database of patients with histologically confirmed papillary thyroid carcinoma, with binary labels indicating lateral lymph-node metastasis confirmed by fine-needle aspiration biopsy. The FTC/PTC subtype dataset combined 200 public images released by Dai \textit{et al.}~\cite{dai2025improving} with 496 institutional images, yielding 696 images in total. Public subtype labels were provided with the dataset; institutional labels were confirmed by post-surgical histopathology.

\subsection{Agentic workflow and evidence store}
ThyroidXAgent decomposes each case into tool calls and structured intermediate outputs. The workflow contains an expert pool for image segmentation and classification, a radiomics branch, a tabular prediction branch, post hoc explanation modules, anatomical-context parsers, measurement tools and report-generation modules. The LLM router operates on structured summaries rather than raw ultrasound images. During inference, it receives candidate masks, class probabilities, confidence estimates, radiomic descriptors and metadata such as image resolution, device and data source. It emits a strict JSON decision that records the selected output, supporting evidence and uncertainty signals. This case-level evidence store is used both for final prediction and for clinician review.

\subsection{Segmentation, classification and radiomics}
The image expert pool used DINOv3-based backbones~\cite{simeoni2025dinov3} with task-specific lightweight heads trained under different stacked-training compositions, dilation designs and input resolutions of 128, 224 and 448 pixels. The segmentation branch used a U-Net-style decoder with skip fusion and was optimized with a weighted binary cross-entropy plus intersection-over-union loss. The classification branch pooled backbone features using global average and max pooling and used a compact attention head with generalized logit adjustment. This heterogeneous expert pool was designed to reduce sensitivity to dataset bias~\cite{torralba2011unbiased,liu2024decade}.

For radiomics, candidate masks were optionally refined by connected-component analysis to remove isolated noisy regions before feature extraction. We extracted two-dimensional PyRadiomics descriptors~\cite{van2017computational}, including shape, intensity and texture features, from image-mask pairs. The selected radiomic features were passed to AutoGluon-tabular classifiers~\cite{erickson2020autogluon}. SHAP analysis~\cite{lundberg2017unified} was used to estimate global and local feature contributions, and Grad-CAM~\cite{selvaraju2017gradcam} was used to visualize image regions contributing to segmentation outputs. The same segmentation, radiomics, tabular classification and SHAP workflow was used for benign--malignant classification, LNM prediction and FTC/PTC subtype classification; only task-specific classifier fine-tuning and the task description supplied to the router were changed.


\subsection{ThyClinScore}
ThyClinScore evaluates thyroid ultrasound reports by clinical semantic agreement. Ground-truth and generated reports are first converted into structured entries containing gland-level findings and lesion-level attributes. Lesion entries are matched using pairwise similarity and bipartite matching. Matched lesions are scored for clinically relevant attributes, including location, size, morphology, echogenicity, vascularity and completeness. False-positive and false-negative lesion entries contribute to lesion-level precision, recall and F1. The final ThyClinScore combines lesion matching, feature agreement, completeness and consistency, thereby penalizing clinically important disagreements that may be missed by surface-overlap metrics.

\subsection{Report generation}
For report generation, ThyroidXAgent accepted case-level multi-view and multimodal ultrasound examinations. ROI cropping and context parsing generated image-level priors, including anatomical region, modality, view, colour Doppler information and nodule presence. These priors conditioned a planner--executor workflow~\cite{wang_plan-and-solve_2023}. The planner generated a case-specific diagnostic outline and dependency structure; the executor used ReAct-style local decision-making~\cite{yao_react:_2022} to select images and tools according to metadata and intermediate observations. Tool outputs were consolidated into gland-level, nodule-level and lymph-node evidence.

Report text was generated by controlled data-to-text assembly~\cite{rebuff_data2text_2020}. To reduce factual hallucination risk~\cite{farquhar2024detecting}, ThyroidXAgent used training-free BM25 template retrieval, slot filling and clause assembly rather than unconstrained free-text decoding. The template library was built from 20,400 real-world thyroid ultrasound reports after excluding all test cases. Findings and impression templates were stored separately; patient-specific measurements and lesion-specific descriptors were abstracted and then filled with the structured evidence at inference time.

\subsection{Reader studies and statistical analysis}
For segmentation review, clinicians corrected AI-generated masks and the correction time and paired Dice scores were compared with manual segmentation. For report writing, two physicians wrote reports for 151 thyroid ultrasound videos under manual and AI-assisted workflows in a cross-over design. Each case was assessed in both workflows, but by different physicians, to reduce memory bias. Performance metrics were summarized using the primary metric for each task: Dice and HD95 for segmentation, AUROC and AUPRC for classification, conventional natural-language generation metrics for report wording, and ThyClinScore and its submetrics for report semantics. Confidence intervals in the supplementary tables were estimated by nonparametric bootstrap resampling of the test set. Correlations between report metrics and the location-aware LLM judge were evaluated using two-sided Pearson correlation tests.

\section{Data availability}
The public datasets used in this study are available from their original sources, as cited in the Methods and Supplementary Table~\ref{tab:dataset_summary}. Institutional ultrasound images and reports contain clinical data and are not publicly released in raw form because of privacy and institutional governance restrictions. De-identified derived data, dataset splits and evaluation outputs can be made available from the corresponding authors upon reasonable request and subject to institutional approval.



\section{Code availability}
The source code, trained model checkpoints and report-generation templates will be released after institutional review. Until public release, code required to reproduce the reported analyses is available from the corresponding authors upon reasonable request.

\section{Acknowledgments}
The authors thank the clinicians, sonographers and data-management staff who contributed to ultrasound acquisition, annotation and clinical interpretation.

\section{Author Contributions}

H.G., S.C., B.W., Y.W., F.C. and G.L. conceived the study. H.G., S.C., B.W., Y.W., X.X. and M.M. developed the computational methods and experiments. G.Y., H.W., Q.L. and F.C. contributed clinical data curation, annotation and interpretation. S.W., D.K. and W.L. contributed statistical and methodological guidance. H.G. drafted the manuscript with input from all authors. W.L., F.C. and G.L. supervised the study. All authors reviewed and approved the manuscript.

\section{Competing Interests}
The authors declare no competing interests.

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

\subsection{Dataset composition and supplementary benchmarks}
\begin{table}[htbp]
\centering
\caption{Composition of the thyroid ultrasound benchmark across source datasets. Numbers indicate images contributed by each dataset to the full benchmark (n=32{,}472) and to the training (n=18{,}277), validation (n=850), and test (n=13{,}345) cohorts. Percentages represent the proportion of each dataset within the corresponding column. DDTI, RJH-7K, and ZJH-2K are independent external test sets.}
\label{tab:dataset_summary}
\renewcommand{\arraystretch}{1.2}
\setlength{\tabcolsep}{5pt}
\begin{tabular}{lccccc}
\toprule
\textbf{Dataset} &
\textbf{Task} &
\textbf{Total (n=32{,}472)} &
\makecell[c]{\textbf{Train}\\\textbf{(n=18{,}277)}} &
\makecell[c]{\textbf{Valid}\\\textbf{(n=850)}} &
\makecell[c]{\textbf{Test}\\\textbf{(n=13{,}345)}} \\
\midrule
TN3K~\cite{gong2021multi} & \makecell[c]{Segmentation,\\Classification} & 5{,}347 (16.47\%) & 4{,}633 (25.35\%) & 100 (11.76\%) & 614 (4.60\%) \\
TN5K~\cite{zhang2025tn5000} & \makecell[c]{Segmentation,\\Classification} & 5{,}000 (15.40\%) & 3{,}500 (19.15\%) & 500 (58.82\%) & 1{,}000 (7.50\%) \\
ThyroidXL~\cite{duong2025thyroidxl} & \makecell[c]{Segmentation,\\Classification} & 11{,}631 (35.82\%) & 9{,}441 (51.66\%) & 100 (11.76\%) & 2{,}090 (15.66\%) \\
PKTN~\cite{sun2025clip} & Segmentation & 1{,}003 (3.09\%) & 703 (3.85\%) & 150 (17.65\%) & 150 (1.12\%) \\
\midrule
DDTI~\cite{pedraza2015open} & Classification & 349 (1.07\%) & --- & --- & 349 (2.62\%) \\
RJH-7K~\cite{zhou2020thyroid} & Segmentation & 7{,}288 (22.45\%) & --- & --- & 7{,}288 (54.64\%) \\
ZJH-2K & \makecell[c]{Segmentation,\\Classification} & 1{,}854 (5.71\%) & --- & --- & 1{,}854 (13.89\%) \\
\bottomrule
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
24-TMI~\cite{li_ultrasound_2024} &
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
ThyroidXL~\cite{duong2025thyroidxl} & 11,635 & 9,541 & 2,094 &
\begin{tabular}[c]{@{}l@{}}Image: PNG\\Mask: PNG\\Label: TXT\end{tabular} &
\begin{tabular}[c]{@{}l@{}}Segmentation\\Classification\\Detection\end{tabular} &
Vietnam &
Hitachi Aloka Arietta V70 \\

\midrule
PKTN~\cite{sun2025clip} & 1,005 & N/A & N/A &
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
& \textbf{ZJH-2K}
& \textbf{RJH-7K} \\
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
& \textbf{ZJH-2K} \\
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
GPT-5~\cite{openai2025gpt5systemcard}
& $0.6924 \pm 0.0421$
& $0.7059 \pm 0.0469$
& $0.7737 \pm 0.0996$
& $0.6346 \pm 0.0914$
& $0.6109 \pm 0.0515$\\
Gemini-2.5-Pro~\cite{comanici_gemini_2025}
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
GPT-5~\cite{openai2025gpt5systemcard}
& $0.6627 \pm 0.0633$
& $0.6237 \pm 0.0666$
& $0.8920 \pm 0.0316$
& $0.3578 \pm 0.1089$
& $0.8311 \pm 0.0377$\\
Gemini-2.5-Pro~\cite{comanici_gemini_2025}
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
GPT-5~\cite{openai2025gpt5systemcard}
& $0.8410 \pm 0.0575$
& $0.8629 \pm 0.0533$
& $0.1604 \pm 0.0706$
& $0.3638 \pm 0.0847$\\
Gemini-2.5-Pro~\cite{comanici_gemini_2025}
& $0.5414 \pm 0.0736$
& $0.5492 \pm 0.0915$
& $0.3324 \pm 0.0872$
& $0.4187 \pm 0.0837$\\
LLNM-Net~\cite{Shen2025NatCommunLLNM}
& $0.7665 \pm 0.0692$
& $0.7363 \pm 0.0849$
& ---
& ---\\
Tiger-Model~\cite{Dai2025NatCommunThyroidSubtype}
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
\setlength{\tabcolsep}{5.2pt}
\renewcommand{\arraystretch}{1.08}

\begin{tabular}{lcccccc}
\toprule
\textbf{Model}
& \textbf{BLEU-1}
& \textbf{BLEU-2}
& \textbf{BLEU-3}
& \textbf{BLEU-4}
& \textbf{METEOR}
& \textbf{ROUGE$_L$} \\
\midrule

\rowcolor{gray!20}
\multicolumn{7}{c}{\textbf{SMU-HMC Testset} ($n=400$)} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.3500$\pm$0.0100
& 0.2535$\pm$0.0080
& 0.1842$\pm$0.0066
& 0.1330$\pm$0.0057
& 0.3247$\pm$0.0047
& 0.3577$\pm$0.0077 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.3836$\pm$0.0085
& 0.2749$\pm$0.0069
& 0.1965$\pm$0.0059
& 0.1374$\pm$0.0054
& 0.3254$\pm$0.0037
& 0.3732$\pm$0.0068 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.3702$\pm$0.0094
& 0.2660$\pm$0.0081
& 0.1907$\pm$0.0070
& 0.1373$\pm$0.0063
& 0.3308$\pm$0.0038
& 0.3584$\pm$0.0071 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.4483$\pm$0.0130
& 0.3623$\pm$0.0111
& 0.2959$\pm$0.0095
& 0.2427$\pm$0.0081
& \textbf{0.3628$\pm$0.0040}
& 0.5147$\pm$0.0088 \\

Claude-Sonnet-4.6
& 0.3326$\pm$0.0099
& 0.2543$\pm$0.0080
& 0.1968$\pm$0.0067
& 0.1528$\pm$0.0056
& 0.3417$\pm$0.0035
& 0.3782$\pm$0.0074 \\

MedGemma~\cite{sellergren2025medgemma}
& 0.0457$\pm$0.0072
& 0.0343$\pm$0.0056
& 0.0265$\pm$0.0044
& 0.0207$\pm$0.0035
& 0.1736$\pm$0.0051
& 0.0829$\pm$0.0075 \\

LLaVA-Med~\cite{li_llavamed_2023}
& 0.1670$\pm$0.0077
& 0.0581$\pm$0.0066
& 0.0290$\pm$0.0040
& 0.0159$\pm$0.0024
& 0.1439$\pm$0.0053
& 0.1482$\pm$0.0073 \\

KMVE~\cite{li_ultrasound_2024}
& 0.1743$\pm$0.0131
& 0.1110$\pm$0.0082
& 0.0684$\pm$0.0052
& 0.0398$\pm$0.0035
& 0.1719$\pm$0.0063
& 0.2212$\pm$0.0039 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.5799$\pm$0.0141}
& \textbf{0.4691$\pm$0.0139}
& \textbf{0.3902$\pm$0.0138}
& \textbf{0.3291$\pm$0.0137}
& 0.3575$\pm$0.0088
& \textbf{0.5390$\pm$0.0119} \\

\midrule

\rowcolor{gray!20}
\multicolumn{7}{c}{\textbf{KMVE Testset} ($n=492$)} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.4467$\pm$0.0154
& 0.3423$\pm$0.0143
& 0.2683$\pm$0.0118
& 0.2136$\pm$0.0102
& 0.2799$\pm$0.0116
& 0.3850$\pm$0.0148 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.4149$\pm$0.0073
& 0.2992$\pm$0.0066
& 0.2190$\pm$0.0059
& 0.1668$\pm$0.0062
& 0.3042$\pm$0.0070
& 0.4128$\pm$0.0089 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.5065$\pm$0.0117
& 0.3851$\pm$0.0103
& 0.2981$\pm$0.0095
& 0.2394$\pm$0.0092
& 0.2863$\pm$0.0083
& 0.4742$\pm$0.0111 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.5425$\pm$0.0135
& 0.4243$\pm$0.0126
& 0.3415$\pm$0.0121
& 0.2783$\pm$0.0120
& 0.2952$\pm$0.0084
& 0.5066$\pm$0.0118 \\

Claude-Sonnet-4.6
& 0.4331$\pm$0.0119
& 0.3380$\pm$0.0112
& 0.2638$\pm$0.0107
& 0.2089$\pm$0.0106
& 0.3284$\pm$0.0079
& 0.4639$\pm$0.0115 \\

MedGemma~\cite{sellergren2025medgemma}
& 0.0374$\pm$0.0195
& 0.0299$\pm$0.0175
& 0.0252$\pm$0.0161
& 0.0219$\pm$0.0151
& 0.1075$\pm$0.0119
& 0.1862$\pm$0.0205 \\

LLaVA-Med~\cite{li_llavamed_2023}
& 0.2842$\pm$0.0149
& 0.2135$\pm$0.0124
& 0.1595$\pm$0.0099
& 0.1244$\pm$0.0088
& 0.2138$\pm$0.0101
& 0.3939$\pm$0.0127 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.6209$\pm$0.0178}
& \textbf{0.5493$\pm$0.0164}
& \textbf{0.4919$\pm$0.0159}
& \textbf{0.4465$\pm$0.0159}
& \textbf{0.3596$\pm$0.0102}
& \textbf{0.5826$\pm$0.0123} \\

\midrule

\rowcolor{gray!20}
\multicolumn{7}{c}{\textbf{ZJH-TS Testset} ($n=159$)} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.4092$\pm$0.0263
& 0.2962$\pm$0.0200
& 0.2171$\pm$0.0149
& 0.1622$\pm$0.0116
& 0.2493$\pm$0.0159
& 0.3686$\pm$0.0214 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.5023$\pm$0.0152
& 0.3718$\pm$0.0125
& 0.2709$\pm$0.0104
& 0.1931$\pm$0.0092
& 0.3275$\pm$0.0058
& 0.4811$\pm$0.0095 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.1819$\pm$0.0109
& 0.1238$\pm$0.0076
& 0.0848$\pm$0.0056
& 0.0584$\pm$0.0043
& 0.2766$\pm$0.0051
& 0.2533$\pm$0.0086 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& \textbf{0.5433$\pm$0.0182}
& \textbf{0.4364$\pm$0.0161}
& \textbf{0.3532$\pm$0.0143}
& \textbf{0.2868$\pm$0.0127}
& \textbf{0.3485$\pm$0.0073}
& 0.5381$\pm$0.0119 \\

Claude-Sonnet-4.6
& 0.4646$\pm$0.0180
& 0.3664$\pm$0.0155
& 0.2917$\pm$0.0132
& 0.2337$\pm$0.0115
& 0.3424$\pm$0.0072
& 0.4864$\pm$0.0124 \\

MedGemma~\cite{sellergren2025medgemma}
& 0.0793$\pm$0.0205
& 0.0612$\pm$0.0162
& 0.0479$\pm$0.0130
& 0.0378$\pm$0.0104
& 0.2179$\pm$0.0090
& 0.1579$\pm$0.0199 \\

LLaVA-Med~\cite{li_llavamed_2023}
& 0.2375$\pm$0.0194
& 0.1358$\pm$0.0138
& 0.0917$\pm$0.0098
& 0.0628$\pm$0.0073
& 0.1609$\pm$0.0103
& 0.2483$\pm$0.0199 \\

KMVE~\cite{li_ultrasound_2024}
& 0.1511$\pm$0.0148
& 0.0948$\pm$0.0092
& 0.0557$\pm$0.0055
& 0.0316$\pm$0.0039
& 0.1604$\pm$0.0070
& 0.2240$\pm$0.0037 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& 0.4654$\pm$0.0229
& 0.3830$\pm$0.0203
& 0.3199$\pm$0.0184
& 0.2706$\pm$0.0169
& 0.2995$\pm$0.0115
& \textbf{0.5393$\pm$0.0153} \\

\bottomrule
\end{tabular}

\end{threeparttable}
\end{table*}

\begin{table*}[!htp]
\centering
\begin{threeparttable}

\caption{Clinical semantic evaluation results on report generation with test-set bootstrap 95\% confidence intervals. Values are reported as mean$\pm$half-width of the 95\% percentile confidence interval. FDR with $\downarrow$ indicates that lower is better.}
\label{tab:report_generation_clinical_ci}

\footnotesize
\setlength{\tabcolsep}{5.2pt}
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
\multicolumn{7}{c}{\textbf{SMU-HMC Testset} ($n=400$)} \\

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

Claude-Sonnet-4.6
& 0.8040$\pm$0.0305
& 0.5580$\pm$0.0464
& 0.2049$\pm$0.0298
& 0.8786$\pm$0.0108
& 0.3886$\pm$0.0147
& 0.4015$\pm$0.0144 \\

MedGemma~\cite{sellergren2025medgemma}
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
\multicolumn{7}{c}{\textbf{KMVE Testset} ($n=492$)} \\

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

Claude-Sonnet-4.6
& 0.5803$\pm$0.0432
& 0.6605$\pm$0.0578
& 0.2721$\pm$0.0375
& \textbf{0.6707$\pm$0.0043}
& 0.3779$\pm$0.0211
& 0.3362$\pm$0.0182 \\

MedGemma~\cite{sellergren2025medgemma}
& 0.1877$\pm$0.0327
& 0.6820$\pm$0.0463
& 0.2868$\pm$0.0381
& 0.6622$\pm$0.0033
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

\midrule

\rowcolor{gray!20}
\multicolumn{7}{c}{\textbf{ZJH-TS Testset} ($n=159$)} \\

GPT-4o~\cite{openai_gpt4_2024}
& 0.4764$\pm$0.0687
& 0.5509$\pm$0.0457
& 0.2627$\pm$0.0516
& 0.7258$\pm$0.0296
& 0.3411$\pm$0.0288
& 0.3108$\pm$0.0256 \\

GPT-5~\cite{openai2025gpt5systemcard}
& 0.4938$\pm$0.0643
& 0.5262$\pm$0.0468
& 0.4034$\pm$0.0523
& 0.9543$\pm$0.0107
& 0.4829$\pm$0.0230
& 0.4604$\pm$0.0244 \\

Gemini2.5 Pro~\cite{comanici_gemini_2025}
& 0.5613$\pm$0.0660
& 0.5477$\pm$0.0546
& 0.3067$\pm$0.0505
& 0.7869$\pm$0.0180
& 0.3846$\pm$0.0287
& 0.3507$\pm$0.0241 \\

Qwen3.5 Plus~\cite{yang_qwen3_2025}
& 0.6352$\pm$0.0453
& 0.5001$\pm$0.0450
& 0.3800$\pm$0.0428
& 0.9697$\pm$0.0064
& \textbf{0.4883$\pm$0.0203}
& 0.4543$\pm$0.0198 \\

Claude-Sonnet-4.6
& 0.6071$\pm$0.0550
& 0.5628$\pm$0.0445
& 0.3466$\pm$0.0470
& 0.8253$\pm$0.0171
& 0.4342$\pm$0.0229
& 0.3897$\pm$0.0213 \\

MedGemma~\cite{sellergren2025medgemma}
& 0.6596$\pm$0.0605
& 0.5427$\pm$0.0490
& 0.2931$\pm$0.0495
& 0.9446$\pm$0.0101
& 0.3869$\pm$0.0218
& 0.3790$\pm$0.0227 \\

LLaVA-Med~\cite{li_llavamed_2023}
& 0.2830$\pm$0.0692
& \textbf{0.6595$\pm$0.1072}
& 0.1171$\pm$0.0435
& 0.6150$\pm$0.0482
& 0.1480$\pm$0.0302
& 0.1785$\pm$0.0263 \\

KMVE~\cite{li_ultrasound_2024}
& 0.7904$\pm$0.0603
& 0.6288$\pm$0.1489
& 0.0420$\pm$0.0243
& 0.6241$\pm$0.0081
& 0.1542$\pm$0.0158
& 0.1626$\pm$0.0119 \\

\rowcolor{lightgray}
\textbf{ThyroidXAgent}
& \textbf{0.2799$\pm$0.0597}
& 0.5491$\pm$0.0447
& \textbf{0.4786$\pm$0.0565}
& \textbf{0.9731$\pm$0.0053}
& 0.4516$\pm$0.0208
& \textbf{0.4630$\pm$0.0257} \\

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
    \caption{Benign and malignant case counts across thyroid ultrasound datasets. Bar plots show the numbers of benign and malignant cases in TN3K, TN5K, ThyroidXL, DDTI and ZJH-2K. The y axis is logarithmic. Dataset size and class balance vary substantially across cohorts.}
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
& \textbf{ZJH-2K}
& \textbf{RJH-7K} \\
\midrule
dataset1
& 82.76 $\pm$ 3.54
& 81.97 $\pm$ 2.63
& 79.21 $\pm$ 2.71
& 72.18 $\pm$ 5.08
& 94.57 $\pm$ 0.43
& 80.77 $\pm$ 0.44 \\
dataset2
& 81.63 $\pm$ 3.81
& 86.84 $\pm$ 1.90
& 81.73 $\pm$ 2.26
& 71.07 $\pm$ 5.35
& 94.85 $\pm$ 0.40
& 82.38 $\pm$ 0.42 \\
dataset3
& 80.81 $\pm$ 3.82
& 86.00 $\pm$ 2.31
& 81.91 $\pm$ 2.26
& 72.82 $\pm$ 4.91
& 94.82 $\pm$ 0.39
& 91.44 $\pm$ 0.15 \\
dataset4
& 81.86 $\pm$ 3.70
& 86.97 $\pm$ 2.19
& 83.28 $\pm$ 2.19
& 82.57 $\pm$ 3.46
& 94.77 $\pm$ 0.39
& 91.46 $\pm$ 0.15 \\

\midrule
dataset1
& 13.49 $\pm$ 3.83
& 8.34 $\pm$ 2.34
& 11.73 $\pm$ 3.07
& 11.37 $\pm$ 3.49
& 2.30 $\pm$ 0.47
& 11.46 $\pm$ 0.50 \\
dataset2
& 15.92 $\pm$ 4.58
& 4.99 $\pm$ 1.58
& 9.72 $\pm$ 2.71
& 13.64 $\pm$ 4.28
& 1.98 $\pm$ 0.41
& 9.65 $\pm$ 0.44 \\
dataset3
& 15.94 $\pm$ 4.34
& 5.46 $\pm$ 1.62
& 10.92 $\pm$ 3.52
& 11.07 $\pm$ 3.28
& 1.93 $\pm$ 0.38
& 1.87 $\pm$ 0.07 \\
dataset4
& 17.00 $\pm$ 5.34
& 4.74 $\pm$ 1.42
& 8.89 $\pm$ 2.93
& 4.64 $\pm$ 1.43
& 2.07 $\pm$ 0.40
& 1.88 $\pm$ 0.07 \\

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
& \textbf{ZJH-2K} \\
\midrule
dataset1
& 0.7666 $\pm$ 0.03
& 0.8713 $\pm$ 0.01
& 0.8272 $\pm$ 0.02
& 0.7244 $\pm$ 0.07
& 0.9924 $\pm$ 0.01 \\
dataset2
& 0.7724 $\pm$ 0.04
& 0.9254 $\pm$ 0.01
& 0.8151 $\pm$ 0.02
& 0.5762 $\pm$ 0.10
& 0.9932 $\pm$ 0.01 \\
dataset3
& 0.7906 $\pm$ 0.03
& 0.9288 $\pm$ 0.01
& 0.9515 $\pm$ 0.01
& 0.7623 $\pm$ 0.07
& 0.9937 $\pm$ 0.01 \\
\midrule
dataset1
& 0.6806 $\pm$ 0.06
& 0.8147 $\pm$ 0.03
& 0.9151 $\pm$ 0.02
& 0.3578 $\pm$ 0.13
& 0.9951 $\pm$ 0.01 \\
dataset2
& 0.7237 $\pm$ 0.05
& 0.9140 $\pm$ 0.01
& 0.9074 $\pm$ 0.01
& 0.3190 $\pm$ 0.14
& 0.9968 $\pm$ 0.01 \\
dataset3
& 0.7188 $\pm$ 0.05
& 0.9144 $\pm$ 0.01
& 0.9803 $\pm$ 0.01
& 0.4029 $\pm$ 0.14
& 0.9967 $\pm$ 0.01 \\
\bottomrule
\end{tabular}
\end{threeparttable}
\end{table*}


\end{appendices}

\clearpage
\bibliography{ref}

\end{document}
