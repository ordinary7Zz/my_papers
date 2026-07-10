# Classification_Agent 与 Segmentation_Agent 决策机制与 Prompt 分析

## 概述

本文档对比分析两个基于 LLM 的医学影像 Agent 系统：

- **Classification_Agent**：甲状腺超声结节良恶性分类
- **Segmentation_Agent**：甲状腺超声图像分割

两者核心设计理念一致：**多模型推理 → 无监督质量/一致性评估 → LLM 综合决策 → 降级兜底**。

---

## 一、Classification_Agent — 分类 Agent

### 1.1 系统架构

5 个分类模型对同一张甲状腺超声图像推理 → LLM Agent 从中选出最可信结果。

**注册模型**：

| 模型名称 | 类型 | 训练数据 | 需要掩码 |
|---------|------|---------|---------|
| `DINO_UNet_all_datasets` | DINO-UNet 多任务 | TN3K+ThyroidXL+TN5K+Cine-Clip (31304) | 否 |
| `DINO_UNet_TN3K` | DINO-UNet 多任务 | TN3K (4633) | 否 |
| `DINO_UNet_TN5K` | DINO-UNet 多任务 | TN5K (3400) | 否 |
| `DINO_UNet_ThyroidXL` | DINO-UNet 多任务 | ThyroidXL (9441) | 否 |
| `AutoGluon_autogluon_radiomics_dataset3` | AutoGluon+PyRadiomics | TN3K+ThyroidXL+TN5K (15109) | 是 |

**LLM 配置**：阿里云 DashScope，模型 `qwen-plus-2025-12-01`，`temperature=0.3`，`max_tokens=1024`（单图）/`8192`（批量），关闭思考模式。

### 1.2 决策机制

```
输入图像
    ↓
所有注册模型推理 → 得到 N 个 ModelOutput
    ↓
所有模型 top_class 一致？
    ├── 是 → 取 top_confidence 最高者（不调用 LLM）
    └── 否 → 进入 LLM 决策
                ↓
          enable_agent?
          ├── false → top_k 个最高置信度模型 soft voting
          └── true → 调用 LLM API
                      ↓
                top_k=1?
                ├── 是 → LLM 返回 selected_model/class/confidence
                └── 否 → LLM 返回 selected_models[] → 程序 soft voting
                      ↓
                API 失败/解析失败?
                ├── 是 → 降级选择（最高置信度或 top_k soft voting）
                └── 否 → 返回 AgentDecision
                      ↓
                _post_check_structured_fields 修正数值
                      ↓
                最终决策输出
```

**三层决策逻辑**（`agent/classification_agent.py`）：

1. **一致性短路**：所有模型 `top_class` 一致时，**不调用 LLM**，直接取 `top_confidence` 最高的模型。
2. **LLM 决策**（存在分歧时）：
   - `top_k=1`：LLM 选出单一最佳模型
   - `top_k>1`：LLM 选出 `top_k` 个最可信模型 → 程序对概率取平均（soft voting）
3. **降级选择**：LLM 调用失败/解析失败时，按 `top_confidence` 排序取 top_k。

**核心决策优先级**（写入 Prompt 中的 `【决策序】`）：

> 主置信度 → 设备匹配 → 验证集指标(acc/AUC/F1) → entropy/margin → 数据集性能/规模 → 投票一致性 → 模型结构差异

### 1.3 Prompt 内容

#### 1.3.1 单图 System Prompt（`top_k=1`）

```
你是甲状腺超声多模型预测整合专家，从若干模型输出中选最可信的一项。

【设备】设备决定成像风格；训练数据覆盖输入同款/同品牌者更可信。GE(Logiq E9/S7 等)与 Hitachi(ARIETTA 等)各系内部风格近；其余品牌与上述有差异。Heterogeneous=多设备混合。输入设备未知则忽略此项。

【字段】主置信度优先 metadata.classification_uncertainty.top_confidence_calibrated，否则 top_confidence_raw 或 top_confidence。entropy(越大越不确定)、margin_top2(越大越稳) 在同路径下。consistency_metrics：num_models_same_class、total_models、vote_entropy。

【决策序】1)主置信度 2)已知输入设备则设备匹配 3)主置信度差<0.05 时比 validation_metrics.on_training_dataset 的 acc/AUC/F1 4)仍接近则 entropy 更低、margin_top2 更高 5)能推断 TN3K/ThyroidXL/TN5K/CineClip 则看 base_dataset_performance，否则 dataset_size 更大优先 6)差<0.05 结合投票与 num_models_same_class；类别冲突时若有单模型主置信度>0.95 可优先 7)仅当差<0.02 再考虑模型结构差异。

【输出】只输出纯 JSON（无 Markdown/思考/代码块），首尾为 { }，字段：
- selected_model, selected_class, confidence
- runner_up_model, runner_up_confidence, delta_confidence
- triggered_rules（如 ["R1","R3"]）
- reasoning

【一致性】delta_confidence=confidence-runner_up_confidence；比较词须与数值一致（delta>=0.05 才能写"显著高于/远高于"，否则写"高于/接近"）。
```

#### 1.3.2 多模型融合 System Prompt（`top_k>1`，动态嵌入 `top_k`）

```
你是甲状腺超声多模型预测整合专家，从若干模型中选出最值得信任的 {tk} 个模型（按信任度从高到低），用于对各类别概率取平均融合。

【设备】设备决定成像风格；训练数据覆盖输入同款/同品牌者更可信。GE(Logiq E9/S7 等)与 Hitachi(ARIETTA 等)各系内部风格近；其余品牌与上述有差异。Heterogeneous=多设备混合。输入设备未知则忽略此项。

【字段】主置信度优先 metadata.classification_uncertainty.top_confidence_calibrated，否则 top_confidence_raw 或 top_confidence。entropy、margin_top2、consistency_metrics 等同单选任务。

【决策序】综合判断哪 {tk} 个模型作为组合最可信，使它们概率向量平均后的融合更可靠；优先级与单选类似，但需考虑组合互补性（如设备覆盖、验证集指标与不确定性）。

【输出】只输出纯 JSON（无 Markdown/思考/代码块），首尾为 { }，字段：
- selected_models: 字符串数组，长度恰好为 {tk}，元素必须为输入中的 model_name，按可信度从高到低
- reasoning: 中文，说明为何选这 {tk} 个模型及关键数值对比

不要输出 selected_class 或 confidence；最终类别与置信度由程序对选中模型的概率分布取平均得到。
```

#### 1.3.3 User Prompt

```python
prompt = f"""{sys_prompt}
{data_info_text}{base_datasets_text}
以下为 {len(predictions)} 个模型的预测(JSON)：

{formatted_preds}

{user_tail}"""
```

其中：
- `user_tail`（`top_k=1`）= `"选出最佳结果，严格按【输出】只回复 JSON。"`
- `user_tail`（`top_k>1`）= `"选出最值得信任的模型组合，严格按【输出】只回复 JSON。"`

#### 1.3.4 批量模式 System Prompt（`top_k=1`）

```
你是甲状腺超声多模型整合专家：对 batch 中每张图单独从多模型输出中选最可信项。

【单图规则】与单图任务相同：主置信度(top_confidence_calibrated 优先)→设备(已知时)→差<0.05 比 on_training_dataset 的 acc/AUC/F1→entropy↓ margin↑→base_dataset_performance/dataset_size→投票与高置信>0.95；字段见各 predictions 的 metadata。

【批处理】每图独立决策；仅当某模型在整批持续极端不合理时，可整体降低其权重。

【输出】纯 JSON，无 Markdown/思考。结构：
{"decisions":[{"image_index":0,"image_name":"","selected_model":"","selected_class":"","confidence":0.0,"runner_up_model":"","runner_up_confidence":0.0,"delta_confidence":0.0,"triggered_rules":["R1"],"reasoning":""},...]}。
decisions 长度必须等于图像数，顺序与输入 image_index 一致。
【一致性】delta_confidence=confidence-runner_up_confidence；delta>=0.05 才能写"显著高于/远高于"，否则写"高于/接近"。
```

#### 1.3.5 批量模式 System Prompt（`top_k>1`）

```
你是甲状腺超声多模型整合专家：对 batch 中每张图单独选出最值得信任的 {tk} 个模型（按信任度从高到低），用于对各类别概率取平均融合。

【单图规则】与单图 top_k 任务相同：主置信度→设备→验证集→entropy→base_dataset 等；字段见各 predictions 的 metadata。

【批处理】每图独立决策；仅当某模型在整批持续极端不合理时，可整体降低其权重。

【输出】纯 JSON，无 Markdown/思考。结构：
{"decisions":[{"image_index":0,"image_name":"","selected_models":[...],"reasoning":""},...]}。
每个 decision 的 selected_models 长度必须恰好为 {tk}；decisions 长度必须等于图像数，顺序与输入 image_index 一致。
不要输出 selected_class 或 confidence；最终类别由程序对选中模型概率取平均得到。
```

#### 1.3.6 批量模式 User Prompt

```python
prompt = f"""{batch_system_prompt}
{data_info_text}
共 {n_img} 张图的多模型预测(JSON)；decisions 必须恰好 {n_img} 条且与 image_index 顺序一致：

{formatted_str}

按【输出】只回复 JSON。"""
```

#### 1.3.7 发送给 LLM 的预测数据格式

```json
{
  "model_name": "DINO_UNet_all_datasets",
  "top_class": "良性",
  "top_confidence": 0.8234,
  "top2_predictions": [{"良性": 0.8234}, {"恶性": 0.1766}],
  "metadata": {
    "classification_uncertainty": {
      "top_confidence_calibrated": 0.7890,
      "top_confidence_raw": 0.8234,
      "entropy": 0.6890,
      "margin_top2": 0.6468
    },
    "consistency_metrics": {
      "num_models_same_class": 3,
      "total_models": 5,
      "vote_entropy": 0.7219
    },
    "training_data_devices": ["GE Logiq E9", "ARIETTA 850"],
    "dataset_info": {
      "training_dataset": "all_datasets",
      "base_datasets": ["TN3K", "ThyroidXL", "TN5K", "Cine-Clip"],
      "dataset_size": 31304
    },
    "validation_metrics": {
      "on_training_dataset": {"accuracy": 0.85, "auc": 0.90, "f1_score": 0.87}
    },
    "base_dataset_performance": {
      "TN3K": {"accuracy": 0.6891, "auc": 0.7685, "ece": 0.2442},
      "ThyroidXL": {"accuracy": 0.8491, "auc": 0.9301, "ece": 0.1089}
    }
  }
}
```

---

## 二、Segmentation_Agent — 分割 Agent

### 2.1 系统架构

6 个 DINO-UNet 分割模型推理 → 对每个模型输出掩码做**无监督质量评估**（形态学+一致性+跨模型分歧）→ LLM 从中选择最佳单模型或 Top-K ensemble。

**注册模型**：6 个 DINO-UNet 模型，各自在不同数据集（TN3K / ThyroidXL / TN5K / Cine-Clip / DDTI / all_datasets）上训练。

**LLM 配置**：阿里云 DashScope，模型 `qwen2.5-32b-instruct`，`temperature=0.3`，强制 `response_format={"type": "json_object"}`，429 限流时指数退避重试。

### 2.2 决策机制

```
输入图像
    ↓
所有注册模型推理 → 得到 N 个掩码
    ↓
无监督质量评估
├── 形态学指标：面积、连通性、圆形度、平滑度、紧凑度、实心度、长宽比
├── 模型间一致性：pairwise IoU 矩阵、平均一致性、HD95 矩阵
└── 跨模型分歧：area_cv, pairwise_hd95_mean/std, area_rel_to_group, mean_hd95_to_others
    ↓
use_agent_selection?
├── false → 按前景区域平均置信度选 Top-K → ensemble
└── true → 调用 LLM Agent
            ↓
      ensemble_top_k=1?
      ├── 是 → LLM 返回 selected_model → 直接用该模型掩码
      └── 否 → LLM 返回 selected_models[]+weights[] → 加权融合概率图 → 阈值二值化 → 保留最大连通区域
            ↓
      API 失败/解析失败?
      ├── 是 → 降级：选与其他模型平均 IoU 一致性最高的模型（或 Top-K 等权融合）
      └── 否 → 后处理（补充分歧数值到 reasoning）→ 最终输出
```

**决策路径**（`agent/segmentation_agent.py` 的 `select_best_mask`）：

1. **质量评估**：计算面积、连通性、圆形度、平滑度、紧凑度等形态学指标；计算 pairwise IoU 矩阵和 HD95 矩阵（模型间一致性）。
2. **LLM 决策**：
   - **单模型模式**（`ensemble_top_k=1`）：LLM 返回 `selected_model`，直接用该模型掩码
   - **Ensemble 模式**（`ensemble_top_k>1`）：LLM 返回 `selected_models[]` + `weights[]` → 按权重加权融合概率图 → 阈值二值化 → 保留最大连通区域
3. **降级选择**：LLM 失败时，选与其他模型平均 IoU 一致性最高的模型（或 Top-K 等权融合）。

### 2.3 Prompt 内容

#### 2.3.1 System Prompt

```
你是甲状腺超声多模型分割智能体。从若干模型对同一图像的分割掩码中选择最可信的输出。

输入为多个分割模型的预测，包含每个模型掩码的形态学质量指标、模型间一致性(IoU/HD95)、跨模型分歧(area_cv, pairwise_hd95_mean, area_rel_to_group, mean_hd95_to_others)、训练数据集性能(Dice/AUC)、数据集信息、前景置信度。

【决策优先级】
1. 模型间一致性：与其他模型平均IoU越高、HD95越低越可信
2. 形态学合理性：面积适中、连通性好、边界平滑、紧凑度合理
3. 前景置信度：前景区域平均置信度越高越可信
4. 设备匹配：训练数据设备与输入设备匹配者优先
5. 验证集性能：Dice/AUC更高的模型更可信
6. 数据集规模与覆盖：训练集更大、覆盖更广的模型更可靠

【分歧处理】
- 当area_cv大(>0.3)或pairwise_hd95_mean高时，说明模型间分歧大，需更谨慎
- 分歧大时优先选一致性高的模型；分歧小时可考虑ensemble
- 若某模型area_rel_to_group偏离1.0较远(>1.5或<0.7)，说明该模型掩码面积异常

【输出要求】
只输出纯JSON，无Markdown/思考过程。
单选模式：{"selected_model":"", "confidence":0.0, "reasoning":""}
Ensemble模式：{"selected_models":["",""], "weights":[0.5,0.5], "confidence":0.0, "reasoning":""}
reasoning须用中文，引用具体数值(如IoU=0.85, area_cv=0.12)说明选择理由。
```

#### 2.3.2 User Prompt 结构

```python
prompt = f"""{system_prompt}

{disagreement_summary}    # 分歧摘要前缀（如有）

输入设备信息: {device_info}
输入数据信息: {input_data_info}

以下是 {n_models} 个模型的预测结果(JSON)：

{formatted_predictions_json}

从上述模型中{'选出最可信的1个模型' if ensemble_top_k==1 else f'选出最值得信任的{ensemble_top_k}个模型进行ensemble融合'}，严格按【输出要求】只回复JSON。"""
```

#### 2.3.3 发送给 LLM 的预测数据格式

```json
{
  "model_name": "DINO_UNet_TN3K",
  "mask_stats": {
    "foreground_area": 12345,
    "num_connected_components": 1,
    "circularity": 0.78,
    "smoothness": 0.92,
    "compactness": 0.65,
    "solidity": 0.88,
    "aspect_ratio": 1.12
  },
  "consistency": {
    "mean_iou_to_others": 0.85,
    "mean_hd95_to_others": 3.2
  },
  "disagreement": {
    "area_rel_to_group": 1.05,
    "mean_hd95_to_others": 3.2
  },
  "training_info": {
    "base_datasets": ["TN3K"],
    "dataset_size": 4633,
    "training_data_devices": ["GE Logiq E9", "ARIETTA 850"]
  },
  "validation_metrics": {"dice": 0.82, "auc": 0.91},
  "foreground_confidence": 0.89
}
```

---

## 三、核心对比

| 维度 | Classification_Agent | Segmentation_Agent |
|------|---------------------|-------------------|
| **任务** | 甲状腺结节良恶性分类 | 甲状腺超声图像分割 |
| **模型数** | 5 个（4 DINO-UNet + 1 AutoGluon） | 6 个 DINO-UNet |
| **评估指标** | 置信度、entropy、margin、验证集 acc/AUC/F1 | 形态学指标（面积/圆形度/连通性等）、IoU/HD95 一致性、前景置信度 |
| **LLM 选择** | 选最佳模型 或 Top-K soft voting | 选最佳模型 或 Top-K 加权 ensemble |
| **分歧处理** | 类别冲突时看投票一致性，高置信(>0.95)优先 | area_cv/pairwise_hd95 量化分歧，分歧大时优先一致性 |
| **LLM 模型** | `qwen-plus-2025-12-01` | `qwen2.5-32b-instruct` |
| **一致性短路** | ✅ 所有模型 top_class 一同时跳过 LLM | ❌ 无（总是评估+决策） |
| **降级策略** | 按 top_confidence 排序 | 按平均 IoU 一致性排序 |
| **输出后处理** | 修正 confidence/delta 数值一致性 | 补充分歧数值到 reasoning、ensemble 融合+二值化 |
| **批量处理** | ✅ 支持（每图独立决策） | ❌ 逐图处理 |
| **融合方式** | 概率算术平均（soft voting） | 概率加权平均/equal_weight/几何平均 → 二值化 |
| **强制 JSON** | 否（Prompt 约束 + 解析容错） | 是（`response_format={"type": "json_object"}`） |

---

## 四、关键文件清单

### Classification_Agent

| 文件路径 | 作用 |
|---------|------|
| `main.py` | 主入口，编排模型注册、推理、决策、评估 |
| `agent/classification_agent.py` | **核心 Agent**：LLM 决策逻辑、所有 Prompt、批量处理 |
| `agent/gemini_agent.py` | 备用 Agent（智谱 GLM 版本，功能子集） |
| `models/base_model.py` | ModelOutput 数据类 + BaseClassificationModel 抽象基类 |
| `models/model_registry.py` | 模型注册表管理 |
| `models/dino_unet_model.py` | DINO-UNet 模型包装器 |
| `models/autogluon_radiomics_model.py` | AutoGluon+PyRadiomics 模型包装器 |
| `model_architectures/dino_unet_multitask.py` | DINOv3+UNet 多任务神经网络架构 |
| `config/config.yaml` | 主配置文件 |
| `calibration/runtime.py` | 概率校准运行时加载与应用 |

### Segmentation_Agent

| 文件路径 | 作用 |
|---------|------|
| `main.py` | 主入口，协调模型推理、质量评估、Agent 决策 |
| `agent/segmentation_agent.py` | **核心 Agent**：LLM 决策逻辑、质量评估编排、Prompt |
| `models/base_model.py` | ModelOutput 数据结构 + 模型基类 |
| `models/model_registry.py` | 模型注册表 |
| `models/dino_unet_model.py` | DINO-UNet 模型实现 |
| `model_architectures/dino_unet.py` | DINOv3_S_UNet 网络结构定义 |
| `utils/image_processor.py` | 图像加载/保存/预处理 |
| `utils/quality_evaluator.py` | 无监督掩码质量评估（形态学+一致性） |
| `utils/metrics.py` | Dice, HD95, IoU, ECE 计算函数 |
| `utils/performance_stats.py` | 批量统计汇总（含 bootstrap CI95） |
| `config/config.yaml` | 主配置文件 |
