# CPU Bundle Artifact Retention Plan

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `d9db9233a6385e13dcdd16b581a493927c190ff0`

Classification: docs / packaging evidence / retention plan

Scope: define a repeatable download, verification, and durable storage handoff
for the currently proven Windows x64 and macOS arm64 CPU bundled-Python smoke
artifacts.

Public distribution risk plan:
[`docs/cpu-bundle-public-distribution-risk-plan.md`](cpu-bundle-public-distribution-risk-plan.md)

This plan does not claim release readiness, public distribution readiness,
signing/notarization/quarantine behavior, Windows antivirus behavior, GPU/CUDA
support, scientific correctness, real-data execution, long-running workload
behavior, macOS x64 / Intel support, or Linux desktop bundle support.

## Source Artifacts

| Platform | Workflow run | Artifact name | Artifact ID | Zip | SHA256 |
| --- | --- | --- | --- | --- | --- |
| Windows x64 CPU | `25173165547` | `tecpg-windows-x64-cpu` | `6733486097` | `tecpg-windows-x64-cpu.zip` | `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd` |
| macOS arm64 CPU | `25176627794` | `tecpg-macos-arm64-cpu` | `6734952276` | `tecpg-macos-arm64-cpu.zip` | `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a` |

## Download Procedure

Create a clean local evidence directory:

```sh
mkdir -p evidence/cpu-bundles
```

Download the Windows x64 CPU artifact:

```sh
gh run download 25173165547 \
  --repo dryheatwindbag/torch-ecpg \
  --name tecpg-windows-x64-cpu \
  --dir evidence/cpu-bundles/windows-x64-25173165547
```

Download the macOS arm64 CPU artifact:

```sh
gh run download 25176627794 \
  --repo dryheatwindbag/torch-ecpg \
  --name tecpg-macos-arm64-cpu \
  --dir evidence/cpu-bundles/macos-arm64-25176627794
```

Each downloaded directory must contain the bundle zip and `SHA256SUMS.txt`.
Do not rename or mutate the zip before checksum verification.

If either GitHub Actions artifact has expired or is unavailable, do not rebuild
or substitute a new artifact under the old evidence record. Create a new
workflow run and a new evidence record for the replacement artifact.

## Checksum Verification

From the Windows artifact directory:

```sh
cd evidence/cpu-bundles/windows-x64-25173165547
expected="19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd"
actual="$(shasum -a 256 tecpg-windows-x64-cpu.zip | awk '{print $1}')"
test "$actual" = "$expected"
grep "$expected  tecpg-windows-x64-cpu.zip" SHA256SUMS.txt
```

From the macOS artifact directory:

```sh
cd evidence/cpu-bundles/macos-arm64-25176627794
expected="a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a"
actual="$(shasum -a 256 tecpg-macos-arm64-cpu.zip | awk '{print $1}')"
test "$actual" = "$expected"
grep "$expected  tecpg-macos-arm64-cpu.zip" SHA256SUMS.txt
```

On Linux, `sha256sum -c SHA256SUMS.txt` may be used instead of `shasum` from
the directory containing each zip and checksum file.

On Windows PowerShell, use `Get-FileHash -Algorithm SHA256` and compare the
lowercase hash to the expected SHA256 listed above.

## Durable Storage Handoff

When a durable storage location is selected, preserve these files and metadata
together for each platform:

- Bundle zip.
- `SHA256SUMS.txt`.
- Workflow run URL.
- Artifact name and artifact ID.
- Evidence PR number.
- Source branch and commit under test.
- Download date.
- Checksum verification command and output.
- Storage object path or release asset URL.

Recommended durable layout:

```text
cpu-bundles/
  windows-x64/
    25173165547/
      tecpg-windows-x64-cpu.zip
      SHA256SUMS.txt
      retention-notes.md
  macos-arm64/
    25176627794/
      tecpg-macos-arm64-cpu.zip
      SHA256SUMS.txt
      retention-notes.md
```

`retention-notes.md` should record the source workflow run, artifact ID,
evidence PR, checksum verification output, and durable storage URL or object
identifier. If a release asset or storage system requires a different layout,
record the original filename, source run, and SHA256 beside the stored object.

## Promotion Gate

Before any artifact is promoted from evidence storage to a release handoff,
confirm:

- The artifact was downloaded from the recorded GitHub Actions run.
- The zip SHA256 matches the recorded `SHA256SUMS.txt`.
- The durable location stores the zip and checksum together.
- The durable location has a documented access and retention policy.
- The handoff notes preserve the original workflow run and artifact ID.
- Release notes do not claim readiness beyond the evidence already recorded.

## Boundaries

This retention plan preserves smoke-tested CPU bundle artifacts only. It does
not prove:

- Release readiness.
- Public distribution readiness.
- Signing/notarization/quarantine behavior.
- Windows antivirus behavior.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Long-running workload behavior.
- macOS x64 / Intel support unless separately validated.
- Linux desktop bundle unless separately validated.

## Next Safest Options

Option A: implement the durable storage handoff once the target storage system
is chosen.

Option B: add a signing/notarization/quarantine and Windows antivirus risk plan
before any public distribution claim.

Option C: add macOS x64 CPU bundle workflow/evidence only if Intel Mac support
is required.

Recommended next step:

- Option A first if reliable internal download handoff is the immediate goal.
- Option B first if public release readiness is the goal.
- Option C first only if Intel Mac support is a requirement.
