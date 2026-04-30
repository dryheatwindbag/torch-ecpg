# Windows Signing SmartScreen Dry-Run Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `main`

Workflow source commit: `c5d0d85508b5feb2adf39f6134a2228d15080817`

Classification: workflow evidence / Windows signing proof / dry-run validation

Scope: record the successful dry-run execution of the Windows signing
SmartScreen proof workflow against the previously proven Windows x64 CPU zip
artifact.

This evidence does not sign files, timestamp files, create a signed zip, prove
Defender acceptance, prove SmartScreen trust, claim release readiness, or claim
public distribution readiness.

## Workflow Run

- Workflow: `Windows Signing SmartScreen Proof`
- Trigger: `workflow_dispatch`
- Mode: `dry_run: "true"`
- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25194658321`
- Run result: `success`
- Branch under test: `main`
- Commit under test: `c5d0d85508b5feb2adf39f6134a2228d15080817`
- Job: `Windows signing SmartScreen proof`
- Job result: `success`
- Job URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25194658321/job/73872434910`
- Job duration: `3m3s`

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

The workflow compared the downloaded zip against the provided expected SHA256
and the downloaded `SHA256SUMS.txt`.

## Completed Steps

The successful dry-run job completed:

- Windows runner confirmation.
- Source artifact download.
- Unsigned source checksum verification.
- Source zip extraction.
- Signable-content inventory.
- Defender scan command execution for unsigned targets.
- Dry-run boundary recording.
- Proof evidence artifact upload.

The proof evidence artifact was named:
`windows-signing-smartscreen-proof-evidence`.

## Inventory

The dry-run evidence artifact recorded:

- Signable files: `357`
- Script launcher files: `6`
- Total inventoried signing-relevant files: `363`

The script launcher inventory included:

```text
D:\a\torch-ecpg\torch-ecpg\proof\work\tecpg-windows-x64-cpu\launchers\tecpg.cmd
```

The signable inventory included embedded Python runtime paths such as:

```text
D:\a\torch-ecpg\torch-ecpg\proof\work\tecpg-windows-x64-cpu\python\python.exe
D:\a\torch-ecpg\torch-ecpg\proof\work\tecpg-windows-x64-cpu\python\python3.dll
D:\a\torch-ecpg\torch-ecpg\proof\work\tecpg-windows-x64-cpu\python\python311.dll
```

The full inventory is preserved in the workflow evidence artifact rather than
copied into this repository.

## Defender Scan Result

The dry-run workflow attempted Microsoft Defender scans for:

- `proof/unsigned-artifact/tecpg-windows-x64-cpu.zip`
- `proof/work/tecpg-windows-x64-cpu`

Both scan commands reported:

```text
CmdTool: Failed with hr = 0x80508023.
```

This is not Defender acceptance evidence. A follow-up PR must either fix the
Defender invocation for CI or move Defender evidence to a clean Windows x64
machine or VM where scan output can be captured reliably.

Expanded Defender diagnostic evidence:
[`docs/windows-defender-diagnostics-dry-run-evidence.md`](windows-defender-diagnostics-dry-run-evidence.md)

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
signed-artifact Defender scan, and SmartScreen boundary steps were skipped in
this dry-run execution.

## Proven

- The Windows signing SmartScreen proof workflow is exposed on the repository
  default branch and can be manually dispatched.
- The workflow can download the previously proven Windows x64 CPU artifact.
- The downloaded zip matched the expected unsigned SHA256.
- The workflow can extract the unsigned source zip on a Windows runner.
- The workflow can inventory signable executable content and script launchers.
- Dry-run mode stops before certificate import, signing, timestamping,
  signed-smoke validation, signed-zip creation, and SmartScreen claims.
- Proof evidence was uploaded as a workflow artifact.

## Not Proven

- Defender acceptance.
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

## Next Safe Action

Fix or replace the Defender evidence path before running proof mode with Windows
signing secrets. Do not claim Defender acceptance or SmartScreen trust from this
dry-run evidence.
