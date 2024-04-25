=========================Requirement based on ECPT-11911. In this folder=========================

- sort_learn.py: learn about etree and xml handling in Python

- test_ecuc_instance_ref.arxml: test arxml file, copied and modified from C:\Users\GYH8HC\dev_tool\03_ConfManager_ECUC_Partition\02_test_ws\confmanager\src\tests\test_files\STLA_ws\RB_RteArch\Others\conf_ecucpartition_ecucvalues.arxml

- xml_tree.txt: file contains what etree.parse() do to xml-structured file


--|folder sort_ecuc_container
	|test_sort_[1,2,3].py		: test scripts to sort ECUC-CONTAINER-VALUE element and modify arxml file in alphabet order
	|test_ecuc_container.arxml	: test arxml file, copied and modified from C:\Users\GYH8HC\dev_tool\03_ConfManager_ECUC_Partition\02_test_ws\confmanager\src\tests\test_files\STLA_ws\RB_RteArch\EcuPartition\conf_ecucpartition_ecucvalues_merged.arxml
	|sorted_file.arxml		: result file


--|folder sort_ecuc_instance_reference
	|test_sort_4.py			: test script to sort the ECUC-INSTANCE-REFERENCE-VALUE element and modify xml file in alphabet order
	|test_sort_4_1.py		: test script to sort the ECUC-INSTANCE-REFERENCE-VALUE element and modify ARXML file in alphabet order
	|test_instance_reference.xml	: self-created xml which stimulates a small part of structure of the real conf_ecucpartition_ecucvalues.arxml TO TEST SORTING ACTION
	|test_instance_reference_2.xml	: same above but is an ARXML
	|sorted_file.arxml		: result file


- test_sort_5.py			: final test script to sort both ECUC-CONTAINER-VALUE and ECUC-INSTANCE-REFERENCE-VALUE elements
- sort_element.py			: final script to implement the requirement
- sorted_file.arxml			: final output file after sorted both elements (ECUC-CONTAINER-VALUE & ECUC-INSTANCE-REFERENCE-VALUE) in alphabet order