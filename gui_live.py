# gui_live.py
# Live view tab for local Equator mode.

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from settings import get_watched_folders, get_global_filters
from parser import load_report
from evaluator import evaluate_report
from visualizer import deviation_bar_chart, summary_donut
from gui_single import StatCard


class LiveTab(QWidget):

    report_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_folder = None
        self.results        = None
        self.last_filepath  = None
        self._build_ui()
        self._refresh_programs()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Program selector row
        selector_row = QHBoxLayout()

        program_label = QLabel("Part Program:")
        program_label.setStyleSheet("color: #7B8099; font-size: 13px;")
        program_label.setFixedWidth(110)

        self.program_combo = QComboBox()
        self.program_combo.setStyleSheet("""
            QComboBox {
                background: #1A1D27;
                color: #E8EAF0;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                min-width: 300px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #1A1D27;
                color: #E8EAF0;
                selection-background-color: #00C896;
            }
        """)
        self.program_combo.currentIndexChanged.connect(self._on_program_changed)

        refresh_btn = QPushButton("Refresh List")
        refresh_btn.setStyleSheet(self._btn_style("#1A1D27", "#7B8099"))
        refresh_btn.clicked.connect(self._refresh_programs)

        self.watch_btn = QPushButton("Start Watching")
        self.watch_btn.setStyleSheet(self._btn_style("#00C896", "#0F1117"))
        self.watch_btn.clicked.connect(self._toggle_watch)

        selector_row.addWidget(program_label)
        selector_row.addWidget(self.program_combo, 1)
        selector_row.addWidget(refresh_btn)
        selector_row.addWidget(self.watch_btn)
        main_layout.addLayout(selector_row)

        # Status banner
        self.status_banner = QLabel("Select a part program and click Start Watching")
        self.status_banner.setStyleSheet("""
            background: #1A1D27;
            color: #7B8099;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 13px;
        """)
        self.status_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_banner)

        # Large pass/fail indicator
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFixedHeight(120)
        self.result_label.setStyleSheet("""
            background: #1A1D27;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            font-size: 48px;
            font-weight: bold;
            font-family: 'Courier New';
        """)
        main_layout.addWidget(self.result_label)

        # Stat cards
        self.stats_widget = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_widget)
        self.stats_layout.setSpacing(12)
        self.stats_widget.hide()
        main_layout.addWidget(self.stats_widget)

        # Charts scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: #0F1117; }
            QScrollArea > QWidget > QWidget { background: #0F1117; }
        """)

        self.charts_widget = QWidget()
        self.charts_widget.setStyleSheet("background: #0F1117;")
        self.charts_layout = QVBoxLayout(self.charts_widget)
        self.charts_layout.setSpacing(16)
        scroll.setWidget(self.charts_widget)
        scroll.viewport().setStyleSheet("background: #0F1117;")
        main_layout.addWidget(scroll)

    def _btn_style(self, bg: str, fg: str) -> str:
        return f"""
            QPushButton {{
                background: {bg};
                color: {fg};
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{ opacity: 0.85; }}
        """

    def _refresh_programs(self):
        """Refreshes the dropdown from settings watched folders."""
        self.program_combo.blockSignals(True)
        self.program_combo.clear()

        folders = get_watched_folders()
        active  = [f for f in folders if f.get("active", True)]

        if not active:
            self.program_combo.addItem("No folders configured — add in Settings")
            self.current_folder = None
        else:
            for folder in active:
                self.program_combo.addItem(
                    folder["name"],
                    userData=folder["path"]
                )
            self.current_folder = active[0]["path"]

        self.program_combo.blockSignals(False)

    def refresh_programs(self):
        """Public method so MainWindow can refresh after settings change."""
        self._refresh_programs()

    def _on_program_changed(self, index):
        self.current_folder = self.program_combo.itemData(index)
        self.watch_btn.setText("Start Watching")
        self.watch_btn.setStyleSheet(self._btn_style("#00C896", "#0F1117"))
        self._update_status("Select Start Watching to begin live monitoring", "#7B8099")

    def _toggle_watch(self):
        if self.watch_btn.text() == "Start Watching":
            if not self.current_folder:
                return
            self.watch_btn.setText("Stop Watching")
            self.watch_btn.setStyleSheet(self._btn_style("#FF4C4C", "#FFFFFF"))
            self._update_status(
                f"Watching: {self.program_combo.currentText()} — waiting for new reports...",
                "#00C896"
            )
            self.report_updated.emit(self.current_folder)
        else:
            self.watch_btn.setText("Start Watching")
            self.watch_btn.setStyleSheet(self._btn_style("#00C896", "#0F1117"))
            self._update_status("Watching stopped", "#7B8099")
            self.report_updated.emit("")

    def _update_status(self, message: str, color: str = "#7B8099"):
        self.status_banner.setText(message)
        self.status_banner.setStyleSheet(f"""
            background: #1A1D27;
            color: {color};
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 13px;
        """)

    def load_report_file(self, filepath: str):
        if filepath == self.last_filepath:
            return
        self.last_filepath = filepath
        try:
            filters   = get_global_filters()
            threshold = filters.get("warning_threshold", 75)
            report    = load_report(filepath)
            results   = evaluate_report(report, threshold)
            # Apply feature type filter
            from settings import get_global_filters as _get_filters
            _filters = _get_filters()
            _feature_types = _filters.get("feature_types", [])
            if _feature_types:
                results = [r for r in results if r.feature_type in _feature_types]

            self.results = results
            self._update_result_display(results)
            self._update_stats(results)
            self._update_charts(results)
            self._update_status(
                f"Last report: {os.path.basename(filepath)}", "#00C896"
            )
        except Exception as e:
            self._update_status(f"Error loading report: {e}", "#FF4C4C")

    def _update_result_display(self, results: list):
        total  = len(results)
        passes = sum(1 for r in results if r.is_pass)
        fails  = total - passes
        if fails == 0:
            self.result_label.setText("✓ PASS")
            self.result_label.setStyleSheet("""
                background: rgba(0,200,150,0.15);
                border: 2px solid #00C896;
                border-radius: 12px;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Courier New';
                color: #00C896;
            """)
        else:
            self.result_label.setText(f"✗ FAIL  ({fails} feature{'s' if fails > 1 else ''})")
            self.result_label.setStyleSheet("""
                background: rgba(255,76,76,0.15);
                border: 2px solid #FF4C4C;
                border-radius: 12px;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Courier New';
                color: #FF4C4C;
            """)

    def _update_stats(self, results: list):
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().deleteLater()

        total    = len(results)
        passes   = sum(1 for r in results if r.is_pass)
        fails    = total - passes
        warnings = sum(1 for r in results if r.severity == "WARNING")
        rate     = round(passes / total * 100) if total > 0 else 0

        for label, value, color in [
            ("Total",     total,       "#4A90D9"),
            ("Passed",    passes,      "#00C896"),
            ("Failed",    fails,       "#FF4C4C"),
            ("Warnings",  warnings,    "#FFA500"),
            ("Pass Rate", f"{rate}%",  "#00C896" if rate >= 80 else "#FFA500"),
        ]:
            self.stats_layout.addWidget(StatCard(label, str(value), color))

        self.stats_widget.show()

    def _update_charts(self, results: list):
        for i in reversed(range(self.charts_layout.count())):
            item = self.charts_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        for fig in [summary_donut(results), deviation_bar_chart(results)]:
            html = fig.to_html(include_plotlyjs="cdn")
            html = html.replace("<body>", '<body style="background-color: #0F1117; margin: 0; padding: 0;">')
            view = QWebEngineView()
            view.setMinimumHeight(380)
            view.setHtml(html)
            view.setStyleSheet("background: #0F1117; border-radius: 12px;")
            view.page().setBackgroundColor(Qt.GlobalColor.transparent)
            self.charts_layout.addWidget(view)