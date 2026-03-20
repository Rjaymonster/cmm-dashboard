# gui_trend.py
# Multi-run trend tab for the CMM Dashboard PyQt6 UI.

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QScrollArea
)
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from trend import load_runs, is_trending, get_all_feature_names
from capability import capability_from_runs
from visualizer import (
    trend_line_chart,
    stability_chart,
    pass_rate_trend_chart,
    capability_chart,
)
from gui_single import StatCard


# ── Worker Thread ─────────────────────────────────────────────────

class TrendWorker(QThread):
    finished = pyqtSignal(object, object)

    def __init__(self, filepaths):
        super().__init__()
        self.filepaths = filepaths

    def run(self):
        try:
            runs        = load_runs(self.filepaths)
            cap_results = capability_from_runs(runs)
            self.finished.emit((runs, cap_results), None)
        except Exception as e:
            self.finished.emit(None, str(e))


# ── Trend Tab ─────────────────────────────────────────────────────

class TrendTab(QWidget):
    def __init__(self):
        super().__init__()
        self.runs        = None
        self.cap_results = None
        self.filepaths   = []
        self.worker      = None
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Upload row
        upload_row = QHBoxLayout()

        self.file_label = QLabel("No files selected")
        self.file_label.setStyleSheet("color: #7B8099; font-size: 13px;")

        browse_btn = QPushButton("Browse Files...")
        browse_btn.setStyleSheet(self._btn_style("#1A1D27", "#7B8099"))
        browse_btn.clicked.connect(self._browse_files)

        analyze_btn = QPushButton("Analyze Trends")
        analyze_btn.setStyleSheet(self._btn_style("#00C896", "#0F1117"))
        analyze_btn.clicked.connect(self._analyze)

        self.export_btn = QPushButton("Export to Excel")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background: #1A1D27;
                color: #3A3D4A;
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 8px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:enabled {
                background: #1A1D27;
                color: #00C896;
                border: 1px solid #00C896;
            }
            QPushButton:enabled:hover {
                background: rgba(0,200,150,0.1);
            }
        """)
        self.export_btn.clicked.connect(self._export_excel)
        self.export_btn.setEnabled(False)

        upload_row.addWidget(self.file_label, 1)
        upload_row.addWidget(browse_btn)
        upload_row.addWidget(analyze_btn)
        upload_row.addWidget(self.export_btn)
        main_layout.addLayout(upload_row)

        # Stat cards
        self.stats_widget = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_widget)
        self.stats_layout.setSpacing(12)
        self.stats_widget.hide()
        main_layout.addWidget(self.stats_widget)

        # Trending warning label
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("""
            background: rgba(255,165,0,0.1);
            color: #FFA500;
            border: 1px solid rgba(255,165,0,0.3);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 13px;
        """)
        self.warning_label.hide()
        main_layout.addWidget(self.warning_label)

        # Scroll area for charts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: #0F1117; }")

        self.charts_widget = QWidget()
        self.charts_layout = QVBoxLayout(self.charts_widget)
        self.charts_layout.setSpacing(16)
        scroll.setWidget(self.charts_widget)
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

    def _browse_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open MODUS Reports", "",
            "Report Files (*.csv *.txt *.res *.rtf);;All Files (*)"
        )
        if paths:
            self.filepaths = sorted(paths)
            self.file_label.setText(f"{len(paths)} files selected")
            self.file_label.setStyleSheet("color: #E8EAF0; font-size: 13px;")

    def _analyze(self):
        if not self.filepaths:
            self.file_label.setText("Please select at least two files")
            self.file_label.setStyleSheet("color: #FF4C4C; font-size: 13px;")
            return

        if len(self.filepaths) < 2:
            self.file_label.setText("Please select at least two files")
            self.file_label.setStyleSheet("color: #FF4C4C; font-size: 13px;")
            return

        self.file_label.setText("Analyzing...")
        self.worker = TrendWorker(self.filepaths)
        self.worker.finished.connect(self._on_analysis_done)
        self.worker.start()

    def _on_analysis_done(self, data, error):
        if error:
            self.file_label.setText(f"Error: {error}")
            self.file_label.setStyleSheet("color: #FF4C4C; font-size: 13px;")
            return

        self.runs, self.cap_results = data
        self._update_stats()
        self._update_charts()
        self.export_btn.setEnabled(True)
        self.file_label.setText(f"{len(self.runs)} runs loaded")
        self.file_label.setStyleSheet("color: #00C896; font-size: 13px;")

    def _update_stats(self):
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().deleteLater()

        feature_names = get_all_feature_names(self.runs)
        trending      = [n for n in feature_names if is_trending(self.runs, n)]

        cards = [
            ("Total Runs",       len(self.runs),        "#4A90D9"),
            ("Features Tracked", len(feature_names),    "#4A90D9"),
            ("Trending",         len(trending),         "#FFA500" if trending else "#00C896"),
        ]

        for label, value, color in cards:
            self.stats_layout.addWidget(StatCard(label, str(value), color))

        self.stats_widget.show()

        if trending:
            self.warning_label.setText(f"⚠ Trending toward failure: {', '.join(trending)}")
            self.warning_label.show()
        else:
            self.warning_label.hide()

    def _update_charts(self):
        for i in reversed(range(self.charts_layout.count())):
            item = self.charts_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        charts = [
            trend_line_chart(self.runs),
            stability_chart(self.runs),
            pass_rate_trend_chart(self.runs),
        ]

        if self.cap_results:
            charts.append(capability_chart(self.cap_results))

        for fig in charts:
            html = fig.to_html(include_plotlyjs="cdn")
            view = QWebEngineView()
            view.setMinimumHeight(450)
            view.setHtml(html)
            view.setStyleSheet("background: #1A1D27; border-radius: 12px;")
            self.charts_layout.addWidget(view)

    def _export_excel(self):
        if not self.runs:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel Report", "",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        if not path:
            return

        if not path.endswith(".xlsx"):
            path += ".xlsx"

        from excel_export import export_to_excel

        success = export_to_excel(
            output_path=path,
            results=self.runs[0].results,
            source_file="Multi-Run Trend Analysis",
            cap_results=self.cap_results,
            runs=self.runs,
        )

        if success:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Export Complete",
                                    f"Report saved to:\n{path}")
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Export Failed",
                                "Failed to save Excel file.")