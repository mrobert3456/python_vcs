import os
from cli.commands.command import Command
from cli.exceptions.pvc_already_initalized_exception import PVCAlreadyInitializedException
from datetime import datetime

class Init(Command):
    def __init__(self):
        super().__init__()


    def initialize_directory(self):
        if(self.root_not_exists()):
            os.mkdir(self.base_directory)
            os.mkdir(self.commit_directory)
            os.mkdir(self.checkout_directory)
            staging = open(self.staging_area_file,'w')
            staging.close()
            status = open(self.status_file, 'w')
            status.close()
        else:
            raise PVCAlreadyInitializedException()

    def add_files_to_status(self):
        files_to_track=[os.path.join(root, file) 
                  for root,directories,files in os.walk(os.getcwd()) 
                  if ".pv" not in root and ".git" not in root 
                  for file in files]

        with open(self.status_file,'w') as f:
            for file in files_to_track:
                f.writelines(f"{file}|{datetime.now()}\n")
        
    def execute(self,*args, **kwargs):
        """
            Initialize version control on the current directory
        :return: 1 - command executed successfully, 0 - command execution failed
        """

        self.initialize_directory()
        self.add_files_to_status()

        return 1