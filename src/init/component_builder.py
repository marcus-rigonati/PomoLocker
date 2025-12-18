import tkinter
from tkinter import ttk

from src.constants import WINDOW_BG_COLOR, FRAME_BG_COLOR, BUTTON_ACTIVE_COLOR
from src.init.ui_components import UIComponents

def create_main_window():
    window = tkinter.Tk()
    window.geometry("400x200")
    window.resizable(True, True)
    window.minsize(400, 200)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.title("PomoLocker")
    window.config(background=WINDOW_BG_COLOR)
    return window

def create_parent_frame(window):
    parent_frame = tkinter.Frame(window, pady=10, background=FRAME_BG_COLOR)
    parent_frame.grid(row=0, column=0)
    return parent_frame

def create_timer_entry(parent_frame):
    timer_var = tkinter.StringVar()
    timer_entry = tkinter.Entry(
        parent_frame,
        textvariable=timer_var,
        font=('Helvetica', 24),
        foreground='white',
        justify='center',
        state='normal',
        background=parent_frame.cget("bg"),
        readonlybackground=parent_frame.cget("bg"),
        borderwidth=0,
        highlightthickness=0,
    )
    timer_entry.grid(row=0, column=0, pady=10, padx=10)
    return timer_var, timer_entry

def create_footer(window):
    footer_text = tkinter.StringVar(value="PomoLocker By Marcus Rigonati")
    footer_entry = tkinter.Entry(
        window,
        textvariable=footer_text,
        font=('Helvetica', 10),
        foreground='white',
        justify='center',
        state='readonly',
        background=window.cget("bg"),
        readonlybackground=window.cget("bg"),
        borderwidth=0,
        highlightthickness=0,
        width=25,
    )
    footer_entry.grid(row=1, column=0, pady=10, padx=10)
    return footer_entry

def configure_button_style(parent_frame):
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
        background=[("active", BUTTON_ACTIVE_COLOR)]
    )
    return style

def create_start_stop_button(parent_frame, button_text, timer):
    button = ttk.Button(
        parent_frame,
        textvariable=button_text,
        command=timer.start_stop,
        style='Red.TButton'
    )
    button.grid(row=1, column=0, pady=10)
    return button

def create_ui_components():
    window = create_main_window()
    parent_frame = create_parent_frame(window)
    timer_var, timer_entry = create_timer_entry(parent_frame)
    footer_entry = create_footer(window)
    style = configure_button_style(parent_frame)
    button_text = tkinter.StringVar(None, "Start")
    return UIComponents(window, parent_frame, timer_var, timer_entry, footer_entry, style, button_text)
