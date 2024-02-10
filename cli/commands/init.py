import os
from cli.commands.command import Command
from cli.exceptions.pvc_already_initalized_exception import PVCAlreadyInitializedException
from datetime import datetime
from cli.commands.status import FileStatus
import subprocess
class Init(Command):
    def __init__(self):
        super().__init__()


    def initialize_directory(self):
        """
            Creates the neccessary directories for version control.
        """
        if(self.root_not_exists()):
            os.mkdir(self.base_directory)
            os.makedirs(self.commit_directory+"/"+self.current_branch)
            os.mkdir(self.checkout_directory)
            os.mkdir(self.index_directory)
            staging = open(self.staging_area_file,'w')
            staging.close()
            status = open(self.status_file, 'w')
            status.close()
        else:
            raise PVCAlreadyInitializedException()

    def add_files_to_status(self):
        """
            Add the files from the working directory to status.
        """
        files_to_track = [os.path.relpath(os.path.join(root, file), os.getcwd())
                  for root, directories, files in os.walk(os.getcwd())
                  if ".pv" not in root and ".git" not in root
                  for file in files]

        with open(self.status_file,'w') as f:
            for file in files_to_track:
                f.writelines(f"{file}|{datetime.now()}|{str(FileStatus.CREATED.name)}\n")

    
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