# Samples (CI / demo only)

Tiny synthetic ZDEM-like `.dat` frames used by unit tests and quick demos.

| File | Role |
|------|------|
| `all_0000001000.dat` | 3 balls + 1 wall, step 1000 |
| `all_0000002000.dat` | same layout shifted, step 2000 |

## Full experiment data (not in git)

Local heavy dirs are **gitignored**:

- `data/`, `data1/` — full ZDEM exports (hundreds of MB)
- `figures/` — rendered PDF/SVG from paper figures

Point the CLI at your own export:

```bash
python Area_Conservation.py --dir=/path/to/your/zdem/data
```

Do **not** commit full simulation outputs. Keep demos on `samples/`.
