from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from orquestador.MainApp import MainApp
from gui.Visualization import MainWindow


class DataLuxApp:
    def __init__(self) -> None:
        self.qt_app: QApplication = QApplication(sys.argv)
        self.main_window: MainWindow = MainWindow()
        self.main_app: MainApp = MainApp()

    def setup_application(self) -> None:
        self.main_app.main_window = self.main_window
        self.main_app.initialize_components()
        self.main_app.initialize_gui()

    def run(self) -> int:
        self.setup_application()
        self.main_window.show()
        return self.qt_app.exec()


if __name__ == "__main__":
    app = DataLuxApp()
    sys.exit(app.run())