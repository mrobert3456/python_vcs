from cli.commands.command import Command
from cli.exceptions.pvc_not_initialized_exception import PVCNotInitializedException
from cli.exceptions.pvc_not_matched_any_files import PVCNotMatchedAnyFiles
from utils.FileHandler import FileHandler
class Add(Command):
    def __init__(self):
        super().__init__()

    def _get_files_from_staging_area(self,files_to_get):
        """
        Returns all files from the staging area that are needs to be discarded
        params:
            files_to_get: file paths that needs to be discarded from staging area
        returns:
            file entries from staging area
        """
        files = FileHandler.read_file(self.staging_area_file)

        files_to_return=[file for file in files for file_ta in files_to_get if file_ta in file]

        if self._files_are_not_matching(files_to_return, files_to_get):
            files_not_matched = ', '.join([file_ta for file_ta in files_to_get if not any(file_ta in file for file in files)])
            raise PVCNotMatchedAnyFiles(files_not_matched)
           
        return files_to_return

    def _get_files_from_status(self,files_to_add):
        """
        Returns all file entries from status that are needs to be added in the staging area
        params:
            files_to_add: file paths that needs to be added in the staging area
        returns:
            file entries from status
        """
        files = FileHandler.read_file(self.status_file)
        files_to_return=[file for file in files for file_ta in files_to_add if file_ta in file]

        if self._files_are_not_matching(files_to_return, files_to_add):
            files_not_matched = ', '.join([file_ta for file_ta in files_to_add if not any(file_ta in file for file in files)])
            raise PVCNotMatchedAnyFiles(files_not_matched)
           
        return files_to_return
    

    def _files_are_not_matching(self,files_to_return, files_to_add):
        """
            Checks if there are any extra files that has not been added to status, but got specified to being added to staging area.
            Returns:
                True -> if there are inconsistencies between the status and to be added files
                False -> if there is no inconsistencies between the status and to be added files
        """
        return len(files_to_return)!=len(files_to_add)

    def _add_files_to_index(self):
        """
            Adds files from staging area lockfile to index directory
        """
        #TODO remove DELETED files from index

        files = [file.split("|")[0] for file in FileHandler.read_file(self.staging_area_file)]
        for file in files:
            FileHandler.copy_file(file,self.index_directory)
                     

    def _add_files_to_staging_area(self,files_to_add):
        """
        Adds the specified files from status lockfile to the staging area lockfile
        params:
        files_to_add: file paths that needs to be added in the staging area lockfile
        """
        status_entries = self._get_files_from_status(files_to_add)
        FileHandler.append_file(self.staging_area_file,status_entries)


    def _delete_files_from_status(self,files):
        """
            Deletes all files added to staging area from status.
        """
        files_to_del = self._get_files_from_status(files)
        files = FileHandler.read_file(self.status_file)
        files_to_keep = [file for file in files if file not in files_to_del]
        FileHandler.write_file(self.status_file,files_to_keep)

        #delete files under status directory
        FileHandler.delete_files([file.split("|")[0] for file in files_to_del],self.status_directory)            

 

    
    def _remove_files_from_staging_area(self, files):
        """
            Remove the specified files from staging area
            params:
                - files: files that needs to be discarded
        """
        files_to_del = self._get_files_from_staging_area(files)

        files = FileHandler.read_file(self.staging_area_file)
        files_to_keep = [file for file in files if file not in files_to_del]
        FileHandler.write_file(self.staging_area_file,files_to_keep)

    def _add_files_to_status(self,files):
        """
            Adds files from staging area lockfile to status
        """
        staging_files = self._get_files_from_staging_area(files)
        files = [file.split("|")[0] for file in staging_files]
        
        for file in files:
            FileHandler.copy_file(file,self.status_directory)

        
        FileHandler.append_file(self.status_file,staging_files)



    def _remove_files_from_index(self,files):
        """
            Remove discarded files from staging area
        """
        files_to_del = [file.split("|")[0] for file in self._get_files_from_staging_area(files)]
        FileHandler.delete_files(files_to_del,self.index_directory)         


    def execute(self, files):
        """
            Adds the specified files from status into staging area
        returns: 
            1 - command executed successfully
            0 - command execution failed
            message - command execution result
        """

        try:
            if(self.root_not_exists()):
                raise PVCNotInitializedException()

            self._add_files_to_staging_area(files)
            self._delete_files_from_status(files)
            self._add_files_to_index()

        except PVCNotInitializedException as e:
            return 0, e
        except PVCNotMatchedAnyFiles as e:
            return 0, e
        return 1, None

    def undo(self, files):
        """
            Restore changes from the staging area
        """
        try:
            if(self.root_not_exists()):
                raise PVCNotInitializedException()

            self._add_files_to_status(files)
            self._remove_files_from_index(files)
            self._remove_files_from_staging_area(files)

        except PVCNotInitializedException as e:
            return 0, e
        except PVCNotMatchedAnyFiles as e:
            return 0, e
        return 1, None