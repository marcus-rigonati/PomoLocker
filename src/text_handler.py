from typing import Optional


def format_time(total_seconds: int) -> str:
    """Converts total seconds into HH:MM:SS string format."""
    if total_seconds < 0:
        total_seconds = 0

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Use f-string formatting with leading zeros (e.g., 01:05:09)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def parse_time_string(time_str: str) -> Optional[int]:
    """Parses HH:MM:SS string into total seconds. Returns None on failure."""
    hours = 0
    minutes = 0
    seconds = 0
    try:
        if len(time_str) == 1:
            # S
            seconds = int(f"{time_str[len(time_str)-1]}", 10)
        elif len(time_str) >= 2:
            # SS or :SS
            seconds = int(f"{time_str[len(time_str)-2]}{time_str[len(time_str)-1]}", 10)

        if len(time_str) == 4:
            # M:SS
            minutes = int(f"{time_str[len(time_str)-4]}", 10)
        elif len(time_str) >= 5:
            # MM:SS or :MM:SS
            minutes = int(f"{time_str[len(time_str)-5]}{time_str[len(time_str)-4]}", 10)

        if len(time_str) == 7:
            # H:MM:SS
            hours = int(f"{time_str[len(time_str)-7]}", 10)
        elif len(time_str) == 8:
            # HH:MM:SS
            hours = int(f"{time_str[len(time_str)-8]}{time_str[len(time_str)-7]}", 10)

        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        print(f"Could not parse time components: {time_str}")
        return None
