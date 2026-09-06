# logic-opt-kit
Math-Insight-Lab 开源项目。
面向数学建模竞赛、运筹课程教学的轻量化MIP/MINLP工具包。

License: MIT

## AI‑Assisted Code Notice
中文：本项目部分代码片段由AI大模型辅助生成，所有AI产出均经过人工审阅、改写、调试验证。项目全部代码统一遵循 MIT License。AI仅作为编码辅助工具，整体架构与核心设计由人类开发者完成。使用本项目请自行承担技术风险。

English: Portions of source code are AI‑assisted generated. All AI outputs have been manually reviewed, rewritten and tested. The entire project is licensed under MIT License. AI serves only as coding assistant; overall architecture and core design are created by human maintainer. Use at your own risk.

## 核心特性
1. **双求解器后端架构**
   - 默认：HiGHS（开源免费MIP/LP求解器，`highspy`）
   - 可选：SCIP (需要安装 pyscipopt>=6.2.1)
2. **PuLP语法兼容层**（原型阶段）：提供 LpProblem / LpVariable 等签名与 PuLP 对齐，变量创建、类型声明可零修改迁移；`solve()` 和约束/目标添加为简化骨架，暂不支持完整表达式解析——适合教学示范迁移路径。
3. **数理逻辑求解原型**：支持命题逻辑（AND/OR/NOT）约束构建；MSO（Monadic Second-Order）一元二阶逻辑约束已完整实现，包括 `mso_for_all`、`mso_exists`、`mso_no_adjacent`、`mso_subset_at_least_one` 等方法。
4. **结果可视化**：求解结果柱状对比（`plot_solution_bar`）已可用；二维LP可行域（`plot_lp_feasible_region`）为骨架阶段，已预留约束线绘制接口。
5. 一键导出 Markdown / LaTeX 建模报告，适配课程作业、建模竞赛文档。

## 安装
```bash
# 基础版本（HiGHS）
pip install -e .

# 带SCIP支持
pip install -e ".[scip]"

# 开发+测试
pip install -e ".[scip,test]"
```

## 快速示例

```Python
from logic_opt_kit.core.solver_backend import get_solver_backend

backend = get_solver_backend(solver="highs")
# 构建模型、添加变量、约束、目标，求解，导出报告
```

## 运行示例

```Bash
cd examples/opt_teaching
python 01_lp_basic_demo.py
```

## 仓库地址

https://github.com/Math-Insight-Lab/logic-opt-kit

> 当前版本 v1.0.0：功能完整版本。
