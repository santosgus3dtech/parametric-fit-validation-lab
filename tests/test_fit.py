import pytest

from fitlab.model import FitSpec, analyze_fit


def spec(**overrides):
    values = dict(
        insert_diameter_mm=21.8,
        insert_height_mm=58.0,
        cavity_diameter_mm=22.2,
        holder_outer_diameter_mm=28.0,
        holder_height_mm=61.0,
        minimum_wall_mm=1.2,
    )
    values.update(overrides)
    return FitSpec(**values)


def test_close_fit_reports_clearances():
    result = analyze_fit(spec())
    assert result.fit_class == "close"
    assert result.diametral_clearance_mm == 0.4
    assert result.wall_thickness_mm == 2.9
    assert result.printable is True


def test_interference_is_a_collision():
    result = analyze_fit(spec(cavity_diameter_mm=21.6))
    assert result.fit_class == "interference"
    assert result.collision is True


def test_thin_wall_is_rejected():
    with pytest.raises(ValueError, match="Wall thickness"):
        analyze_fit(spec(holder_outer_diameter_mm=23.0))
