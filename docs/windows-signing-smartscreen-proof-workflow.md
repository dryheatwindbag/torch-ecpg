# Windows Signing SmartScreen Proof Workflow

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `911860b211a02abbdb9845d8d590f05970b0a774`

Classification: workflow scaffold / Windows signing proof / SmartScreen
evidence planning

Scope: add a manual proof workflow for the signed-zip Windows x64 CPU bundle
path. The workflow downloads an existing Windows CPU zip artifact, verifies the
unsigned checksum, inventories signable content, can run Defender scan evidence,
and can sign and repackage the bundle only when explicitly run with signing
secrets.

This workflow does not run automatically, does not build installers, does not
create MSI or EXE installers, does not change the existing Windows CPU bundle
workflow, does not publish release assets, and does not claim release or public
distribution readiness.

## Workflow

Workflow file:
`.github/workflows/windows-signing-smartscreen-proof.yml`

First dry-run failure evidence:
[`docs/windows-signing-smartscreen-dry-run-failure.md`](windows-signing-smartscreen-dry-run-failure.md)

First successful dry-run evidence:
[`docs/windows-signing-smartscreen-dry-run-evidence.md`](windows-signing-smartscreen-dry-run-evidence.md)

Trigger:
`workflow_dispatch`

Default mode:
`dry_run: "true"`

Dry-run mode downloads and verifies the selected source artifact, extracts it,
records signable-content inventory, runs Defender scan if available, and stops
before certificate import or signing.

Proof mode requires `dry_run: "false"` and the required secrets. It imports
the signing certificate into runner temp storage, locates `signtool.exe`, signs
inventoried executable content, verifies Authenticode signatures, runs
help-command smoke validation, regenerates a signed zip and checksum, runs a
Defender scan, records a SmartScreen boundary, and uploads proof evidence as a
workflow artifact.

## Required Inputs

- `source_run_id`: GitHub Actions run ID that produced the Windows CPU zip.
- `source_artifact_name`: source artifact name, default
  `tecpg-windows-x64-cpu`.
- `bundle_name`: top-level bundle directory and zip stem, default
  `tecpg-windows-x64-cpu`.
- `expected_unsigned_sha256`: optional expected SHA256 for the unsigned source
  zip.
- `dry_run`: `"true"` for inventory only, `"false"` for signing proof.

## Required Secret Names

Proof mode requires these repository secret names:

- `WINDOWS_CERTIFICATE_PFX_BASE64`
- `WINDOWS_CERTIFICATE_PASSWORD`
- `WINDOWS_SIGNING_TIMESTAMP_URL`

Secret values must not be committed, printed, or recorded in evidence docs.

## Proof Steps

The workflow records:

- Windows runner confirmation.
- Downloaded source artifact file list.
- Unsigned source zip SHA256.
- Optional comparison against `expected_unsigned_sha256`.
- Optional comparison against the downloaded `SHA256SUMS.txt`.
- Signable file inventory for `.exe`, `.dll`, `.pyd`, `.sys`, and `.msi`
  files.
- Script launcher inventory for `.cmd`, `.bat`, and `.ps1` files.
- Microsoft Defender scan output if `MpCmdRun.exe` is available.
- `signtool sign` execution in proof mode.
- `signtool verify /pa /v` output in proof mode.
- `Get-AuthenticodeSignature` output in proof mode.
- Help-command smoke output from the signed payload.
- Signed zip SHA256.
- SmartScreen boundary text.

## Artifact Boundaries

The workflow preserves the signed-zip direction:

- Input artifact: existing unsigned Windows x64 CPU zip.
- Signing workspace: extracted zip contents.
- Output candidate: regenerated signed zip.
- Evidence artifact: proof logs and signed candidate files uploaded to the
  workflow run only.

The workflow does not alter the existing bundle build artifact, does not upload
release assets, and does not change the public artifact format.

Checksums from the unsigned zip are not reused for signed outputs. Any signing,
timestamping, Defender scan, or repackaging step requires fresh evidence for
the selected artifact state.

## SmartScreen Boundary

SmartScreen reputation cannot be fully proven by a CI signing run alone.

Before any artifact is described as SmartScreen-trusted or public-download-ready,
record browser-download and first-launch behavior on a clean Windows x64
machine or VM. If SmartScreen warns or blocks, the artifact is not
public-distribution-ready without a separate release decision and user
communication plan.

## Not Proven By This Workflow Scaffold

- Signing works before a successful proof-mode run exists.
- Timestamping succeeded before a successful proof-mode run exists.
- SmartScreen trust.
- Defender acceptance for a signed artifact.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- macOS signing or notarization.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.
- macOS x64 / Intel support.
- Linux desktop bundle support.

## Merge Gate For Evidence Follow-Up

A future evidence PR may describe Windows signing as proven only after it
records a successful proof-mode run with:

- Source run ID and source artifact name.
- Unsigned source SHA256 verification.
- Certificate metadata that does not expose private material.
- Signed-file verification output.
- Signed-payload help-command smoke output.
- Signed zip SHA256.
- Defender scan output for the selected targets.
- Explicit SmartScreen observation boundary or clean-machine SmartScreen
  evidence.
