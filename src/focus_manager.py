import tkinter as tk
import subprocess
import os
import sys

def focus_app():
    """
    Brings the current Python application to the foreground on macOS.
    (Implementation using AppleScript and PID - see previous answer)
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
