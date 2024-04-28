# Test for EcucPartitionParser class desgin - DONE
from lxml import etree
import os
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionParser:
    
    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.ecuc_container_iden = {}


    def locate_ecuc_partition(self):        
        tree =  etree.parse(self.arxml_file)
        containers_rb = tree.findall('.//ns:CONTAINERS', namespaces=namespace)
        ecuc_containers_rb = containers_rb[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)

        i=0
        for ecuc_container in ecuc_containers_rb:            
            def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
            if def_ref is not None:
                if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
                    i = i+1
                    short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                    self.ecuc_container_iden[i] = short_name.text    
        return self.ecuc_container_iden

def main():
    path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/update_ecuc_partition/test_structure/STLA_ws"
    bosch_arxml_file= os.path.join(path, 'test_conf_ecucpartition_ecucvalues.arxml')    
    stla_arxml_file=os.path.join(path,'test_RTEConfGen_EcucPartition_EcucValues.arxml')

    bosch_parser = EcucPartitionParser(arxml_file=bosch_arxml_file)
    #print(bosch_parser.locate_ecuc_partition())
    #bosch_map = bosch_parser.locate_ecuc_container() # dict

    stla_parser = EcucPartitionParser(arxml_file=stla_arxml_file)
    #print(stla_parser.locate_ecuc_partition())
    #stla_map = stla_parser.locate_ecuc_container() # dict

if __name__== "__main__":
    main()


    # OLD def locate_ecuc_container() in class EcucPartitionParser
    # Get a numbered list of ecuc_container of a tree
    # def locate_ecuc_container(self):
    #     count=0
    #     for ecuc_container in self.ecuc_containers:            
    #         if self.check_condition(ecuc_container):
    #             count = count+1        
    #             short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
    #             self.ecuc_container_id[count] = short_name.text                  
    #     return self.ecuc_container_id    # same as hashmap