"""End-to-end isolation and reproducibility checks."""
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_cli_uses_isolated_output_and_records_results(tmp_path):
    output = tmp_path / 'results'
    command = [sys.executable, str(ROOT / 'Area_Conservation.py'), '--dir=' + str(ROOT / 'samples'),
               '--output-dir=' + str(output), '--colors=all', '--threshold=10',
               '--plot-original-tri=false', '--plot-filtered-tri=false']
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    run = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, env=env)
    assert run.returncode == 0, run.stderr
    with (output / 'area_results.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert float(rows[0]['area']) > 0
    assert float(rows[1]['relative_change_percent']) == 0
    metadata = json.loads((output / 'run_metadata.json').read_text(encoding='utf-8'))
    assert metadata['threshold_factor'] == 10
    assert len(metadata['input_files']) == 2
    for item in metadata['input_files']:
        assert item['sha256'] == hashlib.sha256((ROOT / 'samples' / item['name']).read_bytes()).hexdigest()
    assert (output / 'area_trend.pdf').is_file()
    repeat = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True, env=env)
    assert repeat.returncode != 0


@pytest.mark.parametrize('option', ['--threshold=nan', '--threshold=-1', '--xmax=inf', '--plot-filtered-tri=maybe'])
def test_cli_rejects_invalid_options_before_creating_output(tmp_path, option):
    output = tmp_path / 'out'
    result = subprocess.run([sys.executable, str(ROOT / 'Area_Conservation.py'),
                             '--dir=' + str(ROOT / 'samples'), '--output-dir=' + str(output), option],
                            cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode != 0
    assert not output.exists()


@pytest.mark.parametrize('bad_value', ['-5.000000000000e+00', 'nan'])
def test_cli_rejects_invalid_particle_radius(tmp_path, bad_value):
    source = tmp_path / 'input'
    source.mkdir()
    sample = (ROOT / 'samples' / 'all_0000001000.dat').read_text(encoding='utf-8')
    sample = sample.replace('5.000000000000e+00', bad_value, 1)
    (source / 'frame_1000.dat').write_text(sample, encoding='utf-8')
    output = tmp_path / 'out'
    result = subprocess.run([sys.executable, str(ROOT / 'Area_Conservation.py'), '--dir=' + str(source),
                             '--output-dir=' + str(output), '--threshold=100'],
                            cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode != 0
    assert not (output / 'area_results.csv').exists()


def test_cli_rejects_partial_input_failure(tmp_path):
    source = tmp_path / 'input'
    source.mkdir()
    (source / 'good_1000.dat').write_bytes((ROOT / 'samples' / 'all_0000001000.dat').read_bytes())
    (source / 'bad_2000.dat').write_text('invalid', encoding='utf-8')
    result = subprocess.run([sys.executable, str(ROOT / 'Area_Conservation.py'), '--dir=' + str(source),
                             '--output-dir=' + str(tmp_path / 'out'), '--threshold=10'],
                            cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode != 0
