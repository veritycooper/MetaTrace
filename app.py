# app.py — MetaTrace GUI entry point (starts on InitialScreen)

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

# Import screens from the screens package
from gui.screens.initial_screen import InitialScreen
from gui.screens.new_case_screen import NewCaseScreen
from gui.screens.dashboard_screen import DashboardScreen


class MetaTraceWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MetaTrace")
        self.setMinimumSize(1100, 700)

        # Central stacked widget (screen manager)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create screens but do not assume constructor signatures beyond app_window compatibility
        # Pass app_window so screens can derive callbacks if they accept app_window
        self.initial_screen = InitialScreen(navigate_new_case=self.show_new_case,
                                            navigate_open_case=self.show_load_case,
                                            parent=self)
        self.new_case_screen = NewCaseScreen(app_window=self)  # NewCaseScreen is backwards-compatible
        self.dashboard_screen = DashboardScreen(app_window=self)

        # Add screens to stack in the order we want them to appear
        self.stack.addWidget(self.initial_screen)   # index 0 — initial opening screen
        self.stack.addWidget(self.new_case_screen)  # index 1
        self.stack.addWidget(self.dashboard_screen) # index 2

        # Start on InitialScreen (the opening screen)
        self.stack.setCurrentWidget(self.initial_screen)

        # Ensure NewCaseScreen can call back into the window
        # If NewCaseScreen expects navigate_back/navigate_to_app names, it will derive them from app_window
        # But also set explicit methods if needed:
        self.new_case_screen.navigate_back = self.show_initial
        self.new_case_screen.navigate_to_app = self.go_dashboard

    # ---------------------------------------------------------
    # Screen switching helpers
    # ---------------------------------------------------------
    def show_initial(self):
        self.stack.setCurrentWidget(self.initial_screen)

    def show_new_case(self):
        self.stack.setCurrentWidget(self.new_case_screen)

    def show_load_case(self):
        # placeholder for load case flow
        print("Open case flow not implemented yet")

    def go_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_screen)

    # Other placeholders for sidebar callbacks (dashboard_screen may call these)
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
