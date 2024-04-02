from cli.commands.command import Command
import os
import shutil
from datetime import datetime

from utils.FileHandler import FileHandler

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
        """
            Saves the message and the date of the commit.
        """
        with open(commit_dir+"metadata.txt",'w') as f:
            f.writelines(f"{commit_message}|{datetime.now()}")
    
    def _truncate_staging_area(self):
        """
            Truncates the staging area after a successfull commit.
        """
        with open(self.staging_area_file,'w') as f:
            f.truncate(0)

        FileHandler.truncate_directory(self.index_directory)

    def _ignore_files(self,directory, contents):
        """
            Returns what files needs to be ignored from the commit. Files that are in the index directory but not in the staging area.
        """
        with open(self.staging_area_file,"r") as f:
            lines = f.readlines()
            files_staging = [item.split("|")[0] for item in lines]

        files_index = [os.path.relpath(os.path.join(root, file), self.index_directory)
                  for root, directories, files in os.walk(self.index_directory)
                  for file in files]
        
        ignore_list = [file_in for file_in in files_index if file_in not in files_staging]
        return [item for item in contents if item in ignore_list]

    def _commit_files(self, commit_message):
        """
            Commits the files from the staging area.
        """
        commit_version = self._get_commit_version()
        commit_dir =f"{self.commit_directory}/{self.current_branch}/V{commit_version}/"
        
        #TODO outsource the index lock file appending to Add command
        index_files = [file+"\n" for file in FileHandler.get_file_paths_from_dir(self.index_directory)]
        FileHandler.append_file(self.index_lock_file,index_files)

        #copy staging area files to commit directory
        if not(os.path.exists(commit_dir)):
            os.mkdir(commit_dir)
        shutil.copytree(self.index_directory, commit_dir,dirs_exist_ok=True,ignore=self._ignore_files)


        self._write_commit_metadata(commit_dir,commit_message)
       
    
    def _sync_local_repo(self):
        """
            Syncronize local repository with commits
        """
        #NOT FINISHED
        seen_files = []
        commits_dirs = sorted(os.listdir(self.commit_directory+"/"+self.current_branch),reverse=True)

        repo_files = []

        for dir in commits_dirs:  
            for parent, directory, files in os.walk(self.commit_directory+"/"+self.current_branch+"/"+dir):
                for file in files:
                    curr_file = "/".join(os.path.join(parent,file).split("\\")[1:])
                    if curr_file not in seen_files and file not in "metadata.txt":
                        full_curr_file_path = "/".join(os.path.join(dir,parent,file).split("\\")[1:])
                        seen_files.append(curr_file)
                        repo_files.append(full_curr_file_path)

        for index, file in enumerate(repo_files):
            #FileHandler.copy_file(file, os.path.join(self.local_repo,self.current_branch,list(seen_files)[index]))
            shutil.copy(file, os.path.join(self.local_repo,self.current_branch,seen_files[index]))
    def execute(self, commit_message):
        """
            Commits the changes.
        """
        try:
            self._commit_files(commit_message)
            self._truncate_staging_area()
            self._sync_local_repo()
            return 1,"Files commited successfully"
        except Exception as e:
            return 0, e