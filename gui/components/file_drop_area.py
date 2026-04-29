# --- Reusable drag-and-drop file upload area (clean, borderless design) ---

import os
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


def icon_path(name: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "..", "icons", name)


class FileDropArea(QFrame):
    # --- Drag-and-drop area that emits file paths via callback ---

    def __init__(self, on_files_added, parent=None):
        super().__init__(parent)
        self.on_files_added = on_files_added
        self.setAcceptDrops(True)

        # --- Remove ALL borders and frame outlines ---
        self.setFrameShape(QFrame.NoFrame)
        self.setLineWidth(0)

        # --- Clean, open design ---
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(237, 233, 254, 0.25);
                border-radius: 20px;
                padding: 32px;
            }

            /* CRITICAL FIX — remove pink outlines around icon + text */
            QFrame * {
                outline: none;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(14)

        # --- Upload icon ---
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)

        upload_pix = QPixmap(icon_path("upload.svg"))
        self.icon_label.setPixmap(
            upload_pix.scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        # --- Instruction text ---
        self.text_label = QLabel("Drag and drop files here\nor click to browse")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("color: #4B5563; font-size: 14px;")

        # --- Browse button ---
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                border-radius: 12px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E9D5FF,
                    stop:1 #FBCFE8
                );
                color: #1F2937;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #DDD6FE,
                    stop:1 #F9A8D4
                );
            }
        """)
        self.browse_button.clicked.connect(self.open_file_dialog)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addWidget(self.browse_button)

    # --- Drag events ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    background-color: rgba(237, 233, 254, 0.45);
                    border-radius: 20px;
                    padding: 32px;
                }
                QFrame * {
                    outline: none;
                    border: none;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(237, 233, 254, 0.25);
                border-radius: 20px;
                padding: 32px;
            }
            QFrame * {
                outline: none;
                border: none;
            }
        """)

    def dropEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.92);   /* match card */
                border-radius: 20px;
                padding: 32px;
                border: 1px solid #E9D5FF;   /* match input fields */
            }

            /* keep child widgets clean */
            QFrame * {
                outline: none;
                border: none;
            }

        """)
        urls = event.mimeData().urls()
        paths = [u.toLocalFile() for u in urls if u.isLocalFile()]
        if paths:
            self.on_files_added(paths)

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Evidence Files")
        if files:
            self.on_files_added(files)
