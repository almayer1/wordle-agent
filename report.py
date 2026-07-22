from pathlib import Path
from datetime import datetime

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

def build_table(summary: dict) -> str:
    rows = ["| metric | value |", "|---|---|"]
    for name, value in summary.items():
        if value is None or isinstance(value, int):
            rows.append(f"| {name} | {value} |")
        else:
            rows.append(f"| {name} | {value:.2f} |")
    return "\n".join(rows)

def write_table(table: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = REPORTS_DIR / f"{timestamp}.md"
    path.write_text(table)
    return path
