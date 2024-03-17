from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException
import os 
from utils.FileHandler import FileHandler

class Discard(Command):

    def __init__(self):
        super().__init__()


    def _restore_files_from_local_repo(self,files):
        """
            Restores files from local repository to the working directory
        """
        for file in files:
            src = os.path.join(self.local_repo,self.current_branch,file).replace("\\","/")
            dest = file.replace("\\","/")
            FileHandler.overwrite_file(src,dest)

    def _remove_files_from_status(self,files):
        """
            Removes files under status directory
        """
        FileHandler.delete_files(files,self.status_directory)

        status_lines = FileHandler.read_file(self.status_file)
        lines_to_kepp = [file for file in status_lines if file.split("|")[0] not in files]
        FileHandler.write_file(self.status_file,lines_to_kepp)


    def execute(self, files):
        try:
            if(self.root_not_exists()):
                raise PVCNotInitializedException()
            
            self._restore_files_from_local_repo(files)
            self._remove_files_from_status(files)


            return 1, None
        except PVCNotInitializedException as e:
            return 0, e
        except Exception as e:
            return 0, e
        