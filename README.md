# ZDEM Area Conservation

**Area conservation / triangulation analysis for ZDEM color groups**

[English](README.md) | [中文](README.zh-CN.md)

![CI](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

Batch tools for **area conservation** checks on ZDEM particle packs: read `.dat` frames (`zdemio`), build triangulations for selected **color#** groups, plot meshes, and summarize area trends.

Full experiment dumps under `data/`, `data1/`, `figures/` stay **local-only** (gitignored). CI uses tiny synthetic frames in `samples/`.

## Why this exists

Salt / granular papers need evidence that tracked regions conserve area under deformation. Automating triangulation + stats beats ad-hoc MATLAB leftovers.

## Features

- `Area_Conservation.py` — main analysis entry (getopt CLI)
- `zdemio` / `zdemplot` IO and plotting helpers
- Figure scripts `fig*.py` for paper-style panels
- `samples/` mini `.dat` for tests without multi-GB dumps

## Install

```bash
git clone https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation.git
cd ZDEM_Area_Conservation
pip install -r requirements.txt
```

## Usage

```bash
python Area_Conservation.py --help
# point at a directory of all_*.dat frames; see script options for color filters
```

Sample parse test:

```bash
pytest tests/test_samples_dat.py tests/test_zdemio.py
```

## Data policy

| Path | In git? |
|------|---------|
| `samples/` | Yes (tiny synthetic) |
| `data/`, `data1/`, `figures/` | No — local only |

## Related ZDEM tools

| Repo | Role |
|------|------|
| [ZDEM_ParticleTracker](https://github.com/Phoenix0531-sudo/ZDEM_ParticleTracker) | Interactive particle tracking + VisPy true-radius render |
| [ZDEM_Salt_Kinematics](https://github.com/Phoenix0531-sudo/ZDEM_Salt_Kinematics) | Salt geometry / kinematics extraction & plots |
| [ZDEM_Area_Conservation](https://github.com/Phoenix0531-sudo/ZDEM_Area_Conservation) | Area-conservation / triangulation analysis |
| [ZDEM_Bond_Fracture](https://github.com/Phoenix0531-sudo/ZDEM_Bond_Fracture) | Bond damage series + desktop / CLI |
| [ZDEM_Damage_Thresholds](https://github.com/Phoenix0531-sudo/ZDEM_Damage_Thresholds) | Damage thresholds & strain–energy plots |
| [ZDEM_DFN](https://github.com/Phoenix0531-sudo/ZDEM_DFN) | Discrete fracture network generator for ZDEM |
| [ZDEM_Model_Editor](https://github.com/Phoenix0531-sudo/ZDEM_Model_Editor) | Model file visual editor |
| [ZDEM_Archiver](https://github.com/Phoenix0531-sudo/ZDEM_Archiver) | Purge / archive bulky simulation dumps |
| [ZDEM3D_WEB](https://github.com/Phoenix0531-sudo/ZDEM3D_WEB) | CAE cloud UI (Django + React + VTK.js) |
## License

MIT. Free for commercial use with attribution. See [LICENSE](LICENSE).
