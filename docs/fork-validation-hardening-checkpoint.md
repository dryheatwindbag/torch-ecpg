# Fork Validation Hardening Checkpoint

Repository: `dryheatwindbag/torch-ecpg`

Branch: `dev`

Checkpoint commit: `ae62f6af7c3175756cef3478227a9597e08d3b0e`

Classification: dashboard / evidence / signoff

## Merged Sequence

| PR | Area | Classification | Summary |
| --- | --- | --- | --- |
| [#8](https://github.com/dryheatwindbag/torch-ecpg/pull/8) | GPU monitor mock dependency hardening | validation | Made GPU monitor mock tests self-contained for missing optional dependencies. |
| [#9](https://github.com/dryheatwindbag/torch-ecpg/pull/9) | GPU monitor direct execution hygiene | validation | Made the GPU monitor mock test behave cleanly under direct execution. |
| [#10](https://github.com/dryheatwindbag/torch-ecpg/pull/10) | SciPy-missing p-value skip hygiene | validation | Skips p-value recalculation tests when SciPy is unavailable. |
| [#11](https://github.com/dryheatwindbag/torch-ecpg/pull/11) | Auto-scale minimal-environment unittest hardening | validation | Tests `_auto_save_threads` without importing the full CLI runtime dependency graph. |
| [#12](https://github.com/dryheatwindbag/torch-ecpg/pull/12) | Accuracy validation optional-dependency skip | validation | Skips accuracy validation cleanly when optional validation dependencies are unavailable. |
| [#13](https://github.com/dryheatwindbag/torch-ecpg/pull/13) | Focused validation GitHub Actions workflow | workflow / CI validation | Runs the hardened focused minimal-environment unittest bridge on PRs to `dev` and pushes to `dev`. |

## Proven

- The focused minimal-environment unittest bridge exists.
- The focused bridge is covered by GitHub Actions on pull requests to `dev` and pushes to `dev`.
- The workflow installs only `pandas` and `numpy`, so optional heavy dependencies remain dependency-gated skips.
- The focused validation check passed for PR #13 before merge.

Focused validation command:

```bash
python -m unittest \
  tests.test_accuracy \
  tests.test_auto_scale \
  tests.test_recalculate_pvalues \
  tests.test_process_pool_spawn \
  tests.test_pearson_pool_lifecycle \
  tests.test_gpu_monitor_mock
```

## Not Proven

- GPU/performance recovery.
- CUDA runtime behavior.
- Full CLI/runtime behavior.
- Recalculated p-value numeric correctness without SciPy.
- Accuracy validation correctness without optional validation dependencies.
- Upstream `kordk/torch-ecpg` changes.
- Upstream PR #150 or PR #152 action.
- Full MVP closeout beyond the existing fork-only bridge.

## Stop Condition

Stop opening validation-hardening PRs unless a new concrete failure appears.

Continue normal fork development from `dryheatwindbag:dev` at
`ae62f6af7c3175756cef3478227a9597e08d3b0e`.

If GPU proof becomes necessary, run the existing GPU handoff on GPU-capable
hardware instead of changing implementation.
