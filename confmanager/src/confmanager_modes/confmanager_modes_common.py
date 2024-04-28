from utils.filehandling import FileHandling
import boschlibparserarxmlutils.autosar_lib_4_3_0 as autosarlib
from lxml import etree
import os
import re
import constants as csts
import copy
from functools import reduce
import operator


class CommonModeUtils:

    def __init__(self, logger):
        self.logger = logger
        self.file_handling_obj = FileHandling(self.logger)

    def prepare_mode_inputs(self, mode, topic, configuration_data, root_paths):
        arxml_in_pver_list = list()
        content_to_remove_filename = list()
        folders_to_ignore = list()

        # Find all paths for inputs in Merger part of configuration data
        self.logger.info(topic)
        topic_content = configuration_data[topic]
        # Get merger configuration
        mode_configuration_data = topic_content[mode]
        # Get target_file
        target_file = mode_configuration_data['target_file']
        # Get inputs for the topic
        files_to_merge = mode_configuration_data['inputs']
        # folders to be ignored during arxml searching
        if 'ignore_folders' in mode_configuration_data:
            folders_to_ignore.extend(mode_configuration_data['ignore_folders'])
        # Get paths for inputs
        for root_path in root_paths:
            arxml_in_pver_list.extend(self.file_handling_obj.find_file_path_list(root_path,
                                                                                 '*.arxml',
                                                                                 folders_to_ignore))
        files_path_list = self.reduce_file_paths_list(files_to_merge,
                                                      arxml_in_pver_list)

        if 'ignore_folders' in mode_configuration_data:
            content_to_remove_filename = mode_configuration_data['to_remove']

        return target_file, files_path_list, content_to_remove_filename

    def reduce_file_paths_list(self, list_files, list_paths):
        """

        :param list_files:
        :param list_paths:
        :return:
        """
        file_to_be_merged_final_path_list = []
        for file_to_be_merged in list_files:
            indexes_file_to_be_merged = self.file_handling_obj.get_index(list_paths, file_to_be_merged)

            for index in indexes_file_to_be_merged:
                file_to_be_merged_final_path_list.append(list_paths[index])

        return file_to_be_merged_final_path_list

    def check_if_enough_files_for_merge(self, list_files_to_merge):
        merge_can_be_executed = True

        if not list_files_to_merge or len(list_files_to_merge) < 2:
            self.logger.warning("There are not enough files to merge: please check your configuration "
                                "file and your inputs")
            merge_can_be_executed = False

        return merge_can_be_executed

    def export_merged_file(self, output_file_path, merged_root):
        """
        This function create the merged file by exporting the updated root
        :param target_file:
        :param merged_root:
        :return:
        """
        self.logger.info("Writing final file")

        with (open(output_file_path, 'w') as merged_file):
            merged_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            merged_root_lxml = merged_root.to_etree(None, name_="AUTOSAR", mapping_={}, nsmap_= csts.nsmap1)
            merged_xml_string = etree.tostring(merged_root_lxml, pretty_print=True, encoding='utf-8', method="xml"
                                               ).decode('utf-8')
            merged_xml_string = self.postproc_replace_values_in_merged_xml(merged_xml_string,
                                                                           csts.postprocessing_replacements)
            merged_file.write(merged_xml_string)

        merged_file.close()

    @staticmethod
    def postproc_replace_values_in_merged_xml(xml_string, values_to_replace_list):
        """
        This function will replace strings that can't be managed in another way (library regeneration, ...). So it
        must be used as last way to correct the merged file
        :param xml_string:
        :param values_to_replace_list: list of tuples, defined in constants.py
        :return: modified string
        """
        new_xml_string = xml_string
        for value_to_replace in values_to_replace_list:
            new_xml_string = re.sub(value_to_replace[0], value_to_replace[1], new_xml_string)

        return new_xml_string

    @staticmethod
    def convert_dict_to_xml(string_to_convert):
        compiled_regexp = re.compile(r'(\w+)_(\d+)')
        converted_string = compiled_regexp.sub(r'\1[\2]', string_to_convert)
        return converted_string

    def get_dict_hierarchy(self, dictionary, dict_paths_list, prefix=()):
        for key, value in dictionary.items():
            if isinstance(value, dict) and value:
                self.get_dict_hierarchy(value, dict_paths_list, (*prefix, key))
            elif isinstance(value, list) and value:
                path_tuple = (*prefix, key, tuple(value))
                dict_paths_list.append(path_tuple)
            else:
                path_tuple = (*prefix, key, value)
                dict_paths_list.append(path_tuple)

    @staticmethod
    def order_dict_paths(dict_paths_to_order):
        return sorted(dict_paths_to_order, key=lambda elem: len(elem), reverse=True)

    def build_sorted_hierarchy(self, dictionary, not_ordered_paths_list):
        self.get_dict_hierarchy(dictionary, not_ordered_paths_list, ())
        ordered_paths_list = self.order_dict_paths(not_ordered_paths_list)

        return ordered_paths_list

    @staticmethod
    def treat_empty_dict_elem(path_in_dict_list):
        indexes_list = [idx for idx, item in enumerate(path_in_dict_list) if isinstance(item, dict)]
        if indexes_list:
            additional_indexes = list()
            for idx in indexes_list:
                additional_indexes.append(idx-1)
            indexes_list.extend(additional_indexes)
            path_in_dict_list = [item for idx, item in enumerate(path_in_dict_list) if idx not in indexes_list]

        return path_in_dict_list

    @staticmethod
    def append_and_remove_duplicates(list_to_update, elem_to_append):
        local_list = copy.deepcopy(list_to_update)
        local_list.append(elem_to_append)
        local_list = list(set(local_list))

        return local_list

    @staticmethod
    def get_by_path(root, items):
        """Access a nested object in root by item sequence."""
        return reduce(operator.getitem, items, root)

    def set_by_path(self, root, items, value):
        """Set a value in a nested object in root by item sequence."""
        self.get_by_path(root, items[:-1])[items[-1]] = value

    def del_by_path(self, root, items):
        """Delete a key-value in a nested object in root by item sequence."""
        del self.get_by_path(root, items[:-1])[items[-1]]




