# Windows Signing SmartScreen Dry-Run Failure

Repository: `dryheatwindbag/torch-ecpg`

Current `main` commit: `6ff41e1523fe99b8eaea94405e437a309ac368a4`

Classification: workflow evidence / Windows signing proof / dry-run failure

Scope: record the first attempted Windows signing SmartScreen proof dry run and
the workflow fix needed before retrying.

This evidence does not sign files, timestamp files, create a signed zip, prove
Defender acceptance, prove SmartScreen trust, claim release readiness, or claim
public distribution readiness.

## Workflow Run

- Workflow: `Windows Signing SmartScreen Proof`
- Trigger: `workflow_dispatch`
- Mode: `dry_run: "true"`
- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25194523955`
- Run result: `failure`
- Branch under test: `main`
- Job: `Windows signing SmartScreen proof`
- Job URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25194523955/job/73872015126`

## Source Artifact Inputs

- Source workflow run: `25173165547`
- Source artifact name: `tecpg-windows-x64-cpu`
- Bundle name: `tecpg-windows-x64-cpu`
- Source zip: `tecpg-windows-x64-cpu.zip`
- Expected unsigned SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`

## Observed Failure

The workflow downloaded the source artifact and computed the expected zip hash:

```text
19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd  tecpg-windows-x64-cpu.zip
```

The run failed while parsing `SHA256SUMS.txt`:

```text
No checksum entry found for tecpg-windows-x64-cpu.zip
```

The failure happened before extraction, inventory, Defender scan, certificate
import, signing, timestamping, signed-zip creation, or SmartScreen boundary
recording.

## Root Cause

The PowerShell checksum parser used a literal backslash pattern:

```powershell
$_ -split "\\s+"
```

That did not split the checksum line on whitespace, so the workflow could not
find the expected artifact name in `SHA256SUMS.txt`.

## Fix

Use the PowerShell regex whitespace pattern:

```powershell
$_ -split "\s+"
```

After this fix merges to `dev`, expose the corrected workflow on `main` and
rerun dry-run mode against the same source artifact.

## Proven

- The Windows proof workflow can be dispatched from `main`.
- The workflow can download the source Windows artifact.
- The source zip hash matched the expected SHA256 input.
- No signing or proof-mode behavior ran before failure.

## Not Proven

- Source zip extraction.
- Signable-content inventory.
- Defender scan behavior.
- Signing works.
- Timestamping succeeded.
- Signed zip checksum regeneration.
- Signed-payload help-command smoke behavior.
- SmartScreen trust.
- Release readiness.
- Public distribution readiness.
- Installer behavior.
- macOS signing or notarization.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Performance guarantees.
