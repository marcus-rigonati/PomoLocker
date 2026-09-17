from PySide6.QtCore import QObject, Qt, QVariantAnimation
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget

from constants import (
    BUTTON_OBJECT_NAME,
    FOOTER_OBJECT_NAME,
    FRAME_BG_COLOR,
    FRAME_OBJECT_NAME,
    TIMER_ENTRY_OBJECT_NAME,
    WINDOW_BG_COLOR,
    WINDOW_OBJECT_NAME,
)

TEXT_COLOR = "#ffffff"
COLOR_ANIMATION_MS = 500
BUTTON_ACTIVE_COLOR = "#be6b68"  # button hover/pressed, in every state


def interpolate_color(start_color: str, end_color: str, fraction: float) -> str:
    """
    Linearly interpolates between two hex colors. Fraction is a float between 0.0 (start_color) and 1.0 (end_color).
    """
    fraction = max(0.0, min(1.0, fraction))
    start = QColor(start_color)
    end = QColor(end_color)
    r = round(start.red() + (end.red() - start.red()) * fraction)
    g = round(start.green() + (end.green() - start.green()) * fraction)
    b = round(start.blue() + (end.blue() - start.blue()) * fraction)
    return f"#{r:02x}{g:02x}{b:02x}"


def build_stylesheet(window_bg: str, frame_bg: str) -> str:
    """Builds the application stylesheet for the given window and frame background colors. Kinda like CSS."""
    return f"""
QWidget#{WINDOW_OBJECT_NAME} {{
    background-color: {window_bg};
}}
QFrame#{FRAME_OBJECT_NAME} {{
    background-color: {frame_bg};
    border: none;
}}
QLineEdit#{TIMER_ENTRY_OBJECT_NAME}, QLineEdit#{TIMER_ENTRY_OBJECT_NAME}[readOnly="true"] {{
    background-color: {frame_bg};
    color: {TEXT_COLOR};
    border: none;
    font-size: 24pt;
    font-family: "Helvetica", "Arial", sans-serif;
}}
QPushButton#{BUTTON_OBJECT_NAME} {{
    background-color: {frame_bg};
    color: {TEXT_COLOR};
    border: 1px solid white;
    font-weight: bold;
    font-size: 12pt;
    font-family: "Arial", "Helvetica", sans-serif;
    padding: 4px 16px;
    outline: none;
}}
QPushButton#{BUTTON_OBJECT_NAME}:hover, QPushButton#{BUTTON_OBJECT_NAME}:pressed {{
    background-color: {BUTTON_ACTIVE_COLOR};
}}
QLabel#{FOOTER_OBJECT_NAME} {{
    color: {TEXT_COLOR};
    background: transparent;
    font-size: 10pt;
    font-family: "Helvetica", "Arial", sans-serif;
}}
"""


class ThemeAnimator(QObject):
    """Applies the app stylesheet to a window and tweens its two background colors."""

    def __init__(
        self,
        window: QWidget,
        window_bg: str = WINDOW_BG_COLOR,
        frame_bg: str = FRAME_BG_COLOR,
    ) -> None:
        super().__init__(window)
        self.window = window
        self.window_bg = window_bg
        self.frame_bg = frame_bg
        self._start_colors = (window_bg, frame_bg)
        self._end_colors = (window_bg, frame_bg)

        # A plain top-level QWidget only paints stylesheet backgrounds with this attribute
        self.window.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.animation = QVariantAnimation(self)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.valueChanged.connect(self._on_step)
        self.animation.finished.connect(self._on_finished)

        self._apply(window_bg, frame_bg)

    def animate_to(
        self,
        target_window_bg: str,
        target_frame_bg: str,
        duration_ms: int = COLOR_ANIMATION_MS,
    ) -> None:
        """Interrupts any running animation and tweens from the current colors to the given ones."""
        self.animation.stop()
        self._start_colors = (self.window_bg, self.frame_bg)
        self._end_colors = (target_window_bg, target_frame_bg)

        if duration_ms > 0:
            self.animation.setDuration(duration_ms)
            self.animation.start()
        else:
            self._on_finished()

    def _on_step(self, fraction: float) -> None:
        """Applies the interpolated colors for the given animation progress."""
        if self.animation.state() == QVariantAnimation.State.Running:
            self._apply(
                interpolate_color(self._start_colors[0], self._end_colors[0], fraction),
                interpolate_color(self._start_colors[1], self._end_colors[1], fraction),
            )

    def _on_finished(self) -> None:
        """Ensures the final colors are set exactly."""
        self._apply(*self._end_colors)

    def _apply(self, window_bg: str, frame_bg: str) -> None:
        """Stores the current colors and re-applies the stylesheet to the window."""
        self.window_bg = window_bg
        self.frame_bg = frame_bg
        self.window.setStyleSheet(build_stylesheet(window_bg, frame_bg))
