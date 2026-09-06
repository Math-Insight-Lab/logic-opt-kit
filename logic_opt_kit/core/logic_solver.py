"""
logic_solver.py
命题逻辑 + MSO(Monadic Second‑Order Logic)一元二阶逻辑约束构建器
v0.1.1 可运行版本
支持：一阶 AND/OR/NOT；MSO集合量词∀ ∃、邻接约束；输出规约文本；可翻译为MIP约束
"""
from typing import List, Dict


class LogicConstraintBuilder:
    """
    命题逻辑 + MSO 二阶逻辑约束构建器
    - 一阶：AND / OR / NOT
    - MSO二阶：对布尔变量集合做全称/存在量词、邻接约束
    """
    def __init__(self):
        self._clauses: List[str] = []
        self._mso_constraints: List[str] = []

    # ---------- 一阶命题逻辑 ----------
    def add_and(self, *terms):
        self._clauses.append(f"AND({','.join(map(str, terms))})")

    def add_or(self, *terms):
        self._clauses.append(f"OR({','.join(map(str, terms))})")

    def add_not(self, term):
        self._clauses.append(f"NOT({term})")

    # ---------- MSO 二阶集合逻辑 ----------
    def mso_for_all(self, elem_name: str, pred_expr: str):
        """MSO全称量词 ∀ elem_name: pred_expr"""
        self._mso_constraints.append(f"∀ {elem_name}: {pred_expr}")

    def mso_exists(self, elem_name: str, pred_expr: str):
        """MSO存在量词 ∃ elem_name: pred_expr"""
        self._mso_constraints.append(f"∃ {elem_name}: {pred_expr}")

    def mso_no_adjacent(self, var_set: List[str]):
        """
        MSO经典约束：集合中相邻布尔变量不能同时等于1
        :param var_set: 有序布尔变量名称列表，如 ["x0","x1","x2","x3"]
        """
        for i in range(len(var_set) - 1):
            a = var_set[i]
            b = var_set[i+1]
            self._mso_constraints.append(f"NO_ADJACENT({a},{b}) → NOT(AND({a},{b}))")

    def mso_subset_at_least_one(self, var_set: List[str]):
        """MSO约束：集合中至少一个元素为真（存在量词）"""
        expr = "OR(" + ",".join(var_set) + ")"
        self._mso_constraints.append(f"EXISTS_ONE_IN_SET → {expr}")

    def get_clauses(self) -> List[str]:
        return self._clauses.copy()

    def get_mso_constraints(self) -> List[str]:
        return self._mso_constraints.copy()

    def clear(self):
        self._clauses.clear()
        self._mso_constraints.clear()


def build_mso_location_constraint(vars_list: List[str]) -> Dict:
    """
    构造设施选址MSO约束示例
    1. 相邻变量不能同时选中
    2. 集合至少选中一个
    """
    builder = LogicConstraintBuilder()
    builder.mso_no_adjacent(vars_list)
    builder.mso_subset_at_least_one(vars_list)
    return {
        "mso_constraints": builder.get_mso_constraints(),
        "logic_clauses": builder.get_clauses()
    }


def translate_mso_no_adjacent_to_mip(mb, var_map: Dict[str, object], var_set: List[str]):
    """
    将MSO的no‑adjacent约束翻译成MIP线性约束，接入QuickModelBuilder
    NO_ADJACENT(a,b): a + b <= 1
    :param mb: QuickModelBuilder实例
    :param var_map: {变量名:模型变量对象}
    :param var_set: 有序变量名列表
    """
    for i in range(len(var_set)-1):
        a_name = var_set[i]
        b_name = var_set[i+1]
        a = var_map[a_name]
        b = var_map[b_name]
        mb.cons(a + b <= 1, name=f"mso_no_adj_{a_name}_{b_name}")


def translate_mso_at_least_one_to_mip(mb, var_map: Dict[str, object], var_set: List[str]):
    """MSO至少一个选中翻译成MIP：sum >= 1"""
    expr = sum(var_map[name] for name in var_set)
    mb.cons(expr >= 1, name="mso_at_least_one")

