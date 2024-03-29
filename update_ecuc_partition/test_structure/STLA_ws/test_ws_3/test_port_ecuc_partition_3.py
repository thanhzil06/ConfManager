# This file use ecuc_partition_parser_v1.py as library
from ecuc_partition_handling.ecuc_partition_parser_v1 import EcucPartitionParser
import os
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

def add_ecuc_ref(bosch_parser, stla_parser):
    bosch_ecuc_containers = bosch_parser.get_ecuc_containers()     
    stla_ecuc_containers = stla_parser.get_ecuc_containers()

    for stla_ecuc_container in stla_ecuc_containers:
        ref_values = stla_ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace) 
        print('OK1')
    for bosch_ecuc_container in bosch_ecuc_containers:            
        def_ref = bosch_ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        param_values = bosch_ecuc_container.find('.//ns:PARAMETER-VALUES', namespaces=namespace)

        if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            pos = param_values.getparent().index(param_values) + 1
            param_values.getparent().insert(pos, ref_values)
            print('OK2')
    #tree.write('updated_bosch.arxml', encoding='utf-8', xml_declaration=True)
            


def main():

# STLA and Bosch arxml files which then are implemented
    path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/update_ecuc_partition/test_structure/STLA_ws/test_ws_2"
    #bosch_arxml_file= os.path.join(path, 'test_conf_ecucpartition_ecucvalues.arxml')    
    #stla_arxml_file=os.path.join(path,'test_RTEConfGen_EcucPartition_EcucValues.arxml')
    bosch_arxml_file= os.path.join(path, 'test_bosch_2.arxml')    
    stla_arxml_file=os.path.join(path,'test_stla_2.arxml')
    updated_bosch_file = os.path.join(path, 'updated_bosch_2.arxml')
#----------------------------------------------------------------------------------------------------------------------
    bosch_ecuc_parser = EcucPartitionParser(bosch_arxml_file)
    stla_ecuc_parser = EcucPartitionParser(stla_arxml_file)
    # parent: SUB-CONTAINERS -> ECUC-CONTAINER-VALUE -> SHORT-NAME[0] = DEFINITION-REF[1] = PARAMETER-VALUES[2] = REFERENCE-VALUES[3]

    # Get STLA ref tag and add to Bosch, after param tag - OK
    stla_ref_values = stla_ecuc_parser.get_instance_ref()
    bosch_ecuc_parser.add_references(ref_values=stla_ref_values)
#----------------------------------------------------------------------------------------------------------------------
    # Add new container from STLA to Bosch
    bosch_hashmap = bosch_ecuc_parser.map_ecuc_ref() # dict
    stla_hashmap = stla_ecuc_parser.map_ecuc_ref() # dict

    bosch_ecuc_containers_set = set(bosch_hashmap.values())    
    stla_ecuc_containers_set = set(stla_hashmap.values())
    
    bosch_ecuc_containers_set = bosch_ecuc_containers_set.union(stla_ecuc_containers_set)  # set
    add_new_ecuc_containers = []

    for value in bosch_ecuc_containers_set:
        if value in bosch_hashmap.values():            
            print("\n{} Container is in both".format(value))

        else:
            print("\n{} Container is not in Bosch arxml".format(value))
            add_new_ecuc_containers.append(value)
    
    print('-------------------------------------------')
    print(bosch_hashmap)
    print(stla_hashmap)
    print(f'new_ecuc_container needs to be added: {add_new_ecuc_containers}')
    print('-------------------------------------------')


    bosch_container = bosch_ecuc_parser.ecuc_containers
    for new_ecuc_container in add_new_ecuc_containers:
        print(f'new_ecuc_container: {new_ecuc_container}')
        added_container = stla_ecuc_parser.get_ecuc_container(new_ecuc_container)
        
        pos = len(bosch_hashmap) + 1
        print(f'pos: {pos} and len {len(bosch_hashmap)}')
        print(bosch_hashmap)
        bosch_container.insert(pos, added_container)
#----------------------------------------------------------------------------------------------------------------------
        



    # New arxml based on Bosch after all updates
    bosch_ecuc_parser.update_new_arxml(updated_bosch_file=updated_bosch_file)


if __name__== "__main__":
    main()
