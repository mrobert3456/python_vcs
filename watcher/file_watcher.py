from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from cli.commands.status import FileStatus
from cli.commands.command import Command

class CustomHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()
        self.command = Command()

    @property
    def base_directory(self):
        return self.command.base_directory

    def on_created(self, event):
        """
            Adds the created file to status
        """
        if not event.is_directory:
            with open(self.command.status_file,"a") as f:
                 f.writelines(f"{event.src_path}|{datetime.now()}|{str(FileStatus.CREATED.name)}")
        return

def watch_files():
    observer = Observer()
    event_handler = CustomHandler()
    root = event_handler.base_directory
    observer.schedule(event_handler, path="./", recursive=True)
    observer.start()
    while os.path.exists(root):
        pass
    
    observer.stop()
    observer.join()


if __name__ == '__main__':
    watch_files()
