#!/usr/bin/env bash
#
# Builds a standalone PomoLocker binary for the machine it runs on.
#
#   ./build.sh
#
# Output lands in dist/ as both the raw PyInstaller result and a distributable
# archive named PomoLocker-<os>-<arch>.<ext>. The GitHub Actions release
# workflow (.github/workflows/release.yml) calls this same script on Linux,
# Windows and macOS runners, so what you get locally is what ships.
#
# Requires the build dependencies from requirements.txt in the active
# environment. A ./.venv is picked up automatically if you have not already
# activated one.

set -euo pipefail

APP_NAME="PomoLocker"
BUNDLE_ID="com.pomolocker.app"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    if [[ -f .venv/bin/activate ]]; then
        source .venv/bin/activate
    elif [[ -f .venv/Scripts/activate ]]; then  # Windows layout
        source .venv/Scripts/activate
    fi
fi

PYTHON="${PYTHON:-python}"
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python3

case "$(uname -s)" in
    Darwin)                OS=macos ;;
    Linux)                 OS=linux ;;
    MINGW* | MSYS* | CYGWIN* | Windows_NT) OS=windows ;;
    *) echo "build.sh: unsupported host $(uname -s)" >&2; exit 1 ;;
esac

case "$(uname -m)" in
    arm64 | aarch64) ARCH=arm64 ;;
    x86_64 | amd64)  ARCH=x86_64 ;;
    *) ARCH="$(uname -m)" ;;
esac

TARGET="$APP_NAME-$OS-$ARCH"

# src/ uses flat imports (`import text_handler`), so it has to be on the search
# path. platforms/ picks its implementation lazily inside get_platform(), so its
# submodules are collected explicitly rather than left to static analysis.
args=(
    --noconfirm
    --clean
    --name "$APP_NAME"
    --windowed
    --paths "$ROOT/src"
    --collect-submodules platforms
    --distpath "$ROOT/dist"
    --workpath "$ROOT/build"
    --specpath "$ROOT/build"
    --exclude-module tkinter
)

case "$OS" in
    macos)
        # onedir, which is what PyInstaller recommends for .app bundles.
        args+=(--icon "$ROOT/appicon.icns" --osx-bundle-identifier "$BUNDLE_ID")
        ;;
    linux)
        # PyInstaller has to find libpython to copy them into the binary.
        PY_LIB="$("$PYTHON" -c 'import os, sys; print(os.path.join(sys.base_prefix, "lib"))')"
        export LD_LIBRARY_PATH="$PY_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
        args+=(--onefile)
        ;;
    windows)
        # Converting the .png icon needs Pillow; skip the icon rather than fail
        # the build for anyone who only installed pyinstaller.
        args+=(--onefile)
        if "$PYTHON" -c 'import PIL' >/dev/null 2>&1; then
            args+=(--icon "$ROOT/icon/new-icon-final.png")
        else
            echo "build.sh: Pillow not installed, building without an icon" >&2
        fi
        ;;
esac

rm -rf "$ROOT/dist"
"$PYTHON" -m PyInstaller "${args[@]}" "$ROOT/src/main.py"

# Package into a single downloadable file. macOS needs ditto so the .app keeps
# its symlinks and signature; Linux needs tar so the executable bit survives.
cd "$ROOT/dist"
case "$OS" in
    macos)   ditto -c -k --keepParent "$APP_NAME.app" "$TARGET.zip" ;;
    linux)   tar -czf "$TARGET.tar.gz" "$APP_NAME" ;;
    windows) mv "$APP_NAME.exe" "$TARGET.exe" ;;
esac

echo "build.sh: built $TARGET"
ls -la "$ROOT/dist"
