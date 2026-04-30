param(
    [string]$PythonVersion = "3.11.9",
    [string]$TorchPackage = "torch",
    [string]$BundleName = "tecpg-windows-x64-cpu"
)

$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -ge 7) {
    $PSNativeCommandUseErrorActionPreference = $true
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$BuildRoot = Join-Path $RepoRoot "build/windows-cpu-bundle"
$DistRoot = Join-Path $RepoRoot "dist"
$BundleRoot = Join-Path $BuildRoot $BundleName
$PythonRoot = Join-Path $BundleRoot "python"
$LauncherRoot = Join-Path $BundleRoot "launchers"
$LicenseRoot = Join-Path $BundleRoot "licenses"
$UnpackRoot = Join-Path $DistRoot "unpacked"
$ZipPath = Join-Path $DistRoot "$BundleName.zip"
$ChecksumPath = Join-Path $DistRoot "SHA256SUMS.txt"

Remove-Item -Recurse -Force $BuildRoot, $UnpackRoot, $ZipPath, $ChecksumPath -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $BuildRoot, $DistRoot, $BundleRoot, $LauncherRoot, $LicenseRoot | Out-Null

nuget install python -Version $PythonVersion -OutputDirectory $BuildRoot -ExcludeVersion
$NugetPythonRoot = Join-Path $BuildRoot "python/tools"
if (!(Test-Path (Join-Path $NugetPythonRoot "python.exe"))) {
    throw "NuGet Python runtime was not found at $NugetPythonRoot"
}

Copy-Item -Recurse -Force $NugetPythonRoot $PythonRoot
$PythonExe = Join-Path $PythonRoot "python.exe"

& $PythonExe -m ensurepip --upgrade
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install --upgrade --index-url "https://download.pytorch.org/whl/cpu" --extra-index-url "https://pypi.org/simple" $TorchPackage
& $PythonExe -m pip install -r (Join-Path $RepoRoot "requirements.txt")
& $PythonExe -m pip install $RepoRoot

$SitePackagesRoot = (Resolve-Path (Join-Path $PythonRoot "Lib/site-packages")).Path
$SourcePackageRoot = (Resolve-Path (Join-Path $RepoRoot "tecpg")).Path
Push-Location $env:TEMP
try {
    & $PythonExe -c "import pathlib, sys, tecpg; p=pathlib.Path(tecpg.__file__).resolve(); site=pathlib.Path(sys.argv[1]).resolve(); source=pathlib.Path(sys.argv[2]).resolve(); print(p); raise SystemExit(0 if site in p.parents and source not in p.parents else 1)" $SitePackagesRoot $SourcePackageRoot
    & $PythonExe -c "import torch; print(torch.__version__, torch.cuda.is_available()); raise SystemExit(1 if torch.cuda.is_available() else 0)"
}
finally {
    Pop-Location
}

$LauncherPath = Join-Path $LauncherRoot "tecpg.cmd"
@"
@echo off
set "TECPG_BUNDLE_DIR=%~dp0.."
"%TECPG_BUNDLE_DIR%\python\python.exe" -m tecpg %*
"@ | Set-Content -NoNewline -Encoding ASCII $LauncherPath

Copy-Item -Force (Join-Path $RepoRoot "packaging/windows/BUNDLE_README.md") (Join-Path $BundleRoot "README.md")
Copy-Item -Force (Join-Path $RepoRoot "packaging/common/smoke_test.py") (Join-Path $BundleRoot "smoke_test.py")
Copy-Item -Force (Join-Path $RepoRoot "LICENSE") (Join-Path $LicenseRoot "LICENSE.torch-ecpg.txt")
& $PythonExe -m pip freeze | Set-Content -Encoding ASCII (Join-Path $LicenseRoot "python-packages.txt")
@'
# Third-party notices

This CPU bundle includes Python, PyTorch CPU wheels, and Torch-eCpG runtime
dependencies installed by pip. Review `python-packages.txt` for the exact
package set included in this artifact.

Before any public release, verify dependency license notices against the
downloaded wheel metadata and the project's release policy.
'@ | Set-Content -Encoding ASCII (Join-Path $LicenseRoot "THIRD_PARTY_NOTICES.md")

New-Item -ItemType Directory -Force $UnpackRoot | Out-Null
Compress-Archive -Path $BundleRoot -DestinationPath $ZipPath -Force
Expand-Archive -Path $ZipPath -DestinationPath $UnpackRoot -Force

$Hash = (Get-FileHash -Algorithm SHA256 $ZipPath).Hash.ToLowerInvariant()
"$Hash  $BundleName.zip" | Set-Content -Encoding ASCII $ChecksumPath

Push-Location $DistRoot
try {
    $ExpectedHash = (Get-Content $ChecksumPath).Split(" ")[0]
    $ActualHash = (Get-FileHash -Algorithm SHA256 "$BundleName.zip").Hash.ToLowerInvariant()
    if ($ActualHash -ne $ExpectedHash) {
        throw "SHA256 mismatch for $BundleName.zip"
    }
    Write-Output "SHA256 verified for $BundleName.zip"
}
finally {
    Pop-Location
}
