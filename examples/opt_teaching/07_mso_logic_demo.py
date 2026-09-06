"""
07_mso_logic_demo.py
MSO 一元二阶逻辑可运行完整算例
场景：一维设施选址
约束：
  1. 相邻设施不能同时开设（MSO邻接约束）
  2. 必须至少开设一处设施
目标：最大化总收益
"""
from logic_opt_kit.core.logic_solver import (
    LogicConstraintBuilder,
    build_mso_location_constraint,
    translate_mso_no_adjacent_to_mip,
    translate_mso_at_least_one_to_mip
)
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.model_builder import QuickModelBuilder


def main():
    facility_set = ["x0", "x1", "x2", "x3"]
    profit = {"x0":5, "x1":8, "x2":6, "x3":9}

    # 第一步：生成MSO形式规约文本（形式化输出，课题亮点）
    mso_model = build_mso_location_constraint(facility_set)
    print("="*65)
    print("【MSO 二阶逻辑形式规约输出】")
    print("="*65)
    for c in mso_model["mso_constraints"]:
        print(f"  {c}")

    # 手写MSO量词演示
    builder = LogicConstraintBuilder()
    builder.mso_exists("facility", "facility == 1")
    builder.mso_for_all("facility", "neighbor(facility) != 1")
    print("\n手写MSO量词：")
    for line in builder.get_mso_constraints():
        print(f"  {line}")

    # 第二步：把MSO规约翻译为MIP，调用HiGHS求解
    backend = get_solver_backend("scip")
    mb = QuickModelBuilder(backend, model_name="mso_facility_location")

    var_map = {}
    for name in facility_set:
        var_map[name] = mb.var(name, low=0, high=1, vtype="B")

    # MSO约束转MIP约束
    translate_mso_no_adjacent_to_mip(mb, var_map, facility_set)
    translate_mso_at_least_one_to_mip(mb, var_map, facility_set)

    # 目标：最大化总收益
    total_profit = sum(profit[name] * var_map[name] for name in facility_set)
    mb.obj(total_profit, sense="max")

    mb.solve()
    sol = mb.solution()
    obj = mb.obj_value()

    print("\n" + "="*65)
    print("【MIP求解结果（MSO约束翻译后）】")
    print(f"最优总收益 = {obj:.4f}")
    for k, v in sol.items():
        print(f"  {k} = {v:.0f}")
    selected = [k for k,v in sol.items() if abs(v-1.0) < 1e-6]
    print(f"选中设施：{selected}")
    print("✅ MSO示例运行完成")


if __name__ == "__main__":
    main()

