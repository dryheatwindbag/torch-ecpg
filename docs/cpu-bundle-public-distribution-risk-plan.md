# CPU Bundle Public Distribution Risk Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `9622ac49ab26456139fca5c94374cc0e820fc4a5`

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

Option A: choose the durable storage target and execute the retention handoff
for the existing Windows x64 and macOS arm64 CPU artifacts.

Option B: create a signing/notarization validation branch for macOS arm64 only,
because macOS quarantine and notarization are likely to block public downloads.

Option C: create a Windows signing and antivirus validation branch for Windows
x64 only.

Recommended next step:

- Option A first if the immediate goal is reliable internal download handoff.
- Option B first if public macOS distribution is the priority.
- Option C first if public Windows distribution is the priority.
