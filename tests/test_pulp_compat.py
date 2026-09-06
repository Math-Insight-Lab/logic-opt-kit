"""
PuLP兼容层单元测试
覆盖：模型创建、变量添加、参数属性、基础语法兼容
"""
from logic_opt_kit.core.pulp_compat_layer import (
    LpProblem,
    LpVariable,
    LpMinimize,
    LpMaximize,
    LpContinuous,
    LpInteger,
    LpBinary
)

def test_pulp_problem_create():
    """测试PuLP风格模型创建"""
    prob_min = LpProblem("min_test", LpMinimize)
    prob_max = LpProblem("max_test", LpMaximize)

    assert prob_min.name == "min_test"
    assert prob_min.sense == LpMinimize
    assert prob_max.sense == LpMaximize

def test_pulp_var_create():
    """测试三类变量创建与属性校验"""
    # 连续变量
    c_var = LpVariable("x1", lowBound=0, upBound=20, cat=LpContinuous)
    # 整数变量
    i_var = LpVariable("x2", lowBound=1, upBound=10, cat=LpInteger)
    # 二进制变量
    b_var = LpVariable("x3", lowBound=0, upBound=1, cat=LpBinary)

    assert c_var.name == "x1"
    assert c_var.lowBound == 0
    assert c_var.cat == LpContinuous

    assert i_var.cat == LpInteger
    assert b_var.cat == LpBinary

def test_pulp_var_attach():
    """测试变量绑定至模型"""
    prob = LpProblem("attach_test", LpMinimize)
    x = LpVariable("x", 0, 10, LpContinuous)
    y = LpVariable("y", 0, 10, LpContinuous)

    prob.addVariable(x)
    prob.addVariable(y)

    assert len(prob.variables) == 2
    assert prob.variables[0].name == "x"
    assert prob.variables[1].name == "y"

def test_pulp_obj_set():
    """测试目标函数绑定"""
    prob = LpProblem("obj_test", LpMaximize)
    x = LpVariable("x")
    prob.addVariable(x)
    prob.setObjective(5 * x)

    assert prob.objective == 5 * x
