import tkinter as tk
from tkinter import ttk
from typing import Optional


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Converts a hex color string (e.g., '#RRGGBB') to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color format. Should be #RRGGBB or RRGGBB")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b

def rgb_to_hex(rgb_tuple: list[float]) -> str:
    """Converts an (R, G, B) tuple to a hex color string."""
    r, g, b = map(int, rgb_tuple) # Ensure components are integers
    r = max(0, min(255, r)) # Clamp values to 0-255
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f'#{r:02x}{g:02x}{b:02x}'

def interpolate_color(start_color: str, end_color: str, fraction: float) -> str:
    """
    Linearly interpolates between two RGB colors.
    fraction is a float between 0.0 (start_color) and 1.0 (end_color).
    """
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    interpolated_rgb = [
        start + (end - start) * fraction
        for start, end in zip(start_rgb, end_rgb)
    ]
    return rgb_to_hex(interpolated_rgb)

def animate_bg_change(
    widget: tk.Widget,
    end_color: str,
    style: Optional[ttk.Style] = None,
    property_to_change: str = "background",
    duration_ms: int = 500,
    steps: int = 25
) -> None:
    """
    Animates the background color of a widget.

    Args:
        widget: The Tkinter widget to animate.
        end_color: The ending hex color string (e.g., '#0000FF').
        property_to_change: the name of the widget property that should be changed (default: "background")
        duration_ms: Total duration of the animation in milliseconds.
        steps: Number of intermediate steps in the animation.
    """
    if style is not None:
        start_color = style.lookup('Red.TButton', property_to_change)
    else:
        start_color = widget.cget('bg')
    current_step = 0
    delay = duration_ms // steps # Time per step

    def animation_step() -> None:
        nonlocal current_step
        if current_step > steps:
            # Ensures the final color is set
            if style is not None:
                style.configure('Red.TButton', background=end_color)
            else:
                widget[property_to_change] = end_color
            return # Animation finished

        # Calculate the fraction of completion
        fraction = current_step / steps

        # Calculate the intermediate color
        new_color = interpolate_color(start_color, end_color, fraction)

        # Update the widget's background
        try:
            if widget.winfo_exists():
                if style is not None:
                    style.configure('Red.TButton', background=new_color)
                else:
                    widget[property_to_change]=new_color
        except tk.TclError:
            print(f"Warning: Widget {widget} destroyed during animation.")
            return

        current_step += 1
        widget.after(delay, animation_step)

    animation_step()
