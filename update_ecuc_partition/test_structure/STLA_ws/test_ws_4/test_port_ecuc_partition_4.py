# Test script for updating ECUC_Partition from STLA to Bosch
#   If Bosch already has reference tag then just add ecuc instance elements of STLA to Bosch reference
# Write code using OOP concepts
# Use 2 files:
#    test_bosch_4.arxml       - Bosch
#    test_stla_4.arxml - STLA
# Then output: updated_bosch_4.arxml
from lxml import etree
import os
from ecuc_partition_handling.ecuc_partition_parser_v2 import EcucPartitionParser
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

def main():
# STLA and Bosch arxml files which then are implemented
    path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/update_ecuc_partition/test_structure/STLA_ws/test_ws_4"
    bosch_arxml_file= os.path.join(path, 'test_bosch_4.arxml')    
    stla_arxml_file=os.path.join(path,'test_stla_4.arxml')    
    updated_bosch_file = os.path.join(path,'updated_bosch_4.arxml')
#----------------------------------------------------------------------------------------------------------------------
# parent: SUB-CONTAINERS -> ECUC-CONTAINER-VALUE -> SHORT-NAME[0] = DEFINITION-REF[1] = PARAMETER-VALUES[2] = REFERENCE-VALUES[3]
    bosch_parser = EcucPartitionParser(bosch_arxml_file)
    stla_parser = EcucPartitionParser(stla_arxml_file)
# Add STLA ECUC-INSTANCE-REFERENCE-VALUE to Bosch REFERENCE-VALUES     
    stla_ecuc_iref = stla_parser.get_ecuc_iref()
    bosch_parser.add_ecuc_iref(new_iref=stla_ecuc_iref)

    bosch_parser.update_new_arxml(updated_bosch_file)

if __name__== "__main__":
    main()
