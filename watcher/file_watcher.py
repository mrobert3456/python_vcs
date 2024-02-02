from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from cli.commands.command import Command
class CustomHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("New file created:", event.src_path)


def watch_files():
    observer = Observer()
    event_handler = CustomHandler()
    root = Command().base_directory
    observer.schedule(event_handler, path="./", recursive=True)
    observer.start()
    while os.path.exists(root):
        pass
    
    observer.stop()
    observer.join()
