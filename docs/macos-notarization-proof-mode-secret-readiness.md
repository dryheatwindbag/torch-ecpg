# macOS Notarization Proof Mode Secret Readiness

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `81da2fec1205e96979ec7c57852caa06b58b733c`

Classification: docs / evidence blocker / macOS signing proof readiness

Scope: record the secret-readiness check before attempting macOS notarization
proof mode with Apple signing credentials.

This evidence does not run proof mode, import certificates, sign files, submit
notarization, staple artifacts, publish release assets, change artifact format,
claim release readiness, or claim public distribution readiness.

## Current Evidence Baseline

The macOS notarization proof workflow dry run succeeded:

- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25191662840`
- Source artifact: `tecpg-macos-arm64-cpu`
- Source run: `25176627794`
- Verified unsigned SHA256:
  `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a`
- Mach-O files inventoried: `317`
- Executable non-Mach-O files inventoried: `147`

Dry-run mode confirmed that no certificate was imported, no files were signed,
and no notarization request was submitted.

## Secret Readiness Check

Before running proof mode, the repository Actions secrets were checked with:

```sh
gh secret list --repo dryheatwindbag/torch-ecpg
```

The command returned no visible secret names.

## Required Secret Names

Proof mode requires these repository secret names:

- `MACOS_CERTIFICATE_P12_BASE64`
- `MACOS_CERTIFICATE_PASSWORD`
- `MACOS_KEYCHAIN_PASSWORD`
- `MACOS_CODESIGN_IDENTITY`
- `APPLE_ID`
- `APPLE_TEAM_ID`
- `APPLE_APP_SPECIFIC_PASSWORD`

Secret values must not be committed, printed, pasted into logs, or recorded in
evidence documents.

## Decision

Do not run proof mode until the required secret names are configured.

Running proof mode now would fail at the workflow's required-secret gate before
certificate import, signing, or notarization. That failure would not add useful
signing evidence.

## Proven

- The dry-run evidence exists and is recorded.
- The repository did not expose the required macOS proof-mode secret names at
  the time of this readiness check.
- Proof mode is blocked on secret configuration.

## Not Proven

- Signing works.
- Notarization succeeded.
- Stapling succeeded.
- Signed zip checksum regeneration.
- Signed-payload help-command smoke behavior.
- Gatekeeper acceptance.
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

## Next Safe Action

Configure the required macOS signing and notarization secret names in the
repository or selected GitHub Actions environment. After configuration, rerun
the secret-readiness check before dispatching proof mode with `dry_run: "false"`.
