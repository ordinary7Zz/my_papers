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

---

# 中文翻译

## 审稿人 #1

### 问题

**3. 请对论文的相关性进行分类（可多选）。请注意《审稿人指南》中针对不同论文类别的不同评审标准：** https://conferences.miccai.org/2026/en/REVIEWER-GUIDELINES.html  
MIC

**4. 你会如何描述这篇论文？**  
方法学贡献

**5. 请描述论文的主要贡献。**  
本文提出了 ThyroidAgent，这是一种用于甲状腺超声诊断的基于智能体的框架，可动态集成分割与分类。该方法利用多个分割专家与分类专家，并使用一个智能体模块根据信号证据（例如模型置信度、影像组学特征和元数据）来选择或聚合它们的输出。此外，该工作还结合了从分割掩膜中提取的影像组学特征，以增强可解释性和分类性能。作者还构建了一个整合的多源数据集，用于评估跨数据集泛化能力。

**6. 请列出论文的主要优点。** 例如，你可以强调一种新颖的表述方式、原创的数据使用方式、临床可行性的展示、新颖的应用、特别强的实验评估，或其他任何构成该工作的强项。请提供细节，例如，如果某个方法是新颖的，请解释其新颖之处以及为何有趣。  
1. **问题设定动机充分**  
论文聚焦于一个重要的临床任务（甲状腺结节诊断），并指出了将分割与分类割裂开的静态流水线的局限性。

2. **多专家框架提升鲁棒性**  
使用多个分割和分类专家并对其结果进行聚合，有助于减轻模型偏差，并提升在异构数据集上的表现。

3. **跨数据集评估**  
论文在多个公开数据集（TN3K、DDTI、ThyroidXL、TN5K）上进行了评估，展示了较为合理的泛化能力。

4. **可解释性分析**  
使用 SHAP 分析和证据聚合为模型行为提供了一定洞见，这对于医学应用很有价值。

**7. 请列出论文的主要缺点。** 请提供细节：例如，如果你认为某个表述方式、数据使用方式、临床可行性展示或应用缺乏新意，那么你必须提供具体的既有工作参考。  
**缺乏严格且可复现的智能体建模。**  
论文没有对所提出的基于智能体框架给出清晰的数学定义。诸如状态表示、动作空间、奖励函数以及 PPO 优化策略等关键组成部分都描述不足。尤其是，LLM 在其中扮演什么角色（例如策略生成器还是控制器）、奖励如何构造、缺失元数据如何处理，这些都不清楚。此外，诸如解码策略（例如 temperature）、训练稳定性以及推理成本控制等关键实现细节也未报告。这显著削弱了可复现性，也使得人们难以评估该智能体推理过程的可靠性。

**基线比较论证不足，且可能不公平。**  
论文没有清楚地证明基线模型（尤其是基础模型）已被正确适配并针对目标任务进行了公平优化。如果没有经过仔细调参和领域适配，那么与强预训练模型的比较可能具有误导性。若要支撑优越性的结论，需要更严格的基线设置。

**影像组学集成的新颖性有限。**  
使用影像组学特征（例如通过 PyRadiomics）进行甲状腺结节分类在既有文献中已较为成熟。例如，Park V Y 等（European Radiology, 2021）表明，将影像组学与基于超声的风险分层结合能够提升诊断性能。类似地，Shao L 等（Frontiers in Endocrinology, 2025）也展示了多模态影像组学模型的强性能。因此，这一部分不应被视为主要创新。

**缺少对分割误差向分类传播的分析。**  
由于影像组学特征是从分割掩膜中提取的，因此分割质量会直接影响下游分类性能。这种依赖关系在影像组学流水线中是众所周知的。然而，论文没有提供任何系统性分析（例如对掩膜扰动或分割噪声的敏感性分析）来量化分割误差如何传播并影响分类结果，这是一个关键缺失。

**面向临床应用的评估指标不完整。**  
论文主要报告了 AUROC 和 AUPRC，但这些指标不足以支持临床决策。既有临床和影像组学研究通常还会包括敏感度、特异度和准确率，以更好地反映诊断效用。缺少这些指标限制了对真实世界适用性的评估。

**缺失对推理成本和系统稳定性的分析。**  
所提出的基于智能体的系统很可能由于动态决策机制而引入额外的计算开销和结果波动。然而，论文没有报告推理延迟、计算成本或多次运行间的稳定性，而这些都是部署到真实临床工作流中的关键因素。

**8. 请评价论文的清晰度和组织性。**  
较差

**9. 请评价论文的可复现性。请注意，提供代码和数据是加分项，但不是接收的必要条件。**  
该投稿未提供足够的信息以支持复现。

**10. 伦理规范检查。根据你的评审以及你对 MICCAI 科学伦理准则的理解，你是否认为该投稿可能涉及潜在的伦理问题或违规？审稿人在完成此项评估前应熟悉 MICCAI 科学伦理准则：** https://miccai.org/index.php/about-miccai/policies/scientific-code-of-ethics/  
否

**13. 请按 1-6 分为论文打分，其中 6 为最强（6-4：接收；3-1：拒稿）。请充分使用整个分值范围。拉开分数有助于形成决策分布。**  
3. 弱拒 —— 略低于接收门槛，但若最终被接收我也可以接受，取决于 rebuttal

**14. 请说明你的推荐理由。导致你对本文总体评分的主要因素是什么？**  
本文提出了一个具有吸引力且在实践上有明确动机的甲状腺超声诊断框架，将分割、影像组学、分类以及基于智能体的编排机制结合在一起。试图从彼此孤立的任务推进到一个模拟真实临床工作流的多组件系统，这一点是有价值的。特别是，动态选择或协调多个专家模型的思路，以及将多个公开数据集统一为单一基准的努力，体现了较强的系统层面思考与工程投入。从高层次看，该框架动机充分，而在多个数据集上的实验结果也表明其具备一定的鲁棒性和泛化能力。将由分割得到的影像组学特征与分类结合也具有临床意义，并与现有诊断实践相契合。

然而，尽管有这些优点，论文在方法清晰性和严谨性方面存在关键问题。其核心智能体机制——可以说是论文声称的主要贡献——既没有形式化定义，也没有被充分说明到足以复现的程度。诸如智能体的数学建模（状态、动作、奖励）、PPO 优化细节以及 LLM 的确切角色等关键要素都没有说清。重要的实现细节（例如解码策略、奖励构造、缺失元数据处理和推理成本控制）缺失，导致方法学基础较弱。

此外，从方法学层面看，新颖性也较有限，因为影像组学特征的使用已在既有工作中被广泛探索。论文还缺乏对分割误差向下游分类传播的系统分析，而这一点在基于影像组学的流水线中尤为重要。再者，实验评估主要依赖 AUROC 和 AUPRC，没有报告如敏感度和特异度等临床关键指标，从而限制了对真实应用价值的评估。最后，论文没有分析推理成本与系统稳定性，因此难以判断所提出的基于智能体系统是否适合部署到临床场景中。

总体而言，我认可该工作的任务设定、系统集成努力以及临床相关性，但当前稿件缺乏一个足够严谨且定义清楚的方法学核心。因此，尽管实验结果看上去有希望，但还不足以令人信服，也难以复现。

**最终建议：弱拒。**  
我认可这一研究方向的潜力，也认为该工作经过大幅修改后可能会变得很强，但以目前的形式而言，方法不够清晰、评估也不完整，尚不足以达到接收标准。

**16. 综合以上回答以及你的整体评审体验，你会如何评价自己对此评审的信心？**  
有信心，但并非绝对确定（3）

---

## 审稿人 #2

### 问题

**3. 请对论文的相关性进行分类（可多选）。请注意《审稿人指南》中针对不同论文类别的不同评审标准：** https://conferences.miccai.org/2026/en/REVIEWER-GUIDELINES.html  
MIC

**4. 你会如何描述这篇论文？**  
方法学贡献

**5. 请描述论文的主要贡献。**  
- 论文提出了一种基于智能体的框架，用一个基于 LLM 的智能体替代传统静态流水线，以动态选择专家模型。  
- 该方法集成了用 PyRadiomics 提取的特征，以及经强化学习优化的连通域分析。  
- 作者构建了一个整合式基准，用于系统性的跨数据集评估。

**6. 请列出论文的主要优点。** 例如，你可以强调一种新颖的表述方式、原创的数据使用方式、临床可行性的展示、新颖的应用、特别强的实验评估，或其他任何构成该工作的强项。请提供细节，例如，如果某个方法是新颖的，请解释其新颖之处以及为何有趣。  
- **在多样化数据集上具有良好的泛化性：** 所提出框架在五个不同数据集上进行了评估，并在这些数据集上展现出持续较强的性能。  
- **实验设计较完善：** 论文包括消融实验、基于 SHAP 的可解释性分析，以及智能体聚合分析，这增强了方法的可信度，也提供了有用的洞见。

**7. 请列出论文的主要缺点。** 请提供细节：例如，如果你认为某个表述方式、数据使用方式、临床可行性展示或应用缺乏新意，那么你必须提供具体的既有工作参考。  
- **清晰度不足：** 图 2 展示了一个包含许多组件的复杂流水线，但各组件的作用以及它们之间的交互并没有得到充分解释。

- **流水线复杂度不必要地过高：** 该框架需要从头训练大量专家模型，但论文没有充分说明为什么不能改用预训练基础模型或现有医学模型来充当专家池。鉴于医学基础模型能力日益增强，如果没有更严格的论证，这一设计选择显得复杂度过高且缺乏必要性。

**8. 请评价论文的清晰度和组织性。**  
较差

**9. 请评价论文的可复现性。请注意，提供代码和数据是加分项，但不是接收的必要条件。**  
该投稿未提供足够的信息以支持复现。

**10. 伦理规范检查。根据你的评审以及你对 MICCAI 科学伦理准则的理解，你是否认为该投稿可能涉及潜在的伦理问题或违规？审稿人在完成此项评估前应熟悉 MICCAI 科学伦理准则：** https://miccai.org/index.php/about-miccai/policies/scientific-code-of-ethics/  
否

**13. 请按 1-6 分为论文打分，其中 6 为最强（6-4：接收；3-1：拒稿）。请充分使用整个分值范围。拉开分数有助于形成决策分布。**  
2. 拒稿 —— 应当拒稿，与 rebuttal 无关

**14. 请说明你的推荐理由。导致你对本文总体评分的主要因素是什么？**  
尽管本文处理的是一个具有临床相关性的问题，并提出了一个有趣的基于智能体的框架，但若干关键问题导致我建议拒稿。

首先，系统描述不够清晰。该框架引入了多个组件，但这些组件的作用及其相互关系并没有被清楚解释，这使得论文难以理解。

其次，所提方法看起来复杂度过高且未必必要。该框架依赖从头训练大量专家模型，但论文并未充分讨论为什么不能使用预训练基础模型或更简单的替代方案。

**16. 综合以上回答以及你的整体评审体验，你会如何评价自己对此评审的信心？**  
非常有信心（4）

---

## 审稿人 #3

### 问题

**3. 请对论文的相关性进行分类（可多选）。请注意《审稿人指南》中针对不同论文类别的不同评审标准：** https://conferences.miccai.org/2026/en/REVIEWER-GUIDELINES.html  
MIC

**4. 你会如何描述这篇论文？**  
方法学贡献

**5. 请描述论文的主要贡献。**  
论文提出了 ThyroidAgent，这是一种策略驱动的系统，用分割与分类模型之间的动态专家选择和聚合来替代固定的甲状腺超声流水线。它将分割掩膜与影像组学特征结合，以提升恶性分类性能并使决策更具可解释性。作者将多个公开的甲状腺超声数据集进行了统一整理，形成一个用于跨数据集评估的整合基准。该框架使用元数据、模型置信度以及专家分歧信号来支持具备上下文感知能力的决策。

**6. 请列出论文的主要优点。** 例如，你可以强调一种新颖的表述方式、原创的数据使用方式、临床可行性的展示、新颖的应用、特别强的实验评估，或其他任何构成该工作的强项。请提供细节，例如，如果某个方法是新颖的，请解释其新颖之处以及为何有趣。  
1. 整体系统思路很有意思，尤其是从静态流水线转向自适应专家路由这一点。

2. 它将分割、分类和影像组学整合在一个统一工作流中，这比将它们视作彼此独立的任务更强。

3. 跨数据集评估的目标很有价值，因为甲状腺超声数据通常会因扫描设备、机构和采集设置不同而存在差异。

4. 图示和工作流设计清楚地解释了系统预期如何运行。

**7. 请列出论文的主要缺点。** 请提供细节：例如，如果你认为某个表述方式、数据使用方式、临床可行性展示或应用缺乏新意，那么你必须提供具体的既有工作参考。  
1. 实验并未清楚支撑关于鲁棒性、适应性、可解释性或泛化能力的论断。
2. 表 3 仅比较了“最佳单模型”和“智能体”；缺少关于 LLM 与启发式选择、影像组学与原始掩膜特征、专家数量、以及元数据输入与纯图像输入之间差异的消融实验。
3. 图 3 展示了分歧现象，但并未量化智能体选择正确专家的频率，也没有报告延迟和成本开销。
4. 论文似乎遗漏了两项高度相关的工作，未加讨论和比较：论文似乎遗漏了两项高度相关的工作，未加讨论和比较：EchoVLM [R2] 使用动态专家路由处理异构超声任务；knowledge-interpretable multi-task learning framework [R3] 将甲状腺分割与分类以可解释设计方式耦合起来。这两者都与本文方法存在较大重叠，但文中均未讨论或比较。

5. 文中仍存在一些不一致之处，例如 “ThyAgent-Seg” 与 “ThyroidAgent” 的命名不统一。每项任务训练 12 个专家再加上 LLM 推理的训练成本也没有被讨论，而且 VLM 基线（Qwen3-VL、MedGemma）是通过 prompt engineering 而非微调获得结果，这可能削弱比较的公平性。

6. 没有放射科医生参与闭环研究、前瞻性验证或强有力的外部泛化测试。

7. 智能体和 LLM 的角色尚未被完全定义，也没有被严格评估。

8. 表格和图整体上较清晰，但在正文讨论结果时，应明确引用表 1 和表 2。

9. 子图标注应统一规范，例如使用 Fig. 3(a) 而不是 Fig. 3.(a)。

10. 还存在一些小的展示问题，例如图 1 中的拼写错误（“Generalizatior” 应为 “Generalization”）以及不一致的图引用格式。

11. 式（1）中的变量定义不足。𝑦、𝑦𝑏、𝑝𝑝𝑜𝑠、𝑝𝑛𝑒𝑔 的含义，以及 𝑧𝑏 中下标的作用都不清楚。此外，符号 𝐴𝑣𝑔𝑃𝑜𝑜𝑙31 含义模糊，应明确说明。

12. 在式（2）中，多个变量（例如 𝑁𝑔、𝑃(𝑖,𝑗) 以及指示函数 𝐼[⋅]）没有定义，导致公式不完整。

13. 损失函数（例如 𝐿𝑠𝑒𝑔、GLA）被提及但没有明确写出其数学表达式。给出其形式化定义将提升清晰度和可复现性。

14. “证据”（例如分割证据和分类证据）的概念是该方法的核心，但并未被正式定义，因此很难理解这些信号是如何构建并被智能体使用的。

[R1] Duong, V. H., Vu, H., Phan, H. D., Nguyen, D. Q., Pham, D. H., Le, Q. T., ... & Ngo, D. H. (2025, September). ThyroidXL: Advancing Thyroid Nodule Diagnosis with an Expert-Labeled, Pathology-Validated Dataset. In International Conference on Medical Image Computing and Computer-Assisted Intervention (pp. 616-626). Cham: Springer Nature Switzerland.

[R2] She, C., Lu, R., Chen, L., Wang, W., & Huang, Q. (2025). Echovlm: Dynamic mixture-of-experts vision-language model for universal ultrasound intelligence. arXiv preprint arXiv:2509.14977.

[R3] Shin, M., Song, J., Kim, M. G., Yu, H. W., Choe, E. K., & Chai, Y. J. (2025). Thyro-GenAI: a chatbot using retrieval-augmented generative models for personalized thyroid disease management. Journal of Clinical Medicine, 14(7), 2450.

**8. 请评价论文的清晰度和组织性。**  
尚可

**9. 请评价论文的可复现性。请注意，提供代码和数据是加分项，但不是接收的必要条件。**  
该投稿未提供足够的信息以支持复现。

**10. 伦理规范检查。根据你的评审以及你对 MICCAI 科学伦理准则的理解，你是否认为该投稿可能涉及潜在的伦理问题或违规？审稿人在完成此项评估前应熟悉 MICCAI 科学伦理准则：** https://miccai.org/index.php/about-miccai/policies/scientific-code-of-ethics/  
否

**13. 请按 1-6 分为论文打分，其中 6 为最强（6-4：接收；3-1：拒稿）。请充分使用整个分值范围。拉开分数有助于形成决策分布。**  
3. 弱拒 —— 略低于接收门槛，但若最终被接收我也可以接受，取决于 rebuttal

**14. 请说明你的推荐理由。导致你对本文总体评分的主要因素是什么？**  
主要问题在于消融实验较弱、与高度相关工作的比较不足、方法不够清晰，以及对成本和可复现性的分析不充分。

**16. 综合以上回答以及你的整体评审体验，你会如何评价自己对此评审的信心？**  
非常有信心（4）

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