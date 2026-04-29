import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt


def icon_path(name: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "icons", name)


class Sidebar(QFrame):
    def __init__(self, navigate_callbacks=None, parent=None):
        super().__init__(parent)

        # Dictionary of navigation callbacks:
        # {
        #   "dashboard": fn,
        #   "evidence": fn,
        #   "analysis": fn,
        #   ...
        # }
        self.navigate = navigate_callbacks or {}

        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.65);
                border-right: 1px solid #E9D5FF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignTop)

        # ---------------------------------------------------------
        # Logo / App Title
        # ---------------------------------------------------------
        logo = QLabel()
        logo_pix = QPixmap(icon_path("logo.svg"))
        logo.setPixmap(logo_pix.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel("MetaTrace")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 500;
                color: #4B5563;
            }
        """)

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addSpacing(20)

        # ---------------------------------------------------------
        # Navigation Buttons
        # ---------------------------------------------------------
        nav_items = [
            ("Dashboard", "dashboard.svg", "dashboard"),
            ("Evidence", "evidence.svg", "evidence"),
            ("Analysis", "analysis.svg", "analysis"),
            ("Timeline", "timeline.svg", "timeline"),
            ("Reports", "reports.svg", "reports"),
            ("Logs", "logs.svg", "logs"),
            ("New Case", "new.svg", "new_case"),
            ("Load Case", "load.svg", "load_case"),
        ]

        for label, icon_file, key in nav_items:
            btn = self.create_nav_button(label, icon_file, key)
            layout.addWidget(btn)

        layout.addStretch()

    # ---------------------------------------------------------
    # Create a single navigation button
    # ---------------------------------------------------------
    def create_nav_button(self, text, icon_file, key):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(42)
        btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 14px;
                border-radius: 10px;
                background-color: transparent;
                color: #4B5563;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: rgba(233, 213, 255, 0.45);
            }}
        """)

        # Add icon
        icon_label = QLabel(btn)
        pix = QPixmap(icon_path(icon_file))
        icon_label.setPixmap(pix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setGeometry(10, 11, 20, 20)

        # Connect callback if exists
        if key in self.navigate:
            btn.clicked.connect(self.navigate[key])

        return btn
