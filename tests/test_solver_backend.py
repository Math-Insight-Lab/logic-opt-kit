"""
求解器后端单元测试
覆盖：HiGHS默认后端、SCIP可选后端、变量创建、约束添加、求解、结果获取
"""
import pytest
from logic_opt_kit.core.solver_backend import (
    get_solver_backend,
    HAS_HIGHS,
    HAS_SCIP
)

# 基础HiGHS求解器测试
def test_highs_backend_init():
    """测试HiGHS后端初始化与模型创建"""
    assert HAS_HIGHS is True, "HiGHS求解器未安装，请执行 pip install highs-python"
    backend = get_solver_backend("highs")
    backend.create_model("test_highs_model")
    assert backend.model_name == "test_highs_model"

def test_highs_var_create():
    """测试HiGHS各类变量创建（连续、整数、二进制）"""
    backend = get_solver_backend("highs")
    backend.create_model("test_var")

    # 连续变量
    c_var = backend.add_variable("c_x", low=0, high=10, vtype="C")
    # 整数变量
    i_var = backend.add_variable("i_x", low=0, high=5, vtype="I")
    # 二进制变量
    b_var = backend.add_variable("b_x", low=0, high=1, vtype="B")

    assert "c_x" in backend._var_map
    assert "i_x" in backend._var_map
    assert "b_x" in backend._var_map

def test_highs_lp_solve():
    """测试基础线性规划求解正确性"""
    backend = get_solver_backend("highs")
    backend.create_model("lp_test")

    # 创建变量
    x1 = backend.add_variable("x1", 0, None, "C")
    x2 = backend.add_variable("x2", 0, None, "C")

    # 添加约束与目标
    backend.add_constraint(2 * x1 + x2 <= 10)
    backend.add_constraint(x1 + x2 <= 8)
    backend.set_objective(3 * x1 + 2 * x2, "max")

    # 求解并校验结果
    backend.solve()
    sol = backend.get_solution()
    obj_val = backend.get_obj_val()

    assert isinstance(sol, dict)
    assert "x1" in sol and "x2" in sol
    assert obj_val > 0

# SCIP条件测试
@pytest.mark.scip
@pytest.mark.skipif(not HAS_SCIP, reason="未安装SCIP求解器，跳过测试")
def test_scip_backend_init():
    """测试SCIP后端初始化"""
    backend = get_solver_backend("scip")
    backend.create_model("test_scip_model")

@pytest.mark.scip
@pytest.mark.skipif(not HAS_SCIP, reason="未安装SCIP求解器，跳过测试")
def test_scip_minlp_basic():
    """测试SCIP非线性混合整数基础求解"""
    backend = get_solver_backend("scip")
    backend.create_model("minlp_test")

    x = backend.add_variable("x", 0, 4, "I")
    y = backend.add_variable("y", 0, None, "C")

    backend.add_constraint(x * y >= 1.5)
    backend.set_objective((x - 2) ** 2 + y ** 2, "min")
    backend.solve()

    sol = backend.get_solution()
    obj_val = backend.get_obj_val()
    assert obj_val >= 0
    assert isinstance(sol["x"], float)
    assert isinstance(sol["y"], float)

def test_unknown_solver():
    """测试非法求解器参数异常捕获"""
    with pytest.raises(ValueError):
        get_solver_backend("unknown_solver")
