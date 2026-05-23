Reviewer #1
Questions
3. Please categorize the relevance of the paper (you may choose more than one). Note the different assessment criteria for the different paper categories as outlined in the Reviewer Guidelines: https://conferences.miccai.org/2026/en/REVIEWER-GUIDELINES.html
MIC
4. How would you describe the paper?
Methodological contribution
5. Please describe the main contribution of the paper.
This paper proposes ThyroidAgent, an agent-based framework that dynamically integrates segmentation and classification for thyroid ultrasound diagnosis. The method leverages multiple segmentation and classification experts and uses an agent module to select or aggregate their outputs based on evidence signals (e.g., model confidence, radiomics features, and metadata). In addition, the work incorporates radiomics features extracted from segmentation masks to enhance interpretability and classification performance. The authors also construct a consolidated multi-source dataset to evaluate cross-dataset generalization.
6. Please list the major strengths of the paper. For example, you could highlight a novel formulation, an original way to use data, a demonstration of clinical feasibility, a novel application, a particularly strong evaluation, or anything else that is a strong aspect of this work. Please provide details, for instance, if a method is novel, explain what aspect is novel and why this is interesting.
1.Well-motivated problem setting
The paper addresses an important clinical task (thyroid nodule diagnosis) and highlights the limitation of static pipelines that separate segmentation and classification.
2.Multi-expert framework improves robustness
The use of multiple segmentation and classification experts and their aggregation helps mitigate model bias and improves performance across heterogeneous datasets.
3.Cross-dataset evaluation
The paper evaluates on multiple public datasets (TN3K, DDTI, ThyroidXL, TN5K), demonstrating reasonable generalization ability.
4.Interpretability analysis
The use of SHAP analysis and evidence aggregation provides some insights into model behavior, which is valuable for medical applications.
7. Please list the major weaknesses of the paper. Please provide details: for instance, if you state that a formulation, way of using data, demonstration of clinical feasibility, or application is not novel, then you must provide specific references to prior work.
Lack of a rigorous and reproducible agent formulation.
The paper does not provide a clear mathematical definition of the proposed agent-based framework. Critical components such as the state representation, action space, reward function, and PPO optimization strategy are insufficiently specified. In particular, it remains unclear what role the LLM plays (e.g., policy generator vs. controller), how rewards are constructed, and how missing metadata is handled. In addition, key implementation details such as decoding strategies (e.g., temperature), training stability, and inference cost control are not reported. This significantly weakens reproducibility and makes it difficult to assess the reliability of the agent reasoning process.
Insufficiently justified and potentially unfair baseline comparisons.
The paper does not clearly demonstrate that the baseline models (especially foundation models) are properly adapted and fairly optimized for the target task. Without careful tuning and domain adaptation, comparisons against strong pretrained models may be misleading. A more rigorous baseline setup is required to support claims of superiority.
Limited novelty of radiomics integration.
The use of radiomics features (e.g., via PyRadiomics) for thyroid nodule classification is well-established in prior literature. For example, Park V Y et al. (European Radiology, 2021) demonstrated that radiomics combined with ultrasound-based risk stratification improves diagnostic performance. Similarly, Shao L et al. (Frontiers in Endocrinology, 2025) showed strong performance using multimodal radiomics models. Therefore, this component should not be considered a primary innovation.
Lack of analysis on error propagation from segmentation to classification.
Since radiomics features are extracted from segmentation masks, segmentation quality directly affects downstream classification performance. This dependency is well known in radiomics pipelines. However, the paper does not provide any systematic analysis (e.g., sensitivity to mask perturbation or segmentation noise) to quantify how segmentation errors propagate and impact classification outcomes, which is a critical omission.
Incomplete evaluation metrics for clinical applicability.
The evaluation primarily reports AUROC and AUPRC, which are insufficient for clinical decision-making. Prior clinical and radiomics studies typically include sensitivity, specificity, and accuracy to better reflect diagnostic utility. The absence of these metrics limits the assessment of real-world applicability.
Missing analysis of inference cost and system stability.
The proposed agent-based system likely introduces additional computational overhead and variability due to dynamic decision-making. However, the paper does not report inference latency, computational cost, or stability across runs, which are essential factors for deployment in real clinical workflows.
8. Please rate the clarity and organization of the paper.
Poor
9. Please comment on the reproducibility of the paper. Please be aware that providing code and data is a plus, but not a requirement for acceptance.
The submission does not provide sufficient information for reproducibility.
10. Code of Ethics Check. Based on your review and your understanding of the MICCAI Scientific Code of Ethics, do you believe this submission may involve a potential ethics concern or violation? Reviewers are expected to familiarize themselves with the MICCAI Scientific Code of Ethics before completing this assessment: https://miccai.org/index.php/about-miccai/policies/scientific-code-of-ethics/
No
13. Rate the paper on a scale of 1-6, 6 being the strongest (6-4: accept; 3-1: reject). Please use the entire range of the distribution. Spreading the score helps create a distribution for decision-making.
3. Weak Reject — marginally below the acceptance threshold, but would not mind if accepted, dependent on rebuttal
14. Please justify your recommendation. What were the major factors that led you to your overall score for this paper?
This paper presents an appealing and practically motivated framework for thyroid ultrasound diagnosis by integrating segmentation, radiomics, classification, and an agent-based orchestration mechanism. The attempt to move beyond isolated tasks toward a multi-component system that mimics real clinical workflows is valuable. In particular, the idea of dynamically selecting or coordinating multiple expert models, along with the effort to unify multiple public datasets into a single benchmark, demonstrates strong system-level thinking and engineering effort.At a high level, the framework is well-motivated, and the empirical results across multiple datasets suggest reasonable robustness and generalization ability. The integration of segmentation-derived radiomics features with classification is also clinically meaningful and aligns with existing diagnostic practices.
However, despite these strengths, the paper suffers from critical issues in methodological clarity and rigor. The core agent mechanism—arguably the main claimed contribution—is not formally defined nor sufficiently specified for reproducibility. Key elements such as the mathematical formulation of the agent (state, action, reward), PPO optimization details, and the exact role of the LLM remain. Important implementation details (e.g., decoding strategy, reward construction, handling of missing metadata, and inference cost control) are missing, leading to a weak methodological foundation.
In addition, the novelty at the methodological level is limited, as the use of radiomics features has been extensively explored in prior work. The paper also lacks a systematic analysis of error propagation from segmentation to downstream classification, which is particularly important in radiomics-based pipelines. Furthermore, the evaluation primarily relies on AUROC and AUPRC, without reporting clinically critical metrics such as sensitivity and specificity, limiting the assessment of real-world applicability. Finally, inference cost and system stability are not analyzed, making it difficult to judge whether the proposed agent-based system is practical for deployment in clinical settings.
Overall, while I appreciate the problem formulation, system integration effort, and clinical relevance, the current manuscript lacks a sufficiently rigorous and well-defined methodological core. As a result, even though the experimental results appear promising, they are not fully convincing or reproducible.
Final Recommendation: Weak Reject.
I acknowledge the potential of this direction and believe the work could become strong with substantial revisions, but in its current form, the lack of methodological clarity and incomplete evaluation prevent it from meeting the acceptance standard.
16. In view of your answers above and your overall experience, how would you rate your confidence in your review?
Confident but not absolutely certain (3)


Reviewer #2
Questions
3. Please categorize the relevance of the paper (you may choose more than one). Note the different assessment criteria for the different paper categories as outlined in the Reviewer Guidelines: https://conferences.miccai.org/2026/en/REVIEWER-GUIDELINES.html
MIC
4. How would you describe the paper?
Methodological contribution
5. Please describe the main contribution of the paper.
- The paper proposes agent-based framework that replaces conventional static pipelines with an LLM-based agent that dynamically selects expert models
- The method integrates features extracted with PyRadiomics and reinforcement learning-optimized connected component analysis.
- The authors curate a consolidated benchmark for systemic cross-dataset evaluation.
6. Please list the major strengths of the paper. For example, you could highlight a novel formulation, an original way to use data, a demonstration of clinical feasibility, a novel application, a particularly strong evaluation, or anything else that is a strong aspect of this work. Please provide details, for instance, if a method is novel, explain what aspect is novel and why this is interesting.
- Good generalizability across diverse datasets: The proposed framework is evaluated on five different datasets and shows consistent strong performance across them.
- Well-designed experiments: The paper includes ablation studies, SHAP-based interpretability analysis, and agentic aggregation analysis, which strengthens the credibility of the approach and provides useful insights.
7. Please list the major weaknesses of the paper. Please provide details: for instance, if you state that a formulation, way of using data, demonstration of clinical feasibility, or application is not novel, then you must provide specific references to prior work.
- Lack of clarity: Figure 2 presents a complex pipeline with many components, but the role of each component and the interactions between these elements are not sufficiently explained.

- Unnecessary complexity of the pipeline: The framework requires training a large number of expert models from scratch, but the paper does not adequately justify why pretrained foundation models or existing medical models cannot serve as the expert pool instead. Given the growing capability of medical foundation models, this design choice appears unnecessarily complex without a more rigorous justification.
8. Please rate the clarity and organization of the paper.
Poor
9. Please comment on the reproducibility of the paper. Please be aware that providing code and data is a plus, but not a requirement for acceptance.
The submission does not provide sufficient information for reproducibility.
10. Code of Ethics Check. Based on your review and your understanding of the MICCAI Scientific Code of Ethics, do you believe this submission may involve a potential ethics concern or violation? Reviewers are expected to familiarize themselves with the MICCAI Scientific Code of Ethics before completing this assessment: https://miccai.org/index.php/about-miccai/policies/scientific-code-of-ethics/
No
13. Rate the paper on a scale of 1-6, 6 being the strongest (6-4: accept; 3-1: reject). Please use the entire range of the distribution. Spreading the score helps create a distribution for decision-making.
2. Reject — should be rejected, independent of rebuttal
14. Please justify your recommendation. What were the major factors that led you to your overall score for this paper?
While this paper addresses a clinically relevant problem and proposes an interesting agent-based framework, several critical issues lead to rejection recommendation.

First, the system description lacks clarity. The framework introduces multiple components, but the role and their interactions are not clearly explained. This makes the paper difficult to follow.

Second, the proposed method appears to be unnecessarily complex. The framework relies on training a large number of expert models from scratch, yet the paper does not sufficiently discuss why pretrained foundation models or simpler alternatives could not be utilized.
16. In view of your answers above and your overall experience, how would you rate your confidence in your review?
Very confident (4)

Reviewer #3
Questions
3. Please categorize the relevance of the paper (you may choose more than one). Note the different assessment criteria for the different paper categories as outlined in the Reviewer Guidelines: https://conferences.miccai.org/2026/en/REVIEWER-GUIDELINES.html
MIC
4. How would you describe the paper?
Methodological contribution
5. Please describe the main contribution of the paper.
The paper proposes ThyroidAgent, a policy-driven system that replaces a fixed thyroid ultrasound pipeline with dynamic expert selection and aggregation across segmentation and classification models. It combines segmentation masks with radiomics features to improve malignancy classification and make decisions more interpretable. The authors harmonize several public thyroid ultrasound datasets into one consolidated benchmark for cross-dataset evaluation. The framework uses metadata, model confidence, and expert disagreement signals to support context-aware decision-making.
6. Please list the major strengths of the paper. For example, you could highlight a novel formulation, an original way to use data, a demonstration of clinical feasibility, a novel application, a particularly strong evaluation, or anything else that is a strong aspect of this work. Please provide details, for instance, if a method is novel, explain what aspect is novel and why this is interesting.
1. The overall system idea is interesting, especially the shift from a static pipeline to adaptive expert routing.

2.It combines segmentation, classification, and radiomics in a unified workflow, which is stronger than treating them as separate tasks.

3. The cross-dataset ambition is useful, since thyroid ultrasound data often varies across scanners, sites, and acquisition settings.

4. The figures and workflow design clearly explain the intended operation of the system.
7. Please list the major weaknesses of the paper. Please provide details: for instance, if you state that a formulation, way of using data, demonstration of clinical feasibility, or application is not novel, then you must provide specific references to prior work.
1. The experiments do not clearly support claims about robustness, adaptability, explainability, or generalization.
2. Table 3 only compares “best single” vs. “agent”; it lacks ablations on LLM vs. heuristic selection, radiomics vs. raw mask features, number of experts, and metadata vs. image-only inputs.
3. Fig. 3 shows disagreement, but it does not quantify how often the agent selects the correct expert or report latency and cost overhead.
4. Two closely related works appear to be missing from the paper’s discussion and comparison: EchoVLM [R2], which uses dynamic expert routing for heterogeneous ultrasound tasks, and the knowledge-interpretable multi-task learning framework [R3], which couples thyroid segmentation and classification with an interpretable design. Both overlap substantially with the proposed method, yet neither is discussed or compared.

5. Inconsistencies remain, such as “ThyAgent-Seg” versus “ThyroidAgent” branding. The training cost of 12 experts per task plus LLM inference is also not discussed, and the VLM baselines (Qwen3-VL, MedGemma) are prompt-engineered rather than fine-tuned, which may weaken fairness.

6. There is no radiologist-in-the-loop study, prospective validation, or strong external generalization test.

7. The roles of the agent and LLM are not fully defined or rigorously evaluated.

8. The tables and figures are generally clear, but Tables 1 and 2 should be explicitly cited in the main text when discussing the results.

9. The notation for subfigures should be standardized, for example, use Fig. 3(a) instead of Fig. 3.(a).

10. There are a few minor presentation issues, such as the typo in Fig. 1 (“Generalizatior” should be “Generalization”) and inconsistent figure references.

11. The variables in Eq. (1) are insufficiently defined. The meanings of 𝑦,𝑦𝑏,𝑝𝑝𝑜𝑠, and 𝑝𝑛𝑒𝑔, as well as the role of the subscript in 𝑧𝑏, are unclear. Additionally, the notation 𝐴𝑣𝑔𝑃𝑜𝑜𝑙31 is ambiguous and should be explicitly specified.

12. In Eq. (2), several variables (e.g., 𝑁𝑔, 𝑃(𝑖,𝑗), and the indicator function 𝐼[⋅]) are not defined, which makes the formulation incomplete.

13. The loss functions (e.g., 𝐿𝑠𝑒𝑔, GLA) are referenced but not explicitly formulated. Providing their mathematical definitions would improve clarity and reproducibility.

14. The notion of “evidence” (e.g., segmentation and classification evidence) is central to the method but is not formally defined, making it difficult to understand how these signals are constructed and used by the agent.

[R1] Duong, V. H., Vu, H., Phan, H. D., Nguyen, D. Q., Pham, D. H., Le, Q. T., ... & Ngo, D. H. (2025, September). ThyroidXL: Advancing Thyroid Nodule Diagnosis with an Expert-Labeled, Pathology-Validated Dataset. In International Conference on Medical Image Computing and Computer-Assisted Intervention (pp. 616-626). Cham: Springer Nature Switzerland.

[R2] She, C., Lu, R., Chen, L., Wang, W., & Huang, Q. (2025). Echovlm: Dynamic mixture-of-experts vision-language model for universal ultrasound intelligence. arXiv preprint arXiv:2509.14977.

[R3] Shin, M., Song, J., Kim, M. G., Yu, H. W., Choe, E. K., & Chai, Y. J. (2025). Thyro-GenAI: a chatbot using retrieval-augmented generative models for personalized thyroid disease management. Journal of Clinical Medicine, 14(7), 2450.
8. Please rate the clarity and organization of the paper.
Satisfactory
9. Please comment on the reproducibility of the paper. Please be aware that providing code and data is a plus, but not a requirement for acceptance.
The submission does not provide sufficient information for reproducibility.
10. Code of Ethics Check. Based on your review and your understanding of the MICCAI Scientific Code of Ethics, do you believe this submission may involve a potential ethics concern or violation? Reviewers are expected to familiarize themselves with the MICCAI Scientific Code of Ethics before completing this assessment: https://miccai.org/index.php/about-miccai/policies/scientific-code-of-ethics/
No
13. Rate the paper on a scale of 1-6, 6 being the strongest (6-4: accept; 3-1: reject). Please use the entire range of the distribution. Spreading the score helps create a distribution for decision-making.
3. Weak Reject — marginally below the acceptance threshold, but would not mind if accepted, dependent on rebuttal
14. Please justify your recommendation. What were the major factors that led you to your overall score for this paper?
The main concerns are weak ablations, limited comparison with closely related work, unclear methodology, and insufficient analysis of cost and reproducibility.
16. In view of your answers above and your overall experience, how would you rate your confidence in your review?
Very confident (4)