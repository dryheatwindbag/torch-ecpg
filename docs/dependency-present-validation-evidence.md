# Dependency-Present Validation Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `dev`

Base commit: `45df28abfe3a00bc4028a6abfca5c4a2614bf455`

Classification: validation / evidence

Scope: close the focused CI bridge `skipped=3` evidence boundary by running the
SciPy-present p-value tests and the optional-dependency accuracy validation path
in an isolated dependency-present Python environment.

This is independent of the parked GPU/runtime evidence PR #14. It does not
reopen cleanup, lifecycle, GPU bridge, or minimal-environment hardening work.

## Environment

The run used an isolated virtual environment at `/tmp/torch-ecpg-pr15-venv`.

Installed validation package versions:

| Package | Version |
| --- | --- |
| `scipy` | `1.17.1` |
| `torch` | `2.11.0` |
| `statsmodels` | `0.14.6` |
| `matplotlib` | `3.10.9` |
| `pandas` | `3.0.2` |
| `numpy` | `2.4.4` |
| `requests` | `2.33.1` |

Torch CUDA availability in this environment: `False`.

## Commands And Results

```bash
/tmp/torch-ecpg-pr15-venv/bin/python -m unittest tests.test_recalculate_pvalues
```

Result: `Ran 2 tests in 3.273s`, `OK`.

```bash
/tmp/torch-ecpg-pr15-venv/bin/python -m unittest tests.test_accuracy
```

Result: `Ran 1 test in 0.000s`, `OK`.

```bash
/tmp/torch-ecpg-pr15-venv/bin/python -m unittest \
  tests.test_accuracy \
  tests.test_auto_scale \
  tests.test_recalculate_pvalues \
  tests.test_process_pool_spawn \
  tests.test_pearson_pool_lifecycle \
  tests.test_gpu_monitor_mock
```

Result: `Ran 9 tests in 3.505s`, `OK`.

```bash
/tmp/torch-ecpg-pr15-venv/bin/python tests/test_accuracy.py
```

Result: direct accuracy validation ran instead of skipping. It completed both
Beta-value and M-value validation paths, generated CSV reports and plots, and
reported `SUCCESS: Estimates and T-statistics match within tolerance` for both
paths.

## Numeric Evidence

The accuracy validation compares `tecpg` regression output against
`statsmodels.OLS` on generated synthetic data. The acceptance criteria in the
test are:

- estimate absolute difference <= `2e-4`
- t-statistic absolute difference <= `1e-3`

Observed summary:

| Path | Metric | Mean Difference | Max Difference |
| --- | --- | ---: | ---: |
| Beta-values | `diff_est` | `4.36216946438e-05` | `1.73186056474e-04` |
| Beta-values | `diff_err` | `5.51703641536e-06` | `1.6166728237e-05` |
| Beta-values | `diff_t` | `4.18602140707e-06` | `1.52630400661e-05` |
| Beta-values | `diff_p` | `1.56593178395e-03` | `3.28964021442e-03` |
| M-values | `diff_est` | `8.36857610058e-07` | `6.58117162478e-06` |
| M-values | `diff_err` | `1.92864941665e-07` | `2.13531599935e-06` |
| M-values | `diff_t` | `7.48801066455e-07` | `4.84541678802e-06` |
| M-values | `diff_p` | `1.66758204408e-03` | `3.28774058357e-03` |

The p-value differences are expected in this validation because `tecpg` uses a
normal approximation while the independent `statsmodels` comparison reports
Student-t p-values.

## Generated Artifact Hashes

The direct accuracy validation generated these local artifacts during the run:

| Artifact | SHA256 |
| --- | --- |
| `validation_report.csv` | `93c5cd982e5374eff711dcd075feda18dc2e1682783cc4c7211bffa926784248` |
| `validation_report_transformed.csv` | `70d7e8953e9b201456bbd085d35d4413353d68cf8a3520d5db96e675974f3b57` |
| `tests/plots/accuracy_est_comparison.png` | `3dd53d210e26810de93ddcd7a1f226da057c26b0d88e22c5a31ee7aad77a780a` |
| `tests/plots/accuracy_err_comparison.png` | `9bdbd0a36274ad68130c1c82226029571321a94ca0fd1e4d5eca7c637577a94a` |
| `tests/plots/accuracy_t_comparison.png` | `2600bf26e77140289820a603c9a2d8592f488b37cb77669dc93c9a63115dac81` |
| `tests/plots/accuracy_p_comparison.png` | `0f66befe0133b340c49d41a179f28ecece254bc0034d10a2be133ff38d650025` |
| `tests/plots/accuracy_est_comparison_transformed.png` | `61e35a420a07b4d7c3600aaed34e60cd782f6b5197f6cc4de6cd72dd28109874` |
| `tests/plots/accuracy_err_comparison_transformed.png` | `496e0060ca7317caef8d590a01bd9caabdc175b695d190a57eb6403e0164a00f` |
| `tests/plots/accuracy_t_comparison_transformed.png` | `1e07213471601d819cf0e9e28a217726fdbe416e5a7aab230f4dcfa38ddf0b9e` |
| `tests/plots/accuracy_p_comparison_transformed.png` | `67275f800560467ca1f859aa269cd5166a735d513e4fe6b2c1b09a859b5a9d5e` |

## Proven

- SciPy-present p-value recalculation tests pass.
- Accuracy validation dependencies can be installed in an isolated environment.
- Accuracy validation runs directly instead of skipping when optional
  dependencies are present.
- The focused unittest bridge runs without skips in the dependency-present
  environment.
- Numeric validation behavior is acceptable for the test's documented estimate
  and t-statistic tolerances on generated synthetic data.

## Not Proven

- GPU/performance recovery.
- CUDA runtime behavior.
- Full CLI/runtime behavior.
- Numeric correctness on real project datasets.
- Equivalence between normal-approximation p-values and Student-t p-values.
- Upstream `kordk/torch-ecpg` changes.
- Upstream PR #150 or PR #152 action.
- MVP closeout.
