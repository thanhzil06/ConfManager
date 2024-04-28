import os
import subprocess

path = os.path.dirname(__file__)

test_folder = input('Enter name of the folder you want to test: ')
root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), test_folder))

pver_path = os.path.join(root_path, "in", "CIPVER")
cust_path = os.path.join(root_path, "in", "STLAInput")
config_file = os.path.join(root_path, "in", "configuration", "ConfManager_configuration.json")
 
output_path = os.path.join(root_path, "out")
expected_path = os.path.join(root_path, "exp")

def main():
    confmanager_cmd = 'ConfManager.exe ' + ' -m Updater ' + ' -p ' + pver_path + ' -ws ' + cust_path + ' -cf ' + config_file + ' -o ' + output_path
    os.system(confmanager_cmd)

    compare_folders(output_path, expected_path)

def compare_folders(folder_a, folder_b):
    # Path to the Beyond Compare.exe
    beyond_compare_path = os.path.normpath("C:\\Program Files\\Beyond Compare 4\\BCompare.exe")
    
    # Command to execute the .exe file
    beyond_compare_command = [beyond_compare_path, folder_a, folder_b]
    
    # Call Beyond Compare with the provided folders
    try:
        subprocess.run(beyond_compare_command)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()