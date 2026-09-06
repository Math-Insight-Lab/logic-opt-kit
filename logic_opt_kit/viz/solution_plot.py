"""
plot_lp_feasible_region：二维LP可行域可视化（仅两个变量教学用）
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_lp_feasible_region(xlim: tuple[float, float], ylim: tuple[float, float], constraints, save_path: str):
    fig, ax = plt.subplots(figsize=(6, 5))
    x = np.linspace(*xlim, 200)
    # constraints原型：传入函数列表做边界绘制，教学演示骨架
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(alpha=0.3)
    plt.savefig(save_path, dpi=150)
    plt.close()
