import array
import os
import shutil


class FileHandler:
    @classmethod    
    def copy_file(cls,file, destination_dir):
        file_dir ="/".join(file.split("\\")[:-1])
        destination = os.path.join(destination_dir,file).replace("\\","/")
        if not(os.path.exists(destination_dir+"/"+file_dir)):
           cls.create_directories(destination_dir+"/"+file_dir)
        
        shutil.copy(file, destination)
    
    @classmethod
    def delete_files(cls,files_to_del,parent_dir):
        for to_del in files_to_del:
            dest = os.path.join(parent_dir,to_del.split("|")[0]).replace("\\","/")
            os.remove(dest)
    
    @classmethod
    def create_directory(cls,dir):
        os.mkdir(dir)
    
    @classmethod    
    def create_directories(cls,dirs):
        os.makedirs(dirs)

    @classmethod
    def read_file(cls,file):
        with open(file, "r") as f:
            lines = f.readlines()
        return lines
    @classmethod
    def create_file(cls,file):
        cr_file = open(file,'w')
        cr_file.close()

    @classmethod
    def get_file_paths_from_dir(cls,directory):
        files_paths = [os.path.relpath(os.path.join(root, file), directory)
                  for root, directories, files in os.walk(directory)
                  if ".pv" not in root and ".git" not in root
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