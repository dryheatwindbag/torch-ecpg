# macOS Notarization Proof Mode Secret Readiness Recheck

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `c95dcdc89f22e3b51a837f03627bc0651bf06c20`

Classification: docs / evidence blocker / macOS signing proof readiness

Scope: record a follow-up repository secret-readiness check after adding the
macOS notarization proof evidence template.

This evidence does not run proof mode, import certificates, sign files, submit
notarization, staple artifacts, publish release assets, change artifact format,
claim release readiness, or claim public distribution readiness.

## Context

The macOS notarization proof workflow dry run is already recorded, and the
proof-mode evidence template is now available for a future signing and
notarization evidence PR.

Proof mode remains gated on repository Actions secrets. Running proof mode
without those secrets would fail before certificate import, signing, or
notarization and would not add useful signing evidence.

## Secret Readiness Recheck

On May 1, 2026, the repository Actions secrets were checked with:

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

Do not dispatch macOS notarization proof mode with `dry_run: "false"` until the
required secret names are configured.

## Proven

- The required macOS proof-mode secret names were not visible to
  `gh secret list` at the time of this recheck.
- macOS notarization proof mode remains blocked on secret configuration.
- The next evidence PR should use the proof-mode evidence template after
  secrets are configured.

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
