import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QListWidget, QListWidgetItem, QScrollArea
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


# ---------------------------------------------------------
# RESOLVE ICON PATH ROBUSTLY
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ICON_PATH = os.path.join(BASE_DIR, "icons")


def card_frame():
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: rgba(255, 255, 255, 0.97);
            border-radius: 26px;
            border: 1px solid rgba(237, 233, 254, 0.6);
        }
    """)
    return frame


class DashboardScreen(QWidget):
    def __init__(self, app_window=None, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background: transparent;")

        # Safe fallbacks
        self.go_dashboard = getattr(app_window, "go_dashboard", lambda: None)
        self.go_evidence = getattr(app_window, "go_evidence", lambda: None)
        self.go_analysis = getattr(app_window, "go_analysis", lambda: None)
        self.go_timeline = getattr(app_window, "go_timeline", lambda: None)
        self.go_reports = getattr(app_window, "go_reports", lambda: None)
        self.go_logs = getattr(app_window, "go_logs", lambda: None)
        self.go_new_case = getattr(app_window, "show_new_case", lambda: None)
        self.go_load_case = getattr(app_window, "go_load_case", lambda: None)

        self.init_ui()

    # ---------------------------------------------------------
    # SIDEBAR BUTTON (gradient active highlight)
    # ---------------------------------------------------------
    def nav_button(self, text, icon_name, callback, active=False):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)

        icon_file = os.path.join(ICON_PATH, icon_name + ".svg")
        btn.setIcon(QIcon(icon_file))
        btn.setIconSize(QSize(24, 24))

        base = """
            QPushButton {
                text-align: left;
                padding: 14px 16px;
                border-radius: 12px;
                font-size: 16px;
                color: #4B5563;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(139, 92, 246, 0.10);
            }
        """

        if active:
            extra = """
                QPushButton {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #8B5CF6,
                        stop:1 #EC4899
                    );
                    color: white;
                    font-weight: 600;
                }
            """
        else:
            extra = "QPushButton { font-weight: 400; }"

        btn.setStyleSheet(extra + base)
        btn.clicked.connect(callback)
        return btn

    # ---------------------------------------------------------
    # MAIN UI
    # ---------------------------------------------------------
    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---------------------------------------------------------
        # TOPBAR (whiter, softer)
        # ---------------------------------------------------------
        topbar = QFrame()
        topbar.setFixedHeight(72)
        topbar.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.94);
                border-bottom: 1px solid rgba(237, 233, 254, 0.6);
            }
        """)

        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(28, 0, 28, 0)

        title = QLabel("MetaTrace Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #374151;")
        topbar_layout.addWidget(title)
        topbar_layout.addStretch()

        root.addWidget(topbar)

        # ---------------------------------------------------------
        # MAIN AREA (sidebar + content)
        # ---------------------------------------------------------
        main_area = QHBoxLayout()
        main_area.setContentsMargins(0, 0, 0, 0)
        main_area.setSpacing(0)

        # ---------------------------------------------------------
        # SIDEBAR (whiter, icons, gradient active)
        # ---------------------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.96);
                border-right: 1px solid rgba(237, 233, 254, 0.6);
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(24, 28, 24, 28)
        sidebar_layout.setSpacing(18)

        sidebar_layout.addWidget(
            self.nav_button("Dashboard", "dashboard", self.go_dashboard, active=True)
        )
        sidebar_layout.addWidget(self.nav_button("Evidence", "evidence", self.go_evidence))
        sidebar_layout.addWidget(self.nav_button("Analysis", "analysis", self.go_analysis))
        sidebar_layout.addWidget(self.nav_button("Timeline", "timeline", self.go_timeline))
        sidebar_layout.addWidget(self.nav_button("Reports", "report", self.go_reports))
        sidebar_layout.addWidget(self.nav_button("Logs", "log", self.go_logs))

        sidebar_layout.addSpacing(16)

        sidebar_layout.addWidget(self.nav_button("New Case", "new", self.go_new_case))
        sidebar_layout.addWidget(self.nav_button("Load Case", "open", self.go_load_case))

        sidebar_layout.addStretch()
        main_area.addWidget(sidebar)

        # ---------------------------------------------------------
        # CONTENT AREA (ONE COLUMN, BIGGER TEXT)
        # ---------------------------------------------------------
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(48, 48, 48, 48)
        content_layout.setSpacing(48)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.viewport().setStyleSheet("background: transparent;")

        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setSpacing(48)

        # ---------------------------------------------------------
        # CARD 1 — Latest Case Summary
        # ---------------------------------------------------------
        summary = card_frame()
        s_layout = QVBoxLayout(summary)
        s_layout.setContentsMargins(40, 40, 40, 40)
        s_layout.setSpacing(20)

        s_title = QLabel("Latest Case Summary")
        s_title.setStyleSheet("font-size: 24px; font-weight: 600; color: #374151;")
        s_layout.addWidget(s_title)

        for label, value in [
            ("Case Name:", "Case-2026-042-Cyber-Incident"),
            ("Evidence Files:", "127 files"),
            ("Last Activity:", "2 hours ago"),
            ("Case Status:", "Analysis in Progress"),
        ]:
            info = QLabel(f"{label} <b>{value}</b>")
            info.setStyleSheet("font-size: 16px; color: #4B5563;")
            s_layout.addWidget(info)

        inner_layout.addWidget(summary)

        # ---------------------------------------------------------
        # CARD 2 — Investigation Progress
        # ---------------------------------------------------------
        progress = card_frame()
        p_layout = QVBoxLayout(progress)
        p_layout.setContentsMargins(40, 40, 40, 40)
        p_layout.setSpacing(20)

        p_title = QLabel("Investigation Progress")
        p_title.setStyleSheet("font-size: 24px; font-weight: 600; color: #374151;")
        p_layout.addWidget(p_title)

        p_label = QLabel("Overall Completion: 68%")
        p_label.setStyleSheet("font-size: 16px; color: #4B5563;")
        p_layout.addWidget(p_label)

        bar_bg = QFrame()
        bar_bg.setFixedHeight(10)
        bar_bg.setStyleSheet("background-color: #E5E7EB; border-radius: 5px;")

        bar_fill = QFrame(bar_bg)
        bar_fill.setGeometry(0, 0, int(0.68 * 300), 10)
        bar_fill.setStyleSheet("background-color: #8B5CF6; border-radius: 5px;")

        p_layout.addWidget(bar_bg)
        inner_layout.addWidget(progress)

        # ---------------------------------------------------------
        # CARD 3 — Case Actions
        # ---------------------------------------------------------
        actions = card_frame()
        a_layout = QVBoxLayout(actions)
        a_layout.setContentsMargins(40, 40, 40, 40)
        a_layout.setSpacing(24)

        a_title = QLabel("Case Actions")
        a_title.setStyleSheet("font-size: 24px; font-weight: 600; color: #374151;")
        a_layout.addWidget(a_title)

        btn_continue = QPushButton("Continue Current Case")
        btn_continue.clicked.connect(self.go_analysis)
        btn_continue.setStyleSheet("""
            QPushButton {
                padding: 14px 20px;
                border-radius: 14px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8B5CF6,
                    stop:1 #EC4899
                );
                color: white;
                font-size: 16px;
            }
            QPushButton:hover { opacity: 0.9; }
        """)
        a_layout.addWidget(btn_continue)

        btn_load = QPushButton("Load Case")
        btn_load.clicked.connect(self.go_load_case)
        btn_load.setStyleSheet("""
            QPushButton {
                padding: 14px 20px;
                border-radius: 14px;
                background-color: #F3F4F6;
                color: #374151;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #E5E7EB; }
        """)
        a_layout.addWidget(btn_load)

        inner_layout.addWidget(actions)

        # ---------------------------------------------------------
        # CARD 4 — Recent Activity
        # ---------------------------------------------------------
        activity = card_frame()
        act_layout = QVBoxLayout(activity)
        act_layout.setContentsMargins(40, 40, 40, 40)
        act_layout.setSpacing(20)

        act_title = QLabel("Recent Activity")
        act_title.setStyleSheet("font-size: 24px; font-weight: 600; color: #374151;")
        act_layout.addWidget(act_title)

        act_list = QListWidget()
        act_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                background-color: #F5F3FF;
                border-radius: 12px;
                margin: 6px;
                padding: 10px;
                color: #374151;
                font-size: 15px;
            }
        """)
        act_list.addItem(QListWidgetItem("File added — laptop_image_2026.dd (2 hours ago)"))
        act_layout.addWidget(act_list)

        inner_layout.addWidget(activity)

        scroll.setWidget(inner)
        content_layout.addWidget(scroll)

        main_area.addWidget(content)
        root.addLayout(main_area)
