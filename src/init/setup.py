from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QKeyEvent, QKeySequence, QShortcut
from PySide6.QtWidgets import QLineEdit, QPushButton, QWidget

from timer import Timer
from timer_entry_manager import TimerEntryManager


def setup_timer_entry_bindings(
    timer_entry: QLineEdit, timer_entry_manager: TimerEntryManager
) -> None:
    """Format the input whenever the user types, textEdited fires after the edit is applied."""
    timer_entry.textEdited.connect(timer_entry_manager.format_on_change)


def setup_start_stop_button(button: QPushButton, timer: Timer) -> None:
    """Toggle the timer when the button is clicked."""
    button.clicked.connect(timer.start_stop)


class _SpaceToggleFilter(QObject):
    """Event filter that turns Space in the timer entry into a start/stop toggle."""

    def __init__(self, parent: QObject, timer: Timer) -> None:
        super().__init__(parent)
        self.timer = timer

    def eventFilter(self, _: QObject, event: QEvent) -> bool:
        if (
            event.type() == QEvent.Type.KeyPress
            and isinstance(event, QKeyEvent)
            and event.key() == Qt.Key.Key_Space
        ):
            self.timer.start_stop()
            return True  # No space should get inserted
        else:
            return False


def setup_keyboard_shortcuts(
    window: QWidget, timer_entry: QLineEdit, timer: Timer
) -> None:
    """For starting/stopping the timer."""
    for key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
        shortcut = QShortcut(QKeySequence(key), window)
        shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
        shortcut.activated.connect(timer.start_stop)

    space_filter = _SpaceToggleFilter(timer_entry, timer)
    timer_entry.installEventFilter(space_filter)
