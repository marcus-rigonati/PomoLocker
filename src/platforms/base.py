from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget


class Platform:
    """OS-specific behaviors PomoLocker needs, one concrete subclass per platform.

    Subclasses must implement lock_screen(). focus_app() and
    register_reopen_handler() have sensible cross-platform defaults.
    """

    def lock_screen(self) -> None:
        """Lock the screen / put the display to sleep. Every platform must implement this."""
        raise NotImplementedError("Screen lock is not implemented for this platform.")

    def focus_app(self, window: QWidget) -> None:
        """Bring the app window to the foreground. Qt-native default."""
        window.setWindowState(window.windowState() & ~Qt.WindowState.WindowMinimized)
        window.show()
        window.raise_()
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        window.show()
        window.activateWindow()
        QTimer.singleShot(100, window, lambda: self._clear_topmost(window))

    # TODO this function needs testing, is it really necessary? What does it do?
    def _clear_topmost(self, window: QWidget) -> None:
        """Drop the temporary always-on-top hint set by focus_app()."""
        window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        window.show()

    def register_reopen_handler(self, window: QWidget) -> None:
        """Register an OS reopen/restore handler. No-op except on macOS."""
