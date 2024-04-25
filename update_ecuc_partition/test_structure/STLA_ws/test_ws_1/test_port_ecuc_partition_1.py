# Test script for updating ECUC_Partition from STLA to Bosch: Get STLA ref tag and add to Bosch, after param tag - DONE
# Write all in one main. Not use OOP
# Use 2 files:
#    test_bosch.arxml 
#    test_stla.arxml
# Then output: updated_bosch.arxml
# Update: this test code has been modified into OOP in class EcucPartitionParser

from lxml import etree
import os
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

def main():
    path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/update_ecuc_partition/test_structure/STLA_ws/test_ws_1"
    bosch_arxml_file= os.path.join(path, 'test_bosch.arxml')    
    stla_arxml_file=os.path.join(path,'test_stla.arxml')
    updated_bosch_file = os.path.join(path,'updated_bosch.arxml')

    tree = etree.parse(bosch_arxml_file)
    tree2 = etree.parse(stla_arxml_file)

    containers = tree.findall('.//ns:CONTAINERS', namespaces=namespace)
    bosch_ecuc_containers = containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)

    stla_containers = tree2.findall('.//ns:CONTAINERS', namespaces=namespace)
    stla_ecuc_containers = stla_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
    # stupid donkey --> Use sub_containers = tree.findall then ecuc_container = sub_containers.findall
    # then you can create a def to check whether stla_def_ref.text == or not
    
    # parent: SUB-CONTAINERS -> ECUC-CONTAINER-VALUE -> SHORT-NAME[0] = DEFINITION-REF[1] = PARAMETER-VALUES[2] = REFERENCE-VALUES[3]
    # Locate REFERENCE-VALUES in ECUC-CONTAINER-VALUE, mostly for STLA files
    for stla_ecuc_container in stla_ecuc_containers:
        stla_def_ref = stla_ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        if stla_def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            ref_values = stla_ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace) 
            print(ref_values)

    # Locate PARAMETER-VALUES in ECUC-CONTAINER-VALUE, mostly for Bosch files
    for bosch_ecuc_container in bosch_ecuc_containers:            
        def_ref = bosch_ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        param_values = bosch_ecuc_container.find('.//ns:PARAMETER-VALUES', namespaces=namespace)
        print(param_values)

        if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            pos = param_values.getparent().index(param_values) + 1 
            print(pos)
            param_values.getparent().insert(pos, ref_values)
            
    tree.write(updated_bosch_file, encoding='utf-8', xml_declaration=True)

if __name__== "__main__":
    main()
