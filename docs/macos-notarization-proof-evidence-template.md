# macOS Notarization Proof Evidence Template

Repository: `dryheatwindbag/torch-ecpg`

Classification: manual evidence template / macOS signing proof /
notarization readiness planning

Scope: provide the required evidence shape for a future macOS arm64 signed-zip
proof-mode run after Apple signing and notarization secrets are configured.

This template does not sign files, import certificates, submit notarization,
staple artifacts, publish release assets, change artifact format, prove
quarantine behavior, claim release readiness, or claim public distribution
readiness.

## Evidence PR Summary

- Evidence PR:
- Evidence branch:
- Validation date:
- Workflow run URL:
- Workflow source branch:
- Workflow source commit:
- Mode: proof mode with `dry_run: "false"`
- Validator:

Do not include certificate material, Apple account secrets, app-specific
passwords, keychain passwords, private machine identifiers, or unrelated local
paths.

## Required Secret Readiness

Record whether these repository secret names were configured before dispatch:

- `MACOS_CERTIFICATE_P12_BASE64`:
- `MACOS_CERTIFICATE_PASSWORD`:
- `MACOS_KEYCHAIN_PASSWORD`:
- `MACOS_CODESIGN_IDENTITY`:
- `APPLE_ID`:
- `APPLE_TEAM_ID`:
- `APPLE_APP_SPECIFIC_PASSWORD`:

Do not record secret values.

If any required secret name is missing, do not run proof mode and do not claim
signing or notarization evidence.

## Source Artifact

- Source workflow run:
- Source artifact name:
- Source zip filename:
- Expected unsigned SHA256:
- Observed unsigned SHA256:
- Source artifact download path:

The unsigned checksum must match the selected evidence record before signing or
notarization claims are made.

## Signing Evidence

Record the signing scope:

- Mach-O files discovered:
- Executable non-Mach-O files discovered:
- Files selected for signing:
- Files intentionally not signed:
- Codesign identity label used:
- Hardened runtime enabled: yes / no
- Entitlements file used: yes / no

Paste sanitized output or attach the workflow artifact files that show:

```bash
codesign --verify --strict --verbose=4 <signed-path>
codesign --display --verbose=4 <signed-path>
```

Signing may be described as proven only for the exact files and artifact state
validated by the captured proof-mode evidence.

## Signed Candidate Checksum

Record the post-signing artifact identity:

- Signed candidate zip filename:
- Signed candidate SHA256:
- Checksum file path:

Every signing, stapling, notarization, or repackaging step changes the evidence
state and requires a regenerated SHA256. Do not reuse the unsigned checksum for
a signed candidate.

## Notarization Evidence

Record:

- Notarization tool:
- Notarization tool version:
- Apple team ID:
- Submission command shape:
- Notarization request ID:
- Notarization final status:
- Notarization log artifact:

Paste sanitized output or attach the workflow artifact files that show the
submission result and final notarization log.

If notarization is rejected, unavailable, or not submitted, do not claim
notarization success.

## Stapling Boundary

The current signed-zip proof path does not prove stapling for the zip artifact.
Record the exact boundary:

- Stapling attempted: yes / no
- Stapling target:
- Stapling result:
- No-staple boundary recorded: yes / no

If stapling is not performed or not applicable to the selected zip path, do not
claim stapling success.

## Gatekeeper And `spctl` Evidence

Paste sanitized output from the selected launch or executable paths:

```bash
spctl --assess --type execute --verbose=4 <signed-path>
```

Record:

- `spctl` target path:
- `spctl` exit code:
- Assessment result:
- Prompt or block observed during local execution: yes / no

`spctl` output from CI does not replace clean download-path quarantine evidence.

## Clean Download And Quarantine Observation

Record a clean macOS arm64 user-download path before making public distribution
claims:

- Machine type: clean VM / clean physical machine / CI runner
- macOS version:
- Browser or download method:
- Download source URL:
- Quarantine attribute present after download: yes / no
- `xattr -l` output captured: yes / no
- Finder first-open behavior:
- Terminal first-launch behavior:
- Gatekeeper prompt shown: yes / no
- User bypass required: yes / no

Paste sanitized output:

```bash
xattr -l <downloaded-artifact-or-extracted-path>
```

If users must manually remove quarantine attributes or bypass Gatekeeper, do
not claim public distribution readiness.

## Help-Command Smoke Evidence

Paste sanitized output from the signed candidate:

```bash
./tecpg-macos-arm64-cpu/launchers/tecpg --help
./tecpg-macos-arm64-cpu/launchers/tecpg data --help
./tecpg-macos-arm64-cpu/launchers/tecpg run mlr --help
```

Record:

- `tecpg --help` exit code:
- `tecpg data --help` exit code:
- `tecpg run mlr --help` exit code:
- Launch/help behavior acceptable for selected signed candidate: yes / no

This smoke path proves launch/help behavior only.

## Claims Review

State only the claims supported by the captured evidence.

### Proven

- Pending future evidence.

### Not Proven

- Signing works, unless codesign proof mode succeeds and verification output is
  captured for the selected signed candidate.
- Notarization succeeded, unless the notarization request is accepted and the
  notarization log is captured.
- Stapling succeeded, unless stapling is performed and verified for the selected
  artifact type.
- Quarantine or Gatekeeper acceptance, unless clean download-path evidence is
  captured.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- Windows signing or SmartScreen trust.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.
- macOS x64 / Intel support.

## Next Safe Action After Evidence

If the proof-mode run succeeds and clean download-path quarantine evidence is
acceptable, open one narrow follow-up PR deciding whether to keep signed zip as
the public macOS packaging path or add a format-specific installer evidence
gate.

If the proof-mode run fails, secrets are missing, notarization is rejected, or
Gatekeeper requires bypass, keep macOS public distribution readiness parked and
do not claim signing, notarization, quarantine acceptance, release readiness, or
public distribution readiness.
