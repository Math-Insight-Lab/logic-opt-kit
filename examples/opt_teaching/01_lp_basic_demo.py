"""
01_lp_basic_demo.py
基础线性规划示例：2变量LP
max z = 3*x1 + 2*x2
s.t.
2*x1 + x2 <= 10
x1 + x2 <= 8
x1 >=0, x2 >=0
"""
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.model_builder import QuickModelBuilder
from logic_opt_kit.viz import plot_solution_bar

def main():
    backend = get_solver_backend(solver="highs")
    mb = QuickModelBuilder(backend, model_name="lp_basic_demo")

    x1 = mb.var("x1", low=0, high=None, vtype="C")
    x2 = mb.var("x2", low=0, high=None, vtype="C")

    mb.cons(2 * x1 + x2 <= 10, name="c1")
    mb.cons(x1 + x2 <= 8, name="c2")

    mb.obj(3 * x1 + 2 * x2, sense="max")
    mb.solve()

    sol = mb.solution()
    obj = mb.obj_value()

    print("==== LP Basic Demo Result ====")
    print(f"Optimal objective: {obj:.4f}")
    for k, v in sol.items():
        print(f"{k} = {v:.4f}")

    plot_solution_bar(list(sol.keys()), list(sol.values()), save_path="lp_basic_sol.png")
    print("Saved figure: lp_basic_sol.png")

if __name__ == "__main__":
    main()
