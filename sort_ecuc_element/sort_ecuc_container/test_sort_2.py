# OPTION-2: Use lxml        --> SORTED CORRECTLY BUT root tag in WRONG PLACE
#-------------------------- NOT NEED TO UNDERSTAND --------------------------
# Reason: not indicate the right parent of need-to-sort elements
# As structure of needed modified elements:
#<ECUC-CONTAINER-VALUE>
#   <SUB-CONTAINERS>
#       <ECUC-CONTAINER-VALUE>
#           <SHORT-NAME>
# Idea: xml file -> parsed into tree -> root -> elements
from lxml import etree

# Load the XML file
tree = etree.parse('test_ecuc_container.arxml')
root = tree.getroot()   # -->AUTOSAR

# Define the namespace
namespace = "{http://autosar.org/schema/r4.0}"

# Get all ECUC-CONTAINER-VALUE elements --> return a list [] of all ECUC-CONTAINER-VALUE elements
ecuc_container_values = root.findall('.//{0}ECUC-CONTAINER-VALUE'.format(namespace))

# Sort the ECUC-CONTAINER-VALUE elements based on their SHORT-NAME
    #   def sorted(Iterable[_T@sorted], key=)
    #   .text       : retrieves the text content of the {namespace}SHORT-NAME element
ecuc_container_values.sort(key=lambda x: x.find('{0}SHORT-NAME'.format(namespace)).text)


# Create a new XML tree with the sorted elements
sorted_root = etree.Element(root.tag, nsmap=root.nsmap)
# etree.Element: creates a new Element object
# root.tag: retrieves the tag name of the root element (AUTOSAR) of the original XML tree root
# nsmap=root.nsmap: This sets the namespace map of the new element 
#   to be the same as the namespace map of the root element of the original XML tree

for container_value in ecuc_container_values:
    sorted_root.append(container_value)

# Write the sorted XML to a new file
sorted_tree = etree.ElementTree(sorted_root)    #  Library/xml/etree/ElementTree.py
sorted_tree.write('sorted_file.arxml', encoding='utf-8', xml_declaration=True)