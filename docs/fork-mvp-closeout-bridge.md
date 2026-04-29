# Fork MVP Closeout Bridge

Classification: fork-only waiver / signoff / evidence / closeout bridge

This document is a fork-only closeout bridge for `dryheatwindbag/torch-ecpg`.
It does not target `kordk/torch-ecpg`, does not claim upstream acceptance, does
not claim release readiness proven by GPU evidence, and does not claim full MVP
closeout based on GPU validation.

## Scope

- Fork-only.
- Applies only to `dryheatwindbag/torch-ecpg`.
- Active fork branch: `dev`.
- Latest fork `dev` commit at bridge creation:
  `4f86f94894727e08e568a3d71a7854ee44c66c69`.
- Upstream `kordk/torch-ecpg` is not changed by this disposition.
- Upstream PR #150 and PR #152 are superseded only for this fork workflow, not
  merged upstream.

## Resolved In Fork

- PR #130 root-level scratch artifacts were removed:
  - `dummy.py`
  - `test_imports.py`
  - `test_mocked.py`
  - `test_pool.py`
- The `tecpg/pearson_full.py` process-pool lifecycle defect was fixed.
- `tests/test_process_pool_spawn.py` was added for spawn/pickling smoke
  coverage.
- `tests/test_pearson_pool_lifecycle.py` was added for the pearson pool
  lifecycle regression guard.
- The GPU validation plan was added.
- The GPU validation helper was added.
- The blocked GPU validation handoff was documented.

## Evidence

- Merged fork PR #2: cleanup plus lifecycle fix.
- Merged fork PR #3: GPU validation plan.
- Commit `8ccbcf740c0830cdd23b4955265ed910d2f7fff6`: GPU validation helper is
  present in fork `dev`.
- Merged fork PR #6: blocked GPU validation handoff.
- Latest fork `dev` commit at bridge creation:
  `4f86f94894727e08e568a3d71a7854ee44c66c69`.

Supporting documents:

- `docs/fork-gpu-performance-validation-plan.md`
- `docs/fork-gpu-performance-validation-status.md`
- `docs/fork-gpu-run-handoff.md`
- `tools/fork_gpu_performance_validation.sh`

## Validation Completed

Focused non-GPU validation has passed where recorded:

```bash
python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle
```

```bash
python3 -m compileall -q tecpg/pearson_full.py tests/test_process_pool_spawn.py tests/test_pearson_pool_lifecycle.py
```

```bash
git diff --check
git status --short
```

```bash
bash -n tools/fork_gpu_performance_validation.sh
```

The recorded current-machine blocker is:

- `torch` is unavailable: `ModuleNotFoundError: No module named 'torch'`.
- `nvidia-smi` is unavailable: command not found.
- `tools/fork_gpu_performance_validation.sh --run-profiles` was not run because
  required GPU/CUDA prerequisites are unavailable.

## Waiver / Deferred Validation

GPU/performance runtime validation is deferred, not proven. The current
environment cannot perform the validation because torch and nvidia-smi are
unavailable. This is accepted as a scoped fork-only defer/waiver for continuing
work. If GPU behavior becomes release-critical, run
`docs/fork-gpu-run-handoff.md` on GPU-capable hardware before claiming GPU
recovery.

This disposition allows normal fork work to continue from
`dryheatwindbag:dev`. It does not convert the missing GPU runtime artifacts into
GPU/performance proof.

## Remaining Open Issues

- Upstream `kordk/torch-ecpg` remains unchanged.
- Upstream PR #150 and PR #152 are superseded only for this fork workflow.
- GPU/performance recovery is not proven.
- Upstream acceptance is not present.
- Production release evidence is not present.
- Soak or staged rollout evidence is not present unless separately supplied.

## Next Safe Action

- Continue normal fork development from `dryheatwindbag:dev`.
- Do not open more PR #130 cleanup, lifecycle, or GPU-planning branches unless
  new evidence appears.
- If GPU proof becomes necessary, run the existing GPU handoff instead of
  changing implementation.

## Not Claimed

- GPU/performance recovery proven.
- Upstream `kordk/torch-ecpg` changed.
- Upstream PR #150 or PR #152 merged.
- Release readiness proven by GPU evidence.
- Full MVP closeout based on GPU validation.
