from lxml import etree
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionParser:
    
    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.tree =  etree.parse(self.arxml_file)
        self.sub_containers = self.tree.findall('.//ns:SUB-CONTAINERS', namespaces=namespace)
        self.ecuc_containers = self.sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
        self.ecuc_iref = None
        self.ecuc_container_id = {}

    def check_condition(self, ecuc_container):
        # Only the elements <ECUC-CONTAINER-VALUE>, which contain children element <DEFINITION-REF> having the content:
        # /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition is applicable
        def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            return 1
        else:
            return 0      
#----------------------------------------------------------------------------------------------------------------------------------------------    
    # Create a hashmap with key-value pair is SHORT_NAME - REFERENCE_VALUES within an ECUC-CONTAINER-VALUE element of the EcucPartition
    # stla
    def map_ecuc_ref(self):
        for ecuc_container in self.ecuc_containers:            
            if self.check_condition(ecuc_container):       
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                key = short_name.text
                param_values = ecuc_container.find('.//ns:PARAMETER-VALUES', namespaces=namespace)

                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                self.ecuc_container_id[key] = ref_values                                
        return self.ecuc_container_id    # same as hashmap
    
    # Add REFERENCE-VALUES element right after the PARAMETER-VALUES one
    # bosch
    def add_ref_values(self, ecuc_container_id):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                pointer = short_name.text  
                if pointer in ecuc_container_id:
                    ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                    self.ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
                    ecuc_container.append(ecuc_container_id[pointer])
    # Add ECUC-INSTANCE-REFERENCE-VALUE into its parent - REFERENCE-VALUES
    # bosch
    def add_ecuc_iref(self, new_iref):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)            
                if ref_values is not None:
                    # Then add new_iref of stla
                    for iref in new_iref:
                        ref_values.append(iref)
    # Bosch
    def update_ecuc_iref(self, ecuc_container_id):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):    
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                pointer = short_name.text 
                param_values = ecuc_container.find('.//ns:PARAMETER-VALUES', namespaces=namespace)                   
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)

                if ref_values is None: # If container already has reference values
                    ecuc_container.append(ecuc_container_id[pointer])
                else:             
                    ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
                    print(ecuc_iref)
                    # pos = ecuc_container.index(ref_values)
                    # print(pos)
                    #ecuc_container.insert(pos, ecuc_container_id[pointer])
                    ecuc_container.remove(ref_values)
                    ecuc_container.append(ecuc_container_id[pointer])
                    print(ecuc_iref)

                    new_ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                    #new_ref_values.append(ecuc_iref)
                    # new_ecuc_iref = new_ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
                    for iref in ecuc_iref: # Then add new_iref into reference
                        new_ref_values.append(iref)                    
                    


                # if pointer in ecuc_container_id:  
                #     if pos != 0:                     
                #         ecuc_container.insert(pos, ecuc_container_id[pointer])  
                #     else:
                #         ecuc_container.append(ecuc_container_id[pointer])                        
                #     if ref_values is not None:
                #         ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                #         ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
                #         for iref in ecuc_iref: # Then add new_iref into reference
                #             ref_values.append(iref)


    # Get ECUC-INSTANCE-REFERENCE-VALUE
    # stla                
    def get_ecuc_iref(self):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                self.ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
        return self.ecuc_iref
    
    def check_referene(self, ecuc_container, ref_values):
        if self.check_condition(ecuc_container):         
            if ref_values is not None:
                return 1
            else:
                return 0
        
#----------------------------------------------------------------------------------------------------------------------------------------------     
    def update_new_arxml(self, updated_bosch_file):
        self.tree.write(updated_bosch_file, encoding='utf-8', xml_declaration=True)
