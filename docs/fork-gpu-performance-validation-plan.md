# Fork GPU/Performance Validation Plan

This plan is for `dryheatwindbag/torch-ecpg:dev` after fork-only PR #2 merged at
`fdd2c18ad7a183c4592dfc2949b0f301c2e95da0`.

It does not target `kordk/torch-ecpg`, reopen upstream PR #150 or #152, prove
upstream acceptance, prove release readiness, or close MVP. It defines the
evidence needed to determine whether the fork's PR #130 follow-up work improved
GPU/performance behavior.

Current local validation status is tracked in
[`fork-gpu-performance-validation-status.md`](fork-gpu-performance-validation-status.md).

## Baseline Under Test

Use the fork baseline:

```bash
git clone https://github.com/dryheatwindbag/torch-ecpg.git
cd torch-ecpg
git checkout dev
git rev-parse HEAD
```

Expected minimum commit:

```text
fdd2c18ad7a183c4592dfc2949b0f301c2e95da0
```

If `HEAD` is newer, confirm it is a descendant:

```bash
git merge-base --is-ancestor fdd2c18ad7a183c4592dfc2949b0f301c2e95da0 HEAD
```

## Preflight Checks

Run these before performance profiling:

```bash
python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle
python3 -m compileall -q tecpg/pearson_full.py tests/test_process_pool_spawn.py tests/test_pearson_pool_lifecycle.py
git status --short
```

Expected result:

- both unittest cases pass
- compileall exits with status 0
- `git status --short` is empty

## Required Environment Evidence

Record these facts in the validation report:

```bash
git rev-parse HEAD
python3 --version
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
nvidia-smi
```

Also record:

- GPU model and driver/CUDA versions from `nvidia-smi`
- dataset mode used: `dummy`, `gtp`, or `mesa`
- command line used for profiling
- whether `CUDA_VISIBLE_DEVICES` was set
- values for `--save-threads`, `--prefetch-chunks`, `--blas-threads`, `-g`, and `-s`

## Smoke Profile

Run a short synthetic profile first:

```bash
./profiling.sh -d dummy -D 90 --gpu-index 0 --no-nsys --no-nvprof
```

Save the generated archive path, SHA256, and `chunk_profile_summary.txt`.

Pass condition:

- profiling completes
- archive is produced
- `chunk_profile_summary.txt` exists
- `nvidia-smi-query.csv` exists
- no process-pool lifecycle exception occurs

This smoke profile does not prove GPU recovery.

## Recovery Profile

Run a realistic matrix profile when GPU hardware and data are available:

```bash
./profiling.sh -d gtp -D 600 --matrix --gpu-index 0
```

If `gtp` is unavailable, use the closest available realistic dataset and record
the substitution.

Collect these artifacts:

- generated `.tar.gz` archive
- archive SHA256
- `matrix_summary.csv`
- each run's `chunk_profile_summary.txt`
- each run's `nvidia-smi-query.csv`
- each run's `pidstat.csv`
- `env.txt`

## Acceptance Evidence

GPU/performance recovery is only supported when the report includes:

- the fork commit under test
- successful preflight checks
- smoke profile artifacts
- realistic profile artifacts
- a comparison of baseline, prefetch, BLAS, and chunk-size cells from
  `matrix_summary.csv`
- GPU utilization evidence from `nvidia-smi-query.csv`
- bottleneck verdicts from `chunk_profile_summary.txt`
- an explicit conclusion that distinguishes compute-bound, host-bound,
  save-bound, transfer-bound, thermal/power-throttled, and inconclusive results

Do not treat import checks, compile checks, or the synthetic smoke profile alone
as GPU/performance recovery proof.

## Report Template

```text
Repository: dryheatwindbag/torch-ecpg
Branch: dev
Commit:
GPU:
Driver/CUDA:
Dataset:
Command:
Artifacts:
Archive SHA256:

Preflight:
- unittest:
- compileall:
- git status:

Smoke profile:
- completed:
- archive:
- summary verdict:

Realistic profile:
- completed:
- matrix_summary.csv:
- best cell:
- worst cell:
- bottleneck verdict:
- GPU utilization evidence:

Conclusion:
- GPU/performance recovery proven: yes/no
- If no, reason:
- Follow-up:
```

## Remaining Gaps Until This Plan Is Run

- upstream `kordk/torch-ecpg` remains unchanged
- upstream PR #150 and #152 are superseded only for this workflow
- GPU/performance recovery is not proven
- MVP closeout is not claimed
