from fitlab.mesh import annular_holder, is_watertight, solid_insert
from fitlab.model import FitSpec


SPEC = FitSpec(21.8, 58.0, 22.2, 28.0, 61.0)


def test_generated_meshes_are_watertight():
    assert is_watertight(annular_holder(SPEC, segments=24))
    assert is_watertight(solid_insert(SPEC, segments=24))


def test_triangle_counts_are_stable():
    assert len(annular_holder(SPEC, segments=24)) == 192
    assert len(solid_insert(SPEC, segments=24)) == 96
