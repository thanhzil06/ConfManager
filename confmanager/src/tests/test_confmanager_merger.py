import unittest
import os
from logger.loadlogconf import LoadLogconf
from confmanager_modes.confmanager_merger import MergerMode
from confmanager_modes.confmanager_modes_common import CommonModeUtils
import tests.test_constants_merger as test_csts
import shutil
from xmldiff import main, formatting


class TestMergerMode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This method will be called once at the beginning of tests
        :return:
        """
        cls.test_files_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_files"))
        cls.output_path = os.path.join(cls.test_files_root, "out_merger_mode")
        if not (os.path.isdir(cls.output_path)):
            os.mkdir(cls.output_path, 0o777)

        cls.pver_root = os.path.join(cls.test_files_root, "pver_test")
        cls.logger = LoadLogconf(logger_choice="dev", output_path=cls.output_path).log
        cls.expected_files_path = os.path.join(cls.test_files_root, "expected_Merger")
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
        print("End of test_merger_mode")
        # Close logs filehandlers and remove them
        handlers = cls.logger.handlers[:]
        for handler in handlers:
            cls.logger.removeHandler(handler)
            handler.close()
        # Remove output path
        #
        shutil.rmtree(cls.output_path)

    def ut_merger_template(self, test_configuration_data, test_files_to_merge_list):
        for topic in test_configuration_data.keys():
            (target_file,
             files_to_merge_path_list, _) = self.modes_common_obj.prepare_mode_inputs('merger',
                                                                                      topic,
                                                                                      test_configuration_data,
                                                                                      [self.pver_root])
            self.merger_obj.merge_files(target_file, files_to_merge_path_list)
            # Check if all file paths had been fetched
            self.assertEqual(self.merger_obj.files_to_merge_path_list.sort(),
                             test_files_to_merge_list.sort())  # add assertion here

            # Check if generated file is equal to expected file
            target_filename = test_configuration_data[topic]['merger']['target_file']
            generated_merged_file_path = os.path.join(self.output_path, target_filename)
            expected_merged_file_path = os.path.join(self.expected_files_path, target_filename)
            delta_exp_gen = main.diff_files(expected_merged_file_path,
                                            generated_merged_file_path,
                                            formatter=formatting.DiffFormatter())
            self.assertEqual(delta_exp_gen, '')
            print(delta_exp_gen)

    # ---------------------------- TESTS ----------------------------
    @unittest.skip('Skip until correction of multiple files issue')
    def test_merge_ecuextract(self):
        self.logger.info("Running test_merge_ecuextract...")
        self.merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_merger_template(test_csts.ecuextract_conf, test_csts.ecuextract_path_list)

    #@unittest.skip('Skip for now')
    def test_merge_ecuextract_2_files(self):
        self.logger.info("Running test_merge_ecuextract_2_files...")
        self.merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_merger_template(test_csts.ecuextract_conf_2, test_csts.ecuextract_2_path_list)

    @unittest.skip('Skip for now')
    def test_merge_ecuextract_3_files(self):
        self.logger.info("Running test_merge_ecuextract_3_files...")
        self.merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_merger_template(test_csts.ecuextract_conf_3, test_csts.ecuextract_3_path_list)

    @unittest.skip('Skip until correction of multiple files issue')
    def test_merge_flatview(self):
        self.logger.info("Running test_merge_flatview...")
        self.merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_merger_template(test_csts.flatview_conf, test_csts.flatview_path_list)

    @unittest.skip('Skip until correction of multiple files issue')
    def test_merge_flatmap(self):
        self.logger.info("Running test_merge_flatmap...")
        self.merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_merger_template(test_csts.flatmap_conf, test_csts.flatmap_path_list)

    @unittest.skip('Skip until correction of multiple files issue')
    def test_merge_ecupartition(self):
        self.logger.info("Running test_merge_ecupartition..")
        self.merger_obj = MergerMode(self.pver_root, self.output_path, self.logger)

        self.ut_merger_template(test_csts.ecupartition_conf, test_csts.ecupartition_path_list)


if __name__ == "__main__":
    unittest.main()
