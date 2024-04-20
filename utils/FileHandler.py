import array
import os
import shutil


class FileHandler:
    @classmethod    
    def copy_file(cls,file, destination_dir):
        file_dir ="/".join(file.split("\\")[:-1])
        destination = os.path.join(destination_dir,file)

        if not(os.path.exists(os.path.join(destination_dir,file_dir))):
           cls.create_directories(os.path.join(destination_dir,file_dir))

        shutil.copy(file, destination)
    
    @classmethod
    def delete_files(cls, files_to_del, parent_dir):
        for to_del in files_to_del:
            os.remove(os.path.join(parent_dir,to_del))
    
    @classmethod
    def create_directory(cls,dir):
        os.mkdir(dir)
    
    @classmethod    
    def create_directories(cls,dirs):
        os.makedirs(dirs)

    @classmethod
    def read_file(cls,file):
        try:
            with open(file, "r") as f:
                lines = f.readlines()
            return lines
        except Exception as e:
            return []
    @classmethod
    def create_file(cls,file):
        cr_file = open(file,'w')
        cr_file.close()

    @classmethod
    def get_file_paths_from_dir(cls,directory,exclude_dirs=[]):
        files_paths = [os.path.relpath(os.path.join(root, file), directory)
                  for root, directories, files in os.walk(directory)
                  if all(ex_dir not in root for ex_dir in exclude_dirs)
                  for file in files]
        return files_paths

    @classmethod 
    def write_file(cls,file_to_write,content):
        with open(file_to_write,'w') as f:
            if type(content) is array.array:
                for file in file_to_write:
                    f.writelines(file)
            else:
                f.writelines(content)
    @classmethod
    def append_file(cls, file_to_write, content):
        with open(file_to_write,'a+') as f:
            if type(content) is array.array:
                for file in file_to_write:
                    f.writelines(file)
            else:
                f.writelines(content)
        
    @classmethod
    def truncate_directory(cls,dir_path):
        shutil.rmtree(dir_path)
        cls.create_directory(dir_path)
    
    @classmethod
    def delete_directory(cls,dir_path):
        shutil.rmtree(dir_path)
    
    @classmethod
    def overwrite_file(cls,src,dest):
        shutil.copy(src,dest)