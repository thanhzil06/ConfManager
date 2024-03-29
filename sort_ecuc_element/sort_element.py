# Idea: xml file -> parsed into tree -> root -> elements
from lxml import etree

tree = etree.parse('test_ecuc_instance_ref.arxml')
namespace = {'ns': 'http://autosar.org/schema/r4.0'}

# Structure of conf-ecucpartition-ecucvalues ARXML
#<ECUC-CONTAINER-VALUE>
#   <SUB-CONTAINERS>
#       <ECUC-CONTAINER-VALUE>
#           <SHORT-NAME>
#           <REFERENCE-VALUES>
#               <ECUC-INSTANCE-REFERENCE-VALUE>
#                   <VALUE-IREF>
#                       <TARGET-REF>

def sort_ecuc_container():
    sub_containers = tree.xpath('.//ns:SUB-CONTAINERS', namespaces=namespace) 
    # Get all ECUC-CONTAINER-VALUE elements within the SUB-CONTAINERS
    ecuc_container_values = sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
    # Sort the ECUC-CONTAINER-VALUE elements based on their SHORT-NAME
    sorted_ecuc_container_values = sorted(ecuc_container_values, key=lambda x: x.find('ns:SHORT-NAME', namespaces=namespace).text)

    for container_value in ecuc_container_values:
        sub_containers[0].remove(container_value)
    for sorted_container_value in sorted_ecuc_container_values:
        sub_containers[0].append(sorted_container_value) 

    new_ecuc_container_values = sub_containers[0].findall('.//ns:ECUC-CONTAINER-VALUE', namespaces=namespace)
    for new_container_value in new_ecuc_container_values:
        sort_ecuc_instance_ref(new_container_value)  

def sort_ecuc_instance_ref(ecuc_container_value):
    reference_values = ecuc_container_value.findall('.//ns:REFERENCE-VALUES', namespaces=namespace)
    # Get all ECUC-INSTANCE-REFERENCE-VALUE elements within the REFERENCE-VALUES
    ecuc_iref_values = reference_values[0].findall('.//ns:ECUC-INSTANCE-REFERENCE-VALUE', namespaces=namespace)
    # Sort the ECUC-CONTAINER-VALUE elements based on their TARGET-REF value
    sorted_ecuc_iref_values = sorted(ecuc_iref_values, key=lambda x: x.find('ns:VALUE-IREF/ns:TARGET-REF', namespaces=namespace).text)

    for ecuc_iref_value in ecuc_iref_values:
        reference_values[0].remove(ecuc_iref_value)
    for sorted_ecuc_iref_value in sorted_ecuc_iref_values:
        reference_values[0].append(sorted_ecuc_iref_value)

sort_ecuc_container()
tree.write('sorted_file.arxml', encoding='utf-8', xml_declaration=True)