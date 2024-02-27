
from abc import ABC
import os
class Command(ABC):
    def __init__(self):
        self.base_directory = ".pv"

    @property
    def current_branch(self):
        return "main"

    @property
    def index_directory(self):
        return self.base_directory+"/index"
    
    @property
    def status_directory(self):
        return self.base_directory+"/status"
    
    @property
    def local_repo(self):
        return self.base_directory+"/local_repo"
    
    @property
    def checkout_directory(self):
        return self.base_directory+"/checkout"

    @property
    def commit_directory(self):
        return self.base_directory+"/commit"

    @property
    def status_file(self):
        return self.base_directory+"/status.txt"

    @property
    def staging_area_file(self):
        return self.base_directory+"/staging_area.txt"
    
    def root_not_exists(self):
        if not(os.path.exists(self.base_directory)):
            return True
        return False

    def execute(self,*args, **kwargs):
        """
            Abstract method for executing a command
        """
        pass

    def undo(self,*args, **kwargs):
        """
            Abstract method for undoing an execution
        """
        pass

        