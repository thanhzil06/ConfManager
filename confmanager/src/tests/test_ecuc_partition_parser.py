import unittest
from logger.loadlogconf import LoadLogconf
import os
from xmldiff import main, formatting
from ecuc_partition_handling.ecuc_partition_parser import EcucPartitionUpdater
import tests.test_constants_partition as test_part_const

class TestEcucPartitionUpdater(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_file = test_part_const.base_file        
        cls.delta_file = test_part_const.delta_file
        cls.output_file = test_part_const.output_file
        cls.expected_file = test_part_const.expected_file

        cls.merged_obj = EcucPartitionUpdater(cls.base_file)
        cls.delta_obj = EcucPartitionUpdater(cls.delta_file)    

    def setUp(self):
        ''' 
        - This method will be called once at the beginning of tests.
        - With maxDiff set to None,  the unittest framework will display the entire diff output without truncation
        --> be helpful when debugging failures involving large multiline strings.
        '''
        self.maxDiff = None

    def test_update_ecuc_partion(self):                    
        self.ut_ecuc_partition_handle(output_file=self.output_file,
                                      expected_file= self.expected_file)
        
    def ut_ecuc_partition_handle(self, output_file, expected_file):
        ecuc_id = self.delta_obj.map_ecuc_ref()
        self.merged_obj.update_ecuc_iref(ecuc_id)
        self.merged_obj.check_duplicate_iref()            
        # Add the delta changes to build the output which is based on Pver file - conf_ecucpartition_ecucvalues.arxml
        self.merged_obj.update_ecucpartition_file(updated_output_file=output_file)

        # Compare the generated output file with the expected one  
        differ = main.diff_files(output_file,
                                expected_file,
                                formatter=formatting.DiffFormatter())
        self.assertEqual(differ, '')
               
    if __name__ == '__main__':
        unittest.main()