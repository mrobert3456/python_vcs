import os
from command import Command

class Init(Command):
    def __init__(self):
        super().__init__()

    def execute(self):
        """
            Initialize version control on the current directory
        :param self:
        :return:
        """
        if  self.directory_not_exists():
            os.mkdir(self.base_directory)
            os.mkdir(self.commit_directory)
            os.mkdir(self.checkout_directory)
            staging = open(self.staging_area_file,'w')
            staging.close()
            status = open(self.status_file, 'w')
            status.close()

        else:
            return "Version control is already initialized on this project"

        return "Version control is initialized successfully"
    
    def directory_not_exists(self):
        if  not(os.path.exists(self.base_directory)):
            return True
        return False
    
