import unittest
from logger.loadlogconf import LoadLogconf
from xmldiff import main, formatting
from ecuc_partition_handling.ecuc_partition_updater import EcucPartitionUpdater
import tests.test_constants_partition as test_const

class TestEcucPartitionUpdater(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pver_path = test_const.pver_root    
        cls.customer_path = test_const.cust_ws
        cls.output_path = test_const.output_path

        cls.output_file = test_const.output_file
        cls.expected_file = test_const.expected_file

        cls.logger = LoadLogconf(logger_choice="dev", 
                                 output_path=cls.output_path).log

        cls.updater_obj = EcucPartitionUpdater(pver_path=cls.pver_path,
                                               cust_path=cls.customer_path,
                                               output_path=cls.output_path,
                                               logger=cls.logger)    

    def setUp(self):
        self.maxDiff = None

    def test_port_delta(self):
        self.updater_obj.port_delta()
        # Compare the generated output file with the expected one  
        differ = main.diff_files(self.output_file,
                                self.expected_file,
                                formatter=formatting.DiffFormatter())
        self.assertEqual(differ, '')