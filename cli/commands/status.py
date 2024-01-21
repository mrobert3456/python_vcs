import os
from cli.commands.command import Command

class Status(Command):
    def __init__(self):
        super().__init__()

    def execute(self):
        """
            Shows the current changes
        :return: 0 - command executed successfully, 1 - command execution failed
        """
        if(self.root_not_exists()):
            return 0
        

        return 1

