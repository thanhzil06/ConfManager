# OPTION-1: Use ElementTree     --> SORTED CORRECTLY BUT WITH ns0 AND CHANGED IN STRUCTURE

import xml.etree.ElementTree as ET

# Load the XML file
#tree = ET.parse('test_file.arxml')
tree = ET.parse('test_ecuc_container.arxml')
root = tree.getroot()
# root: <Element '{http://autosar.org/schema/r4.0}AUTOSAR' at 0x00000233E22ED030>

# Define the namespace
namespace = "{http://autosar.org/schema/r4.0}"

# Get all ECUC-CONTAINER-VALUE elements
container_value = root.findall('.//{0}ECUC-CONTAINER-VALUE'.format(namespace))
# Use findall method from the root element of an XML tree structure 
#   to search for all elements with the tag name 'ECUC-CONTAINER-VALUE'. 
# The .// prefix in the XPath expression means to search recursively through all descendants of the root element.
# --> return a list of all elements in the XML tree that have the tag name 'ECUC-CONTAINER-VALUE', regardless of their depth in the hierarchy.


# Sort the ECUC-CONTAINER-VALUE elements based on their SHORT-NAME
container_value.sort(key=lambda x: x.find('{0}SHORT-NAME'.format(namespace)).text)

# Reorder the ECUC-CONTAINER-VALUE elements in the XML tree
for index, container_value in enumerate(container_value):
    #root.remove(container_value)
    root.insert(index, container_value)

sorted_tree = ET.ElementTree(root)
sorted_tree.write('sorted_file.arxml', encoding='UTF-8', xml_declaration=True)