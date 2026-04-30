# macOS Bundled Python Scaffold

Target artifacts:

- `tecpg-macos-arm64-cpu.zip`
- `tecpg-macos-x64-cpu.zip` if practical

This scaffold is for macOS CPU-first bundles that include Python. Windows and
macOS artifacts must remain separate because the Python runtime, binary wheels,
launchers, and signing behavior are platform-specific.

Planned bundle requirements:

- Bundled macOS Python runtime for the target architecture.
- Installed `tecpg` package from this repository.
- CPU dependency set, including the CPU-appropriate PyTorch wheel.
- macOS launcher that resolves the bundled Python.
- Bundle README and license notices.
- `packaging/common/smoke_test.py`.
- `SHA256SUMS.txt` for each zip artifact.

Required post-package smoke commands:

```sh
tecpg --help
tecpg data --help
tecpg run mlr --help
```

Open packaging questions:

- Whether macOS x64 is practical with available runner coverage and dependency
  wheels.
- How signing, notarization, and quarantine handling should be addressed before
  a public downloadable release.

GPU/CUDA validation is intentionally out of scope for these CPU bundles.
