"""Smoke tests for the project entry point and supporting modules."""
from pathlib import Path
import importlib
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


PACKAGES = ['zdemio', 'zdemplot']


def test_packages_importable():
    for name in PACKAGES:
        importlib.import_module(name)


def test_entry_compiles():
    src = ROOT / 'Area_Conservation.py'
    assert src.exists()
    compile(src.read_text(encoding='utf-8', errors='replace'), str(src), 'exec')

