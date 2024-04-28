import os
import json


class ConfFileHandling:
    """
    Class that handle configuration files
    """

    def __init__(self, logger):
        """
        Constructor of the class
        :param conf_file_path:
        :param logger:
        """

        # get default configuration file path : search in app folder
        self.logger = logger


    def read_json_configuration_file(self, json_path_list):
        """
        Warning : this function assumes that there is only one JSON file
        :param json_path_list:
        :return:
        """
        for json_path in json_path_list:
            self.logger.info("Reading configuration file " + os.path.basename(json_path))
            with open(json_path) as json_file_handler:
                data = json.load(json_file_handler)

        return data
