"""
solver_backend.py
双求解器抽象层：HiGHS默认；SCIP可选；统一抽象接口
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any
import warnings

try:
    import highspy
    HAS_HIGHS = True
except ImportError:
    HAS_HIGHS = False

try:
    import pyscipopt
    HAS_SCIP = True
except ImportError:
    HAS_SCIP = False


class SolverBackendBase(ABC):
    @abstractmethod
    def create_model(self, name: str):
        ...

    @abstractmethod
    def add_variable(self, name: str, low, high, vtype: str):
        ...

    @abstractmethod
    def add_constraint(self, expr, name: Optional[str] = None):
        ...

    @abstractmethod
    def set_objective(self, expr, sense: str):
        ...

    @abstractmethod
    def solve(self):
        ...

    @abstractmethod
    def get_solution(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def get_obj_val(self) -> float:
        ...


class HighsBackend(SolverBackendBase):
    def __init__(self):
        if not HAS_HIGHS:
            raise RuntimeError("highs-python not installed")
        self.h = highspy.Highs()
        self.model_name = ""
        self._var_map: Dict[str, Any] = {}

    def create_model(self, name: str):
        self.model_name = name
        self.h = highspy.Highs()
        self._var_map.clear()

    def add_variable(self, name: str, low, high, vtype: str):
        """vtype: 'C' continuous, 'I' integer, 'B' binary"""
        lb = low if low is not None else -highspy.kHighsInf
        ub = high if high is not None else highspy.kHighsInf
        
        if vtype == "B":
            # Binary = integer in [0, 1]
            vtype_h = highspy.HighsVarType.kInteger
            lb = max(lb, 0.0)
            ub = min(ub, 1.0)
        elif vtype == "I":
            vtype_h = highspy.HighsVarType.kInteger
        else:
            vtype_h = highspy.HighsVarType.kContinuous
        
        v = self.h.addVariable(lb, ub, 0.0, type=vtype_h, name=name)
        self._var_map[name] = v
        return v

    def add_constraint(self, expr, name: Optional[str] = None):
        self.h.addConstr(expr, name=name)

    def set_objective(self, expr, sense: str):
        if sense.upper() == "MIN":
            self.h.minimize(expr)
        else:
            self.h.maximize(expr)

    def solve(self):
        self.h.run()

    def get_solution(self) -> Dict[str, Any]:
        sol = {}
        solution = self.h.getSolution()
        for name, var in self._var_map.items():
            sol[name] = solution.col_value[var]
        return sol

    def get_obj_val(self) -> float:
        return self.h.getObjectiveValue()


class ScipBackend(SolverBackendBase):
    """SCIP后端骨架，pyscipopt>=6.2.1，支持MINLP"""
    def __init__(self):
        if not HAS_SCIP:
            raise RuntimeError("pyscipopt not installed, install with [scip] extra")
        self.scip = pyscipopt.Model()
        self._var_map: Dict[str, Any] = {}

    def create_model(self, name: str):
        self.scip = pyscipopt.Model(name)
        self._var_map.clear()

    def add_variable(self, name: str, low, high, vtype: str):
        if vtype == "B":
            v = self.scip.addVar(vtype="B", name=name)
        elif vtype == "I":
            v = self.scip.addVar(vtype="I", lb=low, ub=high, name=name)
        else:
            v = self.scip.addVar(vtype="C", lb=low, ub=high, name=name)
        self._var_map[name] = v
        return v

    def add_constraint(self, expr, name: Optional[str] = None):
        try:
            # Try without name first (works for nonlinear expressions)
            self.scip.addCons(expr)
        except TypeError:
            # Fallback for versions where addCons requires different signature
            if name:
                self.scip.addCons(expr, name=name)

    def set_objective(self, expr, sense: str):
        if sense.upper() == "MIN":
            try:
                self.scip.setObjective(expr, sense="minimize")
            except ValueError:
                # Nonlinear objective, use recipes.nonlinear
                from pyscipopt.recipes import nonlinear
                nonlinear.set_nonlinear_objective(self.scip, expr, sense="minimize")
        else:
            try:
                self.scip.setObjective(expr, sense="maximize")
            except ValueError:
                from pyscipopt.recipes import nonlinear
                nonlinear.set_nonlinear_objective(self.scip, expr, sense="maximize")

    def solve(self):
        self.scip.optimize()

    def get_solution(self) -> Dict[str, Any]:
        sol = {}
        for name, var in self._var_map.items():
            sol[name] = self.scip.getVal(var)
        return sol

    def get_obj_val(self) -> float:
        return self.scip.getObjVal()


def get_solver_backend(solver: str = "highs") -> SolverBackendBase:
    slv = solver.lower()
    if slv == "highs":
        if not HAS_HIGHS:
            raise RuntimeError("highs-python missing")
        return HighsBackend()
    elif slv == "scip":
        if not HAS_SCIP:
            raise RuntimeError("pyscipopt missing, install with [scip]")
        return ScipBackend()
    else:
        raise ValueError(f"unknown solver {solver}, choose highs/scip")
