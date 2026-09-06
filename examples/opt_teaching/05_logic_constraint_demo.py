"""
05_logic_constraint_demo.py
数理逻辑约束构建完整演示
- 一阶逻辑：AND/OR/NOT
- MSO二阶逻辑：全称量词forall、存在量词exists、邻接约束NO_ADJACENT、至少一个选中
- MSO约束翻译为MIP线性约束
"""
from logic_opt_kit.core.logic_solver import LogicConstraintBuilder
from logic_opt_kit.core.model_builder import QuickModelBuilder
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.logic_solver import (
    translate_mso_no_adjacent_to_mip,
    translate_mso_at_least_one_to_mip,
)
from logic_opt_kit.viz import plot_solution_bar


def demo_first_order():
    """演示一阶命题逻辑"""
    lb = LogicConstraintBuilder()
    
    lb.add_or("b1", "b2", "b3")
    lb.add_and("b1", "not_b2")
    lb.add_not("b3")
    
    print("==== 一阶命题逻辑演示 ====")
    print("逻辑子句:")
    for c in lb.get_clauses():
        print(f"  {c}")
    
    return lb


def demo_mso():
    """演示MSO二阶逻辑"""
    lb = LogicConstraintBuilder()
    
    # MSO全称量词
    lb.mso_for_all("v", "p(v)")
    # MSO存在量词
    lb.mso_exists("v", "q(v)")
    # MSO邻接约束：相邻变量不能同时为1
    lb.mso_no_adjacent(["x0", "x1", "x2", "x3"])
    # MSO至少一个选中
    lb.mso_subset_at_least_one(["x0", "x1", "x2", "x3"])
    
    print("\n==== MSO二阶逻辑演示 ====")
    print("MSO约束:")
    for c in lb.get_mso_constraints():
        print(f"  {c}")
    
    return lb


def demo_mso_to_mip():
    """演示MSO约束翻译为MIP线性约束并求解"""
    backend = get_solver_backend("scip")
    mb = QuickModelBuilder(backend, model_name="mso_mip_demo")
    
    # 创建4个二元变量
    x_vars = {}
    for i in range(4):
        x_vars[f"x{i}"] = mb.var(f"x{i}", low=0, high=1, vtype="B")
    
    # 将MSO约束翻译为MIP
    translate_mso_no_adjacent_to_mip(mb, x_vars, ["x0", "x1", "x2", "x3"])
    translate_mso_at_least_one_to_mip(mb, x_vars, ["x0", "x1", "x2", "x3"])
    
    # 目标：最大化选中的变量数量
    obj = sum(x_vars[f"x{i}"] for i in range(4))
    mb.obj(obj, sense="max")
    
    mb.solve()
    sol = mb.solution()
    
    print("\n==== MSO->MIP翻译求解演示 ====")
    print("MSO邻接约束: 相邻变量不能同时选中 (x_i + x_{i+1} <= 1)")
    print("MSO存在约束: 至少选中一个变量 (sum >= 1)")
    print(f"\n最优解: 选中 {int(round(sum(sol.values())))} 个变量")
    for k, v in sol.items():
        print(f"  {k} = {v:.0f}")
    
    return sol


def demo_grid_graph_mso():
    """演示网格图上的MSO约束"""
    from logic_opt_kit.core.mso_graph import MSOGridGraphBuilder
    
    print("\n==== 网格图MSO约束演示 ====")
    g = MSOGridGraphBuilder(height=3, width=3)
    
    # 设置种子节点
    seed = [g.coord2vid[(1, 1)]]
    
    # 生成MSO规范
    g.mso_no_isolated_vertex("S")
    g.mso_seed_must_in_subset(seed, "S")
    
    spec = g.get_mso_spec()
    print(f"网格图 {3}x{3}, 顶点数={g.num_vertex}")
    print(f"种子节点: {seed}")
    print(f"MSO规范条目数: {len(spec)}")
    for i, s in enumerate(spec[:3]):
        display = s[:80] + "..." if len(s) > 80 else s
        print(f"  [{i}] {display}")
    
    return g


def main():
    # 1. 一阶逻辑
    demo_first_order()
    
    # 2. MSO二阶逻辑
    mso_lb = demo_mso()
    
    # 3. MSO -> MIP 翻译求解
    sol = demo_mso_to_mip()
    
    # 4. 网格图MSO
    demo_grid_graph_mso()
    
    # 保存结果图
    demo_vars = [f"x{i}" for i in range(4)]
    demo_vals = [sol.get(f"x{i}", 0.0) for i in range(4)]
    plot_solution_bar(demo_vars, demo_vals, save_path="logic_demo.png")
    print("\nSaved figure: logic_demo.png")


if __name__ == "__main__":
    main()
