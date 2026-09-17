import re

from PySide6.QtWidgets import QLineEdit

from text_handler import parse_time_string


class TimerEntryManager:
    def __init__(self, timer_entry: QLineEdit) -> None:
        """
        Initialize the formatter.

        Args:
            timer_entry: The QLineEdit holding the timer text.
                Signals are not connected here (see init/setup.py).
        """
        self.timer_entry = timer_entry

    def format_on_change(self, _: str | None = None) -> None:
        """
        Slot for QLineEdit.textEdited.
        Formats the digits in the entry to HH:MM:SS style automatically.
        """
        current_content = self.timer_entry.text()
        # Extract digits, removing any existing formatting or non-digits and limit to max 6 digits
        digits = re.sub(r"\D", "", current_content)
        digits = digits[:6]

        formatted_str = ""
        len_digits = len(digits)

        if len_digits == 6:  # HH:MM:SS
            formatted_str = f"{digits[:2]}:{digits[2:4]}:{digits[4:]}"
        elif len_digits == 5:  # H:MM:SS
            formatted_str = f"{digits[:1]}:{digits[1:3]}:{digits[3:]}"
        elif len_digits == 4:  # MM:SS
            formatted_str = f"{digits[:2]}:{digits[2:]}"
        elif len_digits == 3:  # M:SS
            formatted_str = f"{digits[:1]}:{digits[1:]}"
        else:  # S or SS or empty
            formatted_str = digits

        if current_content != formatted_str:
            # Get cursor position *before* setting the text (setText moves it to the end)
            cursor_pos = self.timer_entry.cursorPosition()
            self.timer_entry.setText(formatted_str)

            try:
                # If format added colons before cursor, shift right
                new_cursor_pos = cursor_pos

                old_colons = current_content[:cursor_pos].count(":")
                new_colons = formatted_str[:cursor_pos].count(":")
                diff_colons = new_colons - old_colons

                new_cursor_pos += diff_colons

                # Ensures the cursor stays within bounds
                new_cursor_pos = max(0, min(new_cursor_pos, len(formatted_str)))
                self.timer_entry.setCursorPosition(new_cursor_pos)
            except Exception as e:
                # Fallback if index calculation fails
                print(f"new_cursor_pos: Exception {e}")
                self.timer_entry.end(False)

    def safe_set(self, value: str) -> None:
        """
        Programmatically sets the entry text. setText() does not emit
        textEdited, so the formatting logic is not triggered.
        """
        self.timer_entry.setText(value)

    def format_now(self) -> None:
        """Manually triggers the formatting logic once."""
        self.format_on_change()

    def get_time_formatted(self) -> int | None:
        self.format_now()
        result = self.timer_entry.text()
        return parse_time_string(result)
