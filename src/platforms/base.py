from tkinter import Tk


class Platform:
    """OS-specific behaviors PomoLocker needs, one concrete subclass per platform.

    Subclasses must implement lock_screen(). focus_app() and
    register_reopen_handler() have sensible cross-platform defaults that only
    macOS needs to override.
    """

    def lock_screen(self) -> None:
        """Lock the screen / put the display to sleep. Every platform must implement this."""
        raise NotImplementedError("Screen lock is not implemented for this platform.")

    def focus_app(self, window: Tk) -> None:
        """Bring the app window to the foreground.

        Tk-native default that works on Windows and Linux; macOS overrides it
        because Tk focus is unreliable there.
        """
        window.deiconify()
        window.lift()
        window.attributes("-topmost", True)
        window.focus_force()
        window.after(100, lambda: window.attributes("-topmost", False))

    def register_reopen_handler(self, window: Tk) -> None:
        """Register an OS reopen/restore handler. No-op except on macOS."""
        pass
