from cli.commands.command import Command
import os
import shutil
from datetime import datetime
class Commit(Command):
    def __init__(self):
        super().__init__()
        
    def _get_commit_version(self):
        """
            Gets the next commit version by counting the sub-folders inside the /commit directory and increase with 1.
            returns:
                    - commit version number
        """
        sub_dirs = [os.path.join(self.commit_directory,item) for item in os.listdir(self.commit_directory+"/"+self.current_branch)]
        
        return len(sub_dirs) + 1
    
    def _write_commit_metadata(self,commit_dir, commit_message):
        with open(commit_dir+"metadata.txt",'w') as f:
            f.writelines(f"{commit_message}|{datetime.now()}")
        
    
    #def _get_files_from_staging_area(self):
    #    with open(self.staging_area_file,'r')as f:
    #        files = f.readlines()
    #    return files
    
    def _flush_staging_area(self):
        with open(self.staging_area_file,'w') as f:
            f.truncate(0)

    def _commit_files(self, commit_message):
        commit_version = self._get_commit_version()
        commit_dir =f"{self.commit_directory}/{self.current_branch}/V{commit_version}/"
        
        if not(os.path.exists(commit_dir)):
            os.mkdir(commit_dir)
        shutil.copytree(self.index_directory, commit_dir,dirs_exist_ok=True)
        self._write_commit_metadata(commit_dir,commit_message)
       

    def execute(self, commit_message):
        
        #files_to_commit = self._get_files_from_staging_area()
        self._commit_files(commit_message)
        self._flush_staging_area()
        return 1,"Files commited successfully"