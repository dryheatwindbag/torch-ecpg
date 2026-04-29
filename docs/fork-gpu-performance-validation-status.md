# Fork GPU/Performance Validation Status

Status date: 2026-04-29

This status applies only to `dryheatwindbag/torch-ecpg:dev`. It does not target
`kordk/torch-ecpg`, reopen upstream PR #150 or #152, prove upstream acceptance,
prove GPU/performance recovery, prove release readiness, or close MVP.

## Baseline Checked

Repository:

```text
dryheatwindbag/torch-ecpg
```

Branch:

```text
dev
```

Commit checked:

```text
54352adf36b6e691f40361ded9f8f0ee318b308b
```

## Local Preflight Result

Passed:

```bash
python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle
```

Observed result:

```text
Ran 2 tests in 0.296s
OK
```

Passed:

```bash
python3 -m compileall -q tecpg/pearson_full.py tests/test_process_pool_spawn.py tests/test_pearson_pool_lifecycle.py
```

Passed:

```bash
git status --short
```

Observed result: clean working tree.

## Environment Blocker

GPU/performance profiling could not be run in this environment.

Observed blockers:

```text
nvidia-smi: command not found
ModuleNotFoundError: No module named 'torch'
```

Because of those blockers, the smoke profile and realistic recovery profile in
`docs/fork-gpu-performance-validation-plan.md` were not executed.

## Evidence Boundary

The local preflight proves only that:

- the fork baseline is checked out
- the spawn smoke unittest passes
- the pearson pool lifecycle regression unittest passes
- the touched Python files compile
- the local working tree is clean

The local preflight does not prove:

- GPU/performance recovery
- real GPU utilization behavior
- realistic workload throughput
- upstream `kordk/torch-ecpg` acceptance
- release readiness
- MVP closeout

## Next Required Evidence

Run the validation plan on a machine with:

- NVIDIA GPU hardware
- working `nvidia-smi`
- installed Python dependencies, including `torch`
- access to the realistic `gtp` dataset or the closest available substitute

Start with the smoke profile:

```bash
./profiling.sh -d dummy -D 90 --gpu-index 0 --no-nsys --no-nvprof
```

Then run the realistic matrix profile:

```bash
./profiling.sh -d gtp -D 600 --matrix --gpu-index 0
```

GPU/performance recovery remains unproven until the generated artifacts and
summary verdicts support that conclusion.
