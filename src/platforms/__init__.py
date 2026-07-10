import sys

from platforms.base import Platform


def get_platform() -> Platform:
    """Return the Platform implementation for the current operating system."""
    if sys.platform == "darwin":
        from platforms.macos import MacOSPlatform
        return MacOSPlatform()
    if sys.platform == "win32":
        from platforms.windows import WindowsPlatform
        return WindowsPlatform()
    if sys.platform.startswith("linux"):
        from platforms.linux import LinuxPlatform
        return LinuxPlatform()
    raise RuntimeError(f"Unsupported platform: {sys.platform}")
