# macOS Notarization Proof Dry-Run Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `main`

Workflow source commit: `569292283a638677bdde711342a8633ddd553afe`

Classification: workflow evidence / macOS signing proof / dry-run validation

Scope: record the first dry-run execution of the macOS notarization proof
workflow against the previously proven macOS arm64 CPU zip artifact.

This evidence does not sign files, submit notarization, import certificates,
staple artifacts, publish release assets, change artifact format, claim release
readiness, or claim public distribution readiness.

## Workflow Run

- Workflow: `macOS Notarization Proof`
- Trigger: `workflow_dispatch`
- Mode: `dry_run: "true"`
- Run URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25191662840`
- Run result: `success`
- Branch under test: `main`
- Commit under test: `569292283a638677bdde711342a8633ddd553afe`
- Job: `macOS notarization proof`
- Job result: `success`
- Job URL:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25191662840/job/73862843742`
- Job duration: `3m23s`

## Source Artifact

- Source workflow run: `25176627794`
- Source artifact name: `tecpg-macos-arm64-cpu`
- Bundle name: `tecpg-macos-arm64-cpu`
- Source zip: `tecpg-macos-arm64-cpu.zip`
- Expected unsigned SHA256:
  `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a`

The dry-run evidence artifact recorded:

```text
a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a  tecpg-macos-arm64-cpu.zip
```

The workflow compared the downloaded zip against the provided expected SHA256
and the downloaded `SHA256SUMS.txt`.

## Completed Steps

The successful dry-run job completed:

- macOS arm64 runner confirmation.
- Source artifact download.
- Unsigned source checksum verification.
- Source zip extraction.
- Signable-content inventory.
- Dry-run boundary recording.
- Proof evidence artifact upload.

The proof evidence artifact was named:
`macos-notarization-proof-evidence`.

## Signable-Content Inventory

The dry-run evidence artifact recorded:

- Mach-O files: `317`
- Executable non-Mach-O files: `147`
- Total inventoried executable/signing-relevant files: `464`

The non-Mach-O executable inventory included script launch paths such as:

```text
proof/work/tecpg-macos-arm64-cpu/python/bin/tecpg
```

The Mach-O inventory included embedded Python runtime paths such as:

```text
proof/work/tecpg-macos-arm64-cpu/python/bin/python3
proof/work/tecpg-macos-arm64-cpu/python/bin/python
proof/work/tecpg-macos-arm64-cpu/python/bin/python3.11
```

The full inventory is preserved in the workflow evidence artifact rather than
copied into this repository.

## Dry-Run Boundary

The dry-run boundary file recorded:

```text
Dry run completed.
No certificate was imported.
No files were signed.
No notarization request was submitted.
```

The signing, signed-smoke, repackaging, notarization, no-staple, and `spctl`
steps were skipped in this dry-run execution.

## Runner Warning

The workflow emitted a GitHub Actions annotation warning that Node.js 20
actions are deprecated for `actions/checkout@v4` and `actions/upload-artifact@v4`.
This warning did not fail the dry run. It should be tracked separately from
macOS signing/notarization evidence.

## Proven

- The notarization proof workflow is exposed on the repository default branch
  and can be manually dispatched.
- The workflow can download the previously proven macOS arm64 CPU artifact.
- The downloaded zip matched the expected unsigned SHA256.
- The workflow can extract the unsigned source zip on a macOS arm64 runner.
- The workflow can inventory Mach-O and executable non-Mach-O content in the
  extracted bundle.
- Dry-run mode stops before certificate import, signing, notarization,
  stapling, signed-smoke validation, and `spctl` assessment.
- Proof evidence was uploaded as a workflow artifact.

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

Before running proof mode, review whether the inventory scope is acceptable for
the first signing proof. If acceptable, run the workflow once with
`dry_run: "false"` and Apple signing secrets configured. If the inventory scope
is too broad, narrow the signing selection in a separate workflow PR before
using signing secrets.

Proof-mode secret readiness:
[`docs/macos-notarization-proof-mode-secret-readiness.md`](macos-notarization-proof-mode-secret-readiness.md)

Proof-mode evidence template:
[`docs/macos-notarization-proof-evidence-template.md`](macos-notarization-proof-evidence-template.md)
