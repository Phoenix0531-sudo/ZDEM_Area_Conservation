# Samples (CI / demo only)

Tiny synthetic ZDEM-like `.dat` frames used by unit tests and quick demos.

| File | Role |
|------|------|
| `all_0000001000.dat` | 3 balls + 1 wall, step 1000 |
| `all_0000002000.dat` | same layout shifted, step 2000 |

## Full experiment data (not in git)

Local heavy dirs are **gitignored**:

- `data/` — local ZDEM exports and analysis figures

The current CLI writes intermediate particle files and area plots to the project-root `data/` even when `--dir` specifies another directory. Use `data/` for the complete workflow and preserve original data separately; see the main README for details.

Do **not** commit full simulation outputs. The files in `samples/` are synthetic fixtures.
