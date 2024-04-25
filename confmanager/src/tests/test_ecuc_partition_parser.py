import unittest
from xmldiff import main, formatting
from ecuc_partition_handling.ecuc_partition_parser import EcucPartitionParser
import tests.test_constants_partition as test_const

class TestEcucPartitionParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_pver_file = test_const.base_pver_file        
        cls.base_obj = EcucPartitionParser(cls.base_pver_file) 

    def setUp(self):
        self.maxDiff = None
        self.sub_container = self.base_obj.sub_containers    
        self.ecuc_containers = self.base_obj.get_ecuc_container(self.sub_container)

    def test_get_ecuc_container(self):
        base_container_quantity = len(self.ecuc_containers)
        self.assertEqual(base_container_quantity, 3, 
                         "Wrong quantity of containers in the base pver")  

    def test_check_condition(self):
        for ecuc_container in self.ecuc_containers:
            self.assertEqual(self.base_obj.check_condition(ecuc_container), True, 
                             "DEFINITION-REF does not have required content")
            
    def test_get_short_name(self):                
        self.assertEqual(self.base_obj.get_short_name(self.ecuc_containers[-1]).text, 
                             'EcucPartition_OsApp_C', 'Short name does not match')

    def test_get_reference(self):                
            self.assertIsNotNone(self.base_obj.get_reference(self.ecuc_containers[-1]))
    
    def test_get_iref(self):        
            self.assertIsNotNone(self.base_obj.get_iref(self.ecuc_containers[-1]))

    def test_get_target_name(self):         
            self.assertEqual(self.base_obj.get_target_name(self.ecuc_containers[-1]), 
                             'CPT_C1', 'Target name does not match')
            
    def test_get_parameter(self):
         self.assertIsNotNone(self.base_obj.get_parameter(self.ecuc_containers[-1]))
            
    def test_map_container_reference(self):                
        self.assertIsNotNone(self.base_obj.map_container_reference())

    def test_map_container_parameter(self):                
        self.assertIsNotNone(self.base_obj.map_container_parameter())

    def test_map_container_content(self):
        self.assertIsNotNone(self.base_obj.map_container_content())

    def test_sort_ecuc_container(self):
        # Test for checking sort function
        self.base_obj.sort_ecuc_container(ecuc_containers=self.ecuc_containers, 
                                          sub_containers=self.sub_container)
        self.base_obj.update_ecucpartition_file(test_const.output_sort)   

        # Compare the generated output file after sorted with the expected one  
        differ = main.diff_files(test_const.output_sort,
                                test_const.expect_sort,
                                formatter=formatting.DiffFormatter())
        self.assertEqual(differ, '')  

    def test_check_duplicate_iref(self):
        # Test for checking removing duplicate instance references
        dup_obj = EcucPartitionParser(test_const.duplicate_file)
        dup_obj.check_duplicate_iref()
        dup_obj.update_ecucpartition_file(test_const.output_duplicate)
        
        # Compare the generated output file after removing duplicate element with the expected one  
        differ = main.diff_files(test_const.output_duplicate,
                                test_const.expect_dup_remove,
                                formatter=formatting.DiffFormatter())
        self.assertEqual(differ, '')     

    def test_check_empty_element(self):
        # Test for checking removing empty container
        empty_obj = EcucPartitionParser(test_const.empty_file)
        empty_obj.check_empty_element()
        empty_obj.update_ecucpartition_file(test_const.output_empty)
        
        # Compare the generated output file after removing empty element with the expected one  
        differ = main.diff_files(test_const.output_empty,
                                test_const.expect_empty_remove,
                                formatter=formatting.DiffFormatter())
        self.assertEqual(differ, '')

    def test_check_base_param(self):
        # Test for checking whether customer changed the base information (parameter values) or not
        base_param_obj = EcucPartitionParser(test_const.base_param_file)
        changed_param_obj = EcucPartitionParser(test_const.changed_param_file)

        mapper = base_param_obj.map_container_parameter()
        changed_param_obj.check_base_param(mapper)
        changed_param_obj.update_ecucpartition_file(test_const.output_param)
        
        # Compare the generated output file with the base file from CI Pver  
        differ = main.diff_files(test_const.output_param,
                                test_const.base_param_file,
                                formatter=formatting.DiffFormatter())
        self.assertEqual(differ, '')

    if __name__ == '__main__':
        unittest.main()