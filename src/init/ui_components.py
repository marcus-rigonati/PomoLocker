from dataclasses import dataclass

from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QPushButton, QWidget

from color_animation import ThemeAnimator


@dataclass
class UIComponents:
    """Bundles every widget of the main window so they can be passed around together."""
    window: QWidget
    parent_frame: QFrame
    timer_entry: QLineEdit
    start_stop_button: QPushButton
    footer_label: QLabel
    theme: ThemeAnimator
