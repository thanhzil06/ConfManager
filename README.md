# confmanager
This tool is expected to compare the original merged file of Bosch with the new updated merged file from STLA and update the base configuration of STLA with the delta changes into Bosch arxml file in Bosch workspace.

====================================================================

About ConfManager: has 2 modes

+) InitialExport-ConfMerger: provide the merged file to STLA

+) Preprocessing-ConfUpdater: which is my development

====================================================================

- Requirement chung của tool: Từ điểm này thì mới có thể xác định và đưa ra từng task nhỏ của cả quá trình dev tool
  
**********************************NGỮ CẢNH**********************************

- Tool compilation của Bosch không thể compile nhiều file arxml từ STLA, nên ConfMerger phải merge hết mọi tool đó lại với nhau thành 1 file arxml cuối. Sau đó, đưa lại file này cho STLA as an initial export (1 tool khác) để STLA add thêm những configuration RTE vào.
  
- Tiếp theo, Bosch sẽ lại nhận updated file từ STLA đã merge và add config RTE --> để compile. Tuy nhiên, có lỗi vì xảy ra duplicate elements trong file arxml.
  
- Do đó, phải so sánh 2 file của BOSCH (file merged còn trinh) và STLA (file merged mất trinh) với nhau, loại bỏ những ele trùng nhau --> Mode Updater.
	==> Nghĩa là, tool is expected to xác định thành phần mới add bởi STLA để có thể được included trong Bosch workspace.

- Mode merger và updater trong các đợt dev trước ổn với 3 types of arxml files (flatmap, flatview, ecu_extr), và mode updater ổn lòi lìa với type còn lại (ecucpartition_ecucvalues).
  
********************************************************************
---------------------------Problem Statement---------------------------
- With the current version of ISOLAR used by STLA as a part of MDG Shared build for RTE generation, there is a limitation in the ISOLAR tool that doesn't allow import of the multiple ARXML files having the same AUTOSAR TAG and structure. This is blocking STLA to perform RTE configuration. 

- STLA is requesting a solution from Bosch software team to merge all such files before providing to STLA team as an initial export that can be used by STLA to add their configuration. Meanwhile ETAS should release on update of ISOLAR tool to manage the import of multiple files.

- The general idea of solution will be to merge the files [ARXML files] and provide this merged file to STLA. Once STLA provide Bosch back the updated merged file. 
-->Bosch then has to develop a preprocessing tool to compare the original merged file with the new updated merged file from STLA and update the base configuration with the delta changes.

- This tool is expected to compare the original merge file with the new updated merged file from STLA and update the base configuration with the delta changes.
----->The tool is expected to identify new files added by STLA to be included in Bosch workspace.
  
/!\Limitation of Ecucpartition:__EcuCPartition usecases is not fully handled by Updater mode (nghĩa là ở Mode Merger và Updater, các file arxml khác như ecu_extr, ecu_flatmap, ecu_flatview đều hoạt động mượt trừ ECUCPartition). A new strategy (requirements + tool development) will be created for it.

---------------------------Epic ConfManager/updater-ECUC-PARTITION---------------------------

- ECPT-11815
  
- Desc:
	+) Tool Requirement: https://inside-docupedia.bosch.com/confluence/display/PMTECS/Preprocessing+-+Conf+Updater
  
	+) Background:  About delta changes.

With the release of Confupdater v1.1.0 we have below limitation.
/!\ ** EcuCPartition use case is not fully handled as expected; please avoid as possible to use the tool with EcuCPartition. A new strategy will be specified for this use case.
This ticket is planned to write the requirement for the use case of the ECUCPartition.

-------------------------------Issues of epic ECPT-11815------------------------------------------


-----------------------ECPT 11910-----------------------
  
- Requirement #008

- To Do:

+) Update the User Guide to include information about arguments "-h" and "-v"
  
+) Add the parameter "required" to all mandatory arguments

+) In "description" as argument of ArgumentParser add:
	Version of Autosar XSD and related AUTOSAR_MOD_ECUConfigurationParameters.arxml supported by the tool
	Link to User Guide
 
+) In "help" display:
	Ensure that the version of AUTOSAR_MOD_ECUConfigurationParameters.arxml related with Autosar XSD used for the library appears
	Ensure that all mandatory parameters are tagged as Mandatory
 
-----------------------ECPT 11911-----------------------
  
Requirement #011

Sort elements of EcuCPartition as specified in requirement #011
--> Mục đích: để tester dễ dàng compare hơn khi làm so sánh các file sau merged và sau updated
  
-----------------------ECPT 11912-----------------------
 
Requirements #009, #012-#016

Implement the requirements described in above link.

+-----------------------------------------------------Goal of requirement number-----------------------------------------------------

#008	Provide information indicating the following:

    1) version of the tool
    
    2) the supported AR-version schema of ECUCConfigurationParameter for EcuC module and Rte module in help session (example : --help)

#011	For EcuCPartition configuration, process non-sequential elements (ECUC-CONTAINER-VALUE, ECUC-INSTANCE-REFERENCE-VALUE) in input files to generate output with alphabet-ascending-sorted non-sequential elements.

#009	Process files with tolerance/flexibility against different global AR paths to the module.
Usecase : "/AUTOSAR_EcuC/EcucModuleDefs/EcuC","/AUTOSAR/EcucDefs/EcuC"	--> NO NEED as previous developer had dealed with it.

#012	For EcuCPartition configuration, locate  in input files, which are Bosch ARXL files and STLA ARXL files, 
the information of EcucInstanceReferenceValue and EcuCPartition to identify the new content which then can be merged into output ARXML file (based on Bosch CI PVER file).
-->  Nghĩa là cần xác định tất cả EcuCPartition của cả 2 phía, đồng thời xác định EcucInstanceReferenceValue phía STLA.

#013	For EcuCPartition configuration - specifically EcucInstanceReferenceValue use in input files, the content of element <TARGET-REF>, 
which is within the element <ECUC-INSTANCE-REFERENCE-VALUE> as unique identifier for the element <ECUC-INSTANCE-REFERENCE-VALUE>

#014	For EcuCPartition configuration - specifically EcuCPartition-relevant identification, locate in input files, the elements <ECUC-CONTAINER-VALUE>, 
which contain children element <DEFINITION-REF> having the content "/AUTOSAR_EcuC/EcucModuleDefs/EcuC/EcucPartitionCollection/EcucPartition" (without ").

#015	For EcuCPartition configuration - specifically EcuCPartition-relevant identification, use in located EcucContainerValue containers, 
the content of element <SHORT-NAME> as unique identifier for the EcuCPartition.

#016	For processing, port the newly-appearing EcuCInstanceReferenceValue detected by comparing the STLA files against Bosch exported files in input files to build the output which is based on Bosch PVER file.
--> Từ 12-16, cần phải xác định được những element RTE của STLA và add những element này vào file gốc của BOSCH.
<ECUC-CONTAINER-VALUE> -> <SHORT-NAME> -> <DEFINITION-REF> -> <PARAMETER-VALUES> -> 												: BOSCH 
										-> <REFERENCE-VALUES> -> <ECUC-INSTANCE-REFERENCE-VALUE> -> <VALUE-IREF> -> <TARGET-REF>	: STLA
	==> File ARXML của cả Bosch và STLA đều có <ECUC-CONTAINER-VALUE>. Tuy nhiên, nội dung trong đó sẽ khác nhau.	


-----------------------ECPT 12401-----------------------

Based on the most recent update from our team accountable for customer requirements, a new scenario has emerged in the ECUC Partition use case. 

Instead of receiving a single file with the concept _merged from customer, RB will now receive multiple files. Here is a brief summary:

1) From PVER CI
        - file A: RTEConfGen_EcucPartition.arxml
   
   	- file B: conf_ecucpartition_values.arxml

3) Pre RTE received from STLA:
   
   	- file A+: RTEConfGen_EcucPartition.arxml
   
   	- file B+: conf_ecucpartition_values.arxml
   
	- file D: another new file.arxml
   
	delta = delta + additional info from new file.	
								
5) Final goal of Conf updater v_1.2.0
   
- Identify the delta between (File A & File A+) + (File B & File B+)
  
- port delta changes into file B   --> update the File B as B1 with the delta.
