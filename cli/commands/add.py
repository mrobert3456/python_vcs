import os
from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException
class Add(Command):
    def __init__(self):
        super().__init__()

    def execute(self, files):
        """
            Adds the specified files and directories into status and staging area
        :return: 1 - command executed successfully, 0 - command execution failed
        """
        if(self.root_not_exists()):
            raise PVCNotInitializedException()
        
        print(files)

        return 1

