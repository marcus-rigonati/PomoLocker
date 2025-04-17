import tkinter
import re
from text_handler import parse_time_string

class TimerEntryManager:
    def __init__(self, string_var: tkinter.StringVar, entry_widget: tkinter.Entry):
        """
        Initialize the formatter.

        Args:
            string_var: The tk.StringVar linked to the Entry.
            entry_widget: The tk.Entry widget itself.
        """
        self.timer_var = string_var
        self.timer_entry = entry_widget
        self.is_formatting = False # Internal flag to prevent trace recursion

    def format_on_change(self, *args):
        """
        Called by StringVar trace whenever the Entry content changes.
        Formats the digits in the entry to HH:MM:SS style automatically.
        """
        if self.is_formatting: # Prevent recursive calls
            return

        self.is_formatting = True

        current_content = self.timer_var.get()
        # Extract digits, removing any existing formatting or non-digits
        digits = re.sub(r'\D', '', current_content)

        # Limit to max 6 digits
        digits = digits[:6]

        # Build the formatted string
        formatted_str = ""
        len_digits = len(digits)

        if len_digits == 6: # HH:MM:SS
            formatted_str = f"{digits[:2]}:{digits[2:4]}:{digits[4:]}"
        elif len_digits == 5: # H:MM:SS
            formatted_str = f"{digits[:1]}:{digits[1:3]}:{digits[3:]}"
        elif len_digits == 4: # MM:SS
            formatted_str = f"{digits[:2]}:{digits[2:]}"
        elif len_digits == 3: # M:SS
            formatted_str = f"{digits[:1]}:{digits[1:]}"
        else: # S or SS or empty
            formatted_str = digits

        # Update the entry only if the formatted string is different
        if self.timer_var.get() != formatted_str:
            # Store cursor position *before* setting the variable
            cursor_pos = self.timer_entry.index(tkinter.INSERT)
            self.timer_var.set(formatted_str)
            # Try to restore cursor position (this is tricky with auto-format!)
            # Adjusting based on added/removed colons can be complex.
            # Setting to END is simpler, though might not be ideal UX.
            try:
                # Crude adjustment: if format added colons before cursor, shift right
                # This is basic and may not cover all cases well.
                new_cursor_pos = cursor_pos
                # Count colons before cursor in old vs new (approximate)
                old_colons = current_content[:cursor_pos].count(':')
                new_colons = formatted_str[:cursor_pos].count(':') # Approximate target area
                # print(f"old_colons: {old_colons}")
                # print(f"new_colons: {new_colons}")
                diff_colons = new_colons - old_colons
                new_cursor_pos += diff_colons
                # Ensure cursor stays within bounds
                new_cursor_pos = max(0, min(new_cursor_pos, len(formatted_str)))
                # print(f"new_cursor_pos: {new_cursor_pos}")
                self.timer_entry.icursor(new_cursor_pos)
            except Exception: # Fallback if index calculation fails
                print(f"new_cursor_pos: Exception")
                self.timer_entry.icursor(tkinter.END)

        self.is_formatting = False

    def safe_set(self, value):
        """
        Programmatically sets the StringVar's value, bypassing the
        formatting logic temporarily to avoid interference or loops.
        """
        if self.is_formatting:
            # Avoid setting if formatting is already in progress
            print("Warning: safe_set called while formatting was in progress.")
        else:
            self.is_formatting = True
            self.timer_var.set(value)
            self.is_formatting = False

    def format_now(self):
        """ Manually triggers the formatting logic once. """
        self.format_on_change()

    def get_time_formatted(self):
        self.format_now()
        result = self.timer_var.get()
        return parse_time_string(result)
