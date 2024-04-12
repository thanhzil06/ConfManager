import boschlibparserarxmlutils.autosar_lib_4_3_0 as autosarlib 
import constants as csts
from lxml import etree
import re
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionUpdater:    
    ECUC_PARTITON_DEF = '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition'

    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.tree = etree.parse(self.arxml_file)
        self.sub_containers = self.tree.find('.//ns:SUB-CONTAINERS', namespaces=namespace)
        self.ecuc_containers = self.get_ecuc_container(sub_container=self.sub_containers)
        self.container_ref_id = {}
    
    @staticmethod
    def get_ecuc_container(sub_container):
        ecuc_containers = sub_container.findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
        return ecuc_containers
    
    @staticmethod
    def check_condition(ecuc_container):
        # Only the elements <ECUC-CONTAINER-VALUE>, which contain children element         
        # <DEFINITION-REF> having the content: /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition is applicable
        def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)        
        if def_ref.text == EcucPartitionUpdater.ECUC_PARTITON_DEF:
            return True
        return False
    
    @staticmethod
    def get_short_name(ecuc_container):
        name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
        return name
    
    @staticmethod
    def get_reference(ecuc_container):
        ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
        return ref_values
        
    @staticmethod
    def get_iref(ref_values):
        ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
        return ecuc_iref
    
    @staticmethod
    def get_target_name(instance_ref):
        target_ref = instance_ref.find('.//ns:TARGET-REF', namespaces=namespace)
        target_name = target_ref.text.split('/')[-1]
        return target_name

    
    def map_ecuc_ref(self):
    # Create a hashmap with {key-value} pair is {SHORT_NAME - REFERENCE_VALUES} within an ECUC-CONTAINER
        for ecuc_container in self.ecuc_containers:            
            if self.check_condition(ecuc_container):       
                short_name = self.get_short_name(ecuc_container=ecuc_container)
                key = short_name.text
                
                ref_values = self.get_reference(ecuc_container=ecuc_container)                
                self.container_ref_id[key] = ref_values    
        return self.container_ref_id     
                
    def update_ecuc_iref(self, container_ref_id):        
    # Update delta changes from OEM to base file: Add the new INSTANCE-REFERENCE values into each ECUC-CONTAINER        
        for ecuc_container in self.ecuc_containers:
            if not self.check_condition(ecuc_container):    
                continue

            short_name = self.get_short_name(ecuc_container=ecuc_container)
            pointer = short_name.text                   
            ref_values = self.get_reference(ecuc_container=ecuc_container)                
            
            # If ecuc-container of the base has no reference values
            if ref_values is None: 
                ecuc_container.append(container_ref_id[pointer])
        
            else:                             
                self.get_delta(ecuc_container=ecuc_container,
                                ref_id= container_ref_id,
                                pointer=pointer,
                                ref=ref_values)               
                    
        self.sort_ecuc_container(ecuc_containers = self.ecuc_containers, sub_containers = self.sub_containers)

    def get_delta(self, ecuc_container, ref_id, pointer, ref):
        # Within an ECUC-CONTAINER, remove reference values of the base
        base_irefs = self.get_iref(ref_values=ref) 
        ecuc_container.remove(ref)
        
        # And replace with the new ones from OEM, which includes ref of base
        ecuc_container.append(ref_id[pointer])
        new_ref_values = self.get_reference(ecuc_container=ecuc_container)    

        # Add instance references of the base into delta references value
        for iref in base_irefs: 
            new_ref_values.append(iref)          

    def check_duplicate_iref(self):
        '''
        After updating delta changes from OEM to base file, check in each ECUC-CONTAINER-VALUE tag
            whether ECUC-INSTANCE-REFERENCE is duplicated.
        '''
        for ecuc_container in self.ecuc_containers:
            if not self.check_condition(ecuc_container):
                continue

            ref_values = self.get_reference(ecuc_container=ecuc_container)
            iref_name = []
            double_iref = []            
            self.remove_duplicate(reference=ref_values,
                                  single=iref_name,
                                  duplicate=double_iref)

    def remove_duplicate(self, reference, single, duplicate):
        # Look for duplicated ECUC-INSTANCE-REFERENCE based on their TARGET-REF
        for iref in reference:
            target_name = self.get_target_name(instance_ref=iref)                                                          
            if target_name not in single:                        
                single.append(target_name)
            else:
                duplicate.append(target_name)

        # If there are duplicated elements, remove them        
        for iref in reference:
            target_name = self.get_target_name(instance_ref=iref)
            if target_name in duplicate:
                reference.remove(iref)
                
    def sort_ecuc_instance_ref(self, ecuc_container_value):             
        ref_values = self.get_reference(ecuc_container=ecuc_container_value)        
        ecuc_irefs = self.get_iref(ref_values=ref_values)        

        # Sort the ECUC-INSTANCE-REFERENCE-VALUE elements based on their TARGET-REF value
        sorted_ecuc_irefs = sorted(ecuc_irefs, key=lambda x: x.find('ns:VALUE-IREF/ns:TARGET-REF', namespaces=namespace).text)

        # Remove all ECUC-INSTANCE-REFERENCE elements within the REFERENCE-VALUES tags which are not in alphabet order
        for ecuc_iref in ecuc_irefs:
            ref_values.remove(ecuc_iref)

        # Add SORTED ECUC-INSTANCE-REFERENCE elements in their parent tag
        for sorted_ecuc_iref in sorted_ecuc_irefs:
            ref_values.append(sorted_ecuc_iref) 

    def sort_ecuc_container(self, ecuc_containers, sub_containers):
        # Sort the ECUC-CONTAINER-VALUE elements based on their SHORT-NAME
        sorted_ecuc_containers = sorted(ecuc_containers, key=lambda x: x.find('ns:SHORT-NAME', namespaces=namespace).text)  

        # Remove all ECUC-CONTAINER elements which are not in alphabet order and replace with sorted ones
        for container in ecuc_containers:
            sub_containers.remove(container)
        for sorted_container in sorted_ecuc_containers:            
            sub_containers.append(sorted_container) 

        # Sort ECUC-INSTANCE-REFERENCE in each ECUC-CONTAINER-VALUE          
        new_ecuc_containers = self.get_ecuc_container(sub_container=sub_containers)     
        for new_ecuc_container in new_ecuc_containers:
            self.sort_ecuc_instance_ref(new_ecuc_container)               

    def update_ecucpartition_file(self, updated_output_file):
        # This inherits from class CommonModeUtils in confmanager_modes_common
        xml_root = autosarlib.parse(updated_output_file, silence=True)

        with (open(updated_output_file, 'w') as merged_file):
            merged_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            merged_root_lxml = xml_root.to_etree(None, name_="AUTOSAR", mapping_={}, nsmap_= csts.nsmap1)
            merged_xml_string = etree.tostring(merged_root_lxml, pretty_print=True, encoding='utf-8', method="xml"
                                               ).decode('utf-8')
            merged_xml_string = self.postproc_replace_values_in_merged_xml(merged_xml_string,
                                                                           csts.postprocessing_replacements)
            merged_file.write(merged_xml_string)

        merged_file.close()
        #self.tree.write(updated_output_file, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def postproc_replace_values_in_merged_xml(xml_string, values_to_replace_list):
        # This inherits from class CommonModeUtils in confmanager_modes_common
        new_xml_string = xml_string
        for value_to_replace in values_to_replace_list:
            new_xml_string = re.sub(value_to_replace[0], value_to_replace[1], new_xml_string)

        return new_xml_string