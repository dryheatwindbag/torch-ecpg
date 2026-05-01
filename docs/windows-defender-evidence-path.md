# Windows Defender Evidence Path

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `8cde533c63a2b80e5122692bc3580baa30483493`

Classification: workflow scaffold / Windows Defender evidence / release
readiness planning

Scope: define the improved Defender evidence path for the Windows signing
SmartScreen proof workflow after the first dry-run scan commands returned
`0x80508023`.

This plan does not sign files, timestamp files, create a signed zip, prove
Defender acceptance, prove SmartScreen trust, claim release readiness, or claim
public distribution readiness.

## Background

The first successful Windows proof dry run completed artifact download,
checksum verification, extraction, and signable-content inventory. The Defender
scan commands ran but reported:

```text
CmdTool: Failed with hr = 0x80508023.
```

That result is not Defender acceptance evidence.

## Workflow Improvement

The Windows signing SmartScreen proof workflow now records more Defender
diagnostics before and during scan attempts:

- `Get-MpComputerStatus` output, if available.
- `Get-MpPreference` output, if available.
- Resolved `MpCmdRun.exe` path.
- Per-target `MpCmdRun` stdout and stderr.
- Per-target `MpCmdRun` exit code.
- `MpCmdRun.log` copied from the runner temp directory when available.

These diagnostics are recorded for unsigned dry-run scan targets and for signed
artifact scan targets in proof mode.

Expanded diagnostic dry-run evidence:
[`docs/windows-defender-diagnostics-dry-run-evidence.md`](windows-defender-diagnostics-dry-run-evidence.md)

Clean Windows validation plan:
[`docs/windows-clean-vm-defender-smartscreen-validation-plan.md`](windows-clean-vm-defender-smartscreen-validation-plan.md)

Clean Windows evidence template:
[`docs/windows-clean-vm-defender-smartscreen-evidence-template.md`](windows-clean-vm-defender-smartscreen-evidence-template.md)

## Evidence Boundary

Capturing Defender diagnostics does not prove Defender acceptance. A future
evidence PR may describe Defender acceptance only after scan output clearly
shows a completed scan with no detection or block for the selected target.

If GitHub-hosted runners cannot produce reliable Defender scan output, Defender
evidence must move to a clean Windows x64 machine or VM with reproducible scan
commands and logs.

## Not Proven

- Defender acceptance.
- SmartScreen trust.
- Signing works.
- Timestamping succeeded.
- Signed zip checksum regeneration.
- Signed-payload help-command smoke behavior.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- macOS signing or notarization.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.

## Next Safe Action

Park CI-based Defender acceptance and move Defender evidence to a clean Windows
x64 VM or physical machine. Keep the GitHub workflow for artifact download,
checksum, extraction, inventory, and diagnostic evidence, but do not use it to
claim Defender acceptance.
