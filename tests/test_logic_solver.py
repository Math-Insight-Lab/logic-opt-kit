"""
数理逻辑约束构建模块测试
覆盖：与/或/非逻辑子句构建、清空、MSO预留接口异常
"""
from logic_opt_kit.core.logic_solver import LogicConstraintBuilder

def test_logic_clause_build():
    """测试各类逻辑子句构建"""
    builder = LogicConstraintBuilder()

    # 构建多类型逻辑约束
    builder.add_or("b1", "b2", "b3")
    builder.add_and("b1", "not_b2")
    builder.add_not("b3")

    clauses = builder.get_clauses()
    assert len(clauses) == 3
    assert "OR(b1,b2,b3)" in clauses
    assert "AND(b1,not_b2)" in clauses
    assert "NOT(b3)" in clauses

def test_logic_clear():
    """测试约束列表清空功能"""
    builder = LogicConstraintBuilder()
    builder.add_or("a", "b")
    builder.clear()
    assert len(builder.get_clauses()) == 0

def test_mso_no_placeholder():
    """测试MSO功能已实现为真实方法，不再抛出异常"""
    builder = LogicConstraintBuilder()
    # 新方法应该正常工作
    builder.mso_for_all("v", "p(v)")
    builder.mso_exists("v", "q(v)")
    builder.mso_no_adjacent(["x0", "x1", "x2"])
    builder.mso_subset_at_least_one(["x0", "x1"])
    
    # 验证MSO约束已生成
    mso = builder.get_mso_constraints()
    assert len(mso) == 5
    assert "∀ v: p(v)" in mso
    assert "∃ v: q(v)" in mso
    assert any("NO_ADJACENT" in s for s in mso)
    assert any("EXISTS_ONE_IN_SET" in s for s in mso)
    
    # clear 应同时清除一阶和MSO约束
    builder.clear()
    assert len(builder.get_clauses()) == 0
    assert len(builder.get_mso_constraints()) == 0

def test_mso_builder_and_translate():
    from logic_opt_kit.core.logic_solver import (
        LogicConstraintBuilder, build_mso_location_constraint
    )
    vars_list = ["x0","x1","x2"]
    res = build_mso_location_constraint(vars_list)
    mso_lines = res["mso_constraints"]
    assert len(mso_lines) > 0
    # 检查邻接约束生成
    assert any("NO_ADJACENT(x0,x1)" in s for s in mso_lines)
    assert any("EXISTS_ONE_IN_SET" in s for s in mso_lines)

    builder = LogicConstraintBuilder()
    builder.mso_exists("s", "p(s)")
    builder.mso_for_all("s", "q(s)")
    assert "∃ s: p(s)" in builder.get_mso_constraints()
    assert "∀ s: q(s)" in builder.get_mso_constraints()

def test_mso_grid_graph_builder():
    from logic_opt_kit.core.mso_graph import MSOGridGraphBuilder
    g = MSOGridGraphBuilder(height=3, width=3)
    assert g.num_vertex ==9
    seed = [g.coord2vid[(1,1)]]
    g.mso_no_isolated_vertex("S")
    g.mso_seed_must_in_subset(seed, "S")
    spec = g.get_mso_spec()
    assert len(spec)>=2
    assert "MSO‑NO_ISOLATED" in spec[0]

