from platforms.base import Platform
from run_shell_command import run_shell_command


class WindowsPlatform(Platform):
    def lock_screen(self) -> None:
        run_shell_command("rundll32.exe user32.dll,LockWorkStation")

    # focus_app and register_reopen_handler use the base (Tk-native / no-op) defaults.
