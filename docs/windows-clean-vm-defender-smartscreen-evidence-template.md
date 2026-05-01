# Windows Clean VM Defender And SmartScreen Evidence Template

Repository: `dryheatwindbag/torch-ecpg`

Classification: manual evidence template / Windows trust validation /
release-readiness planning

Scope: provide the required evidence shape for a future clean Windows x64 VM or
physical-machine Defender and SmartScreen validation PR.

This template does not sign files, timestamp files, create a signed zip, run an
installer, prove Defender acceptance, prove SmartScreen trust, claim release
readiness, or claim public distribution readiness.

## Evidence PR Summary

- Evidence PR:
- Evidence branch:
- Validation date:
- Validator:
- Machine type: clean VM / clean physical machine
- Windows edition:
- Windows version:
- OS build:
- OS architecture:
- Install source:
- Network state during validation:
- Browser used for download:
- Browser version:

Do not include private hostnames, account names, certificate material, secrets,
or unrelated local paths.

## Selected Artifact

- Artifact state: unsigned zip / signed zip candidate
- Source workflow run:
- Source artifact name:
- Source zip filename:
- Download source URL:
- Expected SHA256:
- Observed SHA256:

For a signed zip candidate, record both:

- Unsigned source SHA256:
- Signed candidate SHA256:

Do not reuse unsigned checksums for signed artifacts.

## Machine Baseline

Paste sanitized output from:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture
Get-MpComputerStatus | Format-List *
Get-MpPreference | Format-List *
```

### Defender Suitability Finding

Record whether the machine is suitable for Defender acceptance evidence:

- `RealTimeProtectionEnabled`:
- `OnAccessProtectionEnabled`:
- Broad drive exclusions present:
- Repository-specific exclusions present:
- Defender service state:
- Suitability finding: suitable / not suitable
- Reason:

If the machine has broad `C:\` or `D:\` exclusions, disabled scan protections,
or scan failures unrelated to the artifact, do not claim Defender acceptance.

## Download Observation

Record the user download path:

- Download method: browser / command line / other
- Download URL:
- Browser warning shown: yes / no
- Browser warning text or screenshot reference:
- Download blocked: yes / no
- User action required:
- Downloaded filename:
- Download location:

SmartScreen reputation cannot be proven from download success alone.

## Checksum Verification

Paste sanitized output from:

```powershell
Get-FileHash -Algorithm SHA256 .\tecpg-windows-x64-cpu.zip
```

Checksum finding:

- Matches selected artifact record: yes / no
- If no, stop validation and do not make scan or trust claims.

## Defender Scan Evidence

Paste sanitized output and exit code from the zip scan:

```powershell
MpCmdRun.exe -Scan -ScanType 3 -File .\tecpg-windows-x64-cpu.zip
```

- Zip scan exit code:
- Zip scan result:
- Detection, block, or remediation required: yes / no

Paste sanitized output and exit code from the extracted directory scan:

```powershell
Expand-Archive .\tecpg-windows-x64-cpu.zip -DestinationPath .\tecpg-windows-x64-cpu -Force
MpCmdRun.exe -Scan -ScanType 3 -File .\tecpg-windows-x64-cpu
```

- Extracted directory scan exit code:
- Extracted directory scan result:
- Detection, block, or remediation required: yes / no

Attach or summarize `MpCmdRun.log` if available. If the scan command fails,
record the failure and do not claim Defender acceptance.

## SmartScreen Observation

Record the interactive first-use path:

- Browser download warning: none / warned / blocked
- Windows Explorer extraction warning: none / warned / blocked
- First launch command:
  `.\tecpg-windows-x64-cpu\launchers\tecpg.cmd --help`
- SmartScreen prompt shown: yes / no
- SmartScreen prompt text or screenshot reference:
- Launch blocked: yes / no
- User bypass action required: yes / no

If SmartScreen warns, blocks, or requires bypass, do not claim SmartScreen
trust or public distribution readiness.

## Help-Command Smoke Evidence

Paste sanitized output from:

```powershell
.\tecpg-windows-x64-cpu\launchers\tecpg.cmd --help
.\tecpg-windows-x64-cpu\launchers\tecpg.cmd data --help
.\tecpg-windows-x64-cpu\launchers\tecpg.cmd run mlr --help
```

Smoke finding:

- `tecpg.cmd --help` exit code:
- `tecpg.cmd data --help` exit code:
- `tecpg.cmd run mlr --help` exit code:
- Launch/help behavior acceptable for selected artifact: yes / no

This smoke path proves launch/help behavior only.

## Claims Review

State only the claims supported by the captured evidence.

### Proven

- Pending future evidence.

### Not Proven

- Signing works.
- Timestamping succeeded.
- Signed zip checksum regeneration, unless this template is used for a signed
  zip candidate and the signed checksum is captured.
- SmartScreen trust, unless no warning/block/bypass is observed on the clean
  validation path.
- Defender acceptance, unless scans complete successfully with no detection,
  block, or remediation requirement.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- macOS signing or notarization.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.

## Next Safe Action After Evidence

If the clean Windows evidence is suitable and no warning, block, detection, or
remediation requirement is observed, open one narrow follow-up PR to decide
whether to proceed with Windows signing proof mode or keep Windows trust parked.

If the evidence is unsuitable, blocked, or warning-producing, keep Windows trust
parked and do not claim Defender acceptance, SmartScreen trust, release
readiness, or public distribution readiness.
