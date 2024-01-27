import os
from cli.commands.command import Command
from cli.exceptions.pvc_already_initalized_exception import PVCAlreadyInitializedException

class Init(Command):
    def __init__(self):
        super().__init__()

    def execute(self,*args, **kwargs):
        """
            Initialize version control on the current directory
        :return: 1 - command executed successfully, 0 - command execution failed
        """

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
        return 1