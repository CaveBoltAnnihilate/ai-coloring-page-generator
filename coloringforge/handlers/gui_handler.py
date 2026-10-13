"""Thin PySide6 launcher. Widgets live in coloringforge.ui."""
from __future__ import annotations

from loguru import logger


def launch_gui(ctx) -> int:
    from PySide6.QtWidgets import QApplication
    from coloringforge.ui.main_window import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow(ctx)
    window.show()
    logger.info("GUI launched")
    return app.exec()