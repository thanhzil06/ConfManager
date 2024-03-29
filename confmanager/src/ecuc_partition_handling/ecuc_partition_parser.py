from lxml import etree
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionUpdater:    
    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.tree = etree.parse(self.arxml_file)
        self.sub_containers = self.tree.find('.//ns:SUB-CONTAINERS', namespaces=namespace)
        self.ecuc_containers = self.sub_containers.findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
        self.container_ref_id = {}

    def check_condition(self, ecuc_container):
        # Only the elements <ECUC-CONTAINER-VALUE>, which contain children element         
        # <DEFINITION-REF> having the content: /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition is applicable
        def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)
        if def_ref.text == '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition':
            return 1
        return 0      

    def map_ecuc_ref(self):
        for ecuc_container in self.ecuc_containers:            
            if self.check_condition(ecuc_container):       
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                key = short_name.text
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)

                self.container_ref_id[key] = ref_values                                
        return self.container_ref_id     
                
    def update_ecuc_iref(self, container_ref_id):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):    
                short_name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
                pointer = short_name.text                   
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)                
                # If ecuc-container already has reference values
                if ref_values is None: 
                    ecuc_container.append(container_ref_id[pointer])
                else:             
                    ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
                    ecuc_container.remove(ref_values)
                    ecuc_container.append(container_ref_id[pointer])
                    new_ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                    # Then add new instance references into references
                    for iref in ecuc_iref: 
                        new_ref_values.append(iref)                  
        self.sort_ecuc_container(ecuc_containers = self.ecuc_containers, sub_containers = self.sub_containers)

    def check_duplicate_iref(self):
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):
                ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
                double_iref_text = []
                iref_text = []
                for iref in ref_values:
                    target_ref = iref.find('.//ns:TARGET-REF', namespaces=namespace)
                    ref_text = target_ref.text.split('/')[-1]                    
                    if ref_text not in iref_text:
                        print(ref_text)
                        iref_text.append(ref_text)
                    else:
                        double_iref_text.append(ref_text)
                
                for iref in ref_values:
                    target_ref1 = iref.find('.//ns:TARGET-REF', namespaces=namespace)
                    ref_text1 = target_ref1.text.split('/')[-1]  
                    if ref_text1 in double_iref_text:
                        ref_values.remove(iref)
                
    def sort_ecuc_instance_ref(self, ecuc_container_value):             
        ref_values = ecuc_container_value.find('.//ns:REFERENCE-VALUES', namespaces=namespace)        
        ecuc_irefs = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)

        # Sort the ECUC-CONTAINER-VALUE elements based on their TARGET-REF value
        sorted_ecuc_irefs = sorted(ecuc_irefs, key=lambda x: x.find('ns:VALUE-IREF/ns:TARGET-REF', namespaces=namespace).text)
        for ecuc_iref in ecuc_irefs:
            ref_values.remove(ecuc_iref)
        for sorted_ecuc_iref in sorted_ecuc_irefs:
            ref_values.append(sorted_ecuc_iref) 

    def sort_ecuc_container(self, ecuc_containers, sub_containers):
        # Sort the ECUC-CONTAINER-VALUE elements based on their SHORT-NAME
        sorted_ecuc_containers = sorted(ecuc_containers, key=lambda x: x.find('ns:SHORT-NAME', namespaces=namespace).text)        
        for container in ecuc_containers:
            sub_containers.remove(container)
        for sorted_container in sorted_ecuc_containers:            
            sub_containers.append(sorted_container) 
        
        new_ecuc_containers = sub_containers.findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)        
        # Sort ECUC-INSTANCE-REFERENCE-VALUE
        for new_ecuc_container in new_ecuc_containers:
            self.sort_ecuc_instance_ref(new_ecuc_container)               

    def update_new_arxml(self, updated_bosch_file):
        self.tree.write(updated_bosch_file, encoding="utf-8", xml_declaration=True)