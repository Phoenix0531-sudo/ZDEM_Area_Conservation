# ZDEM Area Conservation

**Particle-subset area conservation for ZDEM — Delaunay / matplotlib triangulation, color# filtering, paper figure scripts, sample-first CI.**

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml/badge.svg)](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Batch analysis of ZDEM `.dat` frames: select particles by **color group**, build a triangular mesh, track **area statistics** under deformation. Automates what used to be ad-hoc MATLAB leftovers.

## Preview

![ZDEM Area Conservation](docs/screenshots/preview.png)

## Main entry

`Area_Conservation.py` (getopt CLI):

- Reads ZDEM dumps through `zdemio` / plots via `zdemplot`
- Builds triangulation (`matplotlib.tri.Triangulation` / `scipy.spatial.Delaunay`)
- Filters by color# / group conventions used in lab packs
- Writes mesh figures + area trend stats
- Uses `Agg` backend for headless figure export
- Auto-detects Chinese fonts for paper labels when available

Supporting figure scripts: `fig1_*.py` … `fig8_areatrend.py` for algorithm flow, benchmarks, complex models, filtering, area trends.

## Samples vs personal data

| Path | Purpose |
|------|---------|
| `samples/*.dat` | Tiny frames for CI (`all_0000001000.dat`, …) |
| `data/`, `data1/`, full `figures/` | **Local only** — do not force-push multi-GB dumps |

## Install

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation.git
cd ZDEM_Area_Conservation
pip install -r requirements.txt
# or uv sync
```

Python **>= 3.10**. Deps: numpy, scipy, matplotlib.

## Run

```bash
python Area_Conservation.py --help
pytest tests/
```

Point CLI flags at `samples/` first; keep personal campaign data outside git.

## Related

ParticleTracker · Salt Kinematics · Bond Fracture · DFN · Model Editor · Archiver

## Scope

- **In:** color-subset meshes, area conservation stats, paper figure generators, sample CI
- **Out:** interactive VisPy viewer (ParticleTracker), cloud storage of full simulations

## License

MIT. See [LICENSE](LICENSE).
