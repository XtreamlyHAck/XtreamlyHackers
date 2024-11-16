import os
from server.utils.singleton import singleton
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from server.repositories.trades_repository import TradesRepository, TRADES_FILE_FEATURES


@singleton
class DataObserver:
    def __init__(self) -> None:
        data_path = os.environ.get("SHARED_DATA_PATH", "./data")

        self.observer = Observer()
        self.observer.schedule(DataHandler(), path=data_path, recursive=True)

    def start(self):
        TradesRepository()
        self.observer.start()

    def stop(self):
        self.observer.stop()


class DataHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.getsize(event.src_path) <= 0:
            return

        if TRADES_FILE_FEATURES in event.src_path:
            TradesRepository().clear()
            TradesRepository()
