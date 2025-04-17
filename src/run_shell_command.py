import subprocess

def run_shell_command(command_str):
    """Runs a shell command and returns its output and errors."""
    try:
        # Using shell=True can be a security risk if the command string
        # comes from untrusted input. For fixed commands, it's often convenient.
        # Alternatively, pass command parts as a list: e.g., ['ls', '-l']
        # capture_output=True gets stdout/stderr. text=True decodes them as text.
        result = subprocess.run(
            command_str,
            shell=True,
            check=True,  # Raises CalledProcessError if command returns non-zero exit code
            capture_output=True,
            text=True,
            timeout=10 # Optional: prevent hanging indefinitely (in seconds)
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Error Output (stderr):\n", result.stderr) # Often empty on success
        return result.stdout, result.stderr

    except FileNotFoundError:
        print(f"Error: Command not found: {command_str.split()[0]}")
        return None, "Command not found"
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with return code {e.returncode}")
        print("Output (stdout):\n", e.stdout)
        print("Error Output (stderr):\n", e.stderr)
        return e.stdout, e.stderr
    except subprocess.TimeoutExpired:
        print(f"Error: Command timed out after 10 seconds.")
        return None, "Command timed out"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, str(e)
