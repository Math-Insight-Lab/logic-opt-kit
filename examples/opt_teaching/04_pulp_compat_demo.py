"""
04_pulp_compat_demo.py
PuLP兼容层演示：原有PuLP风格模型定义
注意：原型兼容层仅做模型定义语义演示，表达式求值与求解桥接为简化骨架，用于教学迁移示范
"""
from logic_opt_kit.core.pulp_compat_layer import LpProblem, LpVariable, LpMaximize, LpContinuous
from logic_opt_kit.viz import plot_solution_bar

def main():
    # PuLP风格建模
    prob = LpProblem("pulp_style_demo", sense=LpMaximize)
    x = LpVariable("x", lowBound=0, upBound=10, cat=LpContinuous)
    y = LpVariable("y", lowBound=0, upBound=8, cat=LpContinuous)

    prob.addVariable(x)
    prob.addVariable(y)

    print("PuLP-compat problem variables:")
    for v in prob.variables:
        print(f"  {v.name}")

    sol = prob.solve()
    print(f"Compat layer solve result (demo skeleton): {sol}")
    
    # 保存结果图
    plot_solution_bar(list(sol.keys()), list(sol.values()), save_path="pulp_compat_sol.png")
    print("Saved figure: pulp_compat_sol.png")
    
    print("\nNote: This compat layer is prototype, full expression parse not implemented.")

if __name__ == "__main__":
    main()
