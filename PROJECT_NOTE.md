# logic-opt-kit Project Note
Belong to: Math-Insight-Lab GitHub Organization
Version: v1.0.0
Date: 2026-09-01

## Project background
本项目由早期 mip-teaching-kit演进重命名，面向运筹学课程、数学建模竞赛教学场景。
设计双求解器架构：HiGHS作为默认免费求解器；SCIP作为可选高级MINLP求解后端。
内置PuLP兼容层，降低已有建模代码迁移成本；包含数理逻辑求解原型、可视化、Markdown/LaTeX报告导出。

## Current status
✅ 目录结构、pyproject.toml、基础依赖
✅ 求解器抽象层，HiGHS完整实现；SCIP完整实现（全部接口均已实现并通过测试）
✅ PuLP语法兼容层原型
✅ 报告导出模块 Markdown / LaTeX
✅ 基础可视化模块
✅ 示例集：LP、MIP背包、MINLP样例、逻辑约束、报告导出
✅ pytest测试骨架

⚠️ Known limitations
1. SCIP后端已完整实现，但仅在使用pyscipopt的平台上可用；
2. MSO一元二阶逻辑（forall/exists/无相邻/至少一个/无孤立点/种子约束）已实现；集合上二元逻辑（如连通子图完整MIP编码）尚未实现；
3. MINLP依赖底层求解器能力；HiGHS本身不支持MINLP，必须切换SCIP；
4. PULP兼容层为原型骨架，solve()/addConstraint()/setObjective() 仅实现变量创建和类型映射，不支持完整表达式解析；
5. 二维LP可行域 plot_lp_feasible_region 尚未实现约束线绘制，仅做框架占位；
6. 尚未实现与calc-insight-kit双向表达式互转。

## Online status
Repository：git@github.com:Math-Insight-Lab/logic-opt-kit.git
v1.0.0，本地原型，推送后打tag归档。

## Next-step roadmap
1. 完善MSO集合上二元逻辑约束（如连通子图完整MIP编码）
2. 实现与calc-insight-kit符号表达式互相导入
3. 丰富更多建模竞赛经典样例
4. CLI命令行入口

License: MIT
