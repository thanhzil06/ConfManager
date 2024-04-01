import boschlibparserarxmlutils.autosar_lib_4_3_0 as autosarlib 
namespace = {'ns' : 'http://autosar.org/schema/r4.0'}

class EcucPartitionUpdater:    
    ECUC_PARTITON_DEF = '/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition'

    def __init__(self, arxml_file) -> None:
        self.arxml_file = arxml_file
        self.tree = autosarlib.parse(self.arxml_file)
        self.sub_containers = self.tree.find('.//ns:SUB-CONTAINERS', namespaces=namespace)
        self.ecuc_containers = self.get_ecuc_container(sub_container=self.sub_containers)
        self.container_ref_id = {}
    
    def get_ecuc_container(sub_container):
        ecuc_containers = sub_container.findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
        return ecuc_containers
    
    def check_condition(ecuc_container):
        # Only the elements <ECUC-CONTAINER-VALUE>, which contain children element         
        # <DEFINITION-REF> having the content: /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition is applicable
        def_ref = ecuc_container.find('.//ns:DEFINITION-REF', namespaces=namespace)        
        if def_ref.text == EcucPartitionUpdater.ECUC_PARTITON_DEF:
            return 1
        return 0  
    
    def get_short_name(ecuc_container):
        name = ecuc_container.find('.//ns:SHORT-NAME', namespaces=namespace)
        return name
    
    def get_reference(ecuc_container):
        ref_values = ecuc_container.find('.//ns:REFERENCE-VALUES', namespaces=namespace)
        return ref_values
        
    def get_iref(ref_values):
        ecuc_iref = ref_values.findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
        return ecuc_iref


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
            if self.check_condition(ecuc_container):    
                short_name = self.get_short_name(ecuc_container=ecuc_container)
                pointer = short_name.text                   
                ref_values = self.get_reference(ecuc_container=ecuc_container)                
                
                # If ecuc-container already has reference values
                if ref_values is None: 
                    ecuc_container.append(container_ref_id[pointer])
                
                # If not, remove old reference values and replace them with the new ones
                else:                             
                    ecuc_irefs = self.get_iref(ref_values=ref_values) 
                    ecuc_container.remove(ref_values)
                    ecuc_container.append(container_ref_id[pointer])
                    new_ref_values = self.get_reference(ecuc_container=ecuc_container)                
                    # Then add new instance references into references
                    for iref in ecuc_irefs: 
                        new_ref_values.append(iref)                  
        self.sort_ecuc_container(ecuc_containers = self.ecuc_containers, sub_containers = self.sub_containers)

    def check_duplicate_iref(self):
        '''
        After updating delta changes from OEM to base file, check in each ECUC-CONTAINER-VALUE tag
            whether ECUC-INSTANCE-REFERENCE is duplicated.
        '''
        for ecuc_container in self.ecuc_containers:
            if self.check_condition(ecuc_container):
                ref_values = self.get_reference(ecuc_container=ecuc_container)
                double_iref_text = []
                iref_text = []
                
                # Look for duplicated ECUC-INSTANCE-REFERENCE base on their TARGET-REF
                for iref in ref_values:
                    target_ref = iref.find('.//ns:TARGET-REF', namespaces=namespace)
                    ref_text = target_ref.text.split('/')[-1]                    
                    if ref_text not in iref_text:                        
                        iref_text.append(ref_text)
                    else:
                        double_iref_text.append(ref_text)

                # If there are duplicated elements, remove them
                for iref in ref_values:
                    target_ref1 = iref.find('.//ns:TARGET-REF', namespaces=namespace)
                    ref_text1 = target_ref1.text.split('/')[-1]  
                    if ref_text1 in double_iref_text:
                        ref_values.remove(iref)
                
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

    def update_new_ecucpartition_arxml(self, updated_bosch_file):
        self.tree.write(updated_bosch_file, encoding="utf-8", xml_declaration=True)