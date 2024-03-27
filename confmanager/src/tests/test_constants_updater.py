import os

path_exp_updater = os.path.join(os.path.dirname(__file__), "test_files",
                                "expected_Updater")
ignore_folders = ["RB_RteArch/Rte"]

main_input_ecuextract_updater = "ecuextract_2_merged.arxml"

# -------------- ECU EXTRACT --------------
"""
Test case: no Merge, only update.
For it, Update is used to go back to one of files used to merge
"""
ecuextract_updater_conf = {
    'EcuExtract': {
        "updater": {
            "target_file": "ecuextract_updated.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                main_input_ecuextract_updater
            ],
            "to_remove": [
                "RTEConfGen_Ecu_Extract_2.arxml"
            ]
        }
    }
}

"""
A SENDER_RECEIVER_TO_SIGNAL_GROUP_MAPPING_1 to remove 

"""
ecuextract_updater_1_conf = {
    'EcuExtract': {
        "updater": {
            "target_file": "ecuextract_updated_1.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                main_input_ecuextract_updater
            ],
            "to_remove": [
                "RTEConfGen_Ecu_Extract_1.arxml"
            ]
        }
    }
}

ecuextract_updater_2_conf = {
    'EcuExtract': {
        "updater": {
            "target_file": "ecuextract_updated_2.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                main_input_ecuextract_updater,
                'STLA_ecuextract.arxml'
            ],
            "to_remove": [
                "RTEConfGen_Ecu_Extract_4.arxml"
            ]
        }
    }
}

# -------------- FLATVIEW--------------

flatview_updater_conf = {
    'Flatview': {
        "updater": {
            "target_file": "flatview_updated.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                'conf_ecu_flatview_swcd_merged.arxml'
            ],
            "to_remove": [
                "RTEConfGen_FlatView_swcd_1.arxml"
            ]
        }
    }
}

flatview_updater_1_conf = {
    'Flatview': {
        "updater": {
            "target_file": "flatview_updated_1.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                'conf_ecu_flatview_swcd_merged.arxml'
            ],
            "to_remove": [
                "RTEConfGen_FlatView_swcd_3.arxml"
            ]
        }
    }
}


# -------------- FLATMAP --------------

flatmap_updater_conf = {
    'Flatmap': {
        "updater": {
            "target_file": "flatmap_updated.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                'conf_ecu_flatmap_merged.arxml'
            ],
            "to_remove": [
                "RTEConfGen_FlatMap_1.arxml"
            ]
        }
    }
}

# -------------- ECUPARTITION --------------

ecupartition_updater_conf = {
    'EcuPartition': {
        "updater": {
            "target_file": "ecupartition_updated.arxml",
            "ignore_folders": ignore_folders,
            "inputs": [
                'conf_ecucpartition_ecucvalues_merged.arxml'
            ],
            "to_remove": [
                "RTEConfGen_EcucPartition_EcucValues_2.arxml"
            ]
        }
    }
}

