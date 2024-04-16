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
        '''
        self.logger.info("Updating ECUCPartition...")
        base_pver_file = glob.glob(os.path.join(self.pver_path, 
                                      f'**/{EcucPartitionUpdater.BASE_FILE}'), recursive=True)[0]
        gen_file = glob.glob(os.path.join(self.pver_path, 
                                      f'**/{EcucPartitionUpdater.GENERATED_FILE}'), recursive=True)[0]
        
        base_cust_file = glob.glob(os.path.join(self.cust_path, 
                                           f'**/{EcucPartitionUpdater.BASE_FILE}'), recursive=True)[0]    
        gen_cust_file = glob.glob(os.path.join(self.cust_path, 
                                          f'**/{EcucPartitionUpdater.GENERATED_FILE}'), recursive=True)[0]
                                                        
        updated_file = os.path.join(self.output_path, f'{EcucPartitionUpdater.BASE_FILE}')
    
        # Process to port delta changes into Pver base file
        base_pver_parser = EcucPartitionParser(base_pver_file)
        base_cust_parser = EcucPartitionParser(base_cust_file)

        gen_parser = EcucPartitionParser(gen_file)    
        gen_cust_parser = EcucPartitionParser(gen_cust_file)      
        
        # Compare (A - A+) -> delta_1
        mapper_1 = base_cust_parser.map_container_reference()    
        base_pver_parser.update_ecuc_iref(mapper_1)
        base_pver_parser.check_duplicate_iref()

        # Compare (B - B+) -> delta_2
        mapper_2 = gen_cust_parser.map_container_reference()
        gen_parser.update_ecuc_iref(mapper_2)
        gen_parser.check_duplicate_iref()

        # Port (delta_1 + delta_2) into A
        mapper_3 = gen_parser.map_container_reference()
        base_pver_parser.update_ecuc_iref(mapper_3)
        base_pver_parser.check_duplicate_iref()

        base_pver_parser.update_ecucpartition_file(updated_file)                