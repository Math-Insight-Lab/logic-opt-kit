"""
model_builder.py：快速模型构建封装，简化教学代码
"""
from .solver_backend import SolverBackendBase

class QuickModelBuilder:
    def __init__(self, backend: SolverBackendBase, model_name: str = "opt_model"):
        self.backend = backend
        self.backend.create_model(model_name)

    def var(self, name: str, low=0, high=None, vtype="C"):
        return self.backend.add_variable(name, low, high, vtype)

    def cons(self, expr, name=None):
        self.backend.add_constraint(expr, name)

    def obj(self, expr, sense="min"):
        self.backend.set_objective(expr, sense)

    def solve(self):
        self.backend.solve()

    def solution(self):
        return self.backend.get_solution()

    def obj_value(self):
        return self.backend.get_obj_val()
