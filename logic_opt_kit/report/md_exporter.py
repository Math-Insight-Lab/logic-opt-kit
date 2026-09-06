"""
md_exporter.py 导出Markdown建模报告
"""
from typing import Dict, Any

def export_markdown_report(out_path: str, model_name: str, solve_info: Dict[str, Any], solution: Dict[str, float], obj_val: float):
    lines = []
    lines.append(f"# {model_name} — Optimization Report")
    lines.append("## Solver Info")
    for k, v in solve_info.items():
        lines.append(f"- {k}: {v}")
    lines.append("\n## Objective value")
    lines.append(f"{obj_val:.6g}")
    lines.append("\n## Variable Solution")
    for name, val in solution.items():
        lines.append(f"- **{name}** = {val:.6g}")
    content = "\n".join(lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
