# CPU Bundle Draft Release Staging Target

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `14b7d2283241203dca38475e90726bc8a28add9b`

Classification: docs / packaging evidence / durable storage staging decision

Decision: use draft GitHub Release assets as the next durable staging target for
the proven Windows x64 and macOS arm64 CPU bundled-Python smoke artifacts.

Draft release staging evidence:
[`docs/cpu-bundle-draft-release-staging-evidence.md`](cpu-bundle-draft-release-staging-evidence.md)

This decision does not publish downloads, move artifacts, create a public
release, or claim release readiness. It only selects the staging target for a
follow-up handoff evidence step.

## Selected Target

Use a draft GitHub Release in `dryheatwindbag/torch-ecpg` with assets attached
but not published.

Required draft release properties:

- Draft: yes.
- Public release: no.
- Prerelease: yes, if GitHub requires a release classification before publish.
- Tag: choose a non-versioned evidence tag, for example
  `cpu-bundle-evidence-YYYYMMDD`, unless a signed release tag is selected later.
- Title: `CPU bundle evidence staging YYYY-MM-DD`.
- Release notes: must state that the assets are smoke-test evidence artifacts,
  not public release downloads.

## Assets To Stage

Windows x64 CPU:

- Workflow run: `25173165547`
- Artifact name: `tecpg-windows-x64-cpu`
- Artifact ID: `6733486097`
- Zip: `tecpg-windows-x64-cpu.zip`
- SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`
- Checksum file: `SHA256SUMS.txt`

macOS arm64 CPU:

- Workflow run: `25176627794`
- Artifact name: `tecpg-macos-arm64-cpu`
- Artifact ID: `6734952276`
- Zip: `tecpg-macos-arm64-cpu.zip`
- SHA256:
  `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a`
- Checksum file: `SHA256SUMS.txt`

Because both artifacts contain a file named `SHA256SUMS.txt`, preserve platform
context in the staged release assets. Use one of these approaches:

- Upload each checksum as a platform-specific asset name, for example
  `SHA256SUMS-windows-x64-cpu.txt` and `SHA256SUMS-macos-arm64-cpu.txt`.
- Or upload a combined checksum file that records both zip names and hashes.

Do not rename the zip files before staging.

## Upload Handoff Procedure

1. Download both source artifacts from GitHub Actions using the commands in
   `docs/cpu-bundle-artifact-retention-plan.md`.
2. Verify each downloaded zip against its recorded SHA256 before upload.
3. Create the draft GitHub Release with release notes that preserve the
   boundaries in this document.
4. Upload the two zip files and checksum assets to the draft release.
5. Download the uploaded assets from the draft release.
6. Verify the downloaded draft-release assets against the recorded SHA256
   values.
7. Record the draft release URL, asset URLs, upload date, uploader, and
   post-upload verification output in a follow-up evidence PR.

## Draft Release Notes Boundary

The draft release notes must not claim:

- Release readiness.
- Public distribution readiness.
- Signing/notarization/quarantine behavior.
- Windows antivirus acceptance.
- GPU/CUDA support.
- Scientific correctness.
- Real-data execution.
- Long-running workload behavior.
- macOS x64 / Intel support.
- Linux desktop bundle support.

Allowed wording should stay limited to artifact retention, smoke-test evidence,
and next validation gates.

## Follow-Up Evidence Required

The follow-up handoff evidence PR should record:

- Draft release URL.
- Draft release tag.
- Asset names and URLs.
- Upload date.
- Uploader.
- Source workflow runs and artifact IDs.
- Source zip SHA256 values.
- Post-upload download and SHA256 verification output.
- Explicit statement that draft release staging does not prove public release
  readiness.

## Not Proven

- Artifact upload to the draft release.
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

## Next Safest Action

Create the draft GitHub Release, upload the verified CPU bundle assets, download
the staged assets back from the draft release, verify SHA256 again, and record
that evidence in a follow-up docs-only PR.
