import unittest
from logger.loadlogconf import LoadLogconf
import os
from confmanager_modes.confmanager_modes_common import CommonModeUtils
import shutil
import tests.test_constants_mode_common as test_csts


class TestModesCommon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This method will be called once at the beginning of tests
        :return:
        """
        cls.test_files_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_files"))
        cls.STLA_ws_path = os.path.join(cls.test_files_root, "STLA_ws")
        cls.pver_root = os.path.join(cls.test_files_root, "pver_test")
        cls.output_path = os.path.join(cls.test_files_root, "out_modes_common")
        if not (os.path.isdir(cls.output_path)):
            os.mkdir(cls.output_path, 0o777)
        cls.logger = LoadLogconf(logger_choice="dev", output_path=cls.output_path).log
        cls.modes_common_obj = CommonModeUtils(cls.logger)

    def setUp(self):
        """
        This method will be called before each test
        :return:
        """
        self.maxDiff = None

    @classmethod
    def tearDownClass(cls):
        """
        This method will be called once at the end of all tests
        :return:
        """
        print("End of test_modes_common")
        # Close logs filehandlers and remove them
        handlers = cls.logger.handlers[:]
        for handler in handlers:
            cls.logger.removeHandler(handler)
            handler.close()
        # Remove output path
        #
        shutil.rmtree(cls.output_path)

    # ---------------------------- TESTS ----------------------------
    def test_prepare_mode_inputs_merger(self):
        self.logger.info("Running test_prepare_mode_inputs_merger...")
        (target_file,
         files_path_list,
         content_to_remove_filename) = self.modes_common_obj.prepare_mode_inputs('Merger'.lower(),
                                                                                 'EcuExtract',
                                                                                 test_csts.configuration_test,
                                                                                 [self.pver_root])
        # Check target_name
        self.assertEqual(target_file, test_csts.merged_ecuextract_file_name)
        # Check files_path_list
        self.assertEqual(files_path_list.sort(), test_csts.exp_files_to_merge_path_list_merger.sort())
        # Check content_to_remove_filename
        self.assertEqual(content_to_remove_filename, test_csts.exp_content_to_remove_filename_merger)

    def test_prepare_mode_inputs_updater(self):
        self.logger.info("Running test_prepare_mode_inputs_updater...")
        (target_file,
         files_path_list,
         content_to_remove_filename) = self.modes_common_obj.prepare_mode_inputs('Updater'.lower(),
                                                                                 'EcuExtract',
                                                                                 test_csts.configuration_test,
                                                                                 [self.STLA_ws_path])
        # Check target_name
        self.assertEqual(target_file, test_csts.updater_ecuextract_file_name)
        # Check files_path_list
        self.assertEqual(files_path_list.sort(), test_csts.exp_files_to_merge_path_list_updater.sort())
        # Check content_to_remove_filename
        self.assertEqual(content_to_remove_filename, test_csts.exp_content_to_remove_filename_updater)


if __name__ == '__main__':
    unittest.main()
