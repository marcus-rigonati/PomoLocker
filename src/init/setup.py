
def setup_timer_entry_bindings(timer_entry, timer_entry_manager):
    """Add callback in the correct order to format the input whenever the user types"""
    timer_entry.bindtags(((str(timer_entry)), "Entry", "post-processing", ".", "all"))
    timer_entry.bind_class("post-processing", "<KeyPress>", timer_entry_manager.format_on_change)

def setup_keyboard_shortcuts(window, timer_entry, timer):
    """For starting/stopping the timer."""
    window.unbind_all("<Return>")
    window.bind("<Return>", timer.start_stop)
    window.bind("<KP_Enter>", timer.start_stop)

    def custom_on_press_space(event):
        timer.start_stop()
        return "break"

    timer_entry.bind("<space>", custom_on_press_space)

def setup_mac_specific_features(window):
    """
    Set up macOS-specific features.
    Bring app back from minimized state.
    """
    window.createcommand('tk::mac::ReopenApplication', window.deiconify)
