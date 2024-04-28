----------------------------------------------- REQUIREMENTS: For EcuCPartition configuration... -----------------------------------------------
#012	Locate  in input files, which are Bosch ARXL files and STLA ARXL files, 
the information of EcucInstanceReferenceValue and EcuCPartition to identify the new content which then can be merged into output ARXML file (based on Bosch CI PVER file).
		-->  Nghĩa là cần xác định tất cả EcuCPartition của cả 2 phía, đồng thời xác định EcucInstanceReferenceValue phía STLA.

#014	Specifically EcuCPartition-relevant identification, locate in input files, the elements <ECUC-CONTAINER-VALUE>, 
which contain children element <DEFINITION-REF> having the content: /AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition.
--> Vì có 1 ECUC-CONTAINER-VALUE parent chứa các container con, phân biệt bởi definition EcucPartitionCollection, khác với container con - EcucPartitionCollection/EcucPartition

#015	Specifically EcuCPartition-relevant identification, use in located EcucContainerValue containers, 
the content of element <SHORT-NAME> as unique identifier for the EcuCPartition.
		
#013	Specifically EcucInstanceReferenceValue use in input files, the content of element <TARGET-REF>, 
which is within the element <ECUC-INSTANCE-REFERENCE-VALUE> as unique identifier for the element <ECUC-INSTANCE-REFERENCE-VALUE>

#016	For processing, port the newly-appearing EcuCInstanceReferenceValue detected by comparing the STLA files against Bosch exported files in input files to build the output which is based on Bosch PVER file.
--> Từ 12-16, cần phải xác định được những element RTE của STLA và add những element này vào file gốc của BOSCH.
<ECUC-CONTAINER-VALUE> -> <SHORT-NAME> -> <DEFINITION-REF> -> <PARAMETER-VALUES> -> 																	: BOSCH 
															-> <REFERENCE-VALUES> -> <ECUC-INSTANCE-REFERENCE-VALUE> -> <VALUE-IREF> -> <TARGET-REF>	: STLA
	==> File ARXML của cả Bosch và STLA đều có <ECUC-CONTAINER-VALUE>. Tuy nhiên, nội dung trong đó sẽ khác nhau.
--> Trong file arxml của STLA, component của <ECUC-CONTAINER-VALUE> chỉ có <ECUC-INSTANCE-REFERENCE-VALUE>
--> Trong file arxml của BOSCH, component của <ECUC-CONTAINER-VALUE> có <PARAMETER-VALUES> và maybe <ECUC-INSTANCE-REFERENCE-VALUE>

----------------to do---------------> List EcucContainer của cả 2 file ra và so sánh <-------------------------------  
	+) Nếu trùng tên, thì add nội dung EcucInstanceReferenceValue (parent tag: REFERENCE-VALUES) của STLA vào sau tag PARAMETER-VALUES của RB. 
		--Chỉ add những instance nào khác biệt.
	+) Nếu không trùng thì add all contents của STLA vào file Bosch arxml
	+) Sort (dùng lib đã dev ở ECPT-11911) EcucContainer trong file Bosch
==================================================== IN THIS FOLDER ====================================================
--|test_conf_ecucpartition_ecucvalues.arxml			: test file of Bosch ecucpartition which needs to get updated (developer had modified)
--|test_RTEConfGen_EcucPartition_EcucValues.arxml	: test file of Bosch which has RTE configuration	(developer had modified)	
--|updated_ecuc_partition.arxml						: output of test_main.py

--|task_ECPT-11912_infor								: information hins for ECPT-11912 development
--|original_files
	--|conf_ecucpartition_ecucvalues_merged.arxml		: a skeleton test arxml, found in confmanager\src\tests\test_files\STLA_ws\RB_RteArch\EcuPartition\
							---> output of mode Merger. Then STLA sends back this file and Bosch needs to do update this file by ConfUpdater.
							
	--|RTEConfGen_EcucPartition_EcucValues.arxml		: Input file from STLA, found in Pver\ECS1095_T4EVOTL_STLA_C040C5_RSB\_gen\swb\module\rtegen\rteconfgen\
																					or confmanager\src\tests\test_files\STLA_ws\RB_RteArch\Others\
																					
	--|conf_ecucpartition_ecucvalues.arxml				: output file after updated by ConfUpdater. Also, it's the original/based file of Bosch CI PVER before giving to STLA.
																												found in Pver\ECS1095_T4EVOTL_STLA_C040C5_RSB\Conf\__Conf\
	--|ecupartition_merged.arxml						: expected skeleton of ecupartition.arxml after merged
	--|ecupartition_updated.arxml						: expected skeleton of ecupartition.arxml after updated
--|test_structure
	--|Bosch_Pver										: contains REAL original conf_ecucpartition_ecucvalues.arxml of BOSCH CI PVER, where files to merge are present
	--|config											: JSON configuration
	--|STLA_ws											: STLA workspace		
		--|test_conf_ecucpartition_ecucvalues.arxml					: test file of Bosch ecucpartition which needs to get updated (developer had modified)
		--|test_RTEConfGen_EcucPartition_EcucValues.arxml			: test file of Bosch which has RTE configuration	(developer had modified)	
		
		--|test_ws_1	
			--|test_port_ecuc_partition_1.py
			--|test_stla.arxml			: test file of STLA. Only 1 container, used for activity of updating contents of same container from STLA to Bosch
			--|test_bosch.arxml			: test file of Bosch. Only 1 container and same as STLA, used for activity of updating contents of same container from STLA to Bosch
			--|updated_bosch.arxml		: result file of 2 above ones.
		--|test_ws_2	
			--|test_port_ecuc_partition_2		
			--|test_stla_2.arxml		: test file of STLA. 2 containers, used for activity of updating different containers from STLA to Bosch
			--|test_bosch_2.arxml		: test file of Bosch. 1 container, used for activity of updating different containers from STLA to Bosch
			--|updated_bosch_2.arxml	: result file of 2 above ones.		
		--|test_ws_3		
			--|test_port_ecuc_partition_3.py
		--|test_ws_4,5,6
		
--|ecuc_partition_handling								: self library for parsing arxml contents
	--|ecuc_partition_parser.py							: library contains class EcucPartitionParser
	--|test_parse_ecuc_partition.py						: test main script for libray writing
	--|ecuc_partition_parser_no_sort.py					: before final ver, a self library for parsing arxml contents and not yet implement sort function
==========================================JSON==============================================
  "EcuPartition": {
    "merger": {
      "target_file": "conf_ecucpartition_ecucvalues_merged.arxml",
      "inputs": [
        "conf_ecucpartition_ecucvalues.arxml",
        "RTEConfGen_EcucPartition_EcucValues.arxml"
      ]
    },
    "updater": {
      "target_file": "conf_ecucpartition_ecucvalues.arxml",
      "ignore_folders": ["RB_RteArch/Rte"],
      "inputs": [
        "conf_ecucpartition_ecucvalues.arxml",
        "STLA_EcucPartition.arxml"
      ],
      "to_remove": [
        "RTEConfGen_EcucPartition_EcucValues.arxml"
      ]
    }
  }
		
==================================================== QUESTIONS ================================================================					
			
	+) OUTPUT		
-?locate in input files
-?as unique identifier
-?build the output which is based on [Bosch CI PVER file], for which [Bosch CI PVER file] is the one in pver_test  
	
	
==================================================== ANSWER ================================================================
|input file
	--|STLA files				: RTEConfGen_EcucPartition_EcucValues.arxml
	--|Bosch exported files		: conf_ecucpartition_ecucvalues.arxml
	
=============================================== FOR WHOLE PROCESS ===========================================================
-STLA:
RTEConfGen_Ecu_Extract.arxml
RTEConfGen_FlatView_swcd.arxml
RTEConfGen_FlatMap.arxml
RTEConfGen_EcucPartition_EcucValues.arxml
 
-Bosch:
conf_ecu_extr.arxml
conf_ecu_flatview_swcd.arxml
conf_ecu_flatmap.arxml
conf_ecucpartition_ecucvalues.arxml
 
For this development, only need RTEConfGen_EcucPartition_EcucValues.arxml and conf_ecucpartition_ecucvalues.arxml, 
	because it's only related to EcucPartition use case.
==================================================== NEED TO DO ================================================================
+) OUTPUT of conf_ecucpartition_ecucvalues.arxml
<SUB-CONTAINERS> -> <ECUC-CONTAINER-VALUE> -> <SHORT-NAME> -> <DEFINITION-REF> -> <PARAMETER-VALUES> -> (<REFERENCE-VALUES>)							: BOSCH  
															-> <REFERENCE-VALUES> -> <ECUC-INSTANCE-REFERENCE-VALUE> -> <VALUE-IREF> -> <TARGET-REF>	: STLA



==================================================== FOR TEST. NOW NOT CARE ================================================================  
- TEST Input/Output of task
	+) INPUT
|test_files
	--|expected_Merger	: Bosch exported files
	--|expected_Updater	:
	--|pver_test		:
	--|STLA_ws			: is the output of InitialExport tool
		--|RB_BSW
		--|RB_RteArch: Rte configuration files
			--|EcuPartition
			--|EcuExtr, FlatMap, FlatView, Others...
--ecupartition_merged.arxml						: found in test_files\expected_Merger\, là file sau khi đã merged và trước khi gửi cho STLA
--ecupartition_updated.arxml					: file sau khi lấy lại từ STLA		