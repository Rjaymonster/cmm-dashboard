# settings.py
# Manages reading and writing the settings.json configuration file.
# Provides a clean interface for the rest of the app to access settings
# without worrying about file I/O.

import json
import os


# Default settings — used when settings.json doesn't exist yet
DEFAULTS = {
    "global_filters": {
        "warning_threshold": 75,
        "min_cpk_samples": 10,
        "show_status": ["PASS", "FAIL", "WARNING"],
        "feature_types": [],
        "tolerance_range": {"min": 0.0, "max": 999.0}
    },
    "watched_folders": []
}

# Path to settings file — always in the project root
SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "settings.json"
)


def load_settings() -> dict:
    """
    Loads settings from settings.json.
    Returns defaults if file doesn't exist or is corrupted.
    """
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Merge with defaults to handle missing keys
        return _merge_defaults(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULTS.copy()


def save_settings(settings: dict) -> bool:
    """
    Saves settings to settings.json.
    Returns True if successful, False if an error occurred.
    """
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Failed to save settings: {e}")
        return False


def get_global_filters() -> dict:
    """Returns just the global filters section."""
    return load_settings().get("global_filters", DEFAULTS["global_filters"])


def get_watched_folders() -> list:
    """Returns the list of watched folder configurations."""
    return load_settings().get("watched_folders", [])


def add_watched_folder(name: str, path: str) -> bool:
    """
    Adds a new watched folder to settings.
    Returns False if the path already exists.
    """
    settings = load_settings()
    folders  = settings.get("watched_folders", [])

    # Check for duplicate path
    if any(f["path"] == path for f in folders):
        return False

    folders.append({
        "name":    name,
        "path":    path,
        "active":  True,
        "filters": {"use_global": True}
    })

    settings["watched_folders"] = folders
    return save_settings(settings)


def update_watched_folder(path: str, updates: dict) -> bool:
    """Updates an existing watched folder by path."""
    settings = load_settings()
    folders  = settings.get("watched_folders", [])

    for folder in folders:
        if folder["path"] == path:
            folder.update(updates)
            settings["watched_folders"] = folders
            return save_settings(settings)

    return False


def remove_watched_folder(path: str) -> bool:
    """Removes a watched folder by path."""
    settings = load_settings()
    folders  = settings.get("watched_folders", [])
    settings["watched_folders"] = [f for f in folders if f["path"] != path]
    return save_settings(settings)


def _merge_defaults(data: dict) -> dict:
    """
    Ensures all expected keys exist by merging with defaults.
    Existing values are preserved.
    """
    result = DEFAULTS.copy()
    result.update(data)
    if "global_filters" not in result:
        result["global_filters"] = DEFAULTS["global_filters"]
    if "watched_folders" not in result:
        result["watched_folders"] = []
    return result