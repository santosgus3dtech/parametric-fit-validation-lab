from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FitSpec:
    insert_diameter_mm: float
    insert_height_mm: float
    cavity_diameter_mm: float
    holder_outer_diameter_mm: float
    holder_height_mm: float
    minimum_wall_mm: float = 1.2

    def validate(self) -> None:
        values = asdict(self)
        if any(value <= 0 for value in values.values()):
            raise ValueError("All dimensions must be positive")
        if self.holder_outer_diameter_mm <= self.cavity_diameter_mm:
            raise ValueError("Holder outer diameter must exceed cavity diameter")
        wall = (self.holder_outer_diameter_mm - self.cavity_diameter_mm) / 2
        if wall < self.minimum_wall_mm:
            raise ValueError(f"Wall thickness {wall:.2f} mm is below the minimum")


@dataclass(frozen=True)
class FitResult:
    diametral_clearance_mm: float
    radial_clearance_mm: float
    wall_thickness_mm: float
    axial_clearance_mm: float
    fit_class: str
    collision: bool
    printable: bool

    def as_dict(self) -> dict[str, float | str | bool]:
        return asdict(self)


def analyze_fit(spec: FitSpec) -> FitResult:
    spec.validate()
    diametral = spec.cavity_diameter_mm - spec.insert_diameter_mm
    radial = diametral / 2
    wall = (spec.holder_outer_diameter_mm - spec.cavity_diameter_mm) / 2
    axial = spec.holder_height_mm - spec.insert_height_mm
    if diametral < 0:
        fit_class = "interference"
    elif diametral < 0.20:
        fit_class = "press"
    elif diametral <= 0.50:
        fit_class = "close"
    else:
        fit_class = "free"
    collision = diametral < 0 or axial < 0
    return FitResult(
        diametral_clearance_mm=round(diametral, 3),
        radial_clearance_mm=round(radial, 3),
        wall_thickness_mm=round(wall, 3),
        axial_clearance_mm=round(axial, 3),
        fit_class=fit_class,
        collision=collision,
        printable=not collision and wall >= spec.minimum_wall_mm,
    )
