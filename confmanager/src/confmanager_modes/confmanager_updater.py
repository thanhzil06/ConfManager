import os
from utils.filehandling import FileHandling
from confmanager_modes.confmanager_modes_common import CommonModeUtils
from confmanager_modes.confmanager_merger import MergerMode
import constants as csts
import re
import json


class UpdaterMode:

    def __init__(self, pver_root, merged_files_folder, customer_ws, logger):
        self.logger = logger
        self.file_handling_obj = FileHandling(self.logger)
        self.modes_common_obj = CommonModeUtils(self.logger)
        self.customer_ws = self.file_handling_obj.check_if_folder_exists(customer_ws)
        self.pver_root = self.file_handling_obj.check_if_folder_exists(pver_root)
        self.updated_files_folder = self.file_handling_obj.check_if_folder_exists(merged_files_folder)
        self.additional_log_files_folder = (self.file_handling_obj.
                                            check_if_folder_exists(os.path.join(self.updated_files_folder, 'logs')))
        self.merger_obj = MergerMode(self.pver_root, self.updated_files_folder, self.logger)
        self.to_remove_dict = dict()
        self.to_be_updated_dict = dict()

    def update_files(self, target_file, xml_root_to_update, xml_dict_to_update, content_to_remove_list):
        self.logger.info("Updating file...")

        file_to_remove_list = list()
        raw_left_side_paths = list()
        left_side_paths = self.filter_paths_list(self.modes_common_obj.build_sorted_hierarchy(xml_dict_to_update,
                                                                                              raw_left_side_paths))
        # Read content to ignore
        for file_content_to_remove in content_to_remove_list:
            file_to_remove_list.extend(self.file_handling_obj.find_file_path_list(self.pver_root,
                                                                                  file_content_to_remove,
                                                                                  list()))
            # Get root and dict
            self.to_remove_dict[csts.root_main_tag] = {}
            (to_remove_root,
             self.to_remove_dict[csts.root_main_tag]) = self.merger_obj.parse_and_get_dico(file_to_remove_list[0])

            raw_right_side_paths = list()
            right_side_paths = self.filter_paths_list(self.modes_common_obj.build_sorted_hierarchy(self.to_remove_dict,
                                                                                                   raw_right_side_paths))

            # Test dict paths
            for right_side_path in right_side_paths:
                # Filter paths to avoid to remove the common root
                # Check intersection of tags_to_check_tuple and path
                right_side_path = tuple(self.modes_common_obj.treat_empty_dict_elem(list(right_side_path)))
                right_side_path_tag_intersection = tuple(set(right_side_path) & set(csts.tags_to_check))
                # Rules to accept a path:
                # Tag in csts.tags_to_check found
                # Tag just before found tag must not contain 'AR_PACKAGE', because it's the common root

                if right_side_path_tag_intersection:
                    right_side_tag_value = right_side_path[-1]
                    # check if there is an intersection with left_side -> common part
                    left_side_intersection = [item for item in left_side_paths if right_side_tag_value in item]
                    # Update file by removing elements
                    self.remove_element(left_side_intersection, xml_root_to_update, xml_dict_to_update)

        # Create a new file
        self.modes_common_obj.export_merged_file(os.path.join(self.updated_files_folder, target_file),
                                                 xml_root_to_update)

    def filter_paths_list(self, raw_paths_list):
        """
        Apply rules to intersection.
        :param raw_paths_list:
        :return:
        """
        filtered_paths = list()

        for path in raw_paths_list:
            pattern_found = 0
            for pattern_not_to_be_removed in csts.patterns_not_to_be_removed:
                if not isinstance(pattern_not_to_be_removed, tuple):
                    pattern_found += self.handle_not_tuple_patterns(pattern_not_to_be_removed, path)
                else:
                    pattern_found += self.handle_tuple_patterns(pattern_not_to_be_removed, path)

            if pattern_found == 0 and bool(path[-1]):
                filtered_paths.append(path)

        return filtered_paths

    @staticmethod
    def handle_not_tuple_patterns(not_tuple_pattern_not_to_be_removed, path):
            condition_1 = re.search(not_tuple_pattern_not_to_be_removed, path[-3]) is not None
            condition_2 = ((not_tuple_pattern_not_to_be_removed.startswith('@'))
                           and (not_tuple_pattern_not_to_be_removed in path is not None))
            if condition_1 or condition_2:
                return 1
            else:
                return 0

    @staticmethod
    def handle_tuple_patterns(tuple_pattern_not_to_be_removed, path):
        length_pattern = len(tuple_pattern_not_to_be_removed)
        subset_from_path_list = [csts.find_dict_index_compiled.sub('', element)
                                 for element in list(path[(-2 - length_pattern):-2])]
        subset_from_path = tuple(subset_from_path_list)

        if subset_from_path == tuple_pattern_not_to_be_removed:
            return 1
        else:
            return 0

    def remove_element(self, xml_paths_list, left_side_root, xml_dict_to_update):
        """

        :param xml_dict_to_update:
        :param xml_paths_list:
        :param left_side_root:
        :return:
        """

        # Order of elements:
        # N element -> value of the tag
        # N-1 element -> tag searched with intersection
        # N-2 element -> root of searched tag
        # It's necessary to check if the N-2 element has an index (_0, par example) or not. If yes,
        # there is an element of a list, so the root has to finish at N-3 element. The N-2 element
        # will be used to has the list content.
        # The first element of path, "AUTOSAR", must also be removed

        for xml_path_to_element in xml_paths_list:
            found_tag_value = xml_path_to_element[-1]
            tag_name = xml_path_to_element[-2]
            element_n_2 = xml_path_to_element[-3]
            #if match := re.search(r'_\d+', element_n_2):

            index_of_elem_to_remove = None
            if match_1 := csts.find_dict_index_compiled.search(element_n_2):
                index_of_elem_to_remove = match_1.group(0)
            elif match_2 := csts.find_xml_index_compiled.search(element_n_2):
                index_of_elem_to_remove = match_2.group(0)

            if index_of_elem_to_remove:
                element_to_remove = element_n_2.replace(index_of_elem_to_remove, '')

                self.remove_in_xml_and_dict(xml_path_to_element,
                                            element_to_remove,
                                            left_side_root,
                                            tag_name,
                                            found_tag_value,
                                            xml_dict_to_update)

    def remove_in_xml_and_dict(self, xml_path_to_element,
                               element_to_remove,
                               left_side_root,
                               tag_name,
                               found_tag_value,
                               xml_dict_to_update):

        root_list_of_elements = list()
        left_side_xml_path = self.modes_common_obj.convert_dict_to_xml(".".join(xml_path_to_element[1:-3]))

        root_xml_string = "left_side_root." + left_side_xml_path
        if hasattr(eval(root_xml_string), element_to_remove):
            root_list_of_elements = eval(root_xml_string + ".get_" + element_to_remove + "()")

        # Remove the element in the list with the value
        if root_list_of_elements:
            indexes_tag_list = [idx for idx, elem in enumerate(root_list_of_elements)
                                if eval("elem.get_" + tag_name + "().valueOf_") == found_tag_value]

            if indexes_tag_list:
                # Remove in xml
                remove_cmd = ("left_side_root." + left_side_xml_path + ".get_" + element_to_remove +
                              "().pop(" + str(indexes_tag_list[0]) + ")")
                eval(remove_cmd)

                # Remove in dict
                root_dict = [csts.root_main_tag] + list(xml_path_to_element[1:-3])
                root_dict_elements_list = list(self.modes_common_obj.get_by_path(xml_dict_to_update, root_dict))
                self.modes_common_obj.del_by_path(xml_dict_to_update, root_dict +
                                                  [root_dict_elements_list[indexes_tag_list[0]]])
        else:
            # Remove list, because it's empty
            pass
