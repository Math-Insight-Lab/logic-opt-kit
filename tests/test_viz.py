"""
可视化模块单元测试
覆盖：柱状图、可行域绘图、图片文件生成
"""
import os
import tempfile
from logic_opt_kit.viz import plot_solution_bar, plot_lp_feasible_region

def test_bar_plot_export():
    """测试求解结果柱状图生成"""
    var_names = ["x1", "x2", "x3"]
    var_values = [2.5, 4.0, 1.8]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        img_path = f.name

    plot_solution_bar(var_names, var_values, img_path)
    assert os.path.exists(img_path)
    os.unlink(img_path)

def test_feasible_region_plot():
    """测试LP可行域绘图生成"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        img_path = f.name

    # 空约束仅测试绘图框架可用性
    plot_lp_feasible_region(
        xlim=(0, 10),
        ylim=(0, 10),
        constraints=[],
        save_path=img_path
    )

    assert os.path.exists(img_path)
    os.unlink(img_path)
