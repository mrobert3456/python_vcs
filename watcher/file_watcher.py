from datetime import datetime
import shutil
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
    
    @property
    def status_directory(self):
        return self.command.status_directory

    def _add_files_to_status(self,event, status:FileStatus):
        if not event.is_directory and (self.base_directory not in event.src_path):
            with open(self.command.status_file,"a+") as f:
                    f.seek(0)
                    files =[item.split("|")[0] for item in f.readlines()]
                    f.seek(len(files)-1)
                    if event.src_path not in files:
                        f.writelines(f"\n{event.src_path}|{datetime.now()}|{str(status.name)}")
                        #move file under status
                        destination = os.path.join(self.status_directory,event.src_path).replace("\\","/")
                        shutil.copy(event.src_path, destination)
    
    def _add_new_file_to_status(self,event):
        if not event.is_directory and (self.base_directory not in event.src_path):
            with open(self.command.status_file,"a") as f:
                f.writelines(f"\n{event.src_path}|{datetime.now()}|{str(FileStatus.CREATED.name)}")
                #move file under status
                destination = os.path.join(self.status_directory,event.src_path).replace("\\","/")
                shutil.copy(event.src_path, destination)

    def on_created(self, event):
        """
            Adds the created file to status
        """
        self._add_new_file_to_status(event)
        
    def on_modified(self, event):
        """
            Adds the modified file to status
        """
        self._add_files_to_status(event,FileStatus.CHANGED)

    def on_deleted(self, event):
        """
            Adds the deleted file to status
        """
        #TODO if the file is located in the local repository, then add the file to status directory from the local repo
        self._add_files_to_status(event,FileStatus.DELETED)
    

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
