from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException
from cli.exceptions.pvc_not_matched_any_files import PVCNotMatchedAnyFiles
class Add(Command):
    def __init__(self):
        super().__init__()

    def _get_files_from_status(self,files_to_add):
        """
        Returns all file entries from status that are needs to be added in the staging area
        params:
            files_to_add: file paths that needs to be added in the staging area
        returns:
            file entries from status
        """
        with open(self.status_file, "r") as f:
            files = f.readlines()
        files_to_return=[file for file in files for file_ta in files_to_add if file_ta in file]

        if self._files_are_not_matching(files_to_return, files_to_add):
            files_not_matched = ', '.join([file_ta for file_ta in files_to_add if not any(file_ta in file for file in files)])
            raise PVCNotMatchedAnyFiles(files_not_matched)
           
        return files_to_return
    

    def _files_are_not_matching(self,files_to_return, files_to_add):
        return len(files_to_return)!=len(files_to_add)

    def _add_files_to_staging_area(self,files_to_add):
        """
        Adds the specified files from status to the staging area
        params:
        files_to_add: file paths that needs to be added in the staging area
        """
        status_entries = self._get_files_from_status(files_to_add)

        with open(self.staging_area_file,"a") as f:
            f.writelines(status_entries)

    def _delete_files_from_status(self,files):
        files_to_del = self._get_files_from_status(files)
        with open(self.status_file,"r") as f:
            files = f.readlines()
        
        files_to_keep = [file for file in files if file not in files_to_del]
        with open(self.status_file,"w") as f:
            f.writelines(files_to_keep)

    def execute(self, files):
        """
            Adds the specified files and directories into status and staging area
        :return: 1 - command executed successfully, 0 - command execution failed
        """
        if(self.root_not_exists()):
            raise PVCNotInitializedException()

        self._add_files_to_staging_area(files)
        self._delete_files_from_status(files)

        return 1

