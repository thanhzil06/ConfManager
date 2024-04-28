import os

# -------------- ECU EXTRACT --------------
file_ecuextract_1 = 'conf_ecu_extr_1.arxml'
file_ecuextract_2 = 'conf_ecu_extr_2.arxml'
file_ecuextract_3 = 'conf_ecu_extr_3.arxml'
file_ecuextract_4 = 'RTEConfGen_Ecu_Extract_1.arxml'
file_ecuextract_5 = 'RTEConfGen_Ecu_Extract_2.arxml'
file_ecuextract_6 = 'RTEConfGen_Ecu_Extract_3.arxml'

ecuextract_conf = {
    'EcuExtract': {
        'merger': {
            'target_file': 'ecuextract_merged.arxml',
            'inputs': [file_ecuextract_1,
                       file_ecuextract_2,
                       file_ecuextract_3,
                       file_ecuextract_4,
                       file_ecuextract_5,
                       file_ecuextract_6
                       ]
        }
    }
}
ecuextract_path_list = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", file_ecuextract_4),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", file_ecuextract_5),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", file_ecuextract_6),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", file_ecuextract_1),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", file_ecuextract_2),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", file_ecuextract_3)
]

# -------------- ECU EXTRACT 2 --------------
ecuextract_conf_2 = {
    'EcuExtract': {
        'merger': {
            'target_file': 'ecuextract_2_merged.arxml',
            'inputs': [# valeurs inversés !!!
                file_ecuextract_5,
                file_ecuextract_2
            ]
        }
    }
}

ecuextract_2_path_list = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", file_ecuextract_5),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", file_ecuextract_2)
]

# -------------- ECU EXTRACT 3 --------------
ecuextract_conf_3 = {
    'EcuExtract': {
        'merger': {
            'target_file': 'ecuextract_3_merged.arxml',
            'inputs': [
                file_ecuextract_1,
                file_ecuextract_5
            ]
        }
    }
}

ecuextract_3_path_list = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", file_ecuextract_5),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", file_ecuextract_1)
]


# -------------- FLATVIEW --------------
flatview_conf = {
    'FlatView': {
        'merger': {
            'target_file': 'flatview_merged.arxml',
            'inputs': [
                'conf_ecu_flatview_swcd_1.arxml',
                'conf_ecu_flatview_swcd_2.arxml',
                'conf_ecu_flatview_swcd_3.arxml',
                'conf_ecu_flatview_swcd_4.arxml',
                'conf_ecu_flatview_swcd_5.arxml',
                'conf_ecu_flatview_swcd_6.arxml',
                'RTEConfGen_FlatView_swcd_1.arxml',
                'RTEConfGen_FlatView_swcd_2.arxml',
                'RTEConfGen_FlatView_swcd_3.arxml',
                'RTEConfGen_FlatView_swcd_4.arxml',
                'RTEConfGen_FlatView_swcd_5.arxml',
                'RTEConfGen_FlatView_swcd_6.arxml'
            ]
        }
    }
}
flatview_path_list = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatView_swcd_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatView_swcd_2.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatView_swcd_3.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatView_swcd_4.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatView_swcd_5.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatView_swcd_6.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatview_swcd_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatview_swcd_2.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatview_swcd_3.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatview_swcd_4.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatview_swcd_5.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatview_swcd_6.arxml")
]


# -------------- FLATMAP --------------
flatmap_conf = {
    'FlatMap': {
        'merger': {
            'target_file': 'flatmap_merged.arxml',
            'inputs': [
                'conf_ecu_flatmap_1.arxml',
                'conf_ecu_flatmap_2.arxml',
                'conf_ecu_flatmap_3.arxml',
                'conf_ecu_flatmap_4.arxml',
                'conf_ecu_flatmap_5.arxml',
                'RTEConfGen_FlatMap_1.arxml',
                'RTEConfGen_FlatMap_2.arxml',
                'RTEConfGen_FlatMap_3.arxml',
                'RTEConfGen_FlatMap_4.arxml',
                'RTEConfGen_FlatMap_5.arxml'
            ],
        }
    }
}
flatmap_path_list = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatMap_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatMap_2.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatMap_3.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatMap_4.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_FlatMap_5.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatmap_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatmap_2.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatmap_3.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatmap_4.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecu_flatmap_5.arxml")
]

# -------------- ECUPARTITION --------------
ecupartition_conf = {
    'EcuPartition': {
        'merger': {
            'target_file': 'ecupartition_merged.arxml',
            'inputs': [
                'conf_ecucpartition_ecucvalues_1.arxml',
                'conf_ecucpartition_ecucvalues_2.arxml',
                'RTEConfGen_EcucPartition_EcucValues_1.arxml',
                'RTEConfGen_EcucPartition_EcucValues_2.arxml'
            ],
        }
    }
}
ecupartition_path_list = [
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_EcucPartition_EcucValues_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "_gen", "swb", "module", "rtegen", "rteconfgen", "RTEConfGen_EcucPartition_EcucValues_2.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecucpartition_ecucvalues_1.arxml"),
    os.path.join(os.path.dirname(__file__), "test_files", "pver_test",
                 "Conf", "__Conf", "conf_ecucpartition_ecucvalues_2.arxml")
]

