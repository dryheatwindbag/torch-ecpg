# PR #14 GPU/Runtime Validation Evidence

Repository: `dryheatwindbag/torch-ecpg`

Classification: validation / evidence

This report records the GPU-capable run for the parked PR #14 validation gap.
It does not reopen PR #130 cleanup, lifecycle, or GPU-planning work, and it
does not claim MVP closeout.

## Environment

- Branch under test: `dev`
- Commit under test: `acbb889db9709dcf5beddcd10ee50cebbc4e1eff`
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
tools/fork_gpu_performance_validation.sh --run-profiles
```

## Results

- `git pull --ff-only`: already up to date.
- `git rev-parse HEAD`: `acbb889db9709dcf5beddcd10ee50cebbc4e1eff`.
- Focused lifecycle/spawn unittest preflight: passed, 2 tests.
- Requested combined unittest set: passed, 9 tests.
- Torch CUDA prerequisite: `2.5.0+cu121 True`.
- `nvidia-smi`: passed and reported RTX 3080.
- Validation helper status: `profiles_completed_review_required`.
- Smoke profile: completed using generated dummy data.
- Realistic profile slot: completed using an explicitly recorded substitute
  dataset, not the real GTP dataset.

The real GTP dataset was not present locally. The substitute dataset was created
with `tecpg data dummy -s 100 -m 1000 -g 1000` and copied into `data_gtp` /
`annot_gtp` so the `-d gtp` profile path could run without claiming real GTP
coverage.

## Artifacts

Local validation helper directory:

`profiling-runs/fork-validation-JimiJam-20260430T051656Z`

Helper artifact SHA256s:

| Artifact | SHA256 |
| --- | --- |
| `compile_preflight.err` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `compile_preflight.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git_head.out` | `8d460d887993fd85fa35589d1e68141e7d97544243e9225dc8f9d340e638830f` |
| `git_status.out` | `56508ba30a3378be72ebc2784e7281791a2f1e0a7c20982222ed1ed7d90bf9c2` |
| `nvidia_smi.out` | `800d27e0e1564a3d96b9118fb2f52cb1141528246cd0d3e0c68b0014395090e0` |
| `python_version.out` | `2dc0d5541cf70196cb92df8ad4223b66b7c62eb932b290936086e003b1e6f76e` |
| `smoke_profile.out` | `d97daba0688837193bc0ce656e298687ccfb813d481e535eabf416695fc82bba` |
| `smoke_profile.err` | `94569d7a5b1de5e6ba4d8af9d2040ad5e20a3f76f53f7daa09448fce7f22f59f` |
| `realistic_profile.out` | `c38aa23587feb7a6fbcc9597750f0ab6cf77600d5a4b08da4959a13ec6003022` |
| `realistic_profile.err` | `94569d7a5b1de5e6ba4d8af9d2040ad5e20a3f76f53f7daa09448fce7f22f59f` |
| `status.txt` | `0120b16fee4fbb01cbb4faa3dce3901211df34f7d4211e18fc2b2843547e5ec7` |
| `torch.out` | `6f654682af4e3ab07f44ac079e378d935d68639c08e7995e2bbc849a6d116736` |
| `unit_preflight.err` | `e8daecf26c3e8b8bc231b1adaeb70a39215dd704e1c768806091d012ce76dd19` |
| `unit_preflight.out` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `validation.log` | `4f717827af119a15f03f393b9c662c6231864a8a50d9e7df6ade7e75df2c589a` |

Profile archives:

| Artifact | SHA256 | Notes |
| --- | --- | --- |
| `profiling-runs/JimiJam-20260430T051702Z.tar.gz` | `38fa69abf5d3082a70c90155efe114a9d1c7fef139775d39a88c70f7b9ec7dc5` | smoke profile archive |
| `profiling-runs/JimiJam-20260430T051729Z.tar.gz` | `9e64953131c315487cd48927d1762b5f302e27fd1fb2256a2ee7eaa642dd1637` | substitute `gtp` matrix profile archive |

Substitute dataset SHA256s:

| Artifact | SHA256 |
| --- | --- |
| `data_gtp/C.csv` | `4af60f1a9757f83415f510ba8f1903f7263f5baac6c0a8e33f9bbb246d3709ee` |
| `data_gtp/G.csv` | `db785f7c5e0f547d3a03d393234e5e51c21614ee0a937d9c90871bd34bb71132` |
| `data_gtp/M.csv` | `fd20b92f7b3902f424184e1aa3c8665b02d777c10b4747f68b11f4536612080f` |
| `annot_gtp/G.bed6` | `24ba4485c5a3330198e5f8c98a1e96ebb3b48dce11ad1a39b2660612baf7bed8` |
| `annot_gtp/M.bed6` | `07555fdeb02be1d8d98afee810c5fa2afb890d9686430f4ed6f3e650968c7943` |

## Conclusion

Proven:

- The fork `dev` commit is a descendant of the required fork baseline.
- Required focused and combined unittest commands pass in a dependency-present
  environment.
- This machine has visible NVIDIA GPU hardware through `nvidia-smi`.
- CUDA-enabled PyTorch imports successfully and reports CUDA availability.
- The profiling helper can run the smoke and matrix profile command paths to
  completion when supplied with generated substitute inputs.

Not proven:

- Real GTP dataset behavior, because the real dataset was not present.
- GPU/performance recovery, because the realistic profile used a substitute
  dataset and the summaries reported `gpu_ms` as `0.0` with a `save/D2H bound`
  verdict.
- Complete profiler coverage, because `pidstat`, `iostat`, and `vmstat` were
  not available on this Windows/Git Bash host.
- Release readiness, rollback readiness, owner acceptance, or full MVP closeout.

GPU/performance recovery classification: inconclusive.

