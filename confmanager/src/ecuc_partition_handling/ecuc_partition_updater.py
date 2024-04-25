import os
from ecuc_partition_handling.ecuc_partition_parser import EcucPartitionParser
import glob
from utils.filehandling import FileHandling

class EcucPartitionUpdater:

    BASE_FILE = 'conf_ecucpartition_ecucvalues.arxml'
    GENERATED_FILE = 'RTEConfGen_EcucPartition_EcucValues.arxml'

    def __init__(self, pver_path, cust_path, output_path, logger):
        self.logger = logger
        self.file_handling_obj = FileHandling(self.logger)        
        self.pver_path = self.file_handling_obj.check_if_folder_exists(pver_path)
        self.cust_path = self.file_handling_obj.check_if_folder_exists(cust_path)
        self.output_path = self.file_handling_obj.check_if_folder_exists(output_path)
    
    def port_delta(self):
        '''
        From PVER CI
        - file A: conf_ecucpartition_values.arxml
        - file B: RTEConfGen_EcucPartition.arxml

        Pre RTE received from customer: 
        - file A+: conf_ecucpartition_values.arxml
        - file B+: RTEConfGen_EcucPartition.arxml

        --> GOAL: Port delta = (A+_A) & (B+_B) into file A
        '''
        self.logger.info("Updating EcucPartition...")
        base_pver_file = glob.glob(os.path.join(self.pver_path, 
                                           f'**/{EcucPartitionUpdater.BASE_FILE}'), recursive=True)[0]
        base_cust_file = glob.glob(os.path.join(self.cust_path, 
                                           f'**/{EcucPartitionUpdater.BASE_FILE}'), recursive=True)[0]  
        gen_file = glob.glob(os.path.join(self.pver_path, 
                                      f'**/{EcucPartitionUpdater.GENERATED_FILE}'), recursive=True)[0]          
        gen_cust_file = glob.glob(os.path.join(self.cust_path, 
                                          f'**/{EcucPartitionUpdater.GENERATED_FILE}'), recursive=True)[0]
                                                        
        updated_file = os.path.join(self.output_path, f'{EcucPartitionUpdater.BASE_FILE}')
    
        # Process to port delta changes into Pver base file
        base_pver_parser= EcucPartitionParser(base_pver_file)
        base_cust_parser = EcucPartitionParser(base_cust_file)
        gen_parser = EcucPartitionParser(gen_file)    
        gen_cust_parser = EcucPartitionParser(gen_cust_file)             
        
        '''
        Compare (A - A+) -> delta_1: Already in base_cust_parser
        Compare (B - B+) -> delta_2
        '''     
        mapper_ref_delta_2 = gen_cust_parser.map_container_reference()
        mapper_cont_delta_2 = gen_cust_parser.map_container_content()
        gen_parser.update_ecuc_iref(container_ref_id = mapper_ref_delta_2, 
                                    container_content_id = mapper_cont_delta_2)
        gen_parser.check_duplicate_iref()
        
        # Port delta changes = delta_1 + delta_2 into base Pver, i.e file A
        mapper_ref_delta_12 = gen_parser.map_container_reference()        
        mapper_cont_delta_12 = gen_parser.map_container_content()
        base_cust_parser.update_ecuc_iref(container_ref_id = mapper_ref_delta_12, 
                                        container_content_id = mapper_cont_delta_12)
        
        base_cust_parser.check_duplicate_iref()
        base_cust_parser.check_empty_element()

        # Get PARAMETER-VALUES from the base Pver file in case the customer changes it
        mapper_param = base_pver_parser.map_container_parameter()
        base_cust_parser.check_base_param(mapper_param)

        # Update new conf_ecucpartition_values.arxml file
        base_cust_parser.update_ecucpartition_file(updated_file)   