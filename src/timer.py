from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMessageBox

import text_handler
from constants import (
    FRAME_BG_COLOR,
    WINDOW_BG_COLOR,
)
from init.ui_components import UIComponents
from platforms.base import Platform
from timer_entry_manager import TimerEntryManager

RUNNING_FRAME_BG_COLOR = "#373737"
RUNNING_WINDOW_BG_COLOR = "#474747"


class Timer:
    def __init__(
        self,
        ui_components: UIComponents,
        timer_entry_manager: TimerEntryManager,
        platform: Platform,
    ) -> None:
        self.window = ui_components.window
        self.parent_frame = ui_components.parent_frame
        self.timer_entry = ui_components.timer_entry
        self.start_stop_button = ui_components.start_stop_button
        self.footer_label = ui_components.footer_label
        self.theme = ui_components.theme
        self.timer_entry_manager = timer_entry_manager
        self.platform = platform
        self.is_timer_running = False
        self.remaining_seconds = 0

        # Self-repeating 1 s tick; the first tick fires 1 s after start().
        self.countdown_timer = QTimer(self.window)
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.countdown_loop)

    def countdown_loop(self) -> None:
        """Handle one countdown tick."""
        if not self.is_timer_running:
            self.countdown_timer.stop()
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.timer_entry_manager.safe_set(
                text_handler.format_time(self.remaining_seconds)
            )
        else:
            # Timer reached zero
            print("Timer Finished!")
            self.theme.animate_to(WINDOW_BG_COLOR, FRAME_BG_COLOR)
            self.window.setWindowState(
                self.window.windowState() & ~Qt.WindowState.WindowMinimized
            )
            self.window.show()
            self.platform.focus_app(self.window)
            self.platform.lock_screen()
            self.is_timer_running = False
            self.timer_entry.setReadOnly(False)
            self.countdown_timer.stop()

    def start_timer(self) -> None:
        if self.is_timer_running:
            print("Timer is already running.")
            return

        current_seconds = self.timer_entry_manager.get_time_formatted()

        if current_seconds is not None and current_seconds > 0:
            self.remaining_seconds = current_seconds
            self.is_timer_running = True
            self.timer_entry.setReadOnly(True)
            self.theme.animate_to(RUNNING_WINDOW_BG_COLOR, RUNNING_FRAME_BG_COLOR)
            self.start_stop_button.setText("Stop")
            print(
                f"Timer started from {text_handler.format_time(self.remaining_seconds)}."
            )
            self.timer_entry_manager.safe_set(
                text_handler.format_time(self.remaining_seconds)
            )
            self.countdown_timer.start()
        elif current_seconds == 0:
            QMessageBox.warning(
                self.window, "Timer Start", "Cannot start timer from 00:00:00."
            )
            self.timer_entry.setFocus()

    def stop_timer(self) -> None:
        if self.is_timer_running:
            self.is_timer_running = False
            self.theme.animate_to(WINDOW_BG_COLOR, FRAME_BG_COLOR)
            self.timer_entry.setReadOnly(False)
            self.start_stop_button.setText("Start")
            self.countdown_timer.stop()
        else:
            print("Timer is not running.")

    def start_stop(self, *args) -> None:
        if self.is_timer_running:
            self.stop_timer()
        else:
            self.start_timer()
