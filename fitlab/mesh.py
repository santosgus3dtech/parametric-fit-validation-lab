from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

from .model import FitSpec

Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]


def _ring(radius: float, z: float, segments: int) -> list[Point]:
    return [
        (radius * math.cos(2 * math.pi * i / segments), radius * math.sin(2 * math.pi * i / segments), z)
        for i in range(segments)
    ]


def annular_holder(spec: FitSpec, segments: int = 64) -> list[Triangle]:
    spec.validate()
    outer_bottom = _ring(spec.holder_outer_diameter_mm / 2, 0, segments)
    outer_top = _ring(spec.holder_outer_diameter_mm / 2, spec.holder_height_mm, segments)
    inner_bottom = _ring(spec.cavity_diameter_mm / 2, 0, segments)
    inner_top = _ring(spec.cavity_diameter_mm / 2, spec.holder_height_mm, segments)
    triangles: list[Triangle] = []
    for i in range(segments):
        n = (i + 1) % segments
        triangles.extend(
            [
                (outer_bottom[i], outer_bottom[n], outer_top[n]),
                (outer_bottom[i], outer_top[n], outer_top[i]),
                (inner_bottom[i], inner_top[n], inner_bottom[n]),
                (inner_bottom[i], inner_top[i], inner_top[n]),
                (outer_top[i], outer_top[n], inner_top[n]),
                (outer_top[i], inner_top[n], inner_top[i]),
                (outer_bottom[i], inner_bottom[n], outer_bottom[n]),
                (outer_bottom[i], inner_bottom[i], inner_bottom[n]),
            ]
        )
    return triangles


def solid_insert(spec: FitSpec, segments: int = 64) -> list[Triangle]:
    bottom = _ring(spec.insert_diameter_mm / 2, 0, segments)
    top = _ring(spec.insert_diameter_mm / 2, spec.insert_height_mm, segments)
    bottom_center = (0.0, 0.0, 0.0)
    top_center = (0.0, 0.0, spec.insert_height_mm)
    triangles: list[Triangle] = []
    for i in range(segments):
        n = (i + 1) % segments
        triangles.extend(
            [
                (bottom[i], bottom[n], top[n]),
                (bottom[i], top[n], top[i]),
                (bottom_center, bottom[n], bottom[i]),
                (top_center, top[i], top[n]),
            ]
        )
    return triangles


def _normal(triangle: Triangle) -> Point:
    a, b, c = triangle
    u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    cross = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    length = math.sqrt(sum(value * value for value in cross)) or 1.0
    return tuple(value / length for value in cross)  # type: ignore[return-value]


def write_ascii_stl(path: str | Path, name: str, triangles: Iterable[Triangle]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as output:
        output.write(f"solid {name}\n")
        for triangle in triangles:
            normal = _normal(triangle)
            output.write(f"  facet normal {normal[0]:.8f} {normal[1]:.8f} {normal[2]:.8f}\n    outer loop\n")
            for vertex in triangle:
                output.write(f"      vertex {vertex[0]:.8f} {vertex[1]:.8f} {vertex[2]:.8f}\n")
            output.write("    endloop\n  endfacet\n")
        output.write(f"endsolid {name}\n")


def edge_counts(triangles: Iterable[Triangle], precision: int = 6) -> dict[tuple[Point, Point], int]:
    counts: dict[tuple[Point, Point], int] = {}
    for triangle in triangles:
        rounded = [tuple(round(value, precision) for value in point) for point in triangle]
        for first, second in ((rounded[0], rounded[1]), (rounded[1], rounded[2]), (rounded[2], rounded[0])):
            edge = tuple(sorted((first, second)))
            counts[edge] = counts.get(edge, 0) + 1
    return counts


def is_watertight(triangles: Iterable[Triangle]) -> bool:
    return all(count == 2 for count in edge_counts(triangles).values())
