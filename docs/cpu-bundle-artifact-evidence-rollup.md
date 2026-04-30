# CPU Bundle Artifact Evidence Rollup

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `fb08b6fce01765d63c2ab3fccd4fa1faa6be475f`

Classification: docs / packaging evidence / dashboard / signoff

Scope: summarize the current bundled-Python CPU artifact evidence for Windows
x64 and macOS arm64.

Retention plan:
[`docs/cpu-bundle-artifact-retention-plan.md`](cpu-bundle-artifact-retention-plan.md)

This rollup does not claim release readiness, public distribution readiness,
signing/notarization/quarantine behavior, Windows antivirus behavior, GPU/CUDA
support, scientific correctness, real-data execution, long-running workload
behavior, macOS x64 / Intel support, or Linux desktop bundle support.

## Evidence Dashboard

| Platform artifact | Evidence PR | Workflow run | Artifact ID | Zip | SHA256 | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Windows x64 CPU bundled-Python smoke artifact | #23 | `25173165547` | `6733486097` | `tecpg-windows-x64-cpu.zip` | `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd` | Proven |
| macOS arm64 CPU bundled-Python smoke artifact | #27 | `25176627794` | `6734952276` | `tecpg-macos-arm64-cpu.zip` | `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a` | Proven |

## Windows x64 CPU Evidence

- Evidence PR: #23
- Workflow run: `25173165547`
- Artifact: `tecpg-windows-x64-cpu`
- Artifact ID: `6733486097`
- Zip: `tecpg-windows-x64-cpu.zip`
- SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`

Proven:

- The artifact was produced.
- The checksum matched the downloaded zip.
- `tecpg` imported from bundled Python `site-packages`.
- The Torch CPU-only result was recorded.
- Help-command smoke tests passed outside the repository workspace.

## macOS arm64 CPU Evidence

- Evidence PR: #27
- Workflow run: `25176627794`
- Artifact: `tecpg-macos-arm64-cpu`
- Artifact ID: `6734952276`
- Zip: `tecpg-macos-arm64-cpu.zip`
- SHA256:
  `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a`

Proven:

- The artifact was produced.
- The checksum matched the downloaded zip.
- The runner architecture was `arm64`.
- `tecpg` imported from bundled Python `site-packages`.
- The Torch CPU-only result was recorded.
- Help-command smoke tests passed outside the repository workspace.

## Cross-Platform Proven Status

- Windows x64 CPU bundled-Python smoke artifact: proven.
- macOS arm64 CPU bundled-Python smoke artifact: proven.

## Not Proven

- Release readiness.
- Public distribution readiness.
- Signing/notarization/quarantine behavior.
- Windows antivirus behavior.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Long-running workload behavior.
- macOS x64 / Intel support unless separately validated.
- Linux desktop bundle unless separately validated.

## Next Safest Options

Option A: Add macOS x64 CPU bundle workflow/evidence if Intel Mac support is
required.

Option B: Add release retention/download procedure and durable storage plan for
Windows and macOS artifacts.

Option C: Add signing/notarization/antivirus risk plan before public
distribution.

Recommended next step:

- Option B first if the goal is reliable download handoff.
- Option C first if the goal is public release readiness.
- Option A first only if Intel Mac support is a requirement.
