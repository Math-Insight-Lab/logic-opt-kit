# logic-opt-kit 示例集

01_lp_basic_demo.py              基础线性规划求解
02_mip_knapsack_demo.py          0-1背包MIP经典样例
03_minlp_sample_demo.py          MINLP样例（**必须SCIP后端**，安装：pip install -e ".[scip]"）
04_pulp_compat_demo.py           PuLP兼容层迁移演示（原型骨架，仅语义演示）
05_logic_constraint_demo.py      数理逻辑约束构建演示，含MSO一元二阶逻辑约束（已实现）
06_report_export_demo.py         Markdown / LaTeX报告完整导出
07_mso_logic_demo.py             MSO设施选址：邻接约束+至少一个，MSO→MIP翻译求解
08_mso_image_grid_demo.py        MSO图像分割：网格图孤立点+种子约束，MIP重建分割掩码

输出产物说明：
- *.png：求解结果可视化图片
- opt_report.md / opt_report.tex：自动生成的建模报告
