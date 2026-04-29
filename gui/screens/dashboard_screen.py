import os
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ..components.sidebar import Sidebar


class DashboardScreen(QWidget):
    def __init__(self, app_window=None, parent=None):
        super().__init__(parent)
        self.app_window = app_window
        self.init_ui()

    def init_ui(self):
        # ---------------------------------------------------------
        # Window gradient background
        # ---------------------------------------------------------
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FDF4FF,
                    stop:1 #E9D5FF
                );
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------------------------------------------------
        # Sidebar (left) — bind to app_window if available so callbacks call the real navigation methods
        # ---------------------------------------------------------
        target = self.app_window if getattr(self, "app_window", None) is not None else self

        callbacks = {
            "dashboard": getattr(target, "go_dashboard", self.go_dashboard),
            "evidence": getattr(target, "go_evidence", self.go_evidence),
            "analysis": getattr(target, "go_analysis", self.go_analysis),
            "timeline": getattr(target, "go_timeline", self.go_timeline),
            "reports": getattr(target, "go_reports", self.go_reports),
            "logs": getattr(target, "go_logs", self.go_logs),
            "new_case": getattr(target, "go_new_case", self.go_new_case),
            "load_case": getattr(target, "go_load_case", self.go_load_case),
        }

        sidebar = Sidebar(navigate_callbacks=callbacks)
        main_layout.addWidget(sidebar)

        # ---------------------------------------------------------
        # Scrollable dashboard content (right)
        # ---------------------------------------------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        content = QWidget()
        scroll.setWidget(content)

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)

        # ---------------------------------------------------------
        # Dashboard Cards
        # ---------------------------------------------------------
        content_layout.addWidget(self.latest_case_summary_card())
        content_layout.addWidget(self.investigation_progress_card())
        content_layout.addWidget(self.case_actions_card())
        content_layout.addWidget(self.recent_activity_card())

        content_layout.addStretch()

        main_layout.addWidget(scroll)

    # ---------------------------------------------------------
    # Card: Latest Case Summary
    # ---------------------------------------------------------
    def latest_case_summary_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.65);
                border-radius: 16px;
                border: 1px solid #E9D5FF;
            }
            QLabel {
                color: #4B5563;
                font-size: 14px;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: 600;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Latest Case Summary")
        title.setProperty("class", "title")
        layout.addWidget(title)

        layout.addWidget(QLabel("Case Name: Case-2026-042-Cyber-Incident"))
        layout.addWidget(QLabel("Evidence Files: 127 files"))
        layout.addWidget(QLabel("Last Activity: 2 hours ago"))
        layout.addWidget(QLabel("Case Status: Analysis in Progress"))

        return card

    # ---------------------------------------------------------
    # Card: Investigation Progress
    # ---------------------------------------------------------
    def investigation_progress_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.65);
                border-radius: 16px;
                border: 1px solid #E9D5FF;
            }
            QLabel {
                color: #4B5563;
                font-size: 14px;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: 600;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Investigation Progress")
        title.setProperty("class", "title")
        layout.addWidget(title)

        progress_label = QLabel("Overall Completion: 68%")
        layout.addWidget(progress_label)

        # Simple pastel progress bar
        bar_bg = QFrame()
        bar_bg.setFixedHeight(12)
        bar_bg.setStyleSheet("""
            QFrame {
                background-color: #F3E8FF;
                border-radius: 6px;
            }
        """)

        bar_fill = QFrame(bar_bg)
        bar_fill.setGeometry(0, 0, int(0.68 * 400), 12)
        bar_fill.setStyleSheet("""
            QFrame {
                background-color: #C084FC;
                border-radius: 6px;
            }
        """)

        layout.addWidget(bar_bg)

        return card

    # ---------------------------------------------------------
    # Card: Case Actions
    # ---------------------------------------------------------
    def case_actions_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.65);
                border-radius: 16px;
                border: 1px solid #E9D5FF;
            }
            QPushButton {
                height: 42px;
                border-radius: 10px;
                font-size: 14px;
                color: white;
            }
            QPushButton#primary {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F0ABFC,
                    stop:1 #C084FC
                );
            }
            QPushButton#secondary {
                background-color: transparent;
                border: 1px solid #C084FC;
                color: #4B5563;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: 600;
                color: #4B5563;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel("Case Actions")
        title.setProperty("class", "title")
        layout.addWidget(title)

        from PyQt5.QtWidgets import QPushButton

        btn_continue = QPushButton("Continue Current Case")
        btn_continue.setObjectName("primary")

        btn_load = QPushButton("Load Case")
        btn_load.setObjectName("secondary")

        layout.addWidget(btn_continue)
        layout.addWidget(btn_load)

        return card

    # ---------------------------------------------------------
    # Card: Recent Activity
    # ---------------------------------------------------------
    def recent_activity_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.65);
                border-radius: 16px;
                border: 1px solid #E9D5FF;
            }
            QLabel {
                color: #4B5563;
                font-size: 14px;
            }
            QLabel.title {
                font-size: 18px;
                font-weight: 600;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel("Recent Activity")
        title.setProperty("class", "title")
        layout.addWidget(title)

        events = [
            ("File added — laptop_image_2026.dd", "2 hours ago"),
            ("Hash generated — MD5 checksum completed", "3 hours ago"),
            ("Analysis started — Malware scan initiated", "4 hours ago"),
            ("File added — network_logs_april.pcap", "5 hours ago"),
        ]

        for text, time in events:
            row = QHBoxLayout()
            row.addWidget(QLabel(text))
            time_label = QLabel(time)
            time_label.setAlignment(Qt.AlignRight)
            row.addWidget(time_label)
            layout.addLayout(row)

        return card

    # ---------------------------------------------------------
    # Navigation stubs (fallbacks)
    # ---------------------------------------------------------
    def go_dashboard(self): pass
    def go_evidence(self): pass
    def go_analysis(self): pass
    def go_timeline(self): pass
    def go_reports(self): pass
    def go_logs(self): pass
    def go_new_case(self): pass
    def go_load_case(self): pass
