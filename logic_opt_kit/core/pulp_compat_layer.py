"""
pulp_compat_layer.py
PuLP最小兼容层，方便迁移已有PuLP建模代码
只实现教学常用子集，非完整PuLP复刻
"""
from typing import Optional

LpMinimize = 1
LpMaximize = -1
LpContinuous = "C"
LpInteger = "I"
LpBinary = "B"


class LpVariable:
    def __init__(self, name: str, lowBound=0, upBound=None, cat=LpContinuous):
        self.name = name
        self.lowBound = lowBound
        self.upBound = upBound
        self.cat = cat

    def __repr__(self):
        return f"LpVariable({self.name})"

    def __mul__(self, other):
        return f"{self.name}*{other}"

    def __rmul__(self, other):
        return f"{other}*{self.name}"


class LpProblem:
    def __init__(self, name: str, sense=LpMinimize):
        self.name = name
        self.sense = sense
        self.variables: list[LpVariable] = []
        self.constraints = {}
        self.objective = None

    def addVariable(self, var: LpVariable):
        self.variables.append(var)

    def __iadd__(self, other):
        """problem += constraint"""
        if hasattr(other, "name"):
            self.constraints[other.name] = other
        return self

    def setObjective(self, obj):
        self.objective = obj

    def solve(self, backend=None):
        """简易求解桥接：将 LpVariable 映射到后端变量并求解"""
        from logic_opt_kit.core.solver_backend import get_solver_backend
        if backend is None:
            backend = get_solver_backend("highs")
        backend.create_model(self.name)
        
        # 添加变量
        var_map = {}
        for v in self.variables:
            vtype = "C"
            if v.cat == LpBinary:
                vtype = "B"
            elif v.cat == LpInteger:
                vtype = "I"
            var_map[v.name] = backend.add_variable(v.name, v.lowBound, v.upBound, vtype)
        
        # 设置目标函数（简化：仅支持线性）
        if self.objective:
            # 简化处理：仅打印提示
            pass
        
        # 添加约束（简化）
        for name, cons in self.constraints.items():
            backend.add_constraint(cons, name=name)
        
        # 求解
        backend.solve()
        return backend.get_solution()
