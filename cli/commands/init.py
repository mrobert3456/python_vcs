import os
from cli.commands.command import Command
from cli.exceptions.pvc_already_initalized_exception import PVCAlreadyInitializedException
from datetime import datetime
from cli.commands.status import FileStatus
import subprocess
from utils.FileHandler import FileHandler
class Init(Command):
    def __init__(self):
        super().__init__()


    def initialize_directory(self):
        """
            Creates the neccessary directories for version control.
        """
        if(self.root_not_exists()):
            FileHandler.create_directory(self.base_directory)
            FileHandler.create_directories(self.commit_directory+"/"+self.current_branch)
            FileHandler.create_directory(self.checkout_directory)
            FileHandler.create_directory(self.index_directory)
            FileHandler.create_directory(self.status_directory)
            FileHandler.create_directories(self.local_repo+"/"+self.current_branch)
            FileHandler.create_file(self.staging_area_file)
            FileHandler.create_file(self.status_file)
            FileHandler.create_file(self.index_lock_file)
        else:
            raise PVCAlreadyInitializedException()

    def add_files_to_status(self):
        """
            Add the files from the working directory to status.
        """
        files_to_track = FileHandler.get_file_paths_from_dir(os.getcwd(),exclude_dirs=['.pv','.git'])
        content = [f"{file}|{datetime.now()}|{str(FileStatus.CREATED.name)}\n" for file in files_to_track]
        FileHandler.write_file(self.status_file,content)

        
        #copy files to the status directory
        for file in files_to_track:
            FileHandler.copy_file(file, self.status_directory)
            

    def initiate_file_watcher(self):
        """
            Creates a sub process to watch the working directory for file changes.
            It will run until the root directory is exists.
        """
        subprocess.Popen(["python","-m","watcher.file_watcher"])

    def execute(self,*args, **kwargs):
        """
            Initialize version control on the current directory
        returns: 
            1 - command executed successfully
            0 - command execution failed
            message - command execution result
        """

        try:

            self.initiate_file_watcher()
            self.initialize_directory()
            self.add_files_to_status()
        except PVCAlreadyInitializedException as e:
            return 0, e
        return 1, "Version control is initialized successfully"