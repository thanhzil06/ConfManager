import os

merged_ecuextract_file_name = "conf_ecu_extr_merged.arxml"
updater_ecuextract_file_name = "conf_ecu_extr.arxml"

configuration_test = {
    "EcuExtract": {
        "merger": {
            "target_file": merged_ecuextract_file_name,
            "inputs": [
                "conf_ecu_extr_1.arxml",
                "RTEConfGen_Ecu_Extract_1.arxml"
            ]
        },
        "updater": {
            "target_file": updater_ecuextract_file_name,
            "ignore_folders": ["/RB_RteArch/Rte/"],
            "inputs": [
                merged_ecuextract_file_name,
                "STLA_ecuextract.arxml"
            ],
            "to_remove": [
                "RTEConfGen_Ecu_Extract.arxml"
            ]
        }
    }
}

# Expected for Merger
exp_files_to_merge_path_list_merger = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_Ecu_Extract_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_extr_1.arxml")
    ]
exp_content_to_remove_filename_merger = list()

# Expected for Updater
exp_files_to_merge_path_list_updater = [
    os.path.join(os.path.dirname(__file__), "test_files", "STLA_ws",
                 "RB_RteArch", "EcuExtr", merged_ecuextract_file_name),
    os.path.join(os.path.dirname(__file__), "test_files", "STLA_ws",
                 "RB_RteArch", "EcuExtr", "STLA_ecuextract.arxml")
]
exp_content_to_remove_filename_updater = ["RTEConfGen_Ecu_Extract.arxml"]