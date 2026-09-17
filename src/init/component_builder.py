from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from color_animation import ThemeAnimator
from constants import (
    BUTTON_OBJECT_NAME,
    FOOTER_OBJECT_NAME,
    FRAME_OBJECT_NAME,
    TIMER_ENTRY_OBJECT_NAME,
    WINDOW_OBJECT_NAME,
)
from init.ui_components import UIComponents

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
PADDING = 10
TIMER_ENTRY_WIDTH_CHARS = 10
FOOTER_TEXT = "PomoLocker By Marcus Rigonati"


def create_main_window() -> tuple[QWidget, QGridLayout]:
    """Creates the resizable top-level window with a two-row grid layout."""
    window = QWidget()
    window.setObjectName(WINDOW_OBJECT_NAME)
    window.setWindowTitle("PomoLocker")
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    layout = QGridLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    layout.setRowStretch(0, 1)
    layout.setColumnStretch(0, 1)
    return window, layout


def create_parent_frame(
    window: QWidget, layout: QGridLayout
) -> tuple[QFrame, QVBoxLayout]:
    """Creates the frame holding the timer entry and button, centered and sized to its content."""
    parent_frame = QFrame(window)
    parent_frame.setObjectName(FRAME_OBJECT_NAME)

    frame_layout = QVBoxLayout(parent_frame)
    frame_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
    frame_layout.setSpacing(PADDING)

    layout.addWidget(parent_frame, 0, 0, Qt.AlignmentFlag.AlignCenter)
    return parent_frame, frame_layout


def create_timer_entry(parent_frame: QFrame, frame_layout: QVBoxLayout) -> QLineEdit:
    """Creates the entry for HH:MM:SS."""
    timer_entry = QLineEdit(parent_frame)
    timer_entry.setObjectName(TIMER_ENTRY_OBJECT_NAME)
    timer_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
    timer_entry.setMaxLength(8)
    timer_entry.setFrame(False)
    frame_layout.addWidget(timer_entry)
    return timer_entry


def create_start_stop_button(
    parent_frame: QFrame, frame_layout: QVBoxLayout
) -> QPushButton:
    """Creates the Start/Stop button; its clicked signal is connected in setup.py."""
    button = QPushButton("Start", parent_frame)
    button.setObjectName(BUTTON_OBJECT_NAME)
    frame_layout.addWidget(button, 0, Qt.AlignmentFlag.AlignHCenter)
    return button


def create_footer(window: QWidget, layout: QGridLayout) -> QLabel:
    """Creates the footer label at the bottom of the window."""
    footer_label = QLabel(FOOTER_TEXT, window)
    footer_label.setObjectName(FOOTER_OBJECT_NAME)
    footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    footer_label.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
    layout.addWidget(
        footer_label, 1, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
    )
    return footer_label


def size_timer_entry(timer_entry: QLineEdit) -> None:
    """Makes the entry wide enough for "00:00:00" with spare room, using the stylesheet font."""
    timer_entry.ensurePolished()
    text_width = timer_entry.fontMetrics().horizontalAdvance(
        "0" * TIMER_ENTRY_WIDTH_CHARS
    )
    margins = timer_entry.textMargins()
    timer_entry.setMinimumWidth(text_width + margins.left() + margins.right())


def create_ui_components() -> UIComponents:
    """Builds the main window and all its widgets. Requires an existing QApplication."""
    window, layout = create_main_window()
    parent_frame, frame_layout = create_parent_frame(window, layout)
    timer_entry = create_timer_entry(parent_frame, frame_layout)
    start_stop_button = create_start_stop_button(parent_frame, frame_layout)
    footer_label = create_footer(window, layout)
    theme = ThemeAnimator(window)
    size_timer_entry(timer_entry)
    return UIComponents(
        window, parent_frame, timer_entry, start_stop_button, footer_label, theme
    )
