import os
import subprocess
import sys
from tkinter import Tk

from platforms.base import Platform
from run_shell_command import run_shell_command


class MacOSPlatform(Platform):
    def lock_screen(self) -> None:
        run_shell_command("/usr/bin/pmset displaysleepnow")

    def focus_app(self, window: Tk) -> None:
        """Bring the app to the foreground by PID via AppleScript.

        Tk's focus is unreliable on macOS, so the window arg is ignored in favor
        of an osascript call targeting this process.
        """
        pid = os.getpid()
        script = f'''
        tell application "System Events"
            set frontmost of first process whose unix id is {pid} to true
        end tell
        '''
        try:
            subprocess.run(['osascript', '-e', script], check=True, capture_output=True, text=True)
            print(f"Successfully requested focus for PID {pid} via AppleScript")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute AppleScript to focus app: {e.stderr}", file=sys.stderr)
        except FileNotFoundError:
            print("Error: 'osascript' command not found.", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

    def register_reopen_handler(self, window: Tk) -> None:
        """Bring app back from minimized state when reopened from the Dock."""
        window.createcommand('tk::mac::ReopenApplication', window.deiconify)
