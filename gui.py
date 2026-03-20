# gui.py
# PyQt6 desktop application for the CMM Dashboard.
# Replaces the Flask web app with a native Windows UI.

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTabWidget, QPushButton, QLabel,
    QFileDialog, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


# ── Main Window ───────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMM Dashboard")
        self.setMinimumSize(1200, 800)
        self._apply_dark_theme()
        self._build_ui()

    def _apply_dark_theme(self):
        """Applies a dark color palette to the entire application."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window,        QColor("#0F1117"))
        palette.setColor(QPalette.ColorRole.WindowText,    QColor("#E8EAF0"))
        palette.setColor(QPalette.ColorRole.Base,          QColor("#1A1D27"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#0F1117"))
        palette.setColor(QPalette.ColorRole.Text,          QColor("#E8EAF0"))
        palette.setColor(QPalette.ColorRole.Button,        QColor("#1A1D27"))
        palette.setColor(QPalette.ColorRole.ButtonText,    QColor("#E8EAF0"))
        palette.setColor(QPalette.ColorRole.Highlight,     QColor("#00C896"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#0F1117"))
        self.setPalette(palette)

    def _build_ui(self):
        """Builds the main UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        layout.addWidget(self._build_header())

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #0F1117;
            }
            QTabBar::tab {
                background: #1A1D27;
                color: #7B8099;
                padding: 10px 24px;
                border: none;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                color: #00C896;
                border-bottom: 2px solid #00C896;
            }
            QTabBar::tab:hover {
                color: #E8EAF0;
            }
        """)

        # Add tabs
        from gui_single import SingleReportTab
        from gui_trend import TrendTab

        self.tabs.addTab(SingleReportTab(), "Single Report")
        self.tabs.addTab(TrendTab(), "Multi-Run Trend")

        layout.addWidget(self.tabs)

        # Status bar
        self.status = QStatusBar()
        self.status.setStyleSheet("background: #1A1D27; color: #7B8099;")
        self.status.showMessage("Ready — upload a report to get started")
        self.setStatusBar(self.status)

    def _build_header(self) -> QWidget:
        """Builds the top header bar."""
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("background: #1A1D27; border-bottom: 1px solid rgba(255,255,255,0.07);")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QLabel("CMM_DASHBOARD")
        title.setStyleSheet("color: #00C896; font-size: 20px; font-weight: bold; font-family: 'Courier New';")

        subtitle = QLabel("MODUS Inspection Report Analysis")
        subtitle.setStyleSheet("color: #7B8099; font-size: 12px;")

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addLayout(title_layout)
        layout.addStretch()

        return header


# ── Entry Point ───────────────────────────────────────────────────

def main():
    # WebEngine must be initialized before QApplication
    from PyQt6.QtCore import Qt
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()