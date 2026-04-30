# app.py — MetaTrace GUI entry point

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor

# Screens
from gui.screens.initial_screen import InitialScreen
from gui.screens.new_case_screen import NewCaseScreen
from gui.screens.dashboard_screen import DashboardScreen


class MetaTraceWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MetaTrace")
        self.setMinimumSize(1200, 800)

        # ---------------------------------------------------------
        # Global gradient background (matches Figma + New Case)
        # ---------------------------------------------------------
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor("#FDF2F8"))
        gradient.setColorAt(0.5, QColor("#F5F3FF"))
        gradient.setColorAt(1.0, QColor("#EFF6FF"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # ---------------------------------------------------------
        # Screen manager
        # ---------------------------------------------------------
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Screens
        self.initial_screen = InitialScreen(
            navigate_new_case=self.show_new_case,
            navigate_open_case=self.show_load_case,
            parent=self
        )

        self.new_case_screen = NewCaseScreen(app_window=self)
        self.dashboard_screen = DashboardScreen(app_window=self)

        # Add screens
        self.stack.addWidget(self.initial_screen)   # index 0
        self.stack.addWidget(self.new_case_screen)  # index 1
        self.stack.addWidget(self.dashboard_screen) # index 2

        # Start on InitialScreen
        self.stack.setCurrentWidget(self.initial_screen)

        # NewCaseScreen callbacks
        self.new_case_screen.navigate_back = self.show_initial
        self.new_case_screen.navigate_to_app = self.go_dashboard

    # ---------------------------------------------------------
    # Navigation methods
    # ---------------------------------------------------------
    def show_initial(self):
        self.stack.setCurrentWidget(self.initial_screen)

    def show_new_case(self):
        self.stack.setCurrentWidget(self.new_case_screen)

    def show_load_case(self):
        print("Load Case screen not implemented yet")

    def go_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_screen)

    # Sidebar callbacks
    def go_evidence(self):
        print("Evidence screen not built yet")

    def go_analysis(self):
        print("Analysis screen not built yet")

    def go_timeline(self):
        print("Timeline screen not built yet")

    def go_reports(self):
        print("Reports screen not built yet")

    def go_logs(self):
        print("Logs screen not built yet")

    def go_load_case(self):
        print("Load Case screen not built yet")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MetaTraceWindow()
    window.show()
    sys.exit(app.exec_())
