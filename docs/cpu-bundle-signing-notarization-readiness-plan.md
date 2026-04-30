# CPU Bundle Signing And Notarization Readiness Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `b49fd8705b6c229b531fa29fcf1ebb35828c6e62`

Classification: docs / packaging readiness / signing and notarization plan

Scope: define the evidence gates required before the staged Windows x64 and
macOS arm64 CPU bundle artifacts can be described as signed, notarized,
antivirus-validated, or public-release-ready.

This plan does not sign binaries, notarize macOS artifacts, submit Windows
artifacts for reputation checks, publish release downloads, change workflows,
change packaging scripts, or claim release readiness.

## Current Evidence Baseline

The current evidence chain proves:

- Windows x64 and macOS arm64 CPU bundle artifacts were built by GitHub Actions.
- Source artifacts were downloaded and SHA256 verified.
- Assets were uploaded to a draft prerelease staging surface.
- Assets were downloaded back from the draft release and SHA256 verified.

This evidence chain does not prove signing, notarization, quarantine behavior,
Windows SmartScreen trust, antivirus acceptance, public distribution readiness,
GPU/CUDA support, scientific correctness, real-data execution, or performance.

## macOS Signing Gate

Before any macOS CPU bundle is described as signed, record:

- Apple Developer Program account owner.
- Team ID.
- Certificate type selected for the distribution format.
- Signing identity fingerprint.
- Exact artifact layout being signed.
- List of executables, dynamic libraries, launchers, and embedded Python files
  that require signatures.
- Whether ad-hoc signatures are present before signing.
- Whether hardened runtime is required.
- Entitlements file, if any.
- Exact `codesign` commands.
- `codesign --verify --strict --deep --verbose=4` output.
- `codesign --display --verbose=4` output for the final artifact or signed
  executable set.

The evidence must identify whether the staged object remains a zip archive or
is repackaged into an app bundle, pkg installer, dmg, or another distribution
format.

## macOS Notarization Gate

Before any macOS CPU bundle is described as notarized, record:

- Artifact format submitted for notarization.
- Apple notarization tool and version.
- Submission command.
- Notarization request ID.
- Notarization status output.
- Notarization log, including warnings.
- Stapling command and result, if the chosen format supports stapling.
- `spctl` assessment output after notarization.

If the selected artifact format cannot be stapled, the release notes must say
how notarization is validated and what users should expect after download.

## macOS Quarantine Gate

Before any macOS CPU bundle is described as public-download-ready, record a
download-path validation on a clean macOS arm64 machine or VM:

- Download source.
- Browser or command-line download method.
- `xattr -l` output showing quarantine attributes after download, if present.
- First-run behavior from Terminal.
- First-run behavior from Finder, if the chosen layout supports Finder launch.
- Gatekeeper result.
- Any warning dialogs or blocking behavior.
- User steps required to run the artifact.

If users must manually remove quarantine attributes or bypass Gatekeeper, the
artifact is not ready for a public release without an explicit release decision.

## Windows Signing Gate

Before any Windows CPU bundle is described as signed, record:

- Code signing certificate owner.
- Certificate type and issuer.
- Signing tool and version.
- Timestamp server.
- Files signed, including launcher scripts or executable wrappers if
  applicable.
- Exact signing commands.
- Signature verification commands.
- Verification output after downloading the staged artifact.

If the final distribution remains a zip containing unsigned scripts and an
embedded Python runtime, release notes must not imply that the full extracted
bundle is signed.

## Windows SmartScreen And Antivirus Gate

Before any Windows CPU bundle is described as public-download-ready, record
validation on a clean Windows x64 machine or VM:

- Download source.
- Browser or command-line download method.
- Windows SmartScreen behavior for the downloaded artifact.
- Microsoft Defender scan command and output.
- First-run behavior after extracting the zip.
- Any warnings, blocks, or reputation prompts.
- Any additional antivirus or reputation service required by release policy.

If SmartScreen or antivirus blocks or warns on the artifact, the artifact is not
ready for public distribution without an explicit release decision and user
communication plan.

## Release Notes Gate

Before publishing release notes or a download page, review the exact text
against these boundaries:

- Do not claim release readiness until signing, notarization, quarantine,
  SmartScreen, and antivirus gates pass.
- Do not claim GPU/CUDA support for CPU bundle artifacts.
- Do not claim scientific correctness or real-data execution from help-command
  smoke tests.
- Do not claim macOS x64 / Intel or Linux desktop bundle support unless those
  platforms have separate artifact evidence.
- Do not imply the draft prerelease staging URL is a public download surface.

## Minimum Follow-Up PRs

The release-readiness closure should proceed in small evidence PRs:

1. macOS signing evidence.
2. macOS notarization and quarantine evidence.
3. Windows signing evidence.
4. Windows SmartScreen and antivirus evidence.
5. Final release-note boundary review.

Each PR should remain evidence-only unless a separate implementation decision
gate approves workflow or packaging changes.

## Not Proven By This Plan

- Release readiness.
- Public distribution readiness.
- Signed binaries.
- macOS notarization.
- macOS quarantine or Gatekeeper acceptance.
- Windows SmartScreen trust.
- Windows antivirus acceptance.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.

## Next Safest Action

Start with macOS signing evidence if the priority is public macOS distribution.
Start with Windows signing evidence if the priority is public Windows
distribution. Do not publish release downloads until the relevant platform
gates have passed and are recorded.
