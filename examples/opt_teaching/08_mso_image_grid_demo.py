"""
08_mso_image_grid_demo.py
网格图像分割 MSO 一元二阶逻辑示例
模拟小尺寸图像网格(3×3像素)，用MSO描述分割掩码子集S
约束：
  1. S集合不能存在孤立像素 MSO‑NO_ISOLATED
  2. 指定种子像素必须属于S
  3. 目标：尽可能少的像素被选中（最小分割区域）
> 注意：完整MSO连通约束的MIP编码规模大，本示例演示：MSO规约生成 + 孤立点+种子约束编译求解
"""
import numpy as np
from logic_opt_kit.core.mso_graph import MSOGridGraphBuilder
from logic_opt_kit.core.solver_backend import get_solver_backend
from logic_opt_kit.core.model_builder import QuickModelBuilder


def main():
    # 3x3模拟图像网格
    H, W = 3, 3
    g = MSOGridGraphBuilder(height=H, width=W)
    seed_coords = [(1,1)]  # 中心像素作为种子点
    seed_vids = [g.coord2vid[(y,x)] for y,x in seed_coords]

    # 生成MSO高层形式规约（论文/报告输出）
    g.clear_spec()
    g.mso_no_isolated_vertex(subset_name="S")
    g.mso_seed_must_in_subset(seed_vids, subset_name="S")

    print("="*70)
    print("【图像网格 MSO 形式规约输出（图上一元二阶逻辑）】")
    print("网格尺寸：", H, "×", W)
    print("种子像素坐标：", seed_coords)
    for line in g.get_mso_spec():
        print(f"  {line}")
    print("="*70)

    # 构建MIP模型
    backend = get_solver_backend("scip")
    mb = QuickModelBuilder(backend, model_name="mso_image_seg_grid")

    # 每个顶点对应0‑1布尔变量：1表示像素属于分割子集S
    var_map = {}
    for vid in range(g.num_vertex):
        var_map[vid] = mb.var(f"vid_{vid}", low=0, high=1, vtype="B")

    # MSO约束翻译成MIP
    g.translate_no_isolated_to_mip(mb, var_map)
    g.translate_seed_to_mip(mb, var_map, seed_vids)

    # 目标：最小化选中像素数量（最小区域）
    total_select = sum(var_map[vid] for vid in range(g.num_vertex))
    mb.obj(total_select, sense="min")

    mb.solve()
    sol = mb.solution()
    obj_val = mb.obj_value()

    # 重建掩码
    mask = np.zeros((H,W), dtype=np.uint8)
    for vid, val in sol.items():
        # sol key是字符串 "vid_0"，提取数字id
        if isinstance(vid,str) and vid.startswith("vid_"):
            real_vid = int(vid.split("_")[1])
            y,x = g.vid2coord[real_vid]
            if abs(val -1.0) < 1e-6:
                mask[y,x] = 1

    print(f"\nMIP求解完成，最小选中像素数={obj_val:.0f}")
    print("\n重建分割掩码(1=属于MSO子集S):")
    print(mask)

    print("\n✅ MSO网格图像示例运行完成")


if __name__ == "__main__":
    main()

