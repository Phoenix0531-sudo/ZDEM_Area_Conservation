# Samples (CI / demo only)

Tiny synthetic ZDEM-like `.dat` frames used by unit tests and quick demos.

| File | Role |
|------|------|
| `all_0000001000.dat` | 3 balls + 1 wall, step 1000 |
| `all_0000002000.dat` | same layout shifted, step 2000 |

## Local simulation data (not in Git)

Local heavy dirs are **gitignored**:

- `data/` — local ZDEM exports and analysis figures

Run the sample with `python Area_Conservation.py --dir=samples --output-dir=results --threshold=10`. The output directory must be new; see the main README for details.

Do **not** commit full simulation outputs. The files in `samples/` are synthetic fixtures.
