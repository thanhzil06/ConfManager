import os
root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_ecuc_partition"))

BASE_FILE = 'conf_ecucpartition_ecucvalues.arxml'
GENERATED_FILE = 'RTEConfGen_EcucPartition_EcucValues.arxml'

# Constants for the test of porting delta changes 
pver_root = os.path.join(root_path, "test_pver")
cust_ws = os.path.join(root_path, "test_cust_ws")
output_path = os.path.join(root_path, "updated_output")

expected_file = os.path.join(root_path, "expected_output", 
                             "expected_conf_ecucpartition_ecucvalues.arxml")

base_pver_file = os.path.join(pver_root, f"{BASE_FILE}")
gen_file = os.path.join(pver_root, f"{GENERATED_FILE}")

delta_file = os.path.join(cust_ws, f"{BASE_FILE}")
delta_gen = os.path.join(cust_ws, f"{GENERATED_FILE}")

if not (os.path.isdir(output_path)):
    os.makedirs(output_path) 
output_file = os.path.join(output_path, f"{BASE_FILE}")    

# Constants for the test of sorting elements 
sort_root = os.path.join(root_path, "test_sort")
expect_sort = os.path.join(sort_root, "expected_sort.arxml")
output_sort = os.path.join(sort_root, "output_sort.arxml")

# Constants for the test of removing duplicate elements 
dup_root = os.path.join(root_path, "test_duplicate")
duplicate_file = os.path.join(dup_root, "duplicate.arxml")
output_duplicate = os.path.join(dup_root, "output.arxml")
expect_dup_remove = os.path.join(dup_root, "expected_dup_remove.arxml")