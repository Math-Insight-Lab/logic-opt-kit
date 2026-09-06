# Contributing to logic-opt-kit
logic-opt-kit belongs to **Math-Insight-Lab** open-source organization.

## Project Overview
面向运筹教学与数学建模竞赛的MIP/MINLP工具集。
License: MIT

Repository home
https://github.com/Math-Insight-Lab/logic-opt-kit

## Local setup
```bash
git clone git@github.com:Math-Insight-Lab/logic-opt-kit.git
cd logic-opt-kit
pip install -e ".[scip,test]"
pytest
```

## Branch strategy

* `main`：原型稳定分支，对应tag版本
* feature/*：新功能分支，PR合并进入main

## 测试标记

* `@pytest.mark.scip`：依赖SCIP/pyscipopt，无SCIP环境自动skip

## Code style

* PEP-8
* 新增示例放入 examples/opt_teaching
* 报告导出支持 Markdown / LaTeX 两种输出

## Roadmap重点

1. MSO集合上二元逻辑约束（如连通子图完整MIP编码）
2. MINLP案例扩充
3. 与calc-insight-kit做少量跨库联动（符号表达式导入模型）
4. CLI命令行
