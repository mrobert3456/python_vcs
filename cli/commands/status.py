from enum import Enum
import os
from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException
from cli.colors.color_text import TerminalColor, color_text

class FileStatus(Enum):
    CREATED = 1
    CHANGED = 2
    DELETED = 3

class Status(Command):
    def __init__(self):
        super().__init__()

    def _compare_status_and_staging_area(self):
        
        with open(self.status_file,"r") as f:
            status = f.readlines()

        with open(self.staging_area_file,"r") as f:
            staging_area = f.readlines()
        
        if len(status)>0 and len(staging_area)>0:
            staging_area = f"\n{color_text(" ".join(staging_area), TerminalColor.GREEN)}"
            status = f"\n{color_text(" ".join(status), TerminalColor.RED)} "
            files_to_print = f"\nStaging area:{staging_area}\nStatus: {status}"

        return files_to_print

    def execute(self,*args, **kwargs):
        """
            Shows the current changes
        returns: 
            1 - command executed successfully
            0 - command execution failed
            message - command execution result
        """
        try:
            if(self.root_not_exists()):
                raise PVCNotInitializedException()

        except PVCNotInitializedException as e:
            return 0, e
        return 1, self._compare_status_and_staging_area()


