"""Business tests for ZDEM IO helpers."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from zdemio import get_file_list, usage  # noqa: E402


def test_get_file_list_prefix_suffix(tmp_path):
    (tmp_path / "all_1.dat").write_text("a", encoding="utf-8")
    (tmp_path / "all_2.dat").write_text("b", encoding="utf-8")
    (tmp_path / "other.txt").write_text("c", encoding="utf-8")
    files = get_file_list(str(tmp_path), "all_", ".dat")
    joined = " ".join(str(x) for x in files)
    assert "all_1.dat" in joined
    assert "all_2.dat" in joined
    assert "other.txt" not in joined


def test_usage_does_not_crash(capsys):
    usage("Area_Conservation.py")
    out = capsys.readouterr().out
    assert "--dir" in out or "用法" in out
