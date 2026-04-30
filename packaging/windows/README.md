# Windows Bundled Python Scaffold

Target artifact: `tecpg-windows-x64-cpu.zip`.

This scaffold is for a Windows x64 CPU-first bundle that includes Python. End
users should be able to unzip the artifact and run the included launcher
without installing Python manually.

The manual GitHub Actions workflow is `.github/workflows/windows-cpu-bundle.yml`.
It builds the bundle on `windows-latest`, runs
`packaging/common/smoke_test.py` against the unpacked launcher, generates
`SHA256SUMS.txt`, and uploads the zip plus checksum artifacts.

Planned bundle requirements:

- Bundled Windows x64 Python runtime.
- Installed `tecpg` package from this repository.
- CPU dependency set, including the CPU-appropriate PyTorch wheel.
- Windows launcher that resolves the bundled Python.
- Bundle README and license notices.
- `packaging/common/smoke_test.py`.
- `SHA256SUMS.txt` for the zip artifact.

Required post-package smoke commands:

```bat
tecpg --help
tecpg data --help
tecpg run mlr --help
```

GPU/CUDA validation is intentionally out of scope for this CPU bundle.
