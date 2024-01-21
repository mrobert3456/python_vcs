import os
from cli.commands.command import Command

class Init(Command):
    def __init__(self):
        super().__init__()

    def execute(self):
        """
            Initialize version control on the current directory
        :return: 0 - command executed successfully, 1 - command execution failed
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
            return 0
        return 1