# Windows CPU Bundle Artifact Retention Procedure

Repository: `dryheatwindbag/torch-ecpg`

Classification: docs / packaging evidence / retention procedure

Scope: document how to retrieve, preserve, and verify the Windows x64 CPU
bundle artifact produced by GitHub Actions.

This procedure does not claim release readiness, signing, notarization,
antivirus validation, GPU/CUDA support, macOS support, scientific correctness,
real-data execution, or public distribution readiness.

## Source Evidence

- Source workflow run:
  `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25173165547`
- Artifact name: `tecpg-windows-x64-cpu`
- Artifact ID: `6733486097`
- Zip name: `tecpg-windows-x64-cpu.zip`
- Known SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`

## Download From GitHub Actions

1. Open the source workflow run in GitHub Actions:
   `https://github.com/dryheatwindbag/torch-ecpg/actions/runs/25173165547`.
2. In the run summary, find the artifact named `tecpg-windows-x64-cpu`.
3. Download the artifact to a clean local evidence directory and extract it if
   GitHub provides the artifact as a wrapper archive.
4. Confirm that the extracted artifact contents include
   `tecpg-windows-x64-cpu.zip` and `SHA256SUMS.txt`.
5. Keep the bundle zip name as `tecpg-windows-x64-cpu.zip`.
6. Record the download date, GitHub run URL, artifact name, artifact ID, and
   local file path in the evidence notes for the retention location.

The same artifact can also be downloaded with GitHub CLI:

```sh
gh run download 25173165547 \
  --repo dryheatwindbag/torch-ecpg \
  --name tecpg-windows-x64-cpu \
  --dir evidence/windows-cpu-bundle-25173165547
```

If the artifact is no longer available through the GitHub Actions web UI, use
the artifact ID and GitHub API or GitHub CLI to determine whether it has expired
or whether repository retention settings removed it. Do not replace the artifact
with a rebuilt zip without creating a new evidence record for the new workflow
run.

## Verify The Checksum

Unpack or inspect the downloaded artifact bundle and locate `SHA256SUMS.txt`.
The expected checksum entry is:

```text
19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd  tecpg-windows-x64-cpu.zip
```

From the directory containing both `SHA256SUMS.txt` and
`tecpg-windows-x64-cpu.zip`, verify the checksum with one of these commands.

On Windows PowerShell:

```powershell
$expected = "19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd"
$actual = (Get-FileHash -Algorithm SHA256 .\tecpg-windows-x64-cpu.zip).Hash.ToLowerInvariant()
if ($actual -ne $expected) {
    throw "SHA256 mismatch: expected $expected but got $actual"
}
"SHA256 verified for tecpg-windows-x64-cpu.zip"
```

On Linux:

```sh
sha256sum -c SHA256SUMS.txt
```

On macOS:

```sh
expected="19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd"
actual="$(shasum -a 256 tecpg-windows-x64-cpu.zip | awk '{print $1}')"
test "$actual" = "$expected"
```

The verification passes only when the computed SHA256 for
`tecpg-windows-x64-cpu.zip` matches the known SHA256 from `SHA256SUMS.txt`.

## Preserve In A Durable Location

When a durable release or evidence location is selected later, preserve these
items together:

- `tecpg-windows-x64-cpu.zip`
- `SHA256SUMS.txt`
- The source workflow run URL
- The artifact name, artifact ID, zip name, and known SHA256
- The date the artifact was downloaded from GitHub Actions
- The verification command and output used to confirm the checksum

The durable location should be access-controlled according to the release
process and should not rename or mutate the zip after verification. If a
different filename or storage layout is required, record the original zip name
and checksum beside the preserved object so the artifact remains traceable to
the source workflow run.

## Boundaries

This retention procedure only preserves and verifies the Windows x64 CPU bundle
artifact identified above. It does not prove:

- Release readiness.
- Signing, notarization, or antivirus validation.
- GPU/CUDA support.
- macOS support.
- Scientific correctness.
- Real-data execution.
- Public distribution readiness.
- Long-running workload behavior from the bundle.
