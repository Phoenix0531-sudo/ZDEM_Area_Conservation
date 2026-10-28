"""Numerical checks for particle triangulation and data precision."""
import numpy as np
import pytest

import Area_Conservation as area
import area_geometry


def test_square_area_and_edge_threshold():
    coords = np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]])
    radii = np.ones((4, 1))
    tri = area_geometry.create_triangulation(coords)
    kept = area.filter_triangles(tri, coords, radii, 2.0)
    assert area.calculate_triangle_areas(kept, coords) == pytest.approx(1.0)
    with pytest.warns(UserWarning):
        assert area.filter_triangles(tri, coords, radii, 1.0) is None


def test_collinear_points_and_duplicate_points_do_not_produce_mesh():
    collinear = np.array([[0., 0.], [1., 0.], [2., 0.]])
    assert area.create_triangulation(collinear) is None
    duplicate = np.array([[0., 0.], [0., 0.], [1., 1.]])
    with pytest.warns(UserWarning):
        assert area.create_triangulation(duplicate) is None


def test_particle_text_preserves_precision(tmp_path, monkeypatch):
    monkeypatch.setattr(area, 'DEFAULT_DATA_DIR', str(tmp_path))
    coords = np.array([[1.23456789, 2.34567891]])
    radii = np.array([[0.12345678]])
    area.export_particles_txt(coords, radii, np.array([[7]]), 'frame.dat')
    actual_coords, actual_radii, colors = area.read_surface_particles(tmp_path / 'frame_particles.txt')
    assert actual_coords[0, 0] == pytest.approx(coords[0, 0], abs=1e-6)
    assert actual_radii[0, 0] == pytest.approx(radii[0, 0], abs=1e-6)
    assert colors[0, 0] == 7
