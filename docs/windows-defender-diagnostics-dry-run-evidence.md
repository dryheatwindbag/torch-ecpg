# Windows Defender Diagnostics Dry-Run Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `main`

Workflow source commit: `8022eb0de8d5c28fbbe8110beaafd5a13a56cd3f`

Classification: workflow evidence / Windows Defender diagnostics /
release-readiness planning

Scope: record the Windows signing SmartScreen proof dry run after expanding
Defender diagnostics.

This evidence does not sign files, timestamp files, create a signed zip, prove
Defender acceptance, prove SmartScreen trust, claim release readiness, or claim
public distribution readiness.

## Workflow Run

- Workflow: `Windows Signing SmartScreen Proof`
- Trigger: `workflow_dispatch`
- Mode: `dry_run: "true"`
- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25195051648`
- Run result: `success`
- Branch under test: `main`
- Commit under test: `8022eb0de8d5c28fbbe8110beaafd5a13a56cd3f`
- Job: `Windows signing SmartScreen proof`
- Job result: `success`
- Job URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25195051648/job/73873650481`
- Job duration: `3m27s`

## Source Artifact

- Source workflow run: `25173165547`
- Source artifact name: `tecpg-windows-x64-cpu`
- Bundle name: `tecpg-windows-x64-cpu`
- Source zip: `tecpg-windows-x64-cpu.zip`
- Expected unsigned SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`

The dry-run evidence artifact recorded:

```text
19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd  tecpg-windows-x64-cpu.zip
```

## Defender Diagnostics Captured

The proof evidence artifact included:

- `defender-status.txt`
- `defender-scan.txt`
- `MpCmdRun-unsigned-1.log`
- `MpCmdRun-unsigned-2.log`

`Get-MpComputerStatus` reported:

```text
AMRunningMode              : Normal
AMServiceEnabled           : True
AntivirusEnabled           : True
RealTimeProtectionEnabled  : False
OnAccessProtectionEnabled  : False
IoavProtectionEnabled      : False
BehaviorMonitorEnabled     : False
```

`Get-MpPreference` reported broad runner exclusions:

```text
ExclusionPath : {C:\, D:\}
```

It also reported disabled scan/protection settings including:

```text
DisableRealtimeMonitoring : True
DisableIOAVProtection     : True
DisableScriptScanning     : True
DisableArchiveScanning    : True
```

## Defender Scan Attempts

The workflow attempted `MpCmdRun.exe` custom scans for:

- `proof/unsigned-artifact/tecpg-windows-x64-cpu.zip`
- `proof/work/tecpg-windows-x64-cpu`

Both scan attempts recorded:

```text
CmdTool: Failed with hr = 0x80508023.
ExitCode: 2
```

The copied `MpCmdRun` logs recorded:

```text
Warning: MpScan() encounter error. hr = 0x80508023
ERROR: MpScan(dwOptions=1073758209) Completion Failed 0x80508023
```

This is not Defender acceptance evidence.

## Dry-Run Boundary

The dry-run boundary file recorded:

```text
Dry run completed.
No certificate was imported.
No files were signed.
No signed zip was created.
No SmartScreen reputation claim was made.
```

The certificate import, `signtool`, signed-smoke, signed-zip repackaging,
signed-artifact Defender scan, and SmartScreen boundary steps were skipped.

## Conclusion

GitHub-hosted Windows runner Defender diagnostics are useful for explaining why
CI Defender scans are not acceptance evidence, but they are not sufficient for
release-readiness trust claims.

The next Defender acceptance proof should run on a clean Windows x64 machine or
VM without broad repository drive exclusions and with Defender protection
settings enabled enough to complete a custom scan.

## Proven

- The expanded Defender diagnostics workflow can be dispatched from `main`.
- The workflow still downloads, verifies, extracts, and inventories the proven
  Windows artifact.
- Defender status and preference diagnostics are captured.
- `MpCmdRun` logs are copied into the evidence artifact when available.
- The hosted runner configuration is not suitable as Defender acceptance
  evidence for this artifact.

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
