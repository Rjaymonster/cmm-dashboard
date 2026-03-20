# watcher.py
# Watches folders for new MODUS report files and triggers
# automatic processing when new files are detected.
#
# New concept: watchdog
# watchdog is a Python library that monitors filesystem events.
# When a new file appears in a watched folder it fires an event
# that we can respond to — like parsing a new report automatically.

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# File extensions we care about
REPORT_EXTENSIONS = {".csv", ".txt"}


class ReportFileHandler(FileSystemEventHandler):
    """
    Handles filesystem events for a single watched folder.
    Calls the callback function when a new report file appears.
    """

    def __init__(self, folder_name: str, callback):
        """
        Args:
            folder_name: Friendly name of the watched folder
            callback: Function to call when a new file is detected.
                      Signature: callback(folder_name, filepath)
        """
        super().__init__()
        self.folder_name = folder_name
        self.callback    = callback
        # Track recently processed files to avoid duplicate triggers
        self._processed  = set()

    def on_created(self, event):
        """Fired when a new file appears in the watched folder."""
        if event.is_directory:
            return

        filepath = event.src_path
        ext      = os.path.splitext(filepath)[1].lower()

        if ext not in REPORT_EXTENSIONS:
            return

        # Avoid processing the same file twice
        if filepath in self._processed:
            return

        # Wait briefly for the file to finish writing
        time.sleep(0.5)

        # Confirm file is readable and non-empty
        try:
            if os.path.getsize(filepath) == 0:
                return
        except OSError:
            return

        self._processed.add(filepath)
        self.callback(self.folder_name, filepath)

    def on_modified(self, event):
        """
        Some systems fire modified instead of created for new files.
        Handle both to be safe.
        """
        self.on_created(event)


class FolderWatcher:
    """
    Manages multiple folder watchers simultaneously.
    Each watched folder runs its own Observer thread.
    """

    def __init__(self, callback):
        """
        Args:
            callback: Function called when a new report is detected.
                      Signature: callback(folder_name, filepath)
        """
        self.callback  = callback
        self.observers = {}  # path -> Observer

    def start_watching(self, folder_name: str, path: str) -> bool:
        """
        Starts watching a folder for new report files.
        Returns False if path doesn't exist or already being watched.
        """
        if not os.path.exists(path):
            print(f"Folder does not exist: {path}")
            return False

        if path in self.observers:
            print(f"Already watching: {path}")
            return False

        handler  = ReportFileHandler(folder_name, self.callback)
        observer = Observer()
        observer.schedule(handler, path, recursive=False)
        observer.start()

        self.observers[path] = observer
        print(f"Now watching: {folder_name} ({path})")
        return True

    def stop_watching(self, path: str) -> bool:
        """Stops watching a specific folder."""
        if path not in self.observers:
            return False

        observer = self.observers.pop(path)
        observer.stop()
        observer.join()
        print(f"Stopped watching: {path}")
        return True

    def stop_all(self):
        """Stops all active watchers — call when app closes."""
        for path, observer in list(self.observers.items()):
            observer.stop()
            observer.join()
        self.observers.clear()
        print("All watchers stopped.")

    @property
    def active_folders(self) -> list:
        """Returns list of currently watched paths."""
        return list(self.observers.keys())

    def is_watching(self, path: str) -> bool:
        """Returns True if a folder is currently being watched."""
        return path in self.observers