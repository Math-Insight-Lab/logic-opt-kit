"""
03_minlp_sample_demo.py
MINLP 非线性混合整数示例
⚠️ HiGHS不支持MINLP，必须使用solver="scip"，需要安装pyscipopt>=6.2.1
min f = (x-2)**2 + y**2
s.t.
x * y >= 1.5
x ∈ {0,1,2,3,4} 整数变量
y >= 0 连续变量
"""
import sys
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.model_builder import QuickModelBuilder
from logic_opt_kit.viz import plot_solution_bar

def main():
    try:
        backend = get_solver_backend(solver="scip")
    except RuntimeError as e:
        print(f"SCIP not available: {e}")
        print("Hint: install with pip install -e \".[scip]\"")
        sys.exit(1)

    mb = QuickModelBuilder(backend, model_name="minlp_sample")
    x = mb.var("x", low=0, high=4, vtype="I")
    y = mb.var("y", low=0, high=None, vtype="C")

    # 非线性约束 x*y >=1.5
    mb.cons(x * y >= 1.5, name="nonlinear_c1")
    mb.obj((x - 2)**2 + y**2, sense="min")

    mb.solve()
    sol = mb.solution()
    obj = mb.obj_value()

    print("==== MINLP Sample (SCIP only) ====")
    print(f"Objective: {obj:.4f}")
    for k, v in sol.items():
        print(f"{k} = {v:.4f}")

    # 保存解的柱状图
    plot_solution_bar(list(sol.keys()), list(sol.values()), save_path="minlp_sol.png")
    print("Saved figure: minlp_sol.png")

if __name__ == "__main__":
    main()
