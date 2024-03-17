from io import TextIOWrapper
from cli.commands.status import FileStatus
from cli.commands.command import Command
from datetime import datetime
import os
import shutil
from utils.FileHandler import FileHandler
class FileWatcherActions:

    def __init__(self) -> None:
        self.command = Command()

    def add_deleted_file_to_status(self, src_path:str):
        index_files = [line.replace("\n","") for line in FileHandler.read_file(self.command.index_lock_file)]
        if src_path in index_files:
            src = os.path.join(self.command.local_repo,self.command.current_branch, src_path).replace("\\","/")
            dest= os.path.join(self.command.status_directory,src_path).replace("\\","/")
            shutil.copy(src,dest)

    def _is_file_exists_in_status(self, src_path:str, files:list[str]) -> bool:
        
        return src_path in files
    
    def _get_files_from_status(self,file_handler:TextIOWrapper) -> list[str]:
            file_handler.seek(0)
            files =[item.split("|")[0] for item in file_handler.readlines()]
            file_handler.seek(len(files)-1)
            return files
    

    def _is_file_changed(self,src_path:str) -> bool :
        local_src_path = os.path.join(self.command.local_repo,self.command.current_branch,src_path)
        local_file_lines = FileHandler.read_file(local_src_path)
        new_file_lines = FileHandler.read_file(src_path)
        return local_file_lines != new_file_lines
    
    def add_file_to_status(self,src_path:str,file_status:FileStatus):
        try:
            with open(self.command.status_file,"a+") as f:
                status_files = self._get_files_from_status(f)
                if not self._is_file_exists_in_status(src_path.replace("./", ""), status_files) and self._is_file_changed(src_path):
                    f.writelines(f"\n{src_path.replace("./", "")}|{datetime.now()}|{str(file_status.name)}")

                if self._is_file_changed(src_path) and file_status!=FileStatus.DELETED and os.path.exists(src_path):
                    destination = os.path.join(self.command.status_directory,src_path).replace("\\","/")
                    shutil.copy(src_path, destination)

                elif file_status==FileStatus.DELETED:
                    self.add_deleted_file_to_status(src_path.replace("./", ""))

        except Exception as e:
            pass



