from __future__ import annotations

import html
import json
from pathlib import Path

from .model import FitResult, FitSpec


def write_report(path: Path, spec: FitSpec, result: FitResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"spec": spec.__dict__, "result": result.as_dict()}, indent=2), encoding="utf-8")


def write_cross_section_svg(path: Path, spec: FitSpec, result: FitResult) -> None:
    scale = 9
    center_x = 315
    base_y = 360
    outer_w = spec.holder_outer_diameter_mm * scale
    cavity_w = spec.cavity_diameter_mm * scale
    insert_w = spec.insert_diameter_mm * scale
    holder_h = spec.holder_height_mm * scale
    insert_h = spec.insert_height_mm * scale
    outer_x = center_x - outer_w / 2
    cavity_x = center_x - cavity_w / 2
    insert_x = center_x - insert_w / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="470" viewBox="0 0 900 470">
<rect width="900" height="470" fill="#f5f7f8"/>
<text x="42" y="48" font-family="Arial" font-size="24" font-weight="700" fill="#172027">Parametric fit validation</text>
<text x="42" y="74" font-family="Arial" font-size="13" fill="#61707a">Generated from examples/close-fit.json</text>
<rect x="{outer_x:.1f}" y="{base_y-holder_h:.1f}" width="{outer_w:.1f}" height="{holder_h:.1f}" fill="#285a73"/>
<rect x="{cavity_x:.1f}" y="{base_y-holder_h:.1f}" width="{cavity_w:.1f}" height="{holder_h+2:.1f}" fill="#f5f7f8"/>
<rect x="{insert_x:.1f}" y="{base_y-insert_h:.1f}" width="{insert_w:.1f}" height="{insert_h:.1f}" fill="#eaa94f" stroke="#a86612" stroke-width="2"/>
<line x1="{insert_x:.1f}" y1="390" x2="{insert_x+insert_w:.1f}" y2="390" stroke="#384850"/>
<text x="{center_x:.1f}" y="412" text-anchor="middle" font-family="Arial" font-size="12" fill="#384850">Insert {spec.insert_diameter_mm:.2f} mm</text>
<line x1="{outer_x:.1f}" y1="430" x2="{outer_x+outer_w:.1f}" y2="430" stroke="#384850"/>
<text x="{center_x:.1f}" y="450" text-anchor="middle" font-family="Arial" font-size="12" fill="#384850">Holder {spec.holder_outer_diameter_mm:.2f} mm</text>
<g transform="translate(570 126)">
  <rect width="280" height="238" fill="#fff" stroke="#d8e0e4"/>
  <text x="20" y="34" font-family="Arial" font-size="12" fill="#687781">FIT CLASS</text>
  <text x="20" y="70" font-family="Arial" font-size="28" font-weight="700" fill="#1b6b55">{html.escape(result.fit_class.upper())}</text>
  <text x="20" y="112" font-family="Arial" font-size="12" fill="#687781">Diametral clearance</text><text x="250" y="112" text-anchor="end" font-family="Arial" font-size="14" font-weight="700" fill="#172027">{result.diametral_clearance_mm:.3f} mm</text>
  <text x="20" y="145" font-family="Arial" font-size="12" fill="#687781">Wall thickness</text><text x="250" y="145" text-anchor="end" font-family="Arial" font-size="14" font-weight="700" fill="#172027">{result.wall_thickness_mm:.3f} mm</text>
  <text x="20" y="178" font-family="Arial" font-size="12" fill="#687781">Axial clearance</text><text x="250" y="178" text-anchor="end" font-family="Arial" font-size="14" font-weight="700" fill="#172027">{result.axial_clearance_mm:.3f} mm</text>
  <rect x="20" y="200" width="230" height="24" fill="{'#e4f4ed' if result.printable else '#f7e5e5'}"/><text x="135" y="217" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="{'#24674d' if result.printable else '#9b3f45'}">{'PRINTABLE / NO COLLISION' if result.printable else 'REVIEW REQUIRED'}</text>
</g></svg>'''
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
