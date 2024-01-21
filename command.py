
from abc import ABC

class Command(ABC):
    def __init__(self):
        self.base_directory = ".pv"

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

    def execute(self):
        """
            Abstract method for executing a command
        """
        pass