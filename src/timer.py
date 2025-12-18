import text_handler
from tkinter import messagebox
from focus_manager import focus_app
from color_animation import animate_bg_change
from run_shell_command import run_shell_command
from init.ui_components import UIComponents
from timer_entry_manager import TimerEntryManager

class Timer:
    def __init__(self, ui_components: UIComponents, timer_entry_manager: TimerEntryManager):
        self.window = ui_components.window
        self.parent_frame = ui_components.parent_frame
        self.timer_var = ui_components.timer_var
        self.timer_entry = ui_components.timer_entry
        self.footer_entry = ui_components.footer_entry
        self.style = ui_components.style
        self.button_text = ui_components.button_text
        self.timer_entry_manager = timer_entry_manager
        self.is_timer_running = False
        self.next_count_down_call_id = None
        self.is_formatting = False

    def change_background_colors(self, window_color, target_color):
        animate_bg_change(self.window, window_color)
        animate_bg_change(self.footer_entry, window_color, property_to_change="readonlybackground")
        animate_bg_change(self.parent_frame, target_color)
        animate_bg_change(self.timer_entry, target_color)
        animate_bg_change(self.timer_entry, target_color, property_to_change="readonlybackground")
        animate_bg_change(self.window, target_color, self.style) # window is used just to schedule steps here

    def countdown_loop_first_call(self):
        self.next_count_down_call_id = self.window.after(1000, self.countdown_loop)

    def countdown_loop(self):
        if not self.is_timer_running:
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.timer_entry_manager.safe_set(text_handler.format_time(self.remaining_seconds))
            self.next_count_down_call_id = self.window.after(1000, self.countdown_loop)
        else:
            # Timer reached zero
            print("TIMER FINISHED!")
            self.change_background_colors("#ad504d", "#b5625f")
            self.window.deiconify()
            focus_app()
            run_shell_command("/usr/bin/pmset displaysleepnow")
            self.is_timer_running = False
            self.timer_entry.config(state='normal')
            self.next_count_down_call_id = None

    def start_timer(self):
        if self.is_timer_running:
            print("Timer is already running.")
            return

        current_seconds = self.timer_entry_manager.get_time_formatted()

        if current_seconds is not None and current_seconds > 0:
            self.remaining_seconds = current_seconds
            self.is_timer_running = True
            self.timer_entry.config(state='readonly')
            self.change_background_colors("#474747", "#373737")
            self.button_text.set("Stop")
            print(f"Timer started from {text_handler.format_time(self.remaining_seconds)}.")
            self.timer_entry_manager.safe_set(text_handler.format_time(self.remaining_seconds))
            self.countdown_loop_first_call()
        elif current_seconds == 0:
            messagebox.showwarning("Timer Start", "Cannot start timer from 00:00:00.")
            self.timer_entry.focus_force()

    def stop_timer(self):
        if self.is_timer_running:
            self.is_timer_running = False
            self.change_background_colors("#ad504d", "#b5625f")
            self.timer_entry.config(state='normal')
            self.button_text.set("Start")
            if self.next_count_down_call_id:
                self.window.after_cancel(self.next_count_down_call_id)
                self.next_count_down_call_id = None
        else:
            print("Timer is not running.")

    def start_stop(self, *args):
        if self.is_timer_running:
            self.stop_timer()
        else:
            self.start_timer()
