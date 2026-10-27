import sys
from pathlib import Path

# Colors
WINDOW_BG_COLOR = "#ad504d"  # idle window
FRAME_BG_COLOR = "#b5625f"  # idle frame / entry / button

# Qt object names, used as #id selectors in the stylesheet
WINDOW_OBJECT_NAME = "PomoWindow"
FRAME_OBJECT_NAME = "TimerFrame"
TIMER_ENTRY_OBJECT_NAME = "TimerEntry"
BUTTON_OBJECT_NAME = "StartStopButton"
FOOTER_OBJECT_NAME = "Footer"

# Resources: PyInstaller unpacks --add-data files under sys._MEIPASS; from source, use the repo root.
_RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
APP_ICON_PATH = _RESOURCE_ROOT / "icon" / "notification-icon.png"
