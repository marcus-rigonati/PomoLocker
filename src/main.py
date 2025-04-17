import tkinter
from tkinter import ttk

from text_handler import *
from timer_entry_manager import TimerEntryManager
from timer import Timer

INITIAL_TIME_SECONDS = 25 * 60  # Start with 25 minutes
remaining_seconds = INITIAL_TIME_SECONDS
is_timer_running = False
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

# --- Set Initial Display ---
timer_entry_manager.safe_set(format_time(remaining_seconds))

button_text = tkinter.StringVar(None, "Start")
timer = Timer(window, parent_frame, timer_var, timer_entry, timer_entry_manager, button_text, style)

button = ttk.Button(parent_frame, textvariable=button_text, command=timer.start_stop, style='Red.TButton')
button.pack(pady=20)

# Add callback in the correct order to format the input whenever the user types
timer_entry.bindtags(((str(timer_entry)), "Entry", "post-processing", ".", "all"))
timer_entry.bind_class("post-processing", "<KeyPress>", timer_entry_manager.format_on_change)
# Add callback for the Return key (Start/Stop timer)
window.bind_all("<Return>", timer.start_stop)

# Start the Tkinter event loop (keeps the window open)
window.mainloop()
