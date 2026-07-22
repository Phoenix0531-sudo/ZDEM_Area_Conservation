"""Parse mini samples/ .dat frames (CI-reproducible, no local data1/)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zdemio import (  # noqa: E402
    BallListStrToNumpyArray,
    WallListStrToNumpyArray,
    get_file_list,
    read_data,
)

SAMPLES = ROOT / "samples"


def test_samples_dir_has_two_frames():
    files = get_file_list(str(SAMPLES), "all_", ".dat")
    names = sorted(Path(f).name for f in files)
    assert names == ["all_0000001000.dat", "all_0000002000.dat"]


def test_read_sample_step_1000():
    path = SAMPLES / "all_0000001000.dat"
    wall, ball, _contact, _bond, step, _group = read_data(str(path))
    assert str(step) == "1000"
    assert len(ball) >= 3
    assert len(wall) >= 1
    ids, xy, rad, _color = BallListStrToNumpyArray(ball)
    assert ids.shape[0] == 3
    assert xy.shape == (3, 2)
    assert float(np.min(rad)) > 0
    wall_id, wall_pts = WallListStrToNumpyArray(wall)
    assert wall_id.shape[0] >= 1
    assert wall_pts.shape[1] == 4


def test_read_sample_step_2000_shifted():
    _w1, b1, _c1, _b1, step1, _g1 = read_data(str(SAMPLES / "all_0000001000.dat"))
    _w2, b2, _c2, _b2, step2, _g2 = read_data(str(SAMPLES / "all_0000002000.dat"))
    assert str(step1) == "1000"
    assert str(step2) == "2000"
    _, xy1, _, _ = BallListStrToNumpyArray(b1)
    _, xy2, _, _ = BallListStrToNumpyArray(b2)
    assert not np.allclose(np.asarray(xy1, dtype=float), np.asarray(xy2, dtype=float))
