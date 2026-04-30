# PR #14 GPU/Runtime Validation Evidence

Repository: `dryheatwindbag/torch-ecpg`

Classification: validation / evidence

This report records the GPU-capable run for the parked PR #14 validation gap.
It does not reopen PR #130 cleanup, lifecycle, or GPU-planning work, and it
does not claim MVP closeout.

## Environment

- Branch under test: `dev` and evidence branch
  `codex/pr-14-gpu-runtime-validation-evidence`
- Base commit under test: `acbb889db9709dcf5beddcd10ee50cebbc4e1eff`
- Evidence branch commit under test:
  `7cbadf8734ea64bf957554c0f50dd02f3d003e78`
- Required fork baseline: `45df28abfe3a00bc4028a6abfca5c4a2614bf455`
- Baseline descendant check: passed with
  `git merge-base --is-ancestor 45df28abfe3a00bc4028a6abfca5c4a2614bf455 HEAD`
- Machine: `JimiJam`
- GPU: NVIDIA GeForce RTX 3080
- NVIDIA driver: `581.95`
- Driver CUDA version from `nvidia-smi`: `13.0`
- Python: `3.12.13`
- Torch: `2.5.0+cu121`
- Torch CUDA available: `True`
- Torch CUDA runtime: `12.1`
- Pandas for real GTP processing: `2.2.3`
- NumPy for real GTP processing: `2.0.2`

The run used a workspace-local Python wrapper and dependency directory to make
`python3` and `tecpg` available on this Windows/Git Bash host.

## Commands

```bash
git checkout dev
git pull --ff-only
git rev-parse HEAD
git merge-base --is-ancestor 45df28abfe3a00bc4028a6abfca5c4a2614bf455 HEAD
python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle
python3 -m unittest tests.test_accuracy tests.test_auto_scale tests.test_recalculate_pvalues tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle tests.test_gpu_monitor_mock
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
nvidia-smi
tecpg -i data_gtp data gtp -g GTP -y
tools/fork_gpu_performance_validation.sh --run-profiles
```

## Results

- `git pull --ff-only`: already up to date.
- `git rev-parse HEAD`: `acbb889db9709dcf5beddcd10ee50cebbc4e1eff`
  before the report-only branch commit.
- Focused lifecycle/spawn unittest preflight: passed, 2 tests.
- Requested combined unittest set: passed, 9 tests.
- Torch CUDA prerequisite: `2.5.0+cu121 True`.
- `nvidia-smi`: passed and reported RTX 3080.
- Real GTP download/process: completed from NCBI GEO into `data_gtp`.
- Validation helper status: `profiles_completed_review_required`.
- Smoke profile: completed using generated dummy data.
- Realistic profile slot: ran against downloaded and processed real GTP data.

Initial real GTP processing under `pandas 3.0.2` left the covariate `Sex`
column as object dtype and caused tensor conversion to fail. The validation
environment was pinned to `pandas 2.2.3` / `numpy 2.0.2`, the real GTP data was
regenerated, and the profile was rerun.

The real GTP matrix profile reached CUDA execution, but each major profile cell
timed out at the script's 600 second cap before emitting PROFILE summary lines.
The `blas` cell exited with code 127 after reaching CUDA startup. The helper
still marked the profile command as passed because the profiling harness treats
timeouts as expected bounded runs, but the artifacts do not support a recovery
claim.

## Artifacts

Local validation helper directory:

`profiling-runs/fork-validation-JimiJam-20260430T055342Z`

Helper artifact SHA256s:

| Artifact | SHA256 |
| --- | --- |
| `compile_preflight.err` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `compile_preflight.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git_head.out` | `c87e31ea5b68f6840319a4e1f88a842c1c457834cdf0bd8aeb61cec12f20c4f0` |
| `git_status.out` | `3dc348176f92f5733918f41add8f669fb0ad3d14732e9b56beb024872d79a7dd` |
| `nvidia_smi.out` | `6d1bed6332a04a0e8e17dfbb408785168ad1cecbbe84f231c46d8d81680a807d` |
| `python_version.out` | `2dc0d5541cf70196cb92df8ad4223b66b7c62eb932b290936086e003b1e6f76e` |
| `smoke_profile.out` | `249438bf5249029b7c384e983a888985db495d36c82ce3e783c4224144eecfc2` |
| `smoke_profile.err` | `94569d7a5b1de5e6ba4d8af9d2040ad5e20a3f76f53f7daa09448fce7f22f59f` |
| `realistic_profile.out` | `a1d77a64bf3e571db599a1d755a79cc0b5a51dbeb16e99a635ced0f7c7e5b3c8` |
| `realistic_profile.err` | `94569d7a5b1de5e6ba4d8af9d2040ad5e20a3f76f53f7daa09448fce7f22f59f` |
| `status.txt` | `8a0fe9f61bf2cbbad393c070ad50ea8ef7ee2ab43139636ecf6f7b7469791a45` |
| `torch.out` | `6f654682af4e3ab07f44ac079e378d935d68639c08e7995e2bbc849a6d116736` |
| `unit_preflight.err` | `674cbc1a7fba8531aa2696d76ad99b282b87b5419b3cf198223390d52bf8bc4c` |
| `unit_preflight.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `validation.log` | `0436904a106eee4be2732c5c8a735672017152eb394581f2a6745d655882497e` |

Profile archives:

| Artifact | SHA256 | Notes |
| --- | --- | --- |
| `profiling-runs/JimiJam-20260430T055352Z.tar.gz` | `b9649a0514414b57fb0517bbaf6125efb9022534fdb8f88d5766ce7d8bb0c1b4` | smoke profile archive |
| `profiling-runs/JimiJam-20260430T055452Z.tar.gz` | `11701a433e1a2c32cf11eacf7787b46656c2264a34532264f553f9b77ec2d036` | real GTP matrix profile archive |

Real GTP dataset SHA256s:

| Artifact | SHA256 |
| --- | --- |
| `GTP/CovariateMatrix.txt.gz` | `99d9dced29e20ce21d1f89740d9776a66ed97a31af73e6fef9887ef4aa34727c` |
| `GTP/GeneExpressionValues_1.tsv.gz` | `2d0d1ba65b0f14981d93f062e9d8792666bb6370bab2f4adba3535b53f33ef4c` |
| `GTP/GeneExpressionValues_2.tsv.gz` | `b95dd86e3512d9512dec9a0bfa4018d5f374a5f21a0421c98e8311cacb40fde2` |
| `GTP/MethylationBetaValues.tsv.gz` | `cce22f256267ea1fec63dfc6347b346a8ed4b1e7207f4e3bdf04987463dbf4d6` |
| `data_gtp/C.csv` | `a0f0b990dd387d547b225aeee530abfbb11b8ee18c7b0b3f0b488e9c25d9bff1` |
| `data_gtp/G.csv` | `59db2fb554a80977137935ab7190c7830008f7497c908bd954340f5e661b84a9` |
| `data_gtp/M.csv` | `5ec93ae55875b8fce2b798f323df01c5109ccfd67991a1ce854d2533833b469c` |

## Conclusion

Proven:

- The fork `dev` commit is a descendant of the required fork baseline.
- Required focused and combined unittest commands pass in a dependency-present
  environment.
- This machine has visible NVIDIA GPU hardware through `nvidia-smi`.
- CUDA-enabled PyTorch imports successfully and reports CUDA availability.
- The real GTP dataset can be downloaded, processed, and loaded with a
  pandas 2.x validation environment.
- The real GTP matrix profile reaches CUDA execution and records GPU allocation
  during the first methylation chunk.
- The profiling helper can run the smoke and matrix profile command paths to
  completion.

Not proven:

- GPU/performance recovery, because the real GTP matrix profile timed out before
  producing PROFILE summary lines or a successful performance verdict.
- Full real-GTP workload completion under the current 600 second per-cell cap.
- Complete profiler coverage, because `pidstat`, `iostat`, and `vmstat` were
  not available on this Windows/Git Bash host.
- Compatibility with pandas 3.x GTP processing, because pandas 3.0.2 left
  covariates as object dtype and blocked tensor conversion.
- Release readiness, rollback readiness, owner acceptance, or full MVP closeout.

GPU/performance recovery classification: not proven.

