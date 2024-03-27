import glob
import re
import os
import json

class FileHandling:

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def find_file_path_list(root_path, exp_to_search, paths_to_ignore):
        raw_list = glob.glob(root_path + '/**/' + exp_to_search, recursive=True)

        # Remove all paths to be ignored
        if paths_to_ignore:
            final_paths_list = [path for path in raw_list if
                                all(os.path.normpath(path_to_ignore) not in path for path_to_ignore in paths_to_ignore)]
            return final_paths_list
        else:
            return raw_list

    @staticmethod
    def get_index(array_to_search, pattern_to_search):
        indexes_list = [idx for idx, item in enumerate(array_to_search)
                        if re.search(pattern_to_search, item)]
        return indexes_list

    @staticmethod
    def check_if_folder_exists(folder):
        if not (os.path.isdir(folder)):
            raise ValueError(folder + ' does not exist. Please check value given.')
        else:
            return folder

    @staticmethod
    def print_json(folder, filename, dico):
        with open(os.path.join(folder, filename), 'w') as fp:
            json.dump(dico, fp, indent=4)
