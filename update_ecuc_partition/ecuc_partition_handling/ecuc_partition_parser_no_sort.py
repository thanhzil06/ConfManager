from lxml import etree
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionUpdater:
    
    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.tree = etree.parse(self.arxml_file)
        self.sub_containers = self.tree.findall('.//ns:SUB-CONTAINERS', namespaces=namespace)
        self.ecuc_containers = self.sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
        self.ecuc_container_id = {}

    def check_condition(self, ecuc_container):
        # Only the elements <ECUC-CONTAINER-VALUE>, which contain children element <DEFINITION-REF> having the content:
        # /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition is applicable
        def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            return 1
        else:
            return 0      
  
    # Create a hashmap with {key-value} pair: {SHORT_NAME - REFERENCE_VALUES} within an ECUC-CONTAINER-VALUE element of the EcucPartition
    def map_ecuc_ref(self):
        for ecuc_container in self.ecuc_containers:            
            if self.check_condition(ecuc_container):       
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                key = short_name.text
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)

                self.ecuc_container_id[key] = ref_values                                
        return self.ecuc_container_id    
    
    def update_ecuc_iref(self, ecuc_container_id):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):    
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                pointer = short_name.text                   
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                
                # If ecuc-container already has reference values
                if ref_values is None: 
                    ecuc_container.append(ecuc_container_id[pointer])
                else:             
                    ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
                    ecuc_container.remove(ref_values)
                    ecuc_container.append(ecuc_container_id[pointer])
                    new_ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                    # Then add new instance references into references
                    for iref in ecuc_iref: 
                        new_ref_values.append(iref)                    

    def update_new_arxml(self, updated_bosch_file):
        self.tree.write(updated_bosch_file, encoding='utf-8', xml_declaration=True)
