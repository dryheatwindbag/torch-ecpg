# MVP Release Disposition Signoff

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `dev`

Base commit: `b75c1e1fea5f30aaa7f24163a85bb0775af908cc`

Classification: signoff / evidence / waiver

## Decision

MVP is accepted as closed for the `dryheatwindbag/torch-ecpg` fork at
`b75c1e1fea5f30aaa7f24163a85bb0775af908cc`, with the explicit boundaries and
waivers recorded below.

This signoff applies only to the fork. It does not change upstream
`kordk/torch-ecpg` and does not act on upstream PR #150 or PR #152.

## Scope Accepted

Accepted scope:

- fork-only stabilization and validation bridge work
- minimal-environment focused validation hardening
- dependency-present p-value and accuracy validation evidence
- full CLI/runtime smoke validation in a CPU dependency-present environment
- release/rollback disposition for continuing normal fork development

Out of scope for this MVP closeout:

- upstream merge or upstream release
- GPU performance recovery proof
- CUDA runtime proof
- real-dataset runtime or numeric proof
- production-scale runtime proof

## Implementation Accepted

Accepted implementation evidence:

- [PR #8](https://github.com/dryheatwindbag/torch-ecpg/pull/8): GPU monitor
  mock dependency hardening.
- [PR #9](https://github.com/dryheatwindbag/torch-ecpg/pull/9): GPU monitor
  direct execution hygiene.
- [PR #10](https://github.com/dryheatwindbag/torch-ecpg/pull/10):
  SciPy-missing p-value skip hygiene.
- [PR #11](https://github.com/dryheatwindbag/torch-ecpg/pull/11): auto-scale
  minimal-environment unittest hardening.
- [PR #12](https://github.com/dryheatwindbag/torch-ecpg/pull/12): accuracy
  validation optional-dependency skip.
- [PR #13](https://github.com/dryheatwindbag/torch-ecpg/pull/13): focused
  validation GitHub Actions workflow.
- [PR #15](https://github.com/dryheatwindbag/torch-ecpg/pull/15):
  dependency-present validation evidence.
- [PR #16](https://github.com/dryheatwindbag/torch-ecpg/pull/16): full CLI
  runtime smoke validation and manual MLR CLI kwargs fix.

PR #14 was closed unmerged and is explicitly not treated as GPU/runtime
evidence.

## Validation Accepted

Accepted validation evidence:

- Focused minimal-environment unittest bridge exists and runs in GitHub Actions
  on pull requests to `dev` and pushes to `dev`.
- Focused bridge installs only `pandas` and `numpy`, leaving optional heavy
  dependencies dependency-gated.
- SciPy-present p-value recalculation tests pass.
- Accuracy validation dependencies can be installed in an isolated environment.
- Accuracy validation runs instead of skipping when optional dependencies are
  present.
- Accuracy validation numeric behavior is acceptable for the test's documented
  estimate and t-statistic tolerances on generated synthetic data.
- Full `tecpg` CLI imports with real dependencies installed.
- CLI help/version commands run without import-time crashes.
- Logger/runtime dependency path initializes.
- `tecpg init`, `tecpg data dummy`, and CPU manual `tecpg run mlr` complete on
  a generated minimal dataset.

## GPU Evidence Waiver

GPU/runtime evidence is explicitly waived for this MVP closeout.

The waiver means:

- GPU/performance recovery is not proven.
- CUDA runtime behavior is not proven.
- PR #14 remains closed/unmerged and is not treated as evidence.
- If GPU proof becomes necessary later, run the existing GPU handoff on
  GPU-capable hardware before making GPU/CUDA claims.

## Rollback Plan

If a regression is found after this signoff:

1. Stop promoting the affected fork commit.
2. Identify the first bad merge commit using focused reproduction commands.
3. Prefer a targeted revert of the relevant fork PR merge commit.
4. Re-run the focused validation workflow and the specific regression command.
5. For CLI/runtime regressions, also re-run the full dependency CLI smoke from
   `docs/full-cli-runtime-smoke-evidence.md`.
6. Re-open release disposition only after the revert or forward fix is merged
   and validated.

Known rollback anchors:

- pre-PR #15 fork checkpoint:
  `45df28abfe3a00bc4028a6abfca5c4a2614bf455`
- post-PR #15 dependency-present evidence:
  `faed7d67d955eb70277d6fb58f1eeebe1227a3b0`
- post-PR #16 CLI/runtime smoke:
  `b75c1e1fea5f30aaa7f24163a85bb0775af908cc`

## Soak / Staged Rollout

Disposition: no production soak is claimed.

Staged rollout is accepted as:

1. continue normal fork development from current `dev`
2. keep focused validation workflow active on PRs and pushes to `dev`
3. require focused or full dependency validation for future changes touching
   validation, CLI, runtime dependency paths, or regression logic
4. require GPU-capable hardware evidence before accepting future GPU/CUDA claims

## Known Remaining Gaps

- GPU/performance recovery.
- CUDA runtime behavior.
- Real-dataset runtime behavior.
- Real-dataset numeric correctness.
- Production-scale runtime behavior.
- Upstream `kordk/torch-ecpg` changes.
- Upstream PR #150 or PR #152 action.

## Owner Signoff

Owner signoff is recorded for fork-only MVP closeout with the GPU/runtime waiver
and known gaps above.

Signed-off fork baseline:

`dryheatwindbag/torch-ecpg:dev`

`b75c1e1fea5f30aaa7f24163a85bb0775af908cc`
