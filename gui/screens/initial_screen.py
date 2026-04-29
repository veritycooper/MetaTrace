import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor, QPixmap
from PyQt5.QtCore import Qt


def icon_path(name: str) -> str:
    """
    Resolve icons relative to the project root:
    gui/screens/ -> ../../icons/<name>
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "..", "icons", name)


def safe_pixmap(path: str, fallback: str = None) -> QPixmap:
    """
    Load a QPixmap safely. Returns a tiny blank pixmap if load fails to avoid warnings.
    """
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
    # tiny blank pixmap to avoid QPixmap::scaled warnings
    return QPixmap(1, 1)


class InitialScreen(QWidget):
    # Opening screen with MetaTrace title and two main action cards

    def __init__(self, navigate_new_case, navigate_open_case, parent=None):
        super().__init__(parent)
        self.navigate_new_case = navigate_new_case
        self.navigate_open_case = navigate_open_case
        self.init_ui()

    def init_ui(self):
        # Gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor("#FDF2F8"))
        gradient.setColorAt(0.5, QColor("#F5F3FF"))
        gradient.setColorAt(1.0, QColor("#EFF6FF"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Main layout container
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        container = QVBoxLayout()
        container.setAlignment(Qt.AlignCenter)
        container.setSpacing(24)

        # Title
        title_label = QLabel("MetaTrace")
        title_font = QFont()
        title_font.setPointSize(40)
        title_font.setWeight(QFont.Light)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1F2937;")
        title_label.setAlignment(Qt.AlignCenter)

        # Subtitle
        subtitle_label = QLabel("Digital Forensics Toolkit")
        subtitle_label.setStyleSheet("color: #4B5563; font-size: 16px;")
        subtitle_label.setAlignment(Qt.AlignCenter)

        # Instruction text
        instruction_label = QLabel("Create or load a case to begin analysis")
        instruction_label.setStyleSheet("color: #6B7280; font-size: 14px;")
        instruction_label.setAlignment(Qt.AlignCenter)

        # Buttons row
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(24)
        buttons_row.setAlignment(Qt.AlignCenter)

        # --- Start New Case button card ---
        new_case_button = QPushButton()
        new_case_button.setCursor(Qt.PointingHandCursor)
        new_case_button.setFixedSize(220, 200)
        new_case_button.clicked.connect(self.navigate_new_case)
        new_case_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 24px;
                border: 1px solid #E9D5FF;
                padding: 16px;
            }
            QPushButton:hover {
                border: 1px solid #C4B5FD;
            }
        """)

        new_case_layout = QVBoxLayout(new_case_button)
        new_case_layout.setAlignment(Qt.AlignCenter)
        new_case_layout.setSpacing(12)

        # Icon bubble
        new_icon_bg = QLabel()
        new_icon_bg.setFixedSize(72, 72)
        new_icon_bg.setStyleSheet("""
            QLabel {
                border-radius: 24px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #EDE9FE,
                    stop:1 #FCE7F3
                );
            }
        """)

        # Icon inside bubble (safe load)
        new_icon = QLabel(new_icon_bg)
        new_icon.setAlignment(Qt.AlignCenter)
        new_icon_path = icon_path("new.svg")
        # Debug print to terminal so you can verify the resolved path
        print("InitialScreen new.svg resolved path:", os.path.abspath(new_icon_path))
        print("Exists:", os.path.exists(new_icon_path))
        new_pix = safe_pixmap(new_icon_path)
        new_icon.setPixmap(new_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        new_icon.setGeometry(0, 0, 72, 72)

        new_text = QLabel("Start New Case")
        new_text.setAlignment(Qt.AlignCenter)
        new_text.setStyleSheet("color: #374151; font-size: 16px; font-weight: 500;")

        new_case_layout.addWidget(new_icon_bg)
        new_case_layout.addWidget(new_text)

        # --- Open Existing Case button card ---
        open_case_button = QPushButton()
        open_case_button.setCursor(Qt.PointingHandCursor)
        open_case_button.setFixedSize(220, 200)
        open_case_button.clicked.connect(self.navigate_open_case)
        open_case_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 24px;
                border: 1px solid #BFDBFE;
                padding: 16px;
            }
            QPushButton:hover {
                border: 1px solid #60A5FA;
            }
        """)

        open_case_layout = QVBoxLayout(open_case_button)
        open_case_layout.setAlignment(Qt.AlignCenter)
        open_case_layout.setSpacing(12)

        open_icon_bg = QLabel()
        open_icon_bg.setFixedSize(72, 72)
        open_icon_bg.setStyleSheet("""
            QLabel {
                border-radius: 24px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #DBEAFE,
                    stop:1 #EDE9FE
                );
            }
        """)

        open_icon = QLabel(open_icon_bg)
        open_icon.setAlignment(Qt.AlignCenter)
        open_icon_path = icon_path("open.svg")
        print("InitialScreen open.svg resolved path:", os.path.abspath(open_icon_path))
        print("Exists:", os.path.exists(open_icon_path))
        open_pix = safe_pixmap(open_icon_path)
        open_icon.setPixmap(open_pix.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        open_icon.setGeometry(0, 0, 72, 72)

        open_text = QLabel("Open Existing Case")
        open_text.setAlignment(Qt.AlignCenter)
        open_text.setStyleSheet("color: #374151; font-size: 16px; font-weight: 500;")

        open_case_layout.addWidget(open_icon_bg)
        open_case_layout.addWidget(open_text)

        # Add both cards to row
        buttons_row.addWidget(new_case_button)
        buttons_row.addWidget(open_case_button)

        # Assemble container
        container.addWidget(title_label)
        container.addWidget(subtitle_label)
        container.addSpacing(8)
        container.addWidget(instruction_label)
        container.addSpacing(16)
        container.addLayout(buttons_row)

        main_layout.addLayout(container)
