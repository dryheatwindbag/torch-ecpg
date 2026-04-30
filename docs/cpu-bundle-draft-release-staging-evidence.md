# CPU Bundle Draft Release Staging Evidence

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `8779f4f004b4d9c32ef85c921b7a0c06f2c653e0`

Classification: docs / packaging evidence / durable staging evidence

Scope: record the draft GitHub Release staging of the proven Windows x64 and
macOS arm64 CPU bundled-Python smoke artifacts, including post-upload download
and SHA256 verification.

This evidence does not publish downloads, make the draft release public, or
claim release readiness.

## Draft Release

- Draft release tag: `cpu-bundle-evidence-20260430`
- Draft release title: `CPU bundle evidence staging 2026-04-30`
- Draft release URL:
  `https://github.com/dryheatwindbag/torch-ecpg/releases/tag/untagged-81f2655c11a52e889f0f`
- GitHub release ID: `315971891`
- Draft: `true`
- Prerelease: `true`
- Published at: `null`
- Target commit: `8779f4f004b4d9c32ef85c921b7a0c06f2c653e0`
- Created at: `2026-04-30T18:04:10Z`
- Uploader / release author: `dryheatwindbag`

The draft release notes state that the staged assets are smoke-test evidence
artifacts only and are not public release downloads.

## Source Artifacts

Windows x64 CPU:

- Workflow run: `25173165547`
- Artifact name: `tecpg-windows-x64-cpu`
- Artifact ID: `6733486097`
- Zip: `tecpg-windows-x64-cpu.zip`
- Expected SHA256:
  `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd`

macOS arm64 CPU:

- Workflow run: `25176627794`
- Artifact name: `tecpg-macos-arm64-cpu`
- Artifact ID: `6734952276`
- Zip: `tecpg-macos-arm64-cpu.zip`
- Expected SHA256:
  `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a`

## Staged Assets

| Asset | Asset API ID | Size | GitHub digest |
| --- | --- | --- | --- |
| `tecpg-windows-x64-cpu.zip` | `409256968` | `413719424` bytes | `sha256:19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd` |
| `tecpg-macos-arm64-cpu.zip` | `409256966` | `344970403` bytes | `sha256:a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a` |
| `SHA256SUMS-windows-x64-cpu.txt` | `409256962` | `93` bytes | `sha256:f9b31cb85dff080ecb2adadbe1c2dae68328210661e7e50d7470a188e2f47788` |
| `SHA256SUMS-macos-arm64-cpu.txt` | `409256965` | `92` bytes | `sha256:9595220bd01574958d49df026d09aa3bf595e6ea02f679ff1bf1f3354cebf93c` |
| `SHA256SUMS-cpu-bundles.txt` | `409256967` | `185` bytes | `sha256:d17a374b7d1bd1cde8ec9dcb37d489b1362104c0da7308c8da458507871e5d8e` |

Draft release asset URLs:

```text
https://github.com/dryheatwindbag/torch-ecpg/releases/download/untagged-81f2655c11a52e889f0f/tecpg-windows-x64-cpu.zip
https://github.com/dryheatwindbag/torch-ecpg/releases/download/untagged-81f2655c11a52e889f0f/tecpg-macos-arm64-cpu.zip
https://github.com/dryheatwindbag/torch-ecpg/releases/download/untagged-81f2655c11a52e889f0f/SHA256SUMS-windows-x64-cpu.txt
https://github.com/dryheatwindbag/torch-ecpg/releases/download/untagged-81f2655c11a52e889f0f/SHA256SUMS-macos-arm64-cpu.txt
https://github.com/dryheatwindbag/torch-ecpg/releases/download/untagged-81f2655c11a52e889f0f/SHA256SUMS-cpu-bundles.txt
```

## Post-Upload Verification

After upload, the staged assets were downloaded from the draft release with:

```sh
gh release download cpu-bundle-evidence-20260430 \
  --repo dryheatwindbag/torch-ecpg \
  --dir /tmp/torch-ecpg-draft-release-assets-20260430/release-download
```

The downloaded draft-release assets were verified with `shasum -a 256`.

Verification output:

```text
Draft release download verification passed
Windows: 19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd
macOS: a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a
```

The platform-specific checksum files and combined checksum file contained:

```text
19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd  tecpg-windows-x64-cpu.zip
a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a  tecpg-macos-arm64-cpu.zip
```

## Proven

- The two source GitHub Actions artifacts were still available for download.
- The source artifact zips matched their recorded SHA256 values before staging.
- A draft, prerelease GitHub Release was created for evidence staging.
- The Windows x64 CPU zip and macOS arm64 CPU zip were uploaded as draft
  release assets.
- Platform-specific checksum assets and a combined checksum asset were uploaded.
- The uploaded draft-release assets were downloaded back from GitHub.
- The downloaded draft-release zips matched the expected SHA256 values.

## Not Proven

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
