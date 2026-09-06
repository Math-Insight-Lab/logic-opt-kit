"""
Markdown/LaTeX报告导出单元测试
覆盖：文件生成、内容合法性、临时文件自动清理
"""
import os
import tempfile
from logic_opt_kit.report import export_markdown_report, export_latex_report

# 测试模拟数据
TEST_SOLVE_INFO = {"solver": "highs-python", "version": "0.1.0"}
TEST_SOLUTION = {"x1": 4.0, "x2": 4.0}
TEST_OBJ_VAL = 20.0

def test_markdown_export():
    """测试Markdown报告正常生成"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md", encoding="utf-8") as f:
        md_path = f.name

    export_markdown_report(
        out_path=md_path,
        model_name="test_model",
        solve_info=TEST_SOLVE_INFO,
        solution=TEST_SOLUTION,
        obj_val=TEST_OBJ_VAL
    )

    # 校验文件存在且内容完整
    assert os.path.exists(md_path)
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "test_model" in content
    assert "x1" in content
    assert "4" in content
    assert "20" in content

    os.unlink(md_path)

def test_latex_export():
    """测试LaTeX报告正常生成"""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tex", encoding="utf-8") as f:
        tex_path = f.name

    export_latex_report(
        out_path=tex_path,
        model_name="test_model",
        solve_info=TEST_SOLVE_INFO,
        solution=TEST_SOLUTION,
        obj_val=TEST_OBJ_VAL
    )

    assert os.path.exists(tex_path)
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert r"\documentclass{article}" in content
    assert r"\section{test_model Optimization Report}" in content

    os.unlink(tex_path)
