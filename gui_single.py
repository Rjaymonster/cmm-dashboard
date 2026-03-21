# gui_single.py
# Single report tab for the CMM Dashboard PyQt6 UI.

import os
import tempfile
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QScrollArea, QFrame,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from parser import load_report
from evaluator import evaluate_report
from visualizer import (
    deviation_bar_chart,
    tolerance_usage_chart,
    summary_donut,
    feature_type_breakdown,
)


# ── Worker Thread ─────────────────────────────────────────────────
# New concept: QThread
# PyQt6 runs on a single thread by default. If we parse a large file
# on the main thread the UI freezes. QThread runs the work in the
# background and signals the UI when it's done.

class AnalysisWorker(QThread):
    finished = pyqtSignal(object, object)  # results, error
    
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        try:
            report  = load_report(self.filepath)
            results = evaluate_report(report)
            self.finished.emit(results, None)
        except Exception as e:
            self.finished.emit(None, str(e))


# ── Stat Card Widget ──────────────────────────────────────────────

class StatCard(QFrame):
    def __init__(self, label: str, value: str, color: str = "#4A90D9"):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background: #1A1D27;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 10px;
                padding: 8px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        lbl = QLabel(label.upper())
        lbl.setStyleSheet("color: #7B8099; font-size: 10px; letter-spacing: 1px;")

        val = QLabel(str(value))
        val.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold; font-family: 'Courier New';")

        layout.addWidget(lbl)
        layout.addWidget(val)


# ── Single Report Tab ─────────────────────────────────────────────

class SingleReportTab(QWidget):
    def __init__(self):
        super().__init__()
        self.results = None
        self.worker  = None
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Upload row
        upload_row = QHBoxLayout()

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #7B8099; font-size: 13px;")

        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet(self._btn_style("#1A1D27", "#7B8099"))
        browse_btn.clicked.connect(self._browse_file)

        analyze_btn = QPushButton("Analyze Report")
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

        # Stat cards row
        self.stats_widget = QWidget()
        self.stats_layout = QHBoxLayout(self.stats_widget)
        self.stats_layout.setSpacing(12)
        self.stats_widget.hide()
        main_layout.addWidget(self.stats_widget)

        # Scroll area for charts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: #0F1117; }
            QScrollArea > QWidget > QWidget { background: #0F1117; }
        """)

        self.charts_widget = QWidget()
        self.charts_widget.setStyleSheet("background: #0F1117;")
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

    def _browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open MODUS Report", "",
            "Report Files (*.csv *.txt *.res *.rtf);;All Files (*)"
        )
        if path:
            self.filepath = path
            self.file_label.setText(os.path.basename(path))
            self.file_label.setStyleSheet("color: #E8EAF0; font-size: 13px;")

    def auto_load(self, filepath: str):
        """
        Automatically loads and analyzes a report file.
        Called by the folder watcher when a new file is detected.
        """
        self.filepath = filepath
        self.file_label.setText(f"Auto-detected: {os.path.basename(filepath)}")
        self.file_label.setStyleSheet("color: #FFA500; font-size: 13px;")
        self._analyze()

    def _analyze(self):
        if not hasattr(self, "filepath"):
            self.file_label.setText("Please select a file first")
            self.file_label.setStyleSheet("color: #FF4C4C; font-size: 13px;")
            return

        self.file_label.setText("Analyzing...")
        self.worker = AnalysisWorker(self.filepath)
        self.worker.finished.connect(self._on_analysis_done)
        self.worker.start()

    def _on_analysis_done(self, results, error):
        if error:
            self.file_label.setText(f"Error: {error}")
            self.file_label.setStyleSheet("color: #FF4C4C; font-size: 13px;")
            return

        from settings import get_global_filters
        filters = get_global_filters()
        feature_types = filters.get("feature_types", [])
        if feature_types:
            results = [r for r in results if r.feature_type in feature_types]

        self.results = results
        self._update_stats()
        self._update_charts()
        self.export_btn.setEnabled(True)
        self.file_label.setText(f"Loaded: {os.path.basename(self.filepath)}")
        self.file_label.setStyleSheet("color: #00C896; font-size: 13px;")

    def _update_stats(self):
        # Clear old cards
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().deleteLater()

        total    = len(self.results)
        passes   = sum(1 for r in self.results if r.is_pass)
        fails    = total - passes
        warnings = sum(1 for r in self.results if r.severity == "WARNING")
        rate     = round(passes / total * 100) if total > 0 else 0

        cards = [
            ("Total",    total,        "#4A90D9"),
            ("Passed",   passes,       "#00C896"),
            ("Failed",   fails,        "#FF4C4C"),
            ("Warnings", warnings,     "#FFA500"),
            ("Pass Rate",f"{rate}%",   "#00C896" if rate >= 80 else "#FFA500"),
        ]

        for label, value, color in cards:
            self.stats_layout.addWidget(StatCard(label, str(value), color))

        self.stats_widget.show()

    def _update_charts(self):
        # Clear old charts
        for i in reversed(range(self.charts_layout.count())):
            item = self.charts_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Add charts as embedded web views
        charts = [
            summary_donut(self.results),
            feature_type_breakdown(self.results),
            deviation_bar_chart(self.results),
            tolerance_usage_chart(self.results),
        ]

        for fig in charts:
            html = fig.to_html(include_plotlyjs="cdn")
            html = html.replace("<body>", '<body style="background-color: #0F1117; margin: 0; padding: 0;">')
            view = QWebEngineView()
            view.setMinimumHeight(400)
            view.setHtml(html)
            view.setStyleSheet("background: #0F1117; border-radius: 12px;")
            view.page().setBackgroundColor(Qt.GlobalColor.transparent)
            self.charts_layout.addWidget(view)

    def _export_excel(self):
        if not self.results:
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel Report", "",
            "Excel Files (*.xlsx);;All Files (*)"
        )
        if not path:
            return

        if not path.endswith(".xlsx"):
            path += ".xlsx"

        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
        from excel_export import export_to_excel

        source = getattr(self, "filepath", "report")
        success = export_to_excel(
            output_path=path,
            results=self.results,
            source_file=source,
        )

        if success:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(self, "Export Complete",
                                    f"Report saved to:\n{path}")
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Export Failed",
                                "Failed to save Excel file.")