

def format_time(total_seconds):
    """Converts total seconds into HH:MM:SS string format."""
    if total_seconds < 0:
        total_seconds = 0
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    # Use f-string formatting with leading zeros (e.g., 01:05:09)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def parse_time_string(time_str):
    """Parses HH:MM:SS string into total seconds. Returns None on failure."""
    parts = time_str.split(':')
    if len(parts) != 3:
        return None
    try:
        # Ensure parts are treated as base-10 integers
        h = int(parts[0], 10)
        m = int(parts[1], 10)
        s = int(parts[2], 10)
        if 0 <= h <= 99 and 0 <= m <= 59 and 0 <= s <= 59:
            return h * 3600 + m * 60 + s
        else:
            print(f"Time component out of range: H={h}, M={m}, S={s}")
            return None
    except ValueError:
        print(f"Could not parse time components: {parts}")
        return None
