# ZDEM Area Conservation

A Python tool for estimating the area occupied by a selected subset of particles in two-dimensional ZDEM simulation frames. It constructs a Delaunay triangulation, filters long edges, and tracks the resulting area across frames.

[中文说明](README.zh-CN.md) · [License](LICENSE)

![Example visualization](docs/screenshots/preview.png)

## Method

For each ZDEM `.dat` frame, the program extracts particle coordinates, radii and color identifiers. It selects particles by color (all colors by default), constructs a Delaunay triangulation, and retains triangles whose three edge lengths are each at most `k × mean particle radius`. The reported area is the sum of retained triangle areas. The default threshold factor `k` is 3.0.

For selected particle centers $p_i$ and radii $r_i$, let $\bar r$ be their mean radius and $T_k$ the Delaunay triangles for which every edge length is at most $k\bar r$. The reported estimate is $A_k = \sum_{t\in T_k} \operatorname{area}(t)$. It represents the retained triangle area, not the sum of particle disk areas; changing the threshold or selected colors can change the result.

Areas are compared across frames ordered by the number in their filenames. The trend plot uses a normalized frame-number axis; its percentage mode reports change relative to the first valid frame. This is a numerical post-processing method, not a physical measurement or proof of conservation by itself. Coordinate units, input provenance and suitable parameters must be established for each dataset.

## Requirements and installation

Python 3.10 or later is required. Runtime dependencies are NumPy, SciPy and Matplotlib; `requirements.txt` also includes pytest for testing.

```bash
python -m pip install -r requirements.txt
python Area_Conservation.py -h
```

## Data and usage

- `samples/` contains two **synthetic**, minimal ZDEM-like frames for tests. They are not experimental evidence; see [samples/README.md](samples/README.md).
- `data/` is ignored by Git and may contain local simulation data and outputs. Preserve original data separately before running the program.

Run the synthetic example (its large particle spacing requires a threshold of 10):

```bash
python Area_Conservation.py --dir=samples --output-dir=results --colors=all --threshold=10 --plot-area-type=percentage
```

For your own data, choose the input directory, a new output directory and a threshold appropriate to the dataset.

Use `--colors=7,8` to select color identifiers, `--xmax` and `--ymax` to adjust mesh plot limits, and `--plot-area-type=raw|percentage|normalized` to choose the trend display. Run `python Area_Conservation.py -h` for the full option list. The default plot limits and axis unit labels should be checked against the dataset before publication.

**Output and safety:** the output directory must not exist, preventing accidental overwrite. It contains intermediate files in `particles/`, `area_results.csv`, `run_metadata.json` with input hashes and parameters, area trend plots and triangulation plots. Coordinates and radii are retained in double precision; coordinate units must be confirmed from the source data. A failed run may leave a partial output directory; inspect it and choose another output path when retrying.

## Validation and reproducibility

```bash
python -m pytest -q tests
```

The tests cover sample parsing, helper functions and basic imports; they do not establish scientific accuracy or validate results for a particular simulation. For reproducibility, record the source data and simulation conditions, coordinate units, selected colors, threshold factor, plot settings, Python and dependency versions, and repository revision (`git rev-parse HEAD`). The program exports an area table and some parameters; simulation conditions, units and repository revision still need to be recorded separately. Full local simulation data are not included in the repository, so the synthetic fixtures alone cannot reproduce results derived from them.

## Repository structure

| Path | Purpose |
| --- | --- |
| `Area_Conservation.py`, `area_geometry.py` | Analysis entry point and triangulation/area calculations |
| `zdemio.py`, `zdemplot.py` | ZDEM data parsing and plotting helpers |
| `samples/`, `tests/` | Synthetic fixtures and automated tests |
| `data/` | Local, Git-ignored simulation data and generated outputs |

## Citation and license

No publication or citation metadata has been established in this repository. If you use the code in research, cite an associated publication when available and record the repository revision used. The code is distributed under the [MIT License](LICENSE).
