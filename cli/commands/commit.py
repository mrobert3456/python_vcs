from cli.commands.command import Command
import os
class Commit(Command):
    def __init__(self):
        super().__init__()
        
    def _get_commit_version(self):
        """
            Gets the next commit version by counting the sub-folders inside the /commit directory and increase with 1.
            returns:
                    - commit version number
        """
        sub_dirs = [os.path.join(self.commit_directory,item) for item in os.listdir(self.commit_directory)]
        
        return len(sub_dirs) + 1
    
    def _write_commit_metadata(self, commit_message):

        with open(self.commit_directory+"/metadata.txt",'w') as f:
            return
        
    
    def _get_files_from_staging_area(self):
        return []

    def _commit_files(self, files_to_commit):
        commit_version = self._get_commit_version()
        commit_dir =f"{self.commit_directory}/V{commit_version}"
        os.makedirs(commit_dir)

        for file in files_to_commit:
            pass
        return 
    
    def execute(self, commit_message):
        
        files_to_commit = self._get_files_from_staging_area()

        self._commit_files(files_to_commit)

        return 1