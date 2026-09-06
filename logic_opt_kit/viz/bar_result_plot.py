"""
plot_solution_bar：解的柱状对比图
"""
import matplotlib.pyplot as plt

def plot_solution_bar(var_names: list[str], values: list[float], save_path: str):
    plt.figure(figsize=(7, 4))
    plt.bar(var_names, values)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
