# CPU Bundle Durable Storage Target Decision

Repository: `dryheatwindbag/torch-ecpg`

Current `dev` commit: `458f3f5d473cc407a43f06181844b45e4dcaf445`

Classification: docs / packaging evidence / durable storage decision gate

Scope: select the next decision gate for preserving the proven Windows x64 and
macOS arm64 CPU bundled-Python smoke artifacts outside GitHub Actions artifact
retention.

This decision gate does not move artifacts, create release assets, publish
downloads, or claim release readiness.

Selected staging target:
[`docs/cpu-bundle-draft-release-staging-target.md`](cpu-bundle-draft-release-staging-target.md)

## Current Artifact Sources

| Platform | Workflow run | Artifact name | Artifact ID | Zip | SHA256 |
| --- | --- | --- | --- | --- | --- |
| Windows x64 CPU | `25173165547` | `tecpg-windows-x64-cpu` | `6733486097` | `tecpg-windows-x64-cpu.zip` | `19ad9df4ab404fbffc89a5a3c20b12d938f18eeab52be9567bbdc493e6d308fd` |
| macOS arm64 CPU | `25176627794` | `tecpg-macos-arm64-cpu` | `6734952276` | `tecpg-macos-arm64-cpu.zip` | `a3595cf2d05de093aadee5b46614c65587387a5ea0fe3146427edb850712de6a` |

The current evidence proves smoke-tested CPU bundle artifacts only. GitHub
Actions artifacts are not the durable storage target because their retention is
time-limited and controlled by repository settings.

## Candidate Targets

### Option A: Internal Object Storage

Use an access-controlled bucket or object store controlled by the project owner.

Pros:

- Clear durable retention policy can be configured outside GitHub Actions.
- Access can remain private while release readiness is unresolved.
- Object metadata can include source run, artifact ID, SHA256, and evidence PR.

Risks:

- Requires an existing storage account, owner, and access policy.
- Requires manual or scripted upload procedure.
- Public download URLs should not be enabled until release gates pass.

### Option B: Draft GitHub Release Assets

Attach the zips and checksums to a draft GitHub Release that is not published.

Pros:

- Keeps artifacts near repository evidence and tags.
- GitHub release assets are easier for maintainers to inspect.
- A draft release can stay private to repository collaborators.

Risks:

- Draft release assets are close to public-release workflow and may be confused
  with distribution readiness.
- Requires careful release-note wording to avoid readiness claims.
- A release tag or naming convention must be selected.

### Option C: Repository-External Evidence Archive

Store the zips and checksums in an internal evidence archive such as a shared
drive, artifact vault, or records system.

Pros:

- Good fit when the goal is audit retention rather than distribution.
- Can preserve verification notes and review records beside artifacts.

Risks:

- Discoverability may be weaker than object storage or GitHub release assets.
- Access policy and retention duration may be informal unless documented.
- Future release handoff may require copying artifacts again.

## Selection Criteria

Select a durable target only after these questions have answers:

- Who owns the storage location?
- Who can upload artifacts?
- Who can download artifacts?
- What is the minimum retention duration?
- Are public URLs disabled until release-readiness gates pass?
- Can the storage record preserve source workflow run, artifact ID, SHA256, and
  evidence PR?
- Can the zip and `SHA256SUMS.txt` be stored together without renaming or
  mutation?
- Is there an audit trail for upload date and uploader?

## Recommended Decision

Use Option A, internal object storage, if a suitable project-controlled bucket
or object store already exists.

Use Option B, draft GitHub Release assets, only if the team wants a repository
native staging area and accepts the extra release-wording discipline.

Use Option C, repository-external evidence archive, only if audit retention is
the immediate goal and release handoff can wait.

## Required Handoff Evidence

After a target is selected and artifacts are uploaded, record:

- Durable storage target name and owner.
- Storage object path or draft release asset URL.
- Upload date.
- Uploader.
- Source workflow run.
- Artifact name and artifact ID.
- Zip name and SHA256.
- `SHA256SUMS.txt` content.
- Verification command and output after download from the durable target.
- Explicit statement that the storage handoff does not prove public release
  readiness.

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

## Next Safest Action

Choose one storage target and open a follow-up evidence PR that records the
actual artifact upload, durable location, and post-upload checksum verification.
