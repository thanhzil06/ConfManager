from config_handling.configuration_handling import ConfFileHandling
from logger.loadlogconf import LoadLogconf

output_path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/test_json/output/"
conf_file_path = "C:/Users/GYH8HC/dev_tool/03_ConfManager_ECUC_Partition/02_test_ws/test_json/ConfManager_configuration.json"
logger = LoadLogconf(logger_choice="dev", output_path=output_path).log
conf_handler_obj = ConfFileHandling(logger)

conf_file_path_list = [conf_file_path]
configuration_data = conf_handler_obj.read_json_configuration_file(conf_file_path_list)

print(configuration_data.keys())

for topic in configuration_data.keys():
    print(topic=='EcuPartition')