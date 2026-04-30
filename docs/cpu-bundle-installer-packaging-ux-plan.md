# CPU Bundle Installer And Packaging UX Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `c18315cf36e3f1862e9d113413ba14d00c8231d9`

Classification: docs / packaging UX / release-readiness planning

Scope: define the installer and packaging user-experience decision gates for
the staged Windows x64 and macOS arm64 CPU bundle artifacts.

This plan does not change workflows, packaging scripts, runtime
implementation, Pearson lifecycle files, GPU/CUDA behavior, release automation,
or draft release assets. Installer formats are not implemented by this plan.
It does not claim release readiness.

## Current Evidence Baseline

The current staged evidence proves:

- Windows x64 CPU zip staged as draft release evidence:
  `tecpg-windows-x64-cpu.zip`.
- macOS arm64 CPU zip staged as draft release evidence:
  `tecpg-macos-arm64-cpu.zip`.
- SHA256 integrity was preserved across GitHub Actions artifact download and
  draft release upload/download.
- The staged draft release is `cpu-bundle-evidence-20260430`.
- The draft release is a draft prerelease only and is not a public release
  download surface.

The evidence does not prove release readiness.

## macOS Packaging UX Options

### Keep Zip

Pros:

- Preserves the currently verified artifact format and checksum chain.
- Keeps the packaging surface small while signing and notarization evidence is
  still missing.
- Avoids adding Finder-launch expectations before an app layout exists.

Risks:

- Users must extract the archive and launch from Terminal.
- Quarantine and Gatekeeper behavior may still warn or block execution after
  browser download.
- A zip does not by itself communicate app-like installation or update
  behavior.

Evidence required:

- SHA256 verification for the downloaded zip.
- Clean macOS arm64 first-run evidence after browser or command-line download.
- Quarantine attributes, Gatekeeper behavior, and Terminal launch transcript.
- Signing and notarization status for the extracted executable set or final
  distribution object.

### App Bundle

Pros:

- Provides a familiar Finder-launch shape if the product needs an app-like
  entry point.
- Creates a clearer target for macOS signing, hardened runtime, and
  notarization review.
- Can hide internal bundle layout from users.

Risks:

- Requires a new artifact layout and fresh smoke testing.
- May require entitlements, hardened runtime decisions, Info.plist metadata,
  icon assets, and launcher behavior not currently proven.
- Finder launch can create different first-run behavior than Terminal launch.

Evidence required:

- Exact app bundle layout.
- Codesigning evidence for the app bundle and embedded executable content.
- Notarization, stapling if applicable, and `spctl` assessment output.
- Finder and Terminal first-run evidence on clean macOS arm64.
- SHA256 preservation for the final distributed object.

### DMG

Pros:

- Gives macOS users a familiar downloadable container.
- Can carry an app bundle or documented archive layout.
- Can be signed and notarized as a distribution object.

Risks:

- Introduces another packaging layer that can break checksum, quarantine, or
  first-run assumptions.
- DMG signing/notarization evidence differs from app bundle evidence and must
  be recorded separately.
- If the DMG contains a raw zip or folder, user expectations may still be
  unclear.

Evidence required:

- DMG creation inputs and final layout.
- DMG signing and notarization submission evidence.
- Stapling result if supported by the selected flow.
- Browser-download quarantine behavior and first-run path from a mounted DMG.
- SHA256 preservation for the final DMG.

### PKG Installer

Pros:

- Supports a guided install flow and conventional installation locations.
- Can define system integration points explicitly.
- Can be signed and notarized with installer-specific evidence.

Risks:

- Highest operational and trust surface among the macOS options.
- Requires uninstall, upgrade, permissions, install-location, and rollback
  decisions.
- Installer behavior can create system changes not covered by current smoke
  evidence.

Evidence required:

- Installer payload layout and install locations.
- Package signing evidence and notarization evidence.
- Clean install, first-run, upgrade, and uninstall evidence.
- Gatekeeper and quarantine behavior after browser download.
- SHA256 preservation for the final pkg.

## Windows Packaging UX Options

### Keep Zip

Pros:

- Preserves the currently verified artifact format and checksum chain.
- Keeps the distribution surface small while signing, SmartScreen, and
  Microsoft Defender evidence is still missing.
- Avoids installer state, registry changes, and uninstall requirements.

Risks:

- Users must extract the archive and launch from the command line or a bundled
  script.
- SmartScreen or antivirus tools may warn on the downloaded zip, extracted
  files, or first launch.
- A zip gives limited first-run guidance unless release notes remain precise.

Evidence required:

- SHA256 verification for the downloaded zip.
- Clean Windows x64 extraction and first-run transcript.
- Microsoft Defender scan result.
- SmartScreen behavior for the downloaded zip and first launched executable or
  launcher.
- Signing status for any launcher or executable content.

### Signed Zip With Launcher

Pros:

- Keeps the zip transport while providing a clearer launch target.
- Allows a signed launcher to carry basic version and publisher identity if
  signing succeeds.
- Avoids full installer state while improving command discoverability.

Risks:

- Signing a launcher does not prove every extracted component is signed.
- The zip, launcher, embedded Python, and libraries may each trigger different
  trust or antivirus behavior.
- Requires fresh smoke evidence because the launch path and layout changed.

Evidence required:

- Launcher source, build command, and signing command.
- Signature verification after download and extraction.
- SmartScreen and Defender behavior for both the zip and launcher.
- Help-command smoke transcript through the launcher.
- SHA256 preservation for the final zip.

### Installer/MSI/EXE

Pros:

- Provides the most familiar Windows installation path for many users.
- Can support Start Menu shortcuts, install location selection, and uninstall
  registration.
- Creates an obvious object for Authenticode signing.

Risks:

- Introduces installer-specific maintenance, rollback, upgrade, and uninstall
  behavior.
- SmartScreen reputation can still warn on a properly signed installer until
  reputation exists.
- Requires evidence for installed layout, not just archive contents.

Evidence required:

- Installer technology, inputs, and installed file layout.
- Authenticode signing and timestamp verification.
- SmartScreen behavior from browser download.
- Microsoft Defender scan of the installer and installed files.
- Clean install, help-command smoke, upgrade if applicable, and uninstall
  evidence.
- SHA256 preservation for the final installer.

## First-Run UX Expectations

Before any artifact is promoted beyond draft evidence, record the user-facing
first-run path for each platform and format:

- Launch command or launcher path.
- Help-command smoke path, including exact command and output boundary.
- Expected warnings, prompts, or blocks during download, extraction,
  installation, and first execution.
- Whether the user starts from Terminal, Finder, Command Prompt, PowerShell, or
  a launcher.
- How signing, notarization, quarantine, SmartScreen, Microsoft Defender, and
  other antivirus status affect the first run.

Help-command smoke evidence is only a packaging and launch-path check. It does
not prove scientific correctness, real-data execution, long-running workload
behavior, or performance.

## Decision Gates Before Changing Artifact Format

Do not change the staged artifact format from the currently proven zips until a
format-specific evidence PR records:

- Signing evidence for the selected platform and format.
- macOS notarization and quarantine evidence, if the change affects macOS.
- Windows SmartScreen and Microsoft Defender evidence, if the change affects
  Windows.
- SHA256 checksum preservation from produced artifact to downloaded artifact.
- Fresh smoke test evidence after any format, layout, launcher, install path,
  or extraction-path change.

Format changes include moving from zip to app bundle, dmg, pkg, signed zip with
launcher, MSI, EXE installer, or any layout that changes the launch command.

## Not Proven By This Plan

- Release readiness.
- Public distribution readiness.
- Signing/notarization success.
- Windows SmartScreen/AV trust.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.
- macOS x64 / Intel support.
- Linux desktop bundle support.

## Recommended Next Safe Action

Keep zip artifacts as the current evidence format until signing/notarization
and Windows trust evidence exists.

Do not switch to installers before a format-specific evidence PR records the
new artifact layout, checksum preservation, platform trust behavior, and fresh
smoke evidence.
