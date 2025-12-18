import tkinter
from tkinter import ttk
from dataclasses import dataclass

@dataclass
class UIComponents:
    window: tkinter.Tk
    parent_frame: tkinter.Frame
    timer_var: tkinter.StringVar
    timer_entry: tkinter.Entry
    footer_entry: tkinter.Entry
    style: ttk.Style
    button_text: tkinter.StringVar
