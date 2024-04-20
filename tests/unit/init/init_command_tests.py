from unittest import TestCase
from cli.commands.init import Init
from unittest.mock import patch
from cli.exceptions.pvc_already_initalized_exception import PVCAlreadyInitializedException

class InitTests(TestCase):

    def setUp(self) -> None:
       self.init = Init()

    @patch("utils.FileHandler.FileHandler.create_directory")
    @patch("utils.FileHandler.FileHandler.create_directories")
    @patch("utils.FileHandler.FileHandler.create_file")
    @patch("cli.commands.init.Init.root_not_exists", return_value=True)
    def test_create_directories(self, root_not_exists, create_file, create_dirs, create_dir ):
        self.init.initialize_directory()

        root_not_exists.assert_called_once()

        create_file.assert_any_call(self.init.index_lock_file)
        create_file.assert_any_call(self.init.status_file)
        create_file.assert_any_call(self.init.staging_area_file)

        create_dirs.assert_any_call(self.init.local_repo+"/"+self.init.current_branch)
        create_dirs.assert_any_call(self.init.commit_directory+"/"+self.init.current_branch)

        create_dir.assert_any_call(self.init.status_directory)
        create_dir.assert_any_call(self.init.index_directory)
        create_dir.assert_any_call(self.init.checkout_directory)
        create_dir.assert_any_call(self.init.base_directory)
       
    def test_throws_PVCAlreadyInitializedException(self):
        with patch("cli.commands.init.Init.root_not_exists") as mocked_root_check:
            mocked_root_check.return_value=False
            self.assertRaises(PVCAlreadyInitializedException, self.init.initialize_directory)
    
    @patch("utils.FileHandler.FileHandler.copy_file")
    @patch("utils.FileHandler.FileHandler.write_file")
    def test_add_files_to_status(self, write_file, copy_file):
       with patch("utils.FileHandler.FileHandler.get_file_paths_from_dir") as files_to_track:
            files_to_track.return_value=["main.py", "vmi.py"]
            content =self.init.return_created_file_metadata(files_to_track.return_value) # should this be mocked??
            
            self.init.add_files_to_status()

            write_file.assert_called_once_with(self.init.status_file, content)
            copy_file.assert_any_call("vmi.py", self.init.status_directory)
            copy_file.assert_any_call("main.py", self.init.status_directory)
        