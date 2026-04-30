# Windows Bundled Python Scaffold

Target artifact: `tecpg-windows-x64-cpu.zip`.

This scaffold is for a Windows x64 CPU-first bundle that includes Python. End
users should be able to unzip the artifact and run the included launcher
without installing Python manually.

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
