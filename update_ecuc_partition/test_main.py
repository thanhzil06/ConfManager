import os
from ecuc_partition_handling.ecuc_partition_parser import EcucPartitionUpdater

def main():
# STLA and Bosch arxml files which then are implemented
    path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/update_ecuc_partition"
    bosch_arxml_file= os.path.join(path, 'test_conf_ecucpartition_ecucvalues.arxml')    
    stla_arxml_file=os.path.join(path,'test_RTEConfGen_EcucPartition_EcucValues.arxml')    
    updated_bosch_file = os.path.join(path,'updated_ecuc_partition.arxml')
#----------------------------------------------------------------------------------------------------------------------
# parent: SUB-CONTAINERS -> ECUC-CONTAINER-VALUE -> SHORT-NAME[0] = DEFINITION-REF[1] = PARAMETER-VALUES[2] = REFERENCE-VALUES[3]
    bosch_parser = EcucPartitionUpdater(bosch_arxml_file)
    stla_parser = EcucPartitionUpdater(stla_arxml_file)

# Add REFERENCE-VALUES element of STLA right after the PARAMETER-VALUES element in Bosch arxml    
    bosch_ecuc_container_id = bosch_parser.ecuc_container_id # a hashmap/dict. Firstly empty-{}  
    bosch_ecuc_container_id = stla_parser.map_ecuc_ref()   
    bosch_parser.update_ecuc_iref(bosch_ecuc_container_id)
#----------------------------------------------------------------------------------------------------------------------
    bosch_parser.update_new_arxml(updated_bosch_file)

if __name__== "__main__":
    main()