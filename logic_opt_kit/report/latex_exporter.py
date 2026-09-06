"""
latex_exporter.py LaTeX报告导出
"""
from typing import Dict, Any

def export_latex_report(out_path: str, model_name: str, solve_info: Dict[str, Any], solution: Dict[str, float], obj_val: float):
    lines = []
    lines.append(r"\documentclass{article}")
    lines.append(r"\usepackage{amsmath}")
    lines.append(r"\begin{document}")
    lines.append(f"\\section{{{model_name} Optimization Report}}")
    lines.append(r"\subsection{Solver Info}")
    lines.append(r"\begin{itemize}")
    for k, v in solve_info.items():
        lines.append(f"\\item {k}: {v}")
    lines.append(r"\end{itemize}")
    lines.append(f"\nObjective value: ${obj_val:.6g}$")
    lines.append(r"\subsection{Solution}")
    lines.append(r"\begin{itemize}")
    for name, val in solution.items():
        lines.append(f"\\item ${name} = {val:.6g}$")
    lines.append(r"\end{itemize}")
    lines.append(r"\end{document}")
    content = "\n".join(lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
