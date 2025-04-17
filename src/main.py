import tkinter
from tkinter import ttk
from tkinter import messagebox

from text_handler import *
from timer_entry_manager import TimerEntryManager
from run_shell_command import run_shell_command
from test_color_fade import animate_bg_change

INITIAL_TIME_SECONDS = 25 * 60  # Start with 5 minutes
remaining_seconds = INITIAL_TIME_SECONDS
is_timer_running = False
after_id = None # To store the ID of the scheduled 'after' event
is_formatting = False # Prevents infinite loops during auto-formatting via trace

# Create the main window
window = tkinter.Tk()
window.geometry("500x500")
window.resizable(True, True)
window.minsize(400, 200)
window.maxsize(1000, 1000)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.title("PomoLocker")
window.config(background="#ad504d")

parent_frame = tkinter.Frame(window, padx=1, pady=1, background="#b5625f")
parent_frame.grid(row=0, column=0)

timer_var = tkinter.StringVar()
timer_entry = tkinter.Entry(
    parent_frame,
    textvariable=timer_var,
    font=('Helvetica', 24),
    foreground='white', # Text color
    justify='center',
    state='readonly' if is_timer_running else 'normal', # sets the initial value only
    background=parent_frame.cget("bg"),
    readonlybackground=parent_frame.cget("bg"),
    borderwidth=0,
    highlightthickness=0,
)
timer_entry.pack(pady=20, padx=10, fill='x')

timer_entry_manager = TimerEntryManager(timer_var, timer_entry)

def change_background_colors(window_color, others_color):
    animate_bg_change(window, window_color)
    animate_bg_change(parent_frame, others_color)
    animate_bg_change(timer_entry, others_color)
    animate_bg_change(timer_entry, others_color, property_to_change="readonlybackground")
    animate_bg_change(button, others_color, style)

def countdown_loop():
    global remaining_seconds, is_timer_running, after_id, is_formatting

    if not is_timer_running:
        return

    if remaining_seconds > 0:
        remaining_seconds -= 1
        # Temporarily disable trace formatting during programmatic update
        is_formatting = True
        timer_var.set(format_time(remaining_seconds))
        is_formatting = False
        after_id = window.after(1000, countdown_loop)
    else:
        # Timer reached zero
        print("TIMER FINISHED!")
        change_background_colors("#ad504d", "#b5625f")
        run_shell_command("/usr/bin/pmset displaysleepnow")
        is_timer_running = False
        timer_entry.config(state='normal') # Make editable again
        after_id = None
        # Keep displaying 00:00:00
        is_formatting = True
        timer_var.set(format_time(0))
        is_formatting = False

def start_timer():
    global is_timer_running, after_id, remaining_seconds, is_formatting, timer_entry, style
    if is_timer_running:
        print("Timer is already running.")
        return

    current_input = timer_var.get()
    # Ensure the displayed value matches the format before parsing
    # (e.g., user typed "1" which became "01", use "00:00:01")
    # A simple way is to force re-format just before parsing
    is_formatting = True
    timer_entry_manager.format_on_change() # Format based on current digits
    current_input = timer_var.get() # Get potentially newly formatted value
    is_formatting = False

    parsed_seconds = parse_time_string(current_input)

    if parsed_seconds is not None and parsed_seconds > 0:
        remaining_seconds = parsed_seconds
        is_timer_running = True
        timer_entry.config(state='readonly')
        change_background_colors("#474747", "#373737")
        button_text.set("Stop")
        print(f"Timer started from {format_time(remaining_seconds)}.")
        countdown_loop() # Start the countdown
    elif parsed_seconds == 0:
        messagebox.showwarning("Timer Start", "Cannot start timer from 00:00:00.")
    else:
        # Handle cases where input is incomplete (e.g., "12:34") or invalid
        messagebox.showerror("Timer Start", f"Invalid or incomplete time: '{current_input}'.\nPlease enter time as HH:MM:SS.")

def stop_timer():
    global is_timer_running, after_id, is_formatting
    if is_timer_running:
        is_timer_running = False
        if after_id:
            window.after_cancel(after_id)
            after_id = None
        change_background_colors("#ad504d", "#b5625f")
        timer_entry.config(state='normal')
        button_text.set("Start")
    else:
        print("Timer is not running.")

def start_stop(*args):
    if is_timer_running:
        stop_timer()
    else:
        start_timer()

style = ttk.Style()
style.theme_use('clam')
style.configure(
    "Red.TButton",
    background=parent_frame.cget("bg"),
    foreground='white',
    borderwidth=1,
    font=('Arial', 12, "bold"),
    bordercolor='white',
    focusthickness=0,
    focuscolor='none',
)
style.map(
    "Red.TButton",
    background=[("active", "#be6b68")]
)

button_text = tkinter.StringVar(None, "Start")
button = ttk.Button(parent_frame, textvariable=button_text, command=start_stop, style='Red.TButton')
button.pack(pady=20)

# --- Set Initial Display ---
timer_entry_manager.safe_set(format_time(remaining_seconds))

# Add callback in the correct order to format the input whenever the user types
timer_entry.bindtags(((str(timer_entry)), "Entry", "post-processing", ".", "all"))
timer_entry.bind_class("post-processing", "<KeyPress>", timer_entry_manager.format_on_change)
# Add callback for the Return key (Start/Stop timer)
window.bind_all("<Return>", start_stop)

# Start the Tkinter event loop (keeps the window open)
window.mainloop()

# Clean up after the window is closed
if after_id:
    try:
        window.after_cancel(after_id)
    except tkinter.TclError:
        pass # Ignore error if window is already destroyed
print("Tkinter app closed.")