from lxml import etree

tree = etree.parse('test_instance_reference.xml')
root = tree.getroot()

ecuc_instance_ref_values = root.findall('ECUC-INSTANCE-REFERENCE-VALUE')    #--> list [ECUC-INSTANCE-REFERENCE-VALUE]
print(ecuc_instance_ref_values)

# Define a function to extract the final component from TARGET-REF
def final_component(element):
    # element__is__ECUC-INSTANCE-REFERENCE-VALUE
    target_ref = element.find("VALUE-IREF/TARGET-REF")
    #print(target_ref.attrib)    #--> {'DEST': 'SW-COMPONENT-PROTOTYPE'}
    return target_ref.text.split("/")[-1]

sorted_ecuc_ins_ref_values = sorted(ecuc_instance_ref_values, key = final_component)


for ecuc_instance_ref_value in ecuc_instance_ref_values:
    ecuc_instance_ref_value.getparent().remove(ecuc_instance_ref_value)

for sorted_ecuc_ins_ref_value in sorted_ecuc_ins_ref_values:
    root.append(sorted_ecuc_ins_ref_value)

tree.write('sorted_file.arxml', encoding='utf-8', xml_declaration=True)
    