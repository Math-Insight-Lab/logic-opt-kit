"""
06_report_export_demo.py
Markdown / LaTeX 建模报告完整导出示例
运行后生成 opt_report.md 与 opt_report.tex
"""
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.model_builder import QuickModelBuilder
from logic_opt_kit.report import export_markdown_report, export_latex_report

def main():
    backend = get_solver_backend("highs")
    mb = QuickModelBuilder(backend, model_name="report_demo_model")

    x = mb.var("x", 0, 20, "C")
    y = mb.var("y", 0, 20, "C")
    mb.cons(x + 2*y <= 15)
    mb.obj(x + y, sense="max")
    mb.solve()

    sol = mb.solution()
    obj_val = mb.obj_value()

    solve_info = {
        "solver": "highs-python",
        "model_name": "report_demo_model"
    }

    export_markdown_report(
        out_path="opt_report.md",
        model_name="report_demo_model",
        solve_info=solve_info,
        solution=sol,
        obj_val=obj_val
    )

    export_latex_report(
        out_path="opt_report.tex",
        model_name="report_demo_model",
        solve_info=solve_info,
        solution=sol,
        obj_val=obj_val
    )

    print("==== Report export demo ====")
    print("Generated: opt_report.md , opt_report.tex")
    print(f"obj = {obj_val:.4f}")

if __name__ == "__main__":
    main()
