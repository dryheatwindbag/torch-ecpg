# Full CLI Runtime Smoke Evidence

Repository: `dryheatwindbag/torch-ecpg`

Base branch: `dev`

Base commit: `faed7d67d955eb70277d6fb58f1eeebe1227a3b0`

Classification: validation

Scope: prove the full `tecpg` CLI/runtime import path works with real
dependencies installed, outside the minimal test stubs.

This is independent of the parked GPU/runtime evidence gate. It does not claim
GPU/performance recovery or CUDA runtime behavior.

## Environment

The smoke used an isolated virtual environment at `/tmp/torch-ecpg-pr15-venv`
with `requirements.txt` installed.

Validation environment facts:

- `python -m pip check`: `No broken requirements found.`
- `tecpg` version: `1.15.0-dev`
- `torch` version: `2.11.0`
- CUDA availability: `False`

## Commands And Results

Full import and logger path:

```bash
/tmp/torch-ecpg-pr15-venv/bin/python - <<'PY'
import tecpg
import tecpg.__main__
import tecpg.cli
from tecpg.logger import Logger
print('tecpg', tecpg.__version__)
print('cli import ok', callable(tecpg.cli.start))
print('logger ok', type(Logger(carry_data={'use_cpu': True})).__name__)
PY
```

Result:

```text
tecpg 1.15.0-dev
cli import ok True
logger ok Logger
```

CLI help/version:

```bash
/tmp/torch-ecpg-pr15-venv/bin/python -m tecpg --help
/tmp/torch-ecpg-pr15-venv/bin/python -m tecpg --version
```

Result: help rendered successfully and version printed `tecpg version
1.15.0-dev`.

Minimal runtime smoke:

```bash
rm -rf /tmp/tecpg-cli-smoke
mkdir -p /tmp/tecpg-cli-smoke
/tmp/torch-ecpg-pr15-venv/bin/python -m tecpg \
  -r /tmp/tecpg-cli-smoke init smoke -y
/tmp/torch-ecpg-pr15-venv/bin/python -m tecpg \
  -r /tmp/tecpg-cli-smoke/smoke data dummy -s 12 -m 4 -g 3
/tmp/torch-ecpg-pr15-venv/bin/python -m tecpg \
  -r /tmp/tecpg-cli-smoke/smoke \
  -t 1 \
  --save-threads 2 \
  run mlr --all -g 2 -m 2 --mlr-method manual
find /tmp/tecpg-cli-smoke/smoke/output \
  -type f -name '*.csv' -size +0c | grep -q .
```

Result: `init`, `data dummy`, and CPU `run mlr --mlr-method manual` completed
successfully and produced non-empty CSV output chunks.

Regression test:

```bash
/tmp/torch-ecpg-pr15-venv/bin/python -m unittest tests.test_cli_runtime_smoke
```

Result: `Ran 1 test in 2.717s`, `OK`.

## Runtime Fix

The first full CLI smoke exposed a manual MLR runtime bug: `tecpg run mlr
--mlr-method manual` passed lstsq-only options such as `subsample_mt_count`,
`subsample_g_count`, `seed`, and `prefetch_chunks` to `regression_full()`,
causing an import/runtime smoke failure:

```text
TypeError: regression_full() got an unexpected keyword argument 'subsample_mt_count'
```

The fix keeps these lstsq-only options out of the default manual
`regression_full()` path.

## Proven

- Full `tecpg` CLI imports with real dependencies installed.
- CLI help and version commands run without import-time crashes.
- Logger/runtime dependency path initializes.
- `tecpg init`, `tecpg data dummy`, and CPU manual `tecpg run mlr` complete on a
  generated minimal dataset.
- The manual MLR CLI path no longer passes lstsq-only options into
  `regression_full()`.

## Not Proven

- GPU/performance recovery.
- CUDA runtime behavior.
- Real-dataset runtime behavior.
- Full production-scale CLI behavior.
- Upstream `kordk/torch-ecpg` changes.
- Upstream PR #150 or PR #152 action.
- MVP closeout.
