# CPU Bundle Signing Implementation Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `6b54f62a32cd7e46e5004f0507b3495e10088d45`

Classification: docs / decision / signing scaffold / release-readiness planning

Chosen packaging direction: signed zip.

Scope: define a reproducible signing, notarization, and trust-validation
approach for the already-proven Windows x64 and macOS arm64 CPU zip artifacts.

macOS notarization proof workflow:
[`docs/macos-notarization-proof-workflow.md`](macos-notarization-proof-workflow.md)

Windows signing and SmartScreen proof workflow:
[`docs/windows-signing-smartscreen-proof-workflow.md`](windows-signing-smartscreen-proof-workflow.md)

This plan does not implement signing, notarization, installers, release
automation, artifact generation, packaging format changes, runtime behavior
changes, or public distribution. It does not claim release readiness or public
distribution readiness.

## Current Evidence Baseline

The repository has evidence for:

- Windows x64 CPU bundle zip artifact.
- macOS arm64 CPU bundle zip artifact.
- SHA256 preservation across GitHub Actions artifact download and draft release
  upload/download.
- Draft prerelease staging for evidence only.
- Installer and packaging UX decision gates.

The current evidence does not prove signing, notarization, quarantine behavior,
Windows SmartScreen trust, antivirus acceptance, release readiness, public
distribution readiness, scientific correctness, real-data execution, or
performance.

## Signed Zip Direction

The next implementation direction is signed zip, not installer packaging.

Rationale:

- Preserve the already-proven zip artifact format.
- Minimize scope expansion while addressing the largest remaining trust gap.
- Avoid pkg, dmg, MSI, and EXE installer behavior until signing strategy is
  proven.
- Keep checksum and first-run evidence comparable to the existing artifact
  evidence chain.

This direction must not change the distributed artifact format until a separate
format-specific evidence PR approves that change.

## Signing Location

Two execution modes are allowed for the first scaffold:

- Manual signing on controlled macOS and Windows signing hosts.
- CI signing in GitHub Actions after secrets, certificates, runner behavior,
  and audit requirements are approved.

The first evidence PR must identify which mode was used. CI signing is not
approved by this plan; it requires a separate workflow PR or stub-to-active
decision gate.

## Artifact States

Each platform must distinguish these artifact states:

- Unsigned source zip: artifact produced by existing CPU bundle workflow.
- Expanded signing workspace: temporary extracted bundle used for signing
  executable content.
- Signed payload: extracted files after signing but before repackaging.
- Signed zip candidate: regenerated zip after signing.
- Notarized macOS candidate: macOS signed zip after notarization acceptance.
- Final evidence artifact: post-signing artifact whose checksum and first-run
  behavior are recorded.

Checksums from unsigned artifacts must not be reused for signed artifacts.
Every signing, notarization, stapling, timestamping, or repackaging step
requires regenerated SHA256 records.

## macOS Signing Requirements

Before a macOS arm64 CPU zip can be described as signed, record:

- Apple Developer Program account owner.
- Team ID.
- Signing certificate type.
- Codesign identity common name.
- Codesign identity fingerprint.
- Exact files that are signed, including launchers, executable binaries,
  dynamic libraries, embedded Python binaries, and helper tools.
- Whether hardened runtime is required.
- Entitlements file path, if any.
- Exact `codesign` commands.
- Verification output after signing and after final download.

Required secret names, if CI signing is later approved:

- `MACOS_CERTIFICATE_P12_BASE64`
- `MACOS_CERTIFICATE_PASSWORD`
- `MACOS_KEYCHAIN_PASSWORD`
- `APPLE_ID`
- `APPLE_TEAM_ID`
- `APPLE_APP_SPECIFIC_PASSWORD`

Secret values must never be committed or logged.

## macOS Notarization Flow

The intended signed-zip flow is:

1. Download the existing macOS arm64 CPU zip artifact.
2. Verify the unsigned source zip SHA256 against its evidence record.
3. Extract the zip into a clean signing workspace.
4. Sign required executable content with `codesign`.
5. Recreate the zip from the signed payload with deterministic inputs where
   practical.
6. Regenerate SHA256 for the signed zip candidate.
7. Submit the signed zip candidate for notarization.
8. Record notarization request ID, status, and log.
9. Staple only if the final selected object or contained object supports
   stapling.
10. Regenerate SHA256 after any stapling or repackaging step.
11. Download the final evidence artifact and verify SHA256.

Important boundary: a plain zip archive is not assumed to be staplable. If
stapling is not supported for the final signed-zip shape, the evidence must say
so explicitly and must not describe the zip as stapled. If a staplable object
is introduced inside the zip, that is a layout decision requiring fresh smoke
evidence.

## macOS Verification Commands

Record exact command output for each signed macOS artifact:

```sh
codesign --verify --strict --deep --verbose=4 <signed-path>
codesign --display --verbose=4 <signed-path>
spctl --assess --type execute --verbose=4 <signed-path>
xcrun notarytool submit <signed-zip> --apple-id "$APPLE_ID" --team-id "$APPLE_TEAM_ID" --wait
xcrun notarytool log <request-id> --apple-id "$APPLE_ID" --team-id "$APPLE_TEAM_ID"
```

If stapling is applicable, also record:

```sh
xcrun stapler staple <staplable-path>
xcrun stapler validate <staplable-path>
```

The exact `spctl` target must match the user launch path. If users launch a
script, launcher, or embedded executable, validate that path specifically.

## macOS Quarantine Expectations

Before any macOS artifact is described as public-download-ready, record a
download-path validation on a clean macOS arm64 machine or VM:

- Download source and method.
- `xattr -l` output before first run.
- Terminal first-run behavior.
- Finder first-run behavior only if the layout supports Finder launch.
- Gatekeeper warning, prompt, or block behavior.
- Any required user bypass steps.

If users must remove quarantine attributes manually or bypass Gatekeeper, the
artifact is not public-distribution-ready without a separate release decision.

## Windows Signing Requirements

Before a Windows x64 CPU zip can be described as signed, record:

- Code signing certificate owner.
- Certificate type and issuer.
- Certificate fingerprint.
- Signing host or runner.
- Exact files signed, including launcher executables, helper executables, DLLs,
  and bundled tools where applicable.
- Timestamp server.
- Exact `signtool` commands.
- Signature verification output after signing and after final download.

Required secret names, if CI signing is later approved:

- `WINDOWS_CERTIFICATE_PFX_BASE64`
- `WINDOWS_CERTIFICATE_PASSWORD`
- `WINDOWS_SIGNING_TIMESTAMP_URL`

Secret values must never be committed or logged.

## Windows Authenticode Flow

The intended signed-zip flow is:

1. Download the existing Windows x64 CPU zip artifact.
2. Verify the unsigned source zip SHA256 against its evidence record.
3. Extract the zip into a clean signing workspace.
4. Sign required executable content with `signtool`.
5. Timestamp every signed file.
6. Verify signatures before repackaging.
7. Recreate the zip from the signed payload.
8. Regenerate SHA256 for the signed zip candidate.
9. Download the final evidence artifact and verify SHA256.
10. Run Defender and SmartScreen observation steps on a clean Windows x64
    machine or VM.

Signing individual executable files inside a zip must not be described as
signing the full zip archive unless the archive itself is covered by a separate
signing mechanism and verification evidence.

## Windows Verification Commands

Record exact command output for each signed Windows artifact:

```powershell
signtool sign /fd SHA256 /tr <timestamp-url> /td SHA256 /f <cert.pfx> /p <password> <path>
signtool verify /pa /v <path>
Get-FileHash -Algorithm SHA256 <signed-zip>
```

If PowerShell Authenticode verification is used, also record:

```powershell
Get-AuthenticodeSignature <path> | Format-List *
```

The timestamp server should be configured as
`WINDOWS_SIGNING_TIMESTAMP_URL`. The selected timestamp URL must be recorded in
the evidence PR.

## Windows SmartScreen Expectations

SmartScreen reputation is not guaranteed by Authenticode signing. The first
Windows proof PR must record:

- Download source and method.
- Browser behavior for the downloaded signed zip.
- Extraction behavior.
- SmartScreen behavior for the first launched signed executable or launcher.
- Whether warnings, reputation prompts, or blocks appear.
- User steps required to continue, if any.

If SmartScreen warns or blocks, the artifact is not public-distribution-ready
without a separate release decision and user communication plan.

## Windows Defender Considerations

Record Microsoft Defender evidence on a clean Windows x64 machine or VM:

```powershell
MpCmdRun.exe -Scan -ScanType 3 -File <signed-zip-or-extracted-path>
```

The evidence should identify whether the scan target was the signed zip, the
extracted directory, the launcher, or all of those targets. Additional
antivirus or reputation checks may be required by a later release policy, but
they are not established by this plan.

## User Verification Steps

Future release notes or internal handoff notes for signed zip artifacts should
provide user-verifiable checks without overstating trust:

- Download the signed zip and matching checksum file.
- Verify SHA256 before extraction.
- Extract the zip.
- Run the documented help-command smoke path.
- On macOS, expect Gatekeeper behavior to match the recorded quarantine
  evidence.
- On Windows, expect SmartScreen and Defender behavior to match the recorded
  trust evidence.

User verification steps do not prove scientific correctness, real-data
execution, long-running workload behavior, GPU/CUDA support, or performance.

## Evidence Required Before Claims

Do not claim signing works until a platform-specific evidence PR records:

- Exact signing commands.
- Signing identity or certificate metadata.
- Signature verification output.
- SHA256 regeneration after signing.
- Fresh help-command smoke output from the signed artifact.

Do not claim macOS notarization works until a macOS evidence PR records:

- Notarization submission command.
- Request ID.
- Accepted status.
- Notarization log.
- Stapling result or explicit no-staple boundary.
- `spctl` and quarantine evidence on a clean macOS arm64 machine or VM.

Do not claim Windows trust until a Windows evidence PR records:

- Authenticode verification after download.
- Timestamp verification.
- Defender scan output.
- SmartScreen observation on a clean Windows x64 machine or VM.

## Not Proven By This Plan

- Signing works.
- Notarization succeeded.
- Stapling succeeded.
- SmartScreen trust was achieved.
- Windows Defender or antivirus acceptance.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.
- macOS x64 / Intel support.
- Linux desktop bundle support.

## Next Safe Action After This Plan

After this plan merges, implement one platform proof only:

- macOS notarization proof, or
- Windows signing plus SmartScreen observation.

Do not implement both platform proofs at once. Do not build pkg, dmg, MSI, or
EXE installers before signing evidence exists and a separate packaging-format
decision gate approves that change.
