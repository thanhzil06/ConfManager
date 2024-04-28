import unittest
from logger.loadlogconf import LoadLogconf
from confmanager_modes.confmanager_merger import MergerMode
from confmanager_modes.confmanager_modes_common import CommonModeUtils
from confmanager_modes.confmanager_updater import UpdaterMode
import tests.test_constants_updater as test_upd_csts
import os
import constants as csts
import shutil
from xmldiff import main, formatting


class TestUpdaterMode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This method will be called once at the beginning of tests
        :return:
        """
        cls.test_files_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_files"))
        cls.output_path = os.path.join(cls.test_files_root, "out_updater_mode")
        if not (os.path.isdir(cls.output_path)):
            os.mkdir(cls.output_path, 0o777)

        cls.pver_root = os.path.join(cls.test_files_root, "pver_test")
        cls.cust_ws = os.path.join(cls.test_files_root, "STLA_ws")
        cls.expected_files_path = os.path.join(cls.test_files_root, "expected_Updater")
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
        print("End of test_updater_mode")
        # Close logs filehandlers and remove them
        handlers = cls.logger.handlers[:]
        for handler in handlers:
            cls.logger.removeHandler(handler)
            handler.close()
        # Remove output path
        #
        shutil.rmtree(cls.output_path)

    def ut_updater_template(self, test_configuration_data):
        for topic in test_configuration_data.keys():
            (target_file,
             files_to_merge_path_list,
             content_to_remove) = self.modes_common_obj.prepare_mode_inputs('updater',
                                                                            topic,
                                                                            test_configuration_data,
                                                                            [self.cust_ws])
            # Read merged file
            merged_file_dict = dict()
            (merged_root,
             merged_file_dict[csts.root_main_tag]) = self.tool_merger_obj.parse_and_get_dico(files_to_merge_path_list[0])

            self.updater_obj.update_files(target_file, merged_root, merged_file_dict, content_to_remove)

            # Check if generated file is equal to expected file
            target_filename = test_configuration_data[topic]['updater']['target_file']
            generated_updated_filepath = os.path.join(self.output_path, target_filename)
            expected_updated_filepath = os.path.join(self.expected_files_path, target_filename)

            delta_exp_gen = main.diff_files(generated_updated_filepath,
                                            expected_updated_filepath,
                                            formatter=formatting.DiffFormatter())
            self.assertEqual(delta_exp_gen, '')

    # ---------------------------- TESTS ----------------------------
    def test_update_file_ecuextract(self):
        """
        Test case: no Merge, only update.
        For it, Update is used to go back to one of files used to merge
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.ecuextract_updater_conf)

    def test_update_file_ecuextract_1(self):
        """
        Test case: no Merge, only update.
        For it, Update is used to go back to one of files used to merge
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.ecuextract_updater_1_conf)

    def test_update_file_ecuextract_2(self):
        """
        Test case: no Merge, only update.
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.ecuextract_updater_2_conf)

    def test_update_file_flatview(self):
        """
        Test case: no Merge, only update. Nothing to remove.
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.flatview_updater_conf)

    def test_update_file_flatview_1(self):
        """
        Test case: no Merge, only update.
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.flatview_updater_1_conf)

    def test_update_file_flatmap(self):
        """
        Test case: no Merge, only update.
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.flatmap_updater_conf)

    @unittest.skip('Skip until decision regarding ecucpartition issue')
    def test_update_file_ecupartition(self):
        """
        Test case: no Merge, only update.
        """
        self.updater_obj = UpdaterMode(self.pver_root, self.output_path, self.cust_ws, self.logger)
        self.tool_merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_updater_template(test_upd_csts.ecupartition_updater_conf)


if __name__ == '__main__':
    unittest.main()
