import sys

from PySide6.QtWidgets import QApplication

import text_handler
from init.component_builder import create_ui_components
from init.setup import (
    setup_keyboard_shortcuts,
    setup_start_stop_button,
    setup_timer_entry_bindings,
)
from platforms import get_platform
from timer import Timer
from timer_entry_manager import TimerEntryManager

INITIAL_TIME_SECONDS = 25 * 60  # 25 minutes


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("PomoLocker")

    ui_components = create_ui_components()
    window = ui_components.window
    platform = get_platform()

    timer_entry_manager = TimerEntryManager(ui_components.timer_entry)
    timer_entry_manager.safe_set(text_handler.format_time(INITIAL_TIME_SECONDS))
    timer = Timer(ui_components, timer_entry_manager, platform)

    # Event bindings
    setup_timer_entry_bindings(ui_components.timer_entry, timer_entry_manager)
    setup_start_stop_button(ui_components.start_stop_button, timer)
    setup_keyboard_shortcuts(window, ui_components.timer_entry, timer)
    platform.register_reopen_handler(window)

    # Start the application
    window.show()
    ui_components.timer_entry.setFocus()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
