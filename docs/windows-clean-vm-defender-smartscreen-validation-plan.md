# Windows Clean VM Defender And SmartScreen Validation Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `cf38970d471f37d3b3fa2b10370897ffe2691de2`

Classification: manual validation plan / Windows trust evidence /
release-readiness planning

Scope: define the clean Windows x64 VM or physical-machine validation path for
Defender scan evidence and SmartScreen observation after GitHub-hosted runner
diagnostics proved unsuitable for Defender acceptance claims.

This plan does not sign files, timestamp files, create a signed zip, run an
installer, publish release assets, claim Defender acceptance, claim SmartScreen
trust, claim release readiness, or claim public distribution readiness.

## Current Evidence Baseline

Windows evidence currently proves:

- Windows x64 CPU zip artifact exists.
- The artifact chain preserves SHA256 through GitHub Actions artifact download
  and draft release staging evidence.
- The Windows signing SmartScreen proof workflow can download, verify, extract,
  and inventory the proven artifact.
- GitHub-hosted Windows runner Defender diagnostics are not suitable for
  Defender acceptance evidence.

GitHub-hosted runner diagnostics recorded:

```text
RealTimeProtectionEnabled  : False
OnAccessProtectionEnabled  : False
ExclusionPath              : {C:\, D:\}
CmdTool: Failed with hr = 0x80508023.
ExitCode: 2
```

Those diagnostics explain the CI limitation but do not prove Defender
acceptance.

## Validation Target

Use a clean Windows x64 VM or physical machine with:

- Windows x64 installed from a trusted source.
- Microsoft Defender enabled.
- Real-time protection enabled.
- On-access protection enabled where available.
- No broad `C:\` or `D:\` Defender exclusions.
- No repository-specific Defender exclusions.
- Network access sufficient for signature updates and SmartScreen checks.
- Browser available for download-path validation.
- PowerShell available for command capture.

Record the Windows edition, version, build number, install source, and whether
the machine is a VM or physical host.

## Source Artifact

Validate the same current Windows CPU bundle evidence artifact unless a newer
signed candidate is explicitly selected by a later PR:

- Source workflow run: `25173165547`
- Source artifact name: `tecpg-windows-x64-cpu`
- Zip: `tecpg-windows-x64-cpu.zip`
- Expected unsigned SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`

If a signed zip candidate is later produced, record both the unsigned source
SHA256 and the signed candidate SHA256. Do not reuse unsigned checksums for
signed artifacts.

## Machine Baseline Commands

Run and save output:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture
Get-MpComputerStatus | Format-List *
Get-MpPreference | Format-List *
```

The evidence must explicitly state whether Defender protections and exclusions
make the machine suitable for acceptance testing.

## Download And Checksum Commands

Download the selected artifact through the intended user path. Prefer browser
download for SmartScreen observation. Record:

- Download source URL.
- Browser name and version.
- Whether the browser warns, blocks, or allows the download.
- Downloaded filename.
- Download location.

Then verify checksum:

```powershell
Get-FileHash -Algorithm SHA256 .\tecpg-windows-x64-cpu.zip
```

The SHA256 must match the selected evidence record before extraction or scan
claims are made.

## Defender Scan Commands

Run and save output:

```powershell
MpCmdRun.exe -Scan -ScanType 3 -File .\tecpg-windows-x64-cpu.zip
```

Extract the zip to a clean directory, then run:

```powershell
Expand-Archive .\tecpg-windows-x64-cpu.zip -DestinationPath .\tecpg-windows-x64-cpu -Force
MpCmdRun.exe -Scan -ScanType 3 -File .\tecpg-windows-x64-cpu
```

Also save `MpCmdRun.log` if present. The evidence must record the exit code for
each scan target.

Defender acceptance may be described only if the scan completes successfully
and reports no detection, block, or remediation requirement for the selected
artifact state.

## SmartScreen Observation

SmartScreen reputation cannot be proven by PowerShell scan commands alone.
Record a user-download and first-launch observation on the clean machine:

- Browser download behavior for the zip.
- Windows Explorer extraction behavior.
- First launch path, usually:
  `tecpg-windows-x64-cpu\launchers\tecpg.cmd --help`
- Whether SmartScreen warns, blocks, or allows the launch.
- Exact prompt text or screenshot reference, if a prompt appears.
- User action required to continue, if any.

If SmartScreen warns or blocks, do not claim SmartScreen trust or public
distribution readiness.

## Help-Command Smoke Path

After extraction, run:

```powershell
.\tecpg-windows-x64-cpu\launchers\tecpg.cmd --help
.\tecpg-windows-x64-cpu\launchers\tecpg.cmd data --help
.\tecpg-windows-x64-cpu\launchers\tecpg.cmd run mlr --help
```

This smoke path proves launch/help behavior only. It does not prove scientific
correctness, real-data execution, long-running workload behavior, GPU/CUDA
support, or performance.

## Evidence Package

A follow-up evidence PR should include:

- Machine baseline output.
- Defender status and preference output.
- Download source and browser behavior.
- SHA256 verification output.
- Defender scan output and exit codes for zip and extracted directory.
- `MpCmdRun.log`, or a note that it was unavailable.
- SmartScreen download and first-launch observation.
- Help-command smoke output.
- Explicit claims and non-claims reviewed against the boundary list.

Do not commit private machine identifiers, user account names, secrets, signing
certificates, or unrelated local paths if they are not needed for evidence.

## Not Proven By This Plan

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

Run this validation on a clean Windows x64 VM or physical machine and record an
evidence PR. If no clean Windows machine is available, keep Defender acceptance
and SmartScreen trust parked.
