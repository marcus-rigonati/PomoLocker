

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
    h = 0
    m = 0
    s = 0
    try:
        if len(time_str) == 1:
            # S
            s = int(f"{time_str[len(time_str)-1]}", 10)
        elif len(time_str) >= 2:
            # SS or :SS
            s = int(f"{time_str[len(time_str)-2]}{time_str[len(time_str)-1]}", 10)

        if len(time_str) == 4:
            # M:SS
            m = int(f"{time_str[len(time_str)-4]}", 10)
        elif len(time_str) >= 5:
            # MM:SS or :MM:SS
            m = int(f"{time_str[len(time_str)-5]}{time_str[len(time_str)-4]}", 10)

        if len(time_str) == 7:
            # H:MM:SS
            h = int(f"{time_str[len(time_str)-7]}", 10)
        elif len(time_str) == 8:
            # HH:MM:SS
            h = int(f"{time_str[len(time_str)-8]}{time_str[len(time_str)-7]}", 10)

        return h * 3600 + m * 60 + s
    except ValueError:
        print(f"Could not parse time components: {time_str}")
        return None
