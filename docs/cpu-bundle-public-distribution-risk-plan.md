# CPU Bundle Public Distribution Risk Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `13f236fc7e2afe82e5201b3cbcfbae33778c3e31`

Classification: docs / packaging risk / public distribution readiness plan

Scope: define the signing, notarization, quarantine, and Windows antivirus risk
gates that must be resolved before the Windows x64 and macOS arm64 CPU
bundled-Python artifacts are described as public release downloads.

This plan does not claim release readiness, public distribution readiness,
signing/notarization/quarantine success, Windows antivirus acceptance, GPU/CUDA
support, scientific correctness, real-data execution, long-running workload
behavior, macOS x64 / Intel support, or Linux desktop bundle support.

Signing and notarization readiness plan:
[`docs/cpu-bundle-signing-notarization-readiness-plan.md`](cpu-bundle-signing-notarization-readiness-plan.md)

Signed-zip implementation plan:
[`docs/cpu-bundle-signing-implementation-plan.md`](cpu-bundle-signing-implementation-plan.md)

Installer and packaging UX plan:
[`docs/cpu-bundle-installer-packaging-ux-plan.md`](cpu-bundle-installer-packaging-ux-plan.md)

## Source Evidence

Current smoke artifact evidence exists for:

- Windows x64 CPU bundled-Python artifact:
  `docs/windows-cpu-bundle-artifact-evidence.md`
- macOS arm64 CPU bundled-Python artifact:
  `docs/macos-arm64-cpu-bundle-artifact-evidence.md`
- Cross-platform rollup:
  `docs/cpu-bundle-artifact-evidence-rollup.md`
- Retention/download plan:
  `docs/cpu-bundle-artifact-retention-plan.md`

Those documents prove smoke-tested CPU bundle artifacts only. They do not prove
public distribution readiness.

## Current Blockers

The short-term packaging direction is signed zip. Installer formats remain out
of scope until a format-specific evidence PR approves a change.

macOS proof mode is currently blocked on repository secret configuration:

- Secret-readiness recheck:
  [`docs/macos-notarization-proof-mode-secret-readiness-recheck.md`](macos-notarization-proof-mode-secret-readiness-recheck.md)
- Proof-mode evidence template:
  [`docs/macos-notarization-proof-evidence-template.md`](macos-notarization-proof-evidence-template.md)

Windows Defender and SmartScreen trust are currently blocked on clean Windows
x64 machine or VM validation:

- Clean Windows validation plan:
  [`docs/windows-clean-vm-defender-smartscreen-validation-plan.md`](windows-clean-vm-defender-smartscreen-validation-plan.md)
- Clean Windows evidence template:
  [`docs/windows-clean-vm-defender-smartscreen-evidence-template.md`](windows-clean-vm-defender-smartscreen-evidence-template.md)

## macOS Signing And Notarization Gate

Before any macOS CPU bundle is offered as a public downloadable artifact,
record evidence for:

- Apple Developer Team ID and signing identity selection.
- Whether the distributed object is a zip, app bundle, package installer, or
  another layout.
- Codesigning of every executable component that requires signing, including
  launchers and embedded Python binaries where applicable.
- Hardened Runtime decision and entitlements, if required by the chosen
  distribution format.
- Notarization submission, result, and request identifier.
- Stapling result, if the selected distribution format supports stapling.
- Post-download validation on a clean macOS arm64 machine or VM.
- Gatekeeper behavior when opening or executing the downloaded artifact.
- Exact commands and logs used for `codesign`, `spctl`, notarization, and
  quarantine validation.

The macOS artifact must not be described as signed, notarized, or public-ready
until these checks have passed and the evidence is recorded.

## macOS Quarantine Gate

Before public distribution, test the preserved macOS artifact through a download
path that applies normal macOS quarantine behavior. Record:

- Download source and method.
- Quarantine extended attributes observed after download.
- First-run user experience from Finder and Terminal, as applicable.
- Whether Gatekeeper blocks, warns, or allows execution.
- Remediation steps required for users, if any.

If users must remove quarantine attributes manually or bypass Gatekeeper, the
artifact is not public-distribution-ready without an explicit release decision.

## Windows Signing And Antivirus Gate

Before any Windows CPU bundle is offered as a public downloadable artifact,
record evidence for:

- Code signing certificate source and signing identity.
- Signing scope for launchers, executable files, and installer or archive
  format if applicable.
- Timestamping configuration and verification result.
- SmartScreen behavior for the downloaded artifact.
- Microsoft Defender scan result on a clean Windows machine or VM.
- At least one additional antivirus or reputation check, if required by the
  release policy.
- First-run user experience from the downloaded zip after extraction.
- Exact commands and logs used for signing, signature verification, Defender
  scans, and first-run validation.

The Windows artifact must not be described as signed, antivirus-validated, or
public-ready until these checks have passed and the evidence is recorded.

## Release Notes Gate

Before publishing any release notes or download page, confirm the wording does
not exceed the evidence. The release text must not claim:

- GPU/CUDA support for CPU bundles.
- Scientific correctness.
- Real-data execution.
- Long-running workload validation.
- macOS x64 / Intel support.
- Linux desktop bundle support.
- Public distribution readiness before signing, notarization, quarantine, and
  antivirus gates pass.

Allowed wording before public-release gates pass should stay limited to
internal evidence, smoke testing, artifact retention, and next validation steps.

## Minimum Evidence Package

A public-distribution readiness PR should include or link:

- Artifact retention evidence for the exact zip files being promoted.
- SHA256 verification output for each promoted zip.
- macOS signing and notarization logs.
- macOS quarantine/Gatekeeper validation notes.
- Windows signing and timestamp verification logs.
- Windows Defender and antivirus/reputation validation notes.
- First-run screenshots or text logs for each supported platform.
- Final release-note wording reviewed against the boundary list above.

## Not Proven By This Plan

- Release readiness.
- Public distribution readiness.
- Signing/notarization/quarantine success.
- Windows antivirus acceptance.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Long-running workload behavior.
- macOS x64 / Intel support unless separately validated.
- Linux desktop bundle unless separately validated.

## Next Safest Options

Option A: configure the required macOS signing and notarization secret names,
rerun secret readiness, and only then dispatch macOS proof mode with
`dry_run: "false"`.

Option B: run the clean Windows x64 Defender and SmartScreen validation path on
a real clean VM or physical machine and record an evidence PR.

Option C: keep both platform trust paths parked until the missing external
resources exist.

Recommended next step:

- Option A first if public macOS distribution is the priority and Apple signing
  credentials are available.
- Option B first if public Windows distribution is the priority and a clean
  Windows validation machine is available.
- Option C if neither external prerequisite is available.
