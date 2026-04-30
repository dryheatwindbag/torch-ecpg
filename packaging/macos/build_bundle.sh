#!/usr/bin/env bash
set -euo pipefail

python_exe="python3"
torch_package="torch"
bundle_name="tecpg-macos-arm64-cpu"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --python-exe)
            python_exe="$2"
            shift 2
            ;;
        --torch-package)
            torch_package="$2"
            shift 2
            ;;
        --bundle-name)
            bundle_name="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 2
            ;;
    esac
done

repo_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
build_root="$repo_root/build/macos-arm64-cpu-bundle"
dist_root="$repo_root/dist"
bundle_root="$build_root/$bundle_name"
python_root="$bundle_root/python"
launcher_root="$bundle_root/launchers"
license_root="$bundle_root/licenses"
unpack_root="$dist_root/unpacked"
zip_path="$dist_root/$bundle_name.zip"
checksum_path="$dist_root/SHA256SUMS.txt"

rm -rf "$build_root" "$unpack_root" "$zip_path" "$checksum_path"
mkdir -p "$build_root" "$dist_root" "$bundle_root" "$launcher_root" "$license_root"

"$python_exe" -m venv --copies "$python_root"
bundle_python="$python_root/bin/python"

"$bundle_python" -m pip install --upgrade pip
"$bundle_python" -m pip install --upgrade "$torch_package"
"$bundle_python" -m pip install -r "$repo_root/requirements.txt"
"$bundle_python" -m pip install "$repo_root"

site_packages_root="$("$bundle_python" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
source_package_root="$repo_root/tecpg"
(
    cd "${TMPDIR:-/tmp}"
    "$bundle_python" -c 'import pathlib, sys, tecpg; package_path = pathlib.Path(tecpg.__file__).resolve(); site = pathlib.Path(sys.argv[1]).resolve(); source = pathlib.Path(sys.argv[2]).resolve(); print(package_path); raise SystemExit(0 if site in package_path.parents and source not in package_path.parents else 1)' "$site_packages_root" "$source_package_root"
    "$bundle_python" -c 'import torch; print(torch.__version__, torch.cuda.is_available()); raise SystemExit(1 if torch.cuda.is_available() else 0)'
)

launcher_path="$launcher_root/tecpg"
cat > "$launcher_path" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
bundle_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
exec "$bundle_dir/python/bin/python" -m tecpg "$@"
SH
chmod 0755 "$launcher_path"

cp "$repo_root/packaging/macos/BUNDLE_README.md" "$bundle_root/README.md"
cp "$repo_root/packaging/common/smoke_test.py" "$bundle_root/smoke_test.py"
cp "$repo_root/LICENSE" "$license_root/LICENSE.torch-ecpg.txt"
"$bundle_python" -m pip freeze > "$license_root/python-packages.txt"
cat > "$license_root/THIRD_PARTY_NOTICES.md" <<'MD'
# Third-party notices

This CPU bundle includes Python, PyTorch CPU wheels, and Torch-eCpG runtime
dependencies installed by pip. Review `python-packages.txt` for the exact
package set included in this artifact.

Before any public release, verify dependency license notices against the
downloaded wheel metadata and the project's release policy.
MD

mkdir -p "$unpack_root"
(
    cd "$build_root"
    ditto -c -k --keepParent "$bundle_name" "$zip_path"
)
ditto -x -k "$zip_path" "$unpack_root"

hash="$(shasum -a 256 "$zip_path" | awk '{print $1}')"
printf "%s  %s.zip\n" "$hash" "$bundle_name" > "$checksum_path"

(
    cd "$dist_root"
    expected_hash="$(awk '{print $1}' SHA256SUMS.txt)"
    actual_hash="$(shasum -a 256 "$bundle_name.zip" | awk '{print $1}')"
    if [ "$actual_hash" != "$expected_hash" ]; then
        echo "SHA256 mismatch for $bundle_name.zip" >&2
        exit 1
    fi
    echo "SHA256 verified for $bundle_name.zip"
)
