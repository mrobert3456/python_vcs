from enum import Enum
import os
from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException

class FileStatus(Enum):
    CREATED = 1
    CHANGED = 2
    DELETED = 3

class Status(Command):
    def __init__(self):
        super().__init__()


    def execute(self,*args, **kwargs):
        """
            Shows the current changes
        :return: 1 - command executed successfully, 0 - command execution failed
        """
        if(self.root_not_exists()):
            raise PVCNotInitializedException()



        return 1

