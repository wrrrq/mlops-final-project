# MLflow 实验追踪报告 (Experiments Tracking)

在本次模型训练中，我们通过 MLflow 记录并对比了两次不同的实验。

## 实验列表
1. **Baseline_Model**：使用基础参数训练的基线模型（`n_estimators=10`, `max_depth=3`）。
2. **Improved_Model_v2**：使用更深层次的随机森林进行调优训练（`n_estimators=100`, `max_depth=10`）。

## 生产模型选择 (Production-worthy)
经过对比，我们团队一致决定将 **`Improved_Model_v2`** 作为最终的生产环境模型（Production Model）。

## 核心指标考量 (Metric)
在医疗健康预测场景下，我们不能仅仅关注 **Accuracy (准确率)**，我们更应该重点优化 **Recall (召回率)**。
- 漏诊（False Negative：把有病的预测成没病）的代价极高，甚至可能危及生命。
- `Improved_Model_v2` 在提升整体准确率的同时，通过增加树的深度，显著提高了对高危患者的敏感度（Recall），这完全符合我们 "HeartGuard" 项目的医疗辅助定位。