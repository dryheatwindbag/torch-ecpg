# Fork GPU Run Handoff

This handoff is for executing fork-only GPU/performance validation on hardware
that can actually run the profile. It does not target `kordk/torch-ecpg`, reopen
upstream PR #150 or #152, prove upstream acceptance, prove release readiness,
prove GPU/performance recovery, or close MVP.

## Current Blocked Status

Repository:

```text
dryheatwindbag/torch-ecpg
```

Branch:

```text
dev
```

Current validated commit:

```text
8ccbcf740c0830cdd23b4955265ed910d2f7fff6
```

Current-machine evidence:

- baseline check passed: `HEAD` is at the required baseline
- unit tests passed:
  `python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle`
- compileall passed:
  `python3 -m compileall -q tecpg/pearson_full.py tests/test_process_pool_spawn.py tests/test_pearson_pool_lifecycle.py`
- `git status --short` was clean
- torch check failed: `ModuleNotFoundError: No module named 'torch'`
- `nvidia-smi` failed: command not found
- `tools/fork_gpu_performance_validation.sh --run-profiles` was not run because
  required GPU/CUDA prerequisites are unavailable

Conclusion: GPU/performance recovery is not proven. This is an environment
blocker, not an implementation failure.

## Required GPU Machine

Run on a machine with:

- NVIDIA GPU
- working `nvidia-smi`
- Python environment with `torch` installed
- `torch.cuda.is_available() == True`
- access to the `gtp` dataset, or a recorded substitute if `gtp` is unavailable

## Commands To Run

```bash
git checkout dev
git pull --ff-only
git rev-parse HEAD
git merge-base --is-ancestor 8ccbcf740c0830cdd23b4955265ed910d2f7fff6 HEAD
python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle
python3 -m compileall -q tecpg/pearson_full.py tests/test_process_pool_spawn.py tests/test_pearson_pool_lifecycle.py
git status --short
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
nvidia-smi
tools/fork_gpu_performance_validation.sh --run-profiles
```

Stop and report `BLOCKED` if `nvidia-smi`, `torch`, CUDA availability, dataset
access, or profiling fails.

## Required GPU Run Report

```text
Repository: dryheatwindbag/torch-ecpg
Branch:
Commit:
At or after 8ccbcf740c0830cdd23b4955265ed910d2f7fff6: yes/no

Machine/GPU:
Torch/CUDA:
nvidia-smi:

Preflight:
- unit tests:
- compileall:
- git status:
- torch CUDA check:
- nvidia-smi:

Evidence directory:
Generated artifacts:

Smoke profile:
- completed:
- result:

Realistic profile:
- dataset:
- completed:
- result:
- substitute used, if any:

Archive:
SHA256:

Conclusion:
- GPU/performance recovery proven: proven/not proven/inconclusive
- reason:
- remaining gap or follow-up:
```

Do not claim GPU/performance recovery unless the generated smoke and realistic
profile artifacts support that conclusion.
