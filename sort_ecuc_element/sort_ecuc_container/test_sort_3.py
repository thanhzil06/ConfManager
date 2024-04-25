# OPTION-3: Use lxml        --> SORTED CORRECTLY
# Idea: xml file -> parsed into tree -> root -> elements
from lxml import etree

# Load the XML file
tree = etree.parse('test_ecuc_container.arxml')
root = tree.getroot()   # -->AUTOSAR

# Define the namespace
namespace = "{http://autosar.org/schema/r4.0}"

# Get all ECUC-MODULE-CONFIGURATION-VALUES elements
# As structure of needed modified elements:
#<ECUC-CONTAINER-VALUE>
#   <SUB-CONTAINERS>
#       <ECUC-CONTAINER-VALUE>
#           <SHORT-NAME>

# root.findall finds only elements with a tag which are direct children of the current element
sub_containers = root.findall('.//{0}SUB-CONTAINERS'.format(namespace))     

# Iterate through each SUB-CONTAINERS element
for sub_container in sub_containers:
    # Get all ECUC-CONTAINER-VALUE elements under the current SUB-CONTAINERS
    #   .//         : at the beginning of the XPath indicates that the search should be performed anywhere in the subtree of ECUC-CONTAINER-VALUE
    ecuc_container_values = sub_container.findall('.//{0}ECUC-CONTAINER-VALUE'.format(namespace))

    # Sort the ECUC-CONTAINER-VALUE elements based on their SHORT-NAME
    #   def sorted(Iterable[_T@sorted], key=)
    #   .text       : retrieves the text content of the {namespace}SHORT-NAME element    
    sorted_ecuc_container_values = sorted(ecuc_container_values, key=lambda x: x.find('{0}SHORT-NAME'.format(namespace)).text)

    # Remove all existing ECUC-CONTAINER-VALUE elements from the XML tree
    for container_value in ecuc_container_values:
        # Use sub_container or container_value.getparent() because:   
        #   --> All 7 ECUC-CONTAINER-VALUE elements have same parent: SUB-CONTAINERS
        sub_container.remove(container_value)

    # Append the sorted ECUC-CONTAINER-VALUE elements to the XML tree
    for sorted_container_value in sorted_ecuc_container_values:
        sub_container.append(sorted_container_value)

# Write the modified XML to a new file
tree.write('sorted_file.arxml', encoding='utf-8', xml_declaration=True)