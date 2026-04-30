# Windows CPU Bundle Artifact Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `dev`

Base commit: `a0ef5402c207e16e461a5becff0674dce78d9779`

Classification: workflow / packaging / validation evidence

Scope: record the first successful Windows x64 CPU bundled-Python artifact
validation after the Windows bundle workflow validation gates were hardened.

This evidence does not claim release readiness, GPU/CUDA support, macOS bundle
support, scientific correctness, real-data execution, signing/notarization, or
public distribution readiness.

## Workflow Run

- Workflow: `Windows CPU Bundle`
- Trigger: `workflow_dispatch`
- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25173165547`
- Run result: `success`
- Branch under test: `codex/windows-bundle-validation-fix`
- Commit under test: `46ed1b08b44ab53f739f787bff09c8349a2c5fb5`
- Job: `Windows x64 CPU bundle`
- Job result: `success`

## Artifact

- Artifact name: `tecpg-windows-x64-cpu`
- Artifact ID: `6733486097`
- Artifact size: `404105998` bytes
- Zip name: `tecpg-windows-x64-cpu.zip`

`SHA256SUMS.txt` contents:

```text
19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd  tecpg-windows-x64-cpu.zip
```

The uploaded artifact was downloaded after the run. The downloaded
`tecpg-windows-x64-cpu.zip` SHA256 matched `SHA256SUMS.txt`.

The downloaded zip contained `tecpg` under the bundled Python environment,
including:

```text
tecpg-windows-x64-cpu/python/Lib/site-packages/tecpg/__init__.py
tecpg-windows-x64-cpu/python/Lib/site-packages/tecpg/__main__.py
tecpg-windows-x64-cpu/python/Lib/site-packages/tecpg/cli.py
```

## Validation Gates

PowerShell syntax parse:

```text
ps1 parse ok
```

Bundled `tecpg` import path printed by the workflow:

```text
D:\a\torch-ecpg\torch-ecpg\build\windows-cpu-bundle\tecpg-windows-x64-cpu\python\Lib\site-packages\tecpg\__init__.py
```

CPU-only Torch check:

```text
2.11.0+cpu False
```

The `False` value is the result of `torch.cuda.is_available()` in the bundled
Python runtime.

Bundle checksum verification:

```text
SHA256 verified for tecpg-windows-x64-cpu.zip
```

Bundle output check:

```text
19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd  tecpg-windows-x64-cpu.zip
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
Passed: ...\launchers\tecpg.cmd --help
Passed: ...\launchers\tecpg.cmd data --help
Passed: ...\launchers\tecpg.cmd run mlr --help
```

## Proven

- The default-branch workflow exposure allowed `workflow_dispatch` to run a
  Windows bundle workflow against a non-default branch.
- The Windows runner parsed the PowerShell build script.
- The Windows bundle build completed after native command failures were made
  fatal.
- The local `tecpg` package installed into the bundled Python environment.
- The bundled `tecpg` import resolved from `python/Lib/site-packages`, not the
  source checkout.
- The installed Torch wheel was CPU-only for this artifact validation run.
- The workflow produced `tecpg-windows-x64-cpu.zip` and `SHA256SUMS.txt`.
- `SHA256SUMS.txt` matched the downloaded zip.
- The unpacked bundle launcher passed the three required help-command smoke
  checks from outside the repository workspace.
- The artifact upload completed successfully.

## Not Proven

- Release readiness.
- GPU/CUDA support in bundled downloads.
- macOS bundle support.
- Scientific correctness.
- Real-data execution.
- Installer signing, notarization, or Windows antivirus behavior.
- Public distribution readiness.
- Long-running workload behavior from the bundle.
