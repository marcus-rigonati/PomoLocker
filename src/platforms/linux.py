import os
from typing import Optional

from platforms.base import Platform
from run_shell_command import run_shell_command


class LinuxPlatform(Platform):
    """Linux support for GNOME, KDE and Hyprland."""

    def lock_screen(self) -> None:
        command = self._lock_command()
        if command is None:
            raise NotImplementedError(
                "Screen lock is not supported for this Linux desktop environment. "
                "Supported: GNOME, KDE and Hyprland."
            )
        run_shell_command(command)

    @staticmethod
    def _lock_command() -> Optional[str]:
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        if "hyprland" in desktop or os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
            return "hyprlock"
        if "gnome" in desktop or "kde" in desktop:
            return "loginctl lock-session"  # both kde and gnome integrate with systemd-logind lock
        return None

    # focus_app and register_reopen_handler use the base (Tk-native / no-op) defaults.
