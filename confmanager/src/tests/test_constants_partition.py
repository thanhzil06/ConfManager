import os
root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_ecuc_partition"))

BASE_FILE = 'conf_ecucpartition_ecucvalues.arxml'
GENERATED_FILE = 'RTEConfGen_EcucPartition_EcucValues.arxml'
OUTPUT_FILE = 'output.arxml'

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
output_sort = os.path.join(sort_root, f"{OUTPUT_FILE}")

# Constants for the test of removing duplicate elements 
dup_root = os.path.join(root_path, "test_duplicate")
duplicate_file = os.path.join(dup_root, "duplicate.arxml")
output_duplicate = os.path.join(dup_root, f"{OUTPUT_FILE}")
expect_dup_remove = os.path.join(dup_root, "expected_dup_remove.arxml")

# Constants for the test of removing empty container
empty_root = os.path.join(root_path, "test_empty")
empty_file = os.path.join(empty_root, "empty.arxml")
output_empty = os.path.join(empty_root, f"{OUTPUT_FILE}")
expect_empty_remove = os.path.join(empty_root, "expected_empty_remove.arxml")

# Constants for the test of getting base parameter of CI PVER
changed_base_root = os.path.join(root_path, "test_change_param")
base_param_file = os.path.join(changed_base_root, "base_file.arxml")
changed_param_file = os.path.join(changed_base_root, "changed_base.arxml")
output_param = os.path.join(changed_base_root, f"{OUTPUT_FILE}")