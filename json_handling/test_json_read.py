import json
with open('ConfManager_configuration.json', 'r') as file:
    data = json.load(file)

for topic in data.values():
    print(topic)

    # {'EcuExtract': {'merger': {'target_file': 'conf_ecu_extr_merged.arxml', 
    #                         'inputs': ['conf_ecu_extr.arxml', 'RTEConfGen_Ecu_Extract.arxml']}, 
    #                 'updater': {'target_file': 'conf_ecu_extr.arxml', 
    #                             'ignore_folders': ['RB_RteArch/Rte'], 
    #                             'inputs': ['conf_ecu_extr_merged.arxml', 'STLA_ecuextract.arxml'], 
    #                             'to_remove': ['RTEConfGen_Ecu_Extract.arxml']}}, 

    # 'FlatView': {'merger': {'target_file': 'conf_ecu_flatview_swcd_merged.arxml', 
    #                         'inputs': ['conf_ecu_flatview_swcd.arxml', 'RTEConfGen_FlatView_swcd.arxml']}, 
    #             'updater': {'target_file': 'conf_ecu_flatview_swcd.arxml', 'ignore_folders': ['RB_RteArch/Rte'], 
    #                         'inputs': ['conf_ecu_flatview_swcd.arxml', 'STLA_FlatView.arxml'], 
    #                         'to_remove': ['RTEConfGen_FlatView_swcd.arxml']}}, 

    # 'FlatMap': {'merger': {'target_file': 'conf_ecu_flatmap_merged.arxml', 
    #                     'inputs': ['conf_ecu_flatmap.arxml', 'RTEConfGen_FlatMap.arxml']}, 
    #             'updater': {'target_file': 'conf_ecu_flatmap.arxml', 'ignore_folders': ['RB_RteArch/Rte'], 
    #                         'inputs': ['conf_ecu_flatmap.arxml', 'STLA_FlatMap.arxml'],
    #                         'to_remove': ['RTEConfGen_FlatMap.arxml']}}, 
                            
                            
    # 'EcuPartition': {'merger': {'target_file': 'conf_ecucpartition_ecucvalues_merged.arxml', 
    #                             'inputs': ['conf_ecucpartition_ecucvalues.arxml', 'RTEConfGen_EcucPartition_EcucValues.arxml']}, 
    #                 'updater': {'target_file': 'conf_ecucpartition_ecucvalues.arxml', 
    #                             'ignore_folders': ['RB_RteArch/Rte'], 
    #                             'inputs': ['conf_ecucpartition_ecucvalues.arxml', 'STLA_EcucPartition.arxml'], 
    #                             'to_remove': ['RTEConfGen_EcucPartition_EcucValues.arxml']}}}
