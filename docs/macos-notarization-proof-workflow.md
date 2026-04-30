# macOS Notarization Proof Workflow

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `55bc47a8ba65eb7cee7186cb25a7233a1df1e475`

Classification: workflow scaffold / macOS signing proof / notarization
evidence planning

Scope: add a manual proof workflow for the signed-zip macOS arm64 CPU bundle
path. The workflow downloads an existing macOS CPU zip artifact, verifies the
unsigned checksum, inventories signable content, and can sign, notarize, and
record evidence when explicitly run with signing secrets.

This workflow does not run automatically, does not build installers, does not
create pkg, dmg, MSI, or EXE artifacts, does not change the existing macOS CPU
bundle workflow, does not publish release assets, and does not claim release or
public distribution readiness.

## Workflow

Workflow file:
`.github/workflows/macos-notarization-proof.yml`

First dry-run evidence:
[`docs/macos-notarization-proof-dry-run-evidence.md`](macos-notarization-proof-dry-run-evidence.md)

Trigger:
`workflow_dispatch`

Default mode:
`dry_run: "true"`

Dry-run mode downloads and verifies the selected source artifact, extracts it,
and records the signable-content inventory. It does not import certificates,
sign files, submit notarization, or create a signed zip.

Proof mode requires `dry_run: "false"` and the required secrets. It signs the
Mach-O content inside the extracted zip, runs help-command smoke validation,
regenerates a signed zip and checksum, submits the signed zip to Apple
notarization, records the notarization log, records the no-staple boundary for
plain zip distribution, and uploads proof evidence as a workflow artifact.

## Required Inputs

- `source_run_id`: GitHub Actions run ID that produced the macOS CPU zip.
- `source_artifact_name`: source artifact name, default
  `tecpg-macos-arm64-cpu`.
- `bundle_name`: top-level bundle directory and zip stem, default
  `tecpg-macos-arm64-cpu`.
- `expected_unsigned_sha256`: optional expected SHA256 for the unsigned source
  zip.
- `dry_run`: `"true"` for inventory only, `"false"` for signing and
  notarization proof.

## Required Secret Names

The proof mode requires these secret names:

- `MACOS_CERTIFICATE_P12_BASE64`
- `MACOS_CERTIFICATE_PASSWORD`
- `MACOS_KEYCHAIN_PASSWORD`
- `MACOS_CODESIGN_IDENTITY`
- `APPLE_ID`
- `APPLE_TEAM_ID`
- `APPLE_APP_SPECIFIC_PASSWORD`

Secret values must not be committed, printed, or recorded in evidence docs.

## Proof Steps

The workflow records:

- macOS arm64 runner confirmation.
- Downloaded source artifact file list.
- Unsigned source zip SHA256.
- Optional comparison against `expected_unsigned_sha256`.
- Optional comparison against the downloaded `SHA256SUMS.txt`.
- Mach-O files selected for signing.
- Executable non-Mach-O files, including the shell launcher.
- Codesign identity inventory.
- `codesign --verify --strict --verbose=4` output for signed Mach-O files.
- `codesign --display --verbose=4` output for signed Mach-O files.
- Help-command smoke output from the signed payload.
- Signed zip SHA256.
- `notarytool submit --wait` output.
- `notarytool log` output.
- Explicit no-staple boundary for plain zip distribution.
- `spctl --assess --type execute --verbose=4` output for launch paths.

## Artifact Boundaries

The workflow preserves the signed-zip direction:

- Input artifact: existing unsigned macOS arm64 CPU zip.
- Signing workspace: extracted zip contents.
- Output candidate: regenerated signed zip.
- Evidence artifact: proof logs and signed candidate files uploaded to the
  workflow run only.

The workflow does not alter the existing bundle build artifact, does not upload
release assets, and does not change the public artifact format.

Checksums from the unsigned zip are not reused for signed outputs. Any signing,
notarization, stapling, or repackaging step requires a regenerated SHA256.

## Stapling Boundary

The workflow does not claim stapling for a plain zip. If the selected artifact
shape remains a zip, the evidence must explicitly state that zip stapling is
not claimed.

If a future proof introduces an app bundle, pkg, or dmg to support stapling,
that is a packaging-format change and requires a separate decision gate before
it can replace the signed-zip path.

## Not Proven By This Workflow Scaffold

- Signing works before a successful proof-mode run exists.
- Notarization succeeded before a successful proof-mode run exists.
- Stapling succeeded.
- Gatekeeper acceptance on a downloaded artifact.
- Quarantine behavior after browser download.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- Windows signing or SmartScreen trust.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.
- macOS x64 / Intel support.
- Linux desktop bundle support.

## Merge Gate For Evidence Follow-Up

A future evidence PR may describe macOS signing or notarization as proven only
after it records a successful proof-mode run with:

- Source run ID and source artifact name.
- Unsigned source SHA256 verification.
- Codesign identity metadata.
- Signed-file verification output.
- Signed-payload help-command smoke output.
- Signed zip SHA256.
- Notarization request ID, accepted status, and log.
- `spctl` assessment output.
- Explicit no-staple boundary, unless the artifact shape has changed under a
  separate approved decision gate.
