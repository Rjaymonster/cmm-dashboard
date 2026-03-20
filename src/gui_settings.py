# gui_settings.py
# Settings screen for the CMM Dashboard.
# Allows users to manage watched folders and global filters
# without touching any code or config files directly.

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QScrollArea,
    QFrame, QCheckBox, QSlider, QSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from settings import (
    load_settings, save_settings,
    add_watched_folder, remove_watched_folder,
    update_watched_folder, get_watched_folders
)


# ── Folder Card Widget ────────────────────────────────────────────

class FolderCard(QFrame):
    """
    Displays a single watched folder with its name, path,
    active toggle, and remove button.
    """
    removed  = pyqtSignal(str)   # emits path when removed
    toggled  = pyqtSignal(str, bool)  # emits path, active state

    def __init__(self, folder: dict):
        super().__init__()
        self.folder = folder
        self.setStyleSheet("""
            QFrame {
                background: #1A1D27;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 10px;
                padding: 4px;
            }
        """)
        self._build()

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        # Info column
        info = QVBoxLayout()
        info.setSpacing(4)

        name_label = QLabel(self.folder["name"])
        name_label.setStyleSheet("color: #E8EAF0; font-size: 14px; font-weight: bold;")

        path_label = QLabel(self.folder["path"])
        path_label.setStyleSheet("color: #7B8099; font-size: 11px;")
        path_label.setWordWrap(True)

        info.addWidget(name_label)
        info.addWidget(path_label)
        layout.addLayout(info, 1)

        # Active toggle
        active_cb = QCheckBox("Active")
        active_cb.setChecked(self.folder.get("active", True))
        active_cb.setStyleSheet("color: #7B8099; font-size: 12px;")
        active_cb.stateChanged.connect(
            lambda state: self.toggled.emit(
                self.folder["path"], state == Qt.CheckState.Checked.value
            )
        )
        layout.addWidget(active_cb)

        # Remove button
        remove_btn = QPushButton("Remove")
        remove_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #FF4C4C;
                border: 1px solid #FF4C4C;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(255,76,76,0.1); }
        """)
        remove_btn.clicked.connect(
            lambda: self.removed.emit(self.folder["path"])
        )
        layout.addWidget(remove_btn)


# ── Settings Tab ──────────────────────────────────────────────────

class SettingsTab(QWidget):
    """
    Full settings screen with two sections:
    1. Watched Folders — add/remove/toggle folders
    2. Global Filters — warning threshold, status filter etc.
    """

    # Signal emitted when settings change so other tabs can react
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._load_folders()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)

        # ── Section 1: Watched Folders ────────────────────────────
        main_layout.addWidget(self._section_title("Watched Folders"))

        # Add folder row
        add_row = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Folder name e.g. Equator 1 - Part ABC")
        self.name_input.setStyleSheet(self._input_style())

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Folder path")
        self.path_input.setStyleSheet(self._input_style())

        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet(self._btn_style("#1A1D27", "#7B8099"))
        browse_btn.clicked.connect(self._browse_folder)

        add_btn = QPushButton("Add Folder")
        add_btn.setStyleSheet(self._btn_style("#00C896", "#0F1117"))
        add_btn.clicked.connect(self._add_folder)

        add_row.addWidget(self.name_input, 2)
        add_row.addWidget(self.path_input, 3)
        add_row.addWidget(browse_btn)
        add_row.addWidget(add_btn)
        main_layout.addLayout(add_row)

        # Folder list scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(300)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.folders_widget = QWidget()
        self.folders_layout = QVBoxLayout(self.folders_widget)
        self.folders_layout.setSpacing(8)
        self.folders_layout.addStretch()
        scroll.setWidget(self.folders_widget)
        main_layout.addWidget(scroll)

        # ── Section 2: Global Filters ─────────────────────────────
        main_layout.addWidget(self._section_title("Global Filters"))

        filters_frame = QFrame()
        filters_frame.setStyleSheet("""
            QFrame {
                background: #1A1D27;
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 10px;
            }
        """)
        filters_layout = QVBoxLayout(filters_frame)
        filters_layout.setContentsMargins(20, 16, 20, 16)
        filters_layout.setSpacing(16)

        # Warning threshold slider
        threshold_row = QHBoxLayout()
        threshold_label = QLabel("Warning Threshold:")
        threshold_label.setStyleSheet("color: #E8EAF0; font-size: 13px;")
        threshold_label.setFixedWidth(180)

        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setMinimum(50)
        self.threshold_slider.setMaximum(95)
        self.threshold_slider.setSingleStep(5)
        self.threshold_slider.setStyleSheet("accent-color: #00C896;")

        self.threshold_value = QLabel("75%")
        self.threshold_value.setStyleSheet(
            "color: #00C896; font-size: 13px; font-family: 'Courier New'; min-width: 40px;"
        )
        self.threshold_slider.valueChanged.connect(
            lambda v: self.threshold_value.setText(f"{v}%")
        )

        threshold_row.addWidget(threshold_label)
        threshold_row.addWidget(self.threshold_slider)
        threshold_row.addWidget(self.threshold_value)
        filters_layout.addLayout(threshold_row)

        # Min Cpk samples
        cpk_row = QHBoxLayout()
        cpk_label = QLabel("Min Cpk Samples:")
        cpk_label.setStyleSheet("color: #E8EAF0; font-size: 13px;")
        cpk_label.setFixedWidth(180)

        self.cpk_spin = QSpinBox()
        self.cpk_spin.setMinimum(2)
        self.cpk_spin.setMaximum(100)
        self.cpk_spin.setStyleSheet("""
            QSpinBox {
                background: #0F1117;
                color: #E8EAF0;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 13px;
            }
        """)

        cpk_row.addWidget(cpk_label)
        cpk_row.addWidget(self.cpk_spin)
        cpk_row.addStretch()
        filters_layout.addLayout(cpk_row)

        # Status filter checkboxes
        status_row = QHBoxLayout()
        status_label = QLabel("Show Status:")
        status_label.setStyleSheet("color: #E8EAF0; font-size: 13px;")
        status_label.setFixedWidth(180)

        self.cb_pass    = QCheckBox("PASS")
        self.cb_fail    = QCheckBox("FAIL")
        self.cb_warning = QCheckBox("WARNING")

        for cb, color in [
            (self.cb_pass,    "#00C896"),
            (self.cb_fail,    "#FF4C4C"),
            (self.cb_warning, "#FFA500")
        ]:
            cb.setStyleSheet(f"color: {color}; font-size: 13px;")
            cb.setChecked(True)
            status_row.addWidget(cb)

        status_row.insertWidget(0, status_label)
        status_row.addStretch()
        filters_layout.addLayout(status_row)

        main_layout.addWidget(filters_frame)

        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet(self._btn_style("#00C896", "#0F1117"))
        save_btn.setFixedWidth(160)
        save_btn.clicked.connect(self._save_filters)
        main_layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addStretch()

        # Load current filter values
        self._load_filters()

    def _section_title(self, text: str) -> QLabel:
        label = QLabel(text.upper())
        label.setStyleSheet("""
            color: #7B8099;
            font-size: 11px;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            padding-bottom: 6px;
        """)
        return label

    def _input_style(self) -> str:
        return """
            QLineEdit {
                background: #0F1117;
                color: #E8EAF0;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus { border-color: #00C896; }
        """

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

    def _browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.path_input.setText(path)

    def _add_folder(self):
        name = self.name_input.text().strip()
        path = self.path_input.text().strip()

        if not name:
            self._show_error("Please enter a folder name.")
            return
        if not path:
            self._show_error("Please select a folder path.")
            return
        if not os.path.exists(path):
            self._show_error("Folder path does not exist.")
            return

        if add_watched_folder(name, path):
            self.name_input.clear()
            self.path_input.clear()
            self._load_folders()
            self.settings_changed.emit()
        else:
            self._show_error("This folder is already being watched.")

    def _load_folders(self):
        # Clear existing cards
        for i in reversed(range(self.folders_layout.count())):
            item = self.folders_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        folders = get_watched_folders()

        if not folders:
            empty = QLabel("No folders added yet. Add a folder above to get started.")
            empty.setStyleSheet("color: #7B8099; font-size: 13px; padding: 16px;")
            self.folders_layout.addWidget(empty)
        else:
            for folder in folders:
                card = FolderCard(folder)
                card.removed.connect(self._remove_folder)
                card.toggled.connect(self._toggle_folder)
                self.folders_layout.addWidget(card)

        self.folders_layout.addStretch()

    def _remove_folder(self, path: str):
        reply = QMessageBox.question(
            self, "Remove Folder",
            "Are you sure you want to remove this watched folder?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            remove_watched_folder(path)
            self._load_folders()
            self.settings_changed.emit()

    def _toggle_folder(self, path: str, active: bool):
        update_watched_folder(path, {"active": active})
        self.settings_changed.emit()

    def _load_filters(self):
        settings = load_settings()
        filters  = settings.get("global_filters", {})

        self.threshold_slider.setValue(filters.get("warning_threshold", 75))
        self.cpk_spin.setValue(filters.get("min_cpk_samples", 10))

        show_status = filters.get("show_status", ["PASS", "FAIL", "WARNING"])
        self.cb_pass.setChecked("PASS" in show_status)
        self.cb_fail.setChecked("FAIL" in show_status)
        self.cb_warning.setChecked("WARNING" in show_status)

    def _save_filters(self):
        settings = load_settings()

        show_status = []
        if self.cb_pass.isChecked():    show_status.append("PASS")
        if self.cb_fail.isChecked():    show_status.append("FAIL")
        if self.cb_warning.isChecked(): show_status.append("WARNING")

        settings["global_filters"] = {
            "warning_threshold": self.threshold_slider.value(),
            "min_cpk_samples":   self.cpk_spin.value(),
            "show_status":       show_status,
            "feature_types":     settings["global_filters"].get("feature_types", []),
            "tolerance_range":   settings["global_filters"].get("tolerance_range",
                                 {"min": 0.0, "max": 999.0})
        }

        if save_settings(settings):
            self.settings_changed.emit()
            QMessageBox.information(self, "Saved", "Settings saved successfully.")
        else:
            self._show_error("Failed to save settings.")

    def _show_error(self, message: str):
        QMessageBox.warning(self, "Error", message)