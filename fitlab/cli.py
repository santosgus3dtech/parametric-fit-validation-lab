from __future__ import annotations

import argparse
import json
from pathlib import Path

from .mesh import annular_holder, is_watertight, solid_insert, write_ascii_stl
from .model import FitSpec, analyze_fit
from .report import write_cross_section_svg, write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate and validate a parametric cylindrical fit")
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()
    spec = FitSpec(**json.loads(args.spec.read_text(encoding="utf-8")))
    result = analyze_fit(spec)
    holder = annular_holder(spec)
    insert = solid_insert(spec)
    args.output.mkdir(parents=True, exist_ok=True)
    write_ascii_stl(args.output / "holder.stl", "parametric_holder", holder)
    write_ascii_stl(args.output / "insert.stl", "reference_insert", insert)
    write_report(args.output / "fit-report.json", spec, result)
    write_cross_section_svg(args.output / "fit-analysis.svg", spec, result)
    print(json.dumps({**result.as_dict(), "holder_watertight": is_watertight(holder), "insert_watertight": is_watertight(insert)}, indent=2))
    return 0 if result.printable and is_watertight(holder) and is_watertight(insert) else 2


if __name__ == "__main__":
    raise SystemExit(main())
