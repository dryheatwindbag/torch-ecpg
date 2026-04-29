#!/usr/bin/env bash
set -euo pipefail

# Fork-only helper for docs/fork-gpu-performance-validation-plan.md.
# It records evidence and refuses to claim GPU recovery when prerequisites are
# missing. It targets dryheatwindbag/torch-ecpg only.

OUT_DIR="${OUT_DIR:-./profiling-runs/fork-validation-$(hostname)-$(date -u +'%Y%m%dT%H%M%SZ')}"
GPU_INDEX="${GPU_INDEX:-0}"
RUN_PROFILES=0

show_help() {
    cat <<'HELP'
Usage: tools/fork_gpu_performance_validation.sh [--run-profiles]

Runs fork-only GPU/performance validation preflight and writes evidence under
OUT_DIR. By default, it stops after preflight and environment checks. With
--run-profiles, it also runs the smoke and realistic profiling commands from
docs/fork-gpu-performance-validation-plan.md.

Environment:
  OUT_DIR     Evidence output directory
  GPU_INDEX   GPU index passed to profiling.sh (default: 0)

This script does not target upstream kordk/torch-ecpg and does not prove GPU
recovery unless generated profiling artifacts support that conclusion.
HELP
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --run-profiles)
            RUN_PROFILES=1
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            show_help >&2
            exit 64
            ;;
    esac
done

mkdir -p "$OUT_DIR"

log() {
    printf '[%s] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*" | tee -a "$OUT_DIR/validation.log"
}

run_capture() {
    local name="$1"
    shift
    log "RUN $name: $*"
    if "$@" >"$OUT_DIR/$name.out" 2>"$OUT_DIR/$name.err"; then
        log "PASS $name"
        return 0
    fi
    local status=$?
    log "FAIL $name status=$status"
    return "$status"
}

write_status() {
    local status="$1"
    cat >"$OUT_DIR/status.txt" <<EOF
status=$status
repo=dryheatwindbag/torch-ecpg
branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)
commit=$(git rev-parse HEAD 2>/dev/null || echo unknown)
gpu_index=$GPU_INDEX
out_dir=$OUT_DIR
EOF
}

log "Fork GPU/performance validation started"
log "Evidence directory: $OUT_DIR"

run_capture git_head git rev-parse HEAD
run_capture python_version python3 --version
run_capture unit_preflight python3 -m unittest tests.test_process_pool_spawn tests.test_pearson_pool_lifecycle
run_capture compile_preflight python3 -m compileall -q tecpg/pearson_full.py tests/test_process_pool_spawn.py tests/test_pearson_pool_lifecycle.py
run_capture git_status git status --short

missing=0

if ! command -v nvidia-smi >/dev/null 2>&1; then
    log "BLOCKED nvidia-smi command not found"
    printf 'nvidia-smi: command not found\n' >"$OUT_DIR/nvidia-smi.err"
    missing=1
else
    run_capture nvidia_smi nvidia-smi || missing=1
fi

if ! python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())" >"$OUT_DIR/torch.out" 2>"$OUT_DIR/torch.err"; then
    log "BLOCKED torch import/CUDA check failed"
    missing=1
else
    log "PASS torch_cuda_check"
fi

if [[ "$missing" -ne 0 ]]; then
    write_status "blocked_missing_gpu_prerequisites"
    log "GPU profiling blocked. See $OUT_DIR/status.txt"
    log "No GPU/performance recovery is proven."
    exit 2
fi

if [[ "$RUN_PROFILES" -ne 1 ]]; then
    write_status "preflight_complete_profiles_not_run"
    log "Preflight complete. Re-run with --run-profiles to execute profiling."
    log "No GPU/performance recovery is proven until profile artifacts support it."
    exit 0
fi

run_capture smoke_profile ./profiling.sh -d dummy -D 90 --gpu-index "$GPU_INDEX" --no-nsys --no-nvprof
run_capture realistic_profile ./profiling.sh -d gtp -D 600 --matrix --gpu-index "$GPU_INDEX"

write_status "profiles_completed_review_required"
log "Profiles completed. Review generated artifacts before claiming GPU/performance recovery."
