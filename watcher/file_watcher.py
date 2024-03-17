from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from cli.commands.status import FileStatus
from cli.commands.command import Command
from watcher.file_watcher_actions import FileWatcherActions

class CustomHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        super().__init__()
        self.command = Command()
        self.file_handler = FileWatcherActions()

    @property
    def base_directory(self):
        return self.command.base_directory
    

    def on_created(self, event):
        """
            Adds the created file to status
        """
        try:
            if not event.is_directory and (self.base_directory not in event.src_path):
                self.file_handler.add_file_to_status(event.src_path, FileStatus.CREATED)
        except:
            pass        
    def on_modified(self, event):
        """
            Adds the modified file to status
        """
        try:
            
            if not event.is_directory and (self.base_directory not in event.src_path):
                self.file_handler.add_file_to_status(event.src_path, FileStatus.CHANGED)
        except:
            pass

    def on_deleted(self, event):
        """
            Adds the deleted file to status
        """
        #TODO if the file is located in the local repository, then add the file to status directory from the local repo
        try:
            if not event.is_directory and (self.base_directory not in event.src_path):
                self.file_handler.add_file_to_status(event.src_path, FileStatus.DELETED)
        except:
            pass
    

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
