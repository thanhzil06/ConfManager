# Test script for updating ECUC_Partition from STLA to Bosch: Get STLA ref tag and add to Bosch, after param tag with corresponding short-name
# Write all in one main. Not use OOP
# Use 2 files:
#    test_bosch_2.arxml 
#    test_stla_2.arxml
# Then output: updated_bosch_2.arxml
# Update: NOT YET this test code be modified into OOP in class EcucPartitionParser
from lxml import etree
import os
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

def main():
    path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/update_ecuc_partition/test_structure/STLA_ws/test_ws_2"
    bosch_arxml_file= os.path.join(path, 'test_bosch_2.arxml')    
    stla_arxml_file=os.path.join(path,'test_stla_2.arxml')
    updated_bosch_file = os.path.join(path,'updated_bosch_2.arxml')

    tree1 = etree.parse(bosch_arxml_file)
    tree2 = etree.parse(stla_arxml_file)
    bosch_sub_containers = tree1.findall('.//ns:SUB-CONTAINERS', namespaces=namespace)
    stla_sub_containers = tree2.findall('.//ns:SUB-CONTAINERS', namespaces=namespace)
    bosch_ecuc_containers =  bosch_sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
    stla_ecuc_containers = stla_sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)


    bosch_list_of_container = {}
    for cont in stla_ecuc_containers:
        short_name = cont.find('.//ns:SHORT-NAME', namespaces=namespace)
        key = short_name.text
        ref_values = cont.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
        bosch_list_of_container[key] = ref_values
    print(bosch_list_of_container) 

    for contt in bosch_ecuc_containers:
        short_name = contt.find('.//ns:SHORT-NAME', namespaces=namespace)
        pointer = short_name.text
        param_values = contt.find('.//ns:PARAMETER-VALUES', namespaces=namespace)
        if pointer in bosch_list_of_container:
            # print(param_values.getparent().index(param_values))
            # pos = param_values.getparent().index(param_values) + 1
            # param_values.insert(pos, bosch_list_of_container[pointer])
            contt.append(bosch_list_of_container[pointer])


    tree1.write(updated_bosch_file, encoding='utf-8', xml_declaration=True)

if __name__== "__main__":
    main()
