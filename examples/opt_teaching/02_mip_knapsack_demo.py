"""
02_mip_knapsack_demo.py
0-1背包MIP示例
物品：(value, weight)
背包容量 W=10
"""
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.model_builder import QuickModelBuilder
from logic_opt_kit.viz import plot_solution_bar

def main():
    items = [
        ("item0", 6, 5),
        ("item1", 5, 4),
        ("item2", 8, 6),
        ("item3", 3, 3),
    ]
    W = 10

    backend = get_solver_backend("highs")
    mb = QuickModelBuilder(backend, model_name="mip_knapsack")

    x_vars = {}
    for name, _, _ in items:
        x_vars[name] = mb.var(name, low=0, high=1, vtype="B")

    # 背包容量约束
    total_weight = 0
    total_value = 0
    for name, val, w in items:
        total_weight += w * x_vars[name]
        total_value += val * x_vars[name]

    mb.cons(total_weight <= W, name="capacity")
    mb.obj(total_value, sense="max")

    mb.solve()
    sol = mb.solution()
    obj = mb.obj_value()

    print("==== 0-1 Knapsack MIP Demo ====")
    print(f"Max value: {obj:.4f}")
    selected = [k for k, v in sol.items() if abs(v - 1.0) < 1e-6]
    print(f"Selected items: {selected}")

    plot_solution_bar(list(sol.keys()), list(sol.values()), save_path="knapsack_sol.png")
    print("Saved figure: knapsack_sol.png")

if __name__ == "__main__":
    main()
