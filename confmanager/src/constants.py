import re

# Autosar tags
nsmap1 = {None: "http://autosar.org/schema/r4.0",
          'xsi': "http://www.w3.org/2001/XMLSchema-instance",
          'schemaLocation': "http://autosar.org/schema/r4.0/AUTOSAR_4-3-0.xsd"}

root_main_tag = "AUTOSAR"

postprocessing_replacements = [('Type\d+', ''),
                               ('xmlns:schemaLocation', 'xsi:schemaLocation'),
                               ('r4.0/AUTOSAR', 'r4.0 AUTOSAR')]

tags_to_check = ['SHORT_NAME', 'SIGNAL_GROUP_REF', 'SYSTEM_SIGNAL_REF', 'DEFINITION_REF']

patterns_not_to_be_removed = ['AR_PACKAGE',
                              'SYSTEM',
                              'COMPOSITION_SW_COMPONENT_TYPE',
                              'FLAT_MAP',
                              'ECUC_MODULE_CONFIGURATION_VALUES',
                              ('CONTAINERS', 'ECUC_CONTAINER_VALUE'),
                              ('SUB_CONTAINERS', 'ECUC_CONTAINER_VALUE'),
                              '@xmlns',
                              '@xmlns:xsi',
                              '@xsi:schemaLocation'
                              ]

find_xml_index_compiled = re.compile(r'\[(\d+)\]')
find_dict_index_compiled = re.compile(r'_(\d+)')



