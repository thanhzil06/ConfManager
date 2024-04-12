import os
root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_ecuc_partition"))

pver_root = os.path.join(root_path, "test_pver", "Conf", "__Conf")
cust_ws = os.path.join(root_path, "test_cust_ws", "RB_RteArch", "EcuPartition")

base_file = os.path.join(pver_root, "conf_ecucpartition_ecucvalues_merged.arxml")
delta_file = os.path.join(cust_ws, "conf_ecucpartition_ecucvalues_merged_delta.arxml")

output = os.path.join(root_path, "updated_output")
if not (os.path.isdir(output)):
    os.makedirs(output) 
expected = os.path.join(root_path, "expected_output")

output_file = os.path.join(output, "conf_ecucpartition_ecucvalues.arxml")
expected_file = os.path.join(expected, "expected.arxml")