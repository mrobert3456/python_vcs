
from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException
class Discard(Command):

    def __init__(self):
        super().__init__()


    def _restore_files_from_local_repo(self,files):
        """
            Restores files from local repository to the working directory
        """

        pass

    def _remove_files_from_status(self,files):
        """
            Removes files under status directory
        """
        pass

    def execute(self, files):
        try:
            if(self.root_not_exists()):
                raise PVCNotInitializedException()
            
            self._restore_files_from_local_repo(files)
            self._remove_files_from_status(files)


            return 1, None
        except PVCNotInitializedException as e:
            return 0, e
        except Exception as e:
            return 0, e
        