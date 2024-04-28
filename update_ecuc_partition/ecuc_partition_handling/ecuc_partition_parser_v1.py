from lxml import etree
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionParser:
    
    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.tree =  etree.parse(self.arxml_file)
        self.sub_containers = self.tree.findall('.//ns:SUB-CONTAINERS', namespaces=namespace)
        self.ecuc_containers = self.sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
        
        self.ref_values = None
        self.ecuc_container_id = {}
        self.ecuc_iref_id = {}

    def check_condition(self, ecuc_container):
        # Only the elements <ECUC-CONTAINER-VALUE>, which contain children element <DEFINITION-REF> having the content:
        # /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition is applicable
        def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            return 1
        else:
            return 0      
        
    # Create a hashmap with key-value pair is SHORT_NAME - REFERENCE_VALUES within an ECUC-CONTAINER-VALUE element of the EcucPartition
    def map_ecuc_ref(self):
        for ecuc_container in self.ecuc_containers:            
            if self.check_condition(ecuc_container):       
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                key = short_name.text
                param_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                self.ecuc_container_id[key] = ref_values                  
        return self.ecuc_container_id    # same as hashmap
    
    # Add REFERENCE-VALUES element right after the PARAMETER-VALUES one
    def add_ref_values(self, ecuc_container_id):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                pointer = short_name.text  
                if pointer in ecuc_container_id:
                    ecuc_container.append(ecuc_container_id[pointer])


    # Get content of an <ECUC-CONTAINER-VALUE> tag which has a specific short-name
    def get_ecuc_container(self, name):
        for ecuc_container in self.ecuc_containers:            
            if self.check_condition(ecuc_container):
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)   
                if short_name.text == name:                   
                    return ecuc_container    

    # Get reference values within a container, use for stla tree
    def get_instance_ref(self):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container): 
                self.ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                return self.ref_values                
    
    # Add reference-values tag contents after parameter tag within a container, use for bosch tree
    def add_references(self, ref_values):                        
        for ecuc_container in self.ecuc_containers:            
            param_values = ecuc_container.find('.//ns:PARAMETER-VALUES', namespaces=namespace)
            if self.check_condition(ecuc_container):   
                # parent: SUB-CONTAINERS -> ECUC-CONTAINER-VALUE -> SHORT-NAME[0] = DEFINITION-REF[1] = PARAMETER-VALUES[2] = REFERENCE-VALUES[3]
                pos = param_values.getparent().index(param_values) + 1
                param_values.getparent().insert(pos, ref_values)

                



    
#--------------------------------------------------------------------------------------------------------------------------    

                # ecuc_iref_values = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)

                # for ecuc_iref_value in ecuc_iref_values:
                #     target_ref = ecuc_iref_value.find('.//ns:TARGET-REF', namespaces=namespace)
                #     print(target_ref)
                #     if target_ref is not None:
                #         ref_text = target_ref.text.split('/')[-1]
                #         #print(ref)
                #         #if not isinstance(self.ecuc_iref_id[i]., list):
                #         #     self.ecuc_iref_id[i] = ref
        #return self.ecuc_iref_id
#--------------------------------------------------------------------------------------------------------------------------    
    def update_new_arxml(self, updated_bosch_file):
        self.tree.write(updated_bosch_file, encoding='utf-8', xml_declaration=True)
