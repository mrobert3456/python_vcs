from unittest import TestCase
from unittest.mock import patch
from utils.FileHandler import FileHandler
import os
class FileHandlerTests(TestCase):

    def setUp(self) -> None:
        self.file = "source\\vmi.txt"
        self.file_dir = "source"
        self.dest = "destination_dir\\sub_dir"

    @patch('os.path.exists', return_value=True)
    @patch('shutil.copy')
    @patch("utils.FileHandler.FileHandler.create_directories")
    def test_copy_file_existing_dir(self, create_dirs, shutil_copy, mock_path_exists):
        FileHandler.copy_file(self.file,self.dest)

        mock_path_exists.assert_called_once_with(os.path.join(self.dest, self.file_dir))
        shutil_copy.assert_called_once_with(self.file, os.path.join(self.dest, self.file))
        create_dirs.assert_not_called()
    

    @patch('os.path.exists', return_value=False)
    @patch('shutil.copy')
    @patch("utils.FileHandler.FileHandler.create_directories")
    def test_copy_file_not_existing_dir(self, create_dirs ,shutil_copy, mock_path_exists):
        FileHandler.copy_file(self.file, self.dest)

        mock_path_exists.assert_called_once_with(os.path.join(self.dest, self.file_dir))
        create_dirs.assert_called_once_with(os.path.join(self.dest, self.file_dir))
        shutil_copy.assert_called_once_with(self.file, os.path.join(self.dest, self.file))



    @patch('os.remove')
    def test_delete_files(self, os_remove):
        FileHandler.delete_files([self.file], self.dest)
        os_remove.assert_called_once_with(os.path.join(self.dest, self.file))


    @patch('os.mkdir')
    def test_create_directory(self, mkdir):
        FileHandler.create_directory(self.file_dir)
        mkdir.assert_called_once_with(self.file_dir)

    @patch('os.makedirs')
    def test_create_directories(self, make_dirs):
        FileHandler.create_directories(self.dest)
        make_dirs.assert_called_once_with(self.dest)

    @patch('builtins.open', create=True)
    def test_read_file_no_exception(self, open_file):
        FileHandler.read_file(self.file)
        open_file.assert_called_once_with(self.file, "r")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_read_file_exception_return_empty_array(self, open_file):
        lines = FileHandler.read_file(self.file)
        self.assertEqual(lines, [])
        open_file.assert_called_once_with(self.file, "r")

    @patch('builtins.open', create=True)
    def test_create_file(self, create_file):
        FileHandler.create_file(self.file)
        create_file.assert_called_once_with(self.file,"w")
        mock_file = create_file.return_value
        mock_file.close.assert_called_once()

    @patch("os.walk")
    def test_get_file_paths_from_dir(self,mock_walk):
        mock_walk.return_value = [
            ("source", ["dir1", "dir2"], ["file1.txt", "file2.txt"]),
            ("source/dir1", [], ["file3.txt"]),
            ("source/dir2", [], ["file4.txt"])
        ]

        exclude_dirs = ["dir1"]

        paths = FileHandler.get_file_paths_from_dir(self.file_dir, exclude_dirs)

        self.assertEqual(paths,[
                    "file1.txt",
                    "file2.txt",
                    "dir2\\file4.txt"
                ])
        

    @patch('builtins.open', create=True)
    def test_write_file_with_array(self, write_file):
        FileHandler.write_file(self.file,["something","test"])
        write_file.assert_called_once_with(self.file,"w")

    @patch('builtins.open', create=True)
    def test_write_file_with_string(self, write_file):
        FileHandler.write_file(self.file,"something")
        write_file.assert_called_once_with(self.file,"w")


    @patch('builtins.open', create=True)
    def test_append_file_with_array(self, write_file):
        FileHandler.append_file(self.file,["something","test"])
        write_file.assert_called_once_with(self.file,"a+")

    @patch('builtins.open', create=True)
    def test_append_file_with_string(self, write_file):
        FileHandler.append_file(self.file,"something")
        write_file.assert_called_once_with(self.file,"a+")

    @patch("shutil.rmtree")
    @patch("utils.FileHandler.FileHandler.create_directory")
    def test_truncate_directory(self,truncate,create_dir):
        FileHandler.truncate_directory(self.file_dir)
        truncate.assert_called_once_with(self.file_dir)
        create_dir.assert_called_once_with(self.file_dir)

    @patch("shutil.rmtree")
    def test_delete_directory(self,delete):
        FileHandler.delete_directory(self.file_dir)
        delete.assert_called_once_with(self.file_dir)

    @patch("shutil.copy")
    def test_overwrite_file(self,copy):
        FileHandler.overwrite_file(self.file, self.dest)
        copy.assert_called_once_with(self.file, self.dest)


