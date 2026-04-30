# macOS arm64 CPU Bundle Artifact Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `dev`

Base commit: `272760107549337419fb0faeb976034ce01075b0`

Classification: workflow / packaging / validation evidence

Scope: record the first successful macOS arm64 CPU bundled-Python artifact
validation after the macOS arm64 bundle workflow scaffold was added.

This evidence does not claim release readiness, GPU/CUDA support, Windows
bundle support, scientific correctness, real-data execution, signing,
notarization, quarantine behavior, antivirus behavior, or public distribution
readiness.

## Workflow Run

- Workflow: `macOS arm64 CPU Bundle`
- Trigger: `workflow_dispatch`
- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25176627794`
- Run result: `success`
- Branch under test: `dev`
- Commit under test: `272760107549337419fb0faeb976034ce01075b0`
- Job: `macOS arm64 CPU bundle`
- Job result: `success`
- Job URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25176627794/job/73810400077`
- Runner image: `macos-14-arm64`
- Python runtime: `CPython 3.11.9` under
  `/Users/runner/hostedtoolcache/Python/3.11.9/arm64`

## Artifact

- Artifact name: `tecpg-macos-arm64-cpu`
- Artifact ID: `6734952276`
- Artifact size: `333287007` bytes
- Zip name: `tecpg-macos-arm64-cpu.zip`

`SHA256SUMS.txt` contents:

```text
a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a  tecpg-macos-arm64-cpu.zip
```

The uploaded artifact was downloaded after the run. The downloaded
`tecpg-macos-arm64-cpu.zip` SHA256 matched `SHA256SUMS.txt`.

## Validation Gates

Runner architecture check:

```text
arm64
```

Shell syntax parse:

```text
shell parse ok
```

Bundled `tecpg` import path printed by the workflow:

```text
/Users/runner/work/torch-ecpg/torch-ecpg/build/macos-arm64-cpu-bundle/tecpg-macos-arm64-cpu/python/lib/python3.11/site-packages/tecpg/__init__.py
```

CPU-only Torch check:

```text
2.11.0 False
```

The `False` value is the result of `torch.cuda.is_available()` in the bundled
Python runtime.

Bundle checksum verification:

```text
SHA256 verified for tecpg-macos-arm64-cpu.zip
```

Bundle output check:

```text
a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a  tecpg-macos-arm64-cpu.zip
```

## Isolated Smoke Test

The smoke test ran from outside the repository workspace and invoked the
unpacked bundle launcher. It passed these help commands:

```text
tecpg --help
tecpg data --help
tecpg run mlr --help
```

The workflow log recorded:

```text
Passed: .../launchers/tecpg --help
Passed: .../launchers/tecpg data --help
Passed: .../launchers/tecpg run mlr --help
```

## Proven

- The default-branch workflow exposure allowed `workflow_dispatch` to run the
  macOS arm64 bundle workflow against `dev`.
- The GitHub-hosted runner image was `macos-14-arm64`.
- The runner architecture check reported `arm64`.
- The macOS runner parsed the shell build script.
- The macOS arm64 CPU bundle build completed.
- The local `tecpg` package installed into the bundled Python environment.
- The bundled `tecpg` import resolved from `python/lib/python3.11/site-packages`,
  not the source checkout.
- The installed Torch wheel reported no CUDA availability for this artifact
  validation run.
- The workflow produced `tecpg-macos-arm64-cpu.zip` and `SHA256SUMS.txt`.
- `SHA256SUMS.txt` matched the downloaded zip.
- The unpacked bundle launcher passed the three required help-command smoke
  checks from outside the repository workspace.
- The artifact upload completed successfully.

## Not Proven

- Release readiness.
- GPU/CUDA support in bundled downloads.
- Windows bundle support.
- Scientific correctness.
- Real-data execution.
- Installer signing, notarization, quarantine behavior, or antivirus behavior.
- Public distribution readiness.
- Long-running workload behavior from the bundle.
