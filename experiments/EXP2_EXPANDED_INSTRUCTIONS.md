# Exp 2 扩展实验运行指南

## 目标
将 Exp 2 (Prompt Strategy Comparison) 从 n=5 扩展到 n=15，提升统计显著性。

## 实验机器准备

1. 确保后端服务运行：
```bash
cd e:\Project\CodeTutor-ITS
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. 安装依赖：
```bash
pip install httpx pandas
```

## 运行实验

```bash
cd e:\Project\CodeTutor-ITS
python experiments/scripts/prompt_comparison.py
```

输出文件: `experiments/results/prompt_comparison_exp2.csv`

## 实验内容

- 15 道编程题，覆盖 6 个主题：
  - python_basics (5题)
  - algorithms (4题)
  - oop (3题)
  - data_structures (2题)
  - control_flow (1题)
  - web_basics (1题)

- 3 种提示策略：
  - zero_shot
  - few_shot
  - cot (Chain-of-Thought)

- 总共 45 个样本 (15题 × 3策略)

## 预期输出

脚本会输出：
1. 每个问题的响应质量指标
2. 按策略分组的汇总统计
3. 按主题分组的统计
4. 按难度分组的统计

## 后续步骤

实验完成后，需要：
1. 将新结果更新到论文 Table (Exp 2)
2. 重新计算 Wilcoxon signed-rank 检验
3. 更新论文中的 n 值 (n=5 → n=15)
4. 更新统计显著性报告
