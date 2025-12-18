import text_handler
from constants import INITIAL_TIME_SECONDS
from init.component_builder import create_ui_components, create_start_stop_button
from init.setup import setup_timer_entry_bindings, setup_keyboard_shortcuts, setup_mac_specific_features
from timer import Timer
from timer_entry_manager import TimerEntryManager

def main():
    ui_components = create_ui_components()
    window = ui_components.window

    timer_entry_manager = TimerEntryManager(ui_components.timer_var, ui_components.timer_entry)
    timer_entry_manager.safe_set(text_handler.format_time(INITIAL_TIME_SECONDS))
    timer = Timer(ui_components, timer_entry_manager)

    create_start_stop_button(ui_components.parent_frame, ui_components.button_text, timer)

    # Event bindings
    setup_timer_entry_bindings(ui_components.timer_entry, timer_entry_manager)
    setup_keyboard_shortcuts(window, ui_components.timer_entry, timer)
    setup_mac_specific_features(window)

    # Start the application
    ui_components.timer_entry.focus_set()
    window.mainloop()

if __name__ == "__main__":
    main()
