import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QListWidget, QListWidgetItem, QPushButton, QFrame,
    QScrollArea
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt

from ..components.file_drop_area import FileDropArea

def icon_path(name: str) -> str:
    # screens live in gui/screens -> icons are at project_root/icons
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "..", "icons", name)

def safe_pixmap(path: str, fallback: str = None) -> QPixmap:
    p = os.path.abspath(path)
    if os.path.exists(p):
        pix = QPixmap(p)
        if not pix.isNull():
            return pix
    if fallback:
        fb = os.path.abspath(fallback)
        if os.path.exists(fb):
            pix = QPixmap(fb)
            if not pix.isNull():
                return pix
    return QPixmap(1, 1)


class NewCaseScreen(QWidget):
    def __init__(self, app_window=None, navigate_back=None, navigate_to_app=None, parent=None, **kwargs):
        """
        Backwards-compatible constructor:
        - Accepts app_window (as used in app.py)
        - Accepts explicit navigate_back and navigate_to_app callbacks
        - Falls back to no-op callbacks if none provided
        """
        super().__init__(parent)

        # Resolve navigation callbacks with fallbacks
        # If explicit callbacks provided, use them. Otherwise try to derive from app_window.
        if navigate_back is not None:
            self.navigate_back = navigate_back
        else:
            self.navigate_back = getattr(app_window, "go_new_case", lambda: None)

        if navigate_to_app is not None:
            self.navigate_to_app = navigate_to_app
        else:
            # Common pattern: app_window.go_dashboard or app_window.go_dashboard
            self.navigate_to_app = getattr(app_window, "go_dashboard", lambda: None)

        # Internal state
        self.case_name = ""
        self.description = ""
        self.files = []

        self.init_ui()

    def init_ui(self):
        # --- Keep your gradient background exactly as before ---
        self.setStyleSheet("QLabel { outline: none; }")

        palette = QPalette()
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor("#FDF2F8"))
        gradient.setColorAt(0.5, QColor("#F5F3FF"))
        gradient.setColorAt(1.0, QColor("#EFF6FF"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # --- Main layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignTop)

        # ============================================================
        # --- Header section ---
        # ============================================================

        header = QVBoxLayout()
        header.setAlignment(Qt.AlignCenter)
        header.setSpacing(8)

        icon_bg = QLabel()
        icon_bg.setFixedSize(56, 56)
        icon_bg.setStyleSheet("""
            QLabel {
                border-radius: 20px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #EDE9FE,
                    stop:1 #FCE7F3
                );
            }
        """)

        icon_label = QLabel(icon_bg)
        icon_label.setAlignment(Qt.AlignCenter)
        # safe load the "new" icon and print debug info
        top_icon_file = icon_path("new.svg")
        print("NewCaseScreen new.svg resolved path:", os.path.abspath(top_icon_file))
        print("Exists:", os.path.exists(top_icon_file))
        pix = safe_pixmap(top_icon_file, fallback=icon_path("open.svg"))
        icon_label.setPixmap(pix.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setGeometry(0, 0, 56, 56)

        title = QLabel("Create New Case")
        title_font = QFont()
        title_font.setPointSize(26)
        title_font.setWeight(QFont.Light)
        title.setFont(title_font)
        title.setStyleSheet("color: #1F2937;")

        subtitle = QLabel("Enter case details and upload evidence files")
        subtitle.setStyleSheet("color: #4B5563; font-size: 14px;")

        header.addWidget(icon_bg)
        header.addWidget(title)
        header.addWidget(subtitle)

        # ============================================================
        # ⭐ SCROLL AREA — fully transparent (viewport too!)
        # ============================================================

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        # ⭐ CRITICAL FIX — this is what stops the grey background
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        scroll.viewport().setStyleSheet("background: transparent;")

        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setSpacing(30)
        scroll_layout.setAlignment(Qt.AlignTop)

        # ============================================================
        # --- Form card ---
        # ============================================================

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 26px;
                border: 1px solid #E9D5FF;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(22)

        # --- Case Name ---
        label_case = QLabel("Case Name *")
        label_case.setStyleSheet("""
            color: #4B5563;
            font-size: 13px;
            font-weight: 400;
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2px 4px;
            border: none;
        """)

        self.case_input = QLineEdit()
        self.case_input.setPlaceholderText("Enter case name...")
        self.case_input.textChanged.connect(self.on_case_name_changed)
        self.case_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 14px;
                border-radius: 12px;
                border: 1px solid #E9D5FF;
            }
            QLineEdit:focus {
                border: 1px solid #C4B5FD;
            }
        """)

        # --- Description ---
        label_desc = QLabel("Description (Optional)")
        label_desc.setStyleSheet("""
            color: #4B5563;
            font-size: 13px;
            font-weight: 400;
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2px 4px;
            border: none;
        """)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter case description...")
        self.desc_input.textChanged.connect(self.on_description_changed)
        self.desc_input.setFixedHeight(110)
        self.desc_input.setStyleSheet("""
            QTextEdit {
                padding: 10px 14px;
                border-radius: 12px;
                border: 1px solid #E9D5FF;
            }
            QTextEdit:focus {
                border: 1px solid #C4B5FD;
            }
        """)

        # --- Evidence Files ---
        label_files = QLabel("Evidence Files *")
        label_files.setStyleSheet("""
            color: #4B5563;
            font-size: 13px;
            font-weight: 400;
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2px 4px;
            border: none;
        """)

        self.drop_area = FileDropArea(self.add_files)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: transparent;
            }
            QListWidget::item {
                background-color: #F5F3FF;
                border-radius: 12px;
                margin: 4px;
                padding: 8px 10px;
            }
        """)

        # --- Buttons ---
        buttons = QHBoxLayout()
        buttons.setAlignment(Qt.AlignRight)
        buttons.setSpacing(12)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.navigate_back)
        cancel.setStyleSheet("""
            QPushButton {
                padding: 10px 18px;
                border-radius: 12px;
                background-color: #F3F4F6;
                color: #4B5563;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)

        self.start = QPushButton("Start Analysis")
        self.start.clicked.connect(self.on_start_analysis)
        self.start.setEnabled(False)
        self.start.setStyleSheet("""
            QPushButton {
                padding: 10px 22px;
                border-radius: 12px;
                background-color: #E5E7EB;
                color: #9CA3AF;
            }
            QPushButton:enabled {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8B5CF6,
                    stop:1 #EC4899
                );
                color: white;
            }
        """)

        buttons.addWidget(cancel)
        buttons.addWidget(self.start)

        # --- Add widgets to card ---
        card_layout.addWidget(label_case)
        card_layout.addWidget(self.case_input)
        card_layout.addWidget(label_desc)
        card_layout.addWidget(self.desc_input)
        card_layout.addWidget(label_files)
        card_layout.addWidget(self.drop_area)
        card_layout.addWidget(self.file_list)
        card_layout.addLayout(buttons)

        # --- Add header + card to scroll container ---
        scroll_layout.addLayout(header)
        scroll_layout.addWidget(card)

        scroll.setWidget(scroll_container)

        # --- Add scroll area to main layout ---
        main_layout.addWidget(scroll)

    # --- Logic ---
    def on_case_name_changed(self, text):
        self.case_name = text.strip()
        self.update_start_button_state()

    def on_description_changed(self):
        self.description = self.desc_input.toPlainText().strip()

    def add_files(self, paths):
        for path in paths:
            if path not in self.files:
                self.files.append(path)
                self.file_list.addItem(QListWidgetItem(path))
        self.update_start_button_state()

    def update_start_button_state(self):
        self.start.setEnabled(bool(self.case_name) and len(self.files) > 0)

    def on_start_analysis(self):
        if self.start.isEnabled():
            # call the navigation callback (derived from app_window or provided directly)
            self.navigate_to_app()
