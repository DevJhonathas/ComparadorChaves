
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from comparador.bootstrap import create_main_window
from comparador.infrastructure.logging.logging_config import configure_logging

import ctypes


def get_application_icon() -> QIcon:
    candidates = [
        Path(sys.argv[0]).resolve().parent / "resources" / "icons" / "app.ico",
        Path(__file__).resolve().parents[2] / "resources" / "icons" / "app.ico",
    ]

    for path in candidates:
        if path.is_file():
            return QIcon(str(path))

    return QIcon()

def main() -> int:
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "ComparadorChaves.Desktop"
        )

    app = QApplication(sys.argv)

    app.setOrganizationName("ComparadorChaves")
    app.setApplicationName("Comparador de Chaves")
    app.setApplicationDisplayName("Comparador de Chaves")

    app_icon = get_application_icon()

    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    configure_logging()

    window = create_main_window()

    if not app_icon.isNull():
        window.setWindowIcon(app_icon)

    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
