import copy
import os
from utils.filehandling import FileHandling
import constants as csts
import boschlibparserarxmlutils.autosar_lib_4_3_0 as autosarlib
import json
import inspect
import deepdiff
import re
from utils.error_beautifier import ErrorBeautifier
from confmanager_modes.confmanager_modes_common import CommonModeUtils
import xmltodict
from lxml import etree
import dictdiffer
import collections


class MergerMode:

    def __init__(self, pver_root, merged_files_folder, logger):
        """
        Constructor of the class
        :param pver_root:
        :param merged_files_folder:
        :param logger:
        """
        self.logger = logger
        self.file_handling_obj = FileHandling(self.logger)
        self.pver_root = self.file_handling_obj.check_if_folder_exists(pver_root)
        self.merged_files_folder = self.file_handling_obj.check_if_folder_exists(merged_files_folder)
        self.additional_log_files_folder = (self.file_handling_obj.
                                            check_if_folder_exists(os.path.join(self.merged_files_folder, 'logs')))
        self.files_to_merge_path_list = list()
        self.right_side_dict = dict()
        self.left_side_dict = dict()
        self.updates_list = list()
        self.paths_already_treated_list = list()
        self.error_beautifier_obj = ErrorBeautifier(self.logger)
        self.modes_common_obj = CommonModeUtils(self.logger)

    def merge_files(self, target_file, files_to_merge_path_list):
        self.files_to_merge_path_list = files_to_merge_path_list
        # Read all inputs to merge: if there are no input files or there is only one file, return
        if not self.modes_common_obj.check_if_enough_files_for_merge(files_to_merge_path_list):
            return
        else:
            self.logger.info("Reading %s" % (self.files_to_merge_path_list[0]))
            self.left_side_dict[csts.root_main_tag] = {}
            (left_root,
             self.left_side_dict[csts.root_main_tag]) = self.parse_and_get_dico(self.files_to_merge_path_list[0])

            raw_left_side_paths = list()
            left_side_paths = self.modes_common_obj.build_sorted_hierarchy(self.left_side_dict, raw_left_side_paths)

            for index, arxml_file_path in enumerate(self.files_to_merge_path_list):
                if index > 0:
                    self.logger.info("Reading %s" % (arxml_file_path))
                    # Build right side dictionary from both side
                    self.right_side_dict[csts.root_main_tag] = {}
                    (right_root,
                     self.right_side_dict[csts.root_main_tag]) = self.parse_and_get_dico(arxml_file_path)
                    # Update Left XML
                    self.update_xml(left_root, right_root, left_side_paths)
                    self.paths_already_treated_list = list()

            # Create a new file
            self.modes_common_obj.export_merged_file(os.path.join(self.merged_files_folder, target_file), left_root)

            return left_root, self.left_side_dict

    def parse_and_get_dico(self, filepath_to_parse):
        # TODO: possible improvement => beautify errors to improve user comprehension
        # try:
        #     left_root = autosarlib.parse(self.files_to_merge_path_list[0], silence=True)
        # except autosarlib.parse as err:
        #     self.error_beautifier_obj.beautify_lxml_parse_errors(err)
        xml_root = autosarlib.parse(filepath_to_parse, silence=True)
        xml_dict = self.build_xml_dict(xml_root)

        return xml_root, xml_dict

    def update_xml(self, left_side_root, right_side_root, left_side_paths):
        """
        This method will check updates and modify the xml
        :param left_side_root:
        :param right_side_root:
        :param left_side_paths:
        :return:
        """
        self.logger.info("Checking differences")
        delta_left_right = deepdiff.DeepDiff(self.left_side_dict, self.right_side_dict)

        for update_detected in delta_left_right.keys():
            # dictionary_item_added : complete block to add to left
            # dictionary_item_removed : to ignore, there are things not found in right
            # values_changed : potentially a new element to add to left (start with this assumption)
            if update_detected != "dictionary_item_removed":
                # check if value is a list or a dict
                # values_changed is a dictionary,
                # dictionary_item_added and dictionary_item_removed are prettyOrderedSet ("other thing")
                self.updates_list = list()
                if isinstance(delta_left_right[update_detected], dict):
                    self.updates_list = list(delta_left_right[update_detected].keys())
                else:
                    self.updates_list = list(delta_left_right[update_detected])

                for xmldiff_path_to_element in self.updates_list:
                    self.insert_element_in_xml(xmldiff_path_to_element,
                                               left_side_root,
                                               right_side_root,
                                               left_side_paths)

    def insert_element_in_xml(self, xmldiff_path_to_element, left_side_root, right_side_root, left_side_paths):
        """
        This method will insert element in xml
        :param right_side_dict:
        :param xmldiff_path_to_element:
        :param left_side_root:
        :param right_side_root:
        :return:
        """
        (r_xml_path_parts,
         r_xml_paths,
         dict_path_paths,
         dict_path_parts) = self.xmldiff_path_to_xml_path(xmldiff_path_to_element)
        all_checks_ok, index_check_nok = self.check_tags(dict_path_paths)

        if not all_checks_ok:
            # Root will change
            dict_path_parts = dict_path_paths[index_check_nok].split(".")
            del r_xml_paths[index_check_nok + 1:]
            del dict_path_paths[index_check_nok + 1:]

        # Check if r_xml_path is in self.paths_already_treated_list or not
        # TODO : After improving self.check_existing_element to reduce execution time, those lines must be uncommented
        # left_side_paths_wo_indexes = self.build_dict_path_wo_indexes(left_side_paths)
        # _ = self.check_existing_element(dict_path_paths[index_check_nok], left_side_paths_wo_indexes)

        if r_xml_paths[index_check_nok] not in self.paths_already_treated_list:
            root_to_insertion_path = self.modes_common_obj.convert_dict_to_xml(".".join(dict_path_parts[:-1]))
            r_element_name_to_insert = self.modes_common_obj.convert_dict_to_xml(dict_path_parts[-1])
            left_root_of_insertion = eval("left_side_root." + root_to_insertion_path)

            insertion_method = self.get_insertion_method_name(left_root_of_insertion, r_element_name_to_insert)

            if insertion_method is not None:
                if r_xml_paths[index_check_nok] not in self.paths_already_treated_list:
                    self.paths_already_treated_list = (self.modes_common_obj.
                                                       append_and_remove_duplicates(self.paths_already_treated_list,
                                                                                    r_xml_paths[index_check_nok]))

                r_element_to_insert = eval("right_side_root." + r_xml_paths[-1])

                eval("left_root_of_insertion." + insertion_method + "(r_element_to_insert)")

                # Update left side dictionary
                r_elem_to_insert_in_dict_items = [csts.root_main_tag] + dict_path_parts
                root_to_insertion_dict = [csts.root_main_tag] + dict_path_parts[:-1] + [r_element_name_to_insert]
                self.modes_common_obj.set_by_path(self.left_side_dict,
                                                  root_to_insertion_dict,
                                                  self.modes_common_obj.get_by_path(self.right_side_dict,
                                                                                    r_elem_to_insert_in_dict_items))
            else:
                self.logger.warning("Insertion method for " + r_element_name_to_insert + " not found")

    def get_insertion_method_name(self, root_of_element_to_insert, element_to_insert):
        """
        This method search the class method insertion name. According with element type, it could be "add_xxx" or
        "get_xxx"
        :param root_of_element_to_insert:
        :param element_to_insert:
        :return:
        """
        element_to_insert = csts.find_xml_index_compiled.sub('', element_to_insert)
        methods_tuple_list = inspect.getmembers(root_of_element_to_insert, inspect.ismethod)

        insertion_method_tuple = list(filter(lambda method_tuple: self.filter_insertion_method_name(element_to_insert,
                                                                                                    method_tuple),
                                             methods_tuple_list))
        return insertion_method_tuple[0][0]

    @staticmethod
    def filter_insertion_method_name(element_to_insert, method_tuple):
        return (re.search(element_to_insert, method_tuple[0]) is not None and
                (method_tuple[0].startswith("add_") or method_tuple[0].startswith("set_")))

    def check_tags(self, elem_xml_paths):
        """
        Check if tags are present and have similar values in left side and right side dictionaries.
        The goal is to find the last common index to be able to get the root of the potential new element to be
        inserted in left side
        :param elem_xml_paths:
        :return:
        """
        check_result = True

        for index, elem_xml_dict_path in enumerate(elem_xml_paths[:-1]):
            right_side_path_tag_intersection = tuple(set(elem_xml_dict_path) & set(csts.tags_to_check))
            for tag_name in csts.tags_to_check:
                r_value_of_tag = eval("self.right_side_dict['AUTOSAR']['" +
                                      self.xml_path_to_dict_path(elem_xml_dict_path) +
                                      ".get('" +
                                      tag_name + "')")

                if r_value_of_tag is not None:
                    l_value_of_tag = eval("self.left_side_dict['AUTOSAR']['" +
                                          self.xml_path_to_dict_path(elem_xml_dict_path) +
                                          ".get('" +
                                          tag_name + "')")

                    if l_value_of_tag != r_value_of_tag:
                        check_result = False
                        return check_result, index
                    else:
                        check_result = True

        return check_result, -1

    @staticmethod
    def xml_path_to_dict_path(xml_path):
        """
        Convert xml paths to dictionary paths
        :param xml_path:
        :return:
        """
        return xml_path.replace(".", "']['") + "']"

    def check_existing_element(self, path_to_be_checked, left_side_paths):
        check_element_exists = False

        complete_dict_path = eval("self.right_side_dict['AUTOSAR']['" + self.xml_path_to_dict_path(path_to_be_checked))
        flag_is_dict = isinstance(complete_dict_path, dict)

        path_where_check_tags = path_to_be_checked
        if flag_is_dict:
            path_where_check_tags = complete_dict_path

        tag_found_result = self.find_string_in_path(path_where_check_tags, csts.tags_to_check)

        self.find_intersection_left_right(flag_is_dict,
                                          tag_found_result,
                                          left_side_paths,
                                          complete_dict_path,
                                          path_to_be_checked)

        return check_element_exists

    def build_dict_path_wo_indexes(self, dico_paths):
        left_side_paths_wo_indexes = list()
        for element in dico_paths:
            # element is tuple
            element_list = list(element)
            # Remove indexes, except for last two elements of path
            element_wo_indexes_list = [csts.find_dict_index_compiled.sub('', sub_element) for sub_element in element_list[:-2]]
            element_wo_indexes_list.extend(element_list[-2:])
            element_wo_indexes_list = self.modes_common_obj.treat_empty_dict_elem(element_wo_indexes_list)

            left_side_paths_wo_indexes.append(tuple(element_wo_indexes_list))

        return left_side_paths_wo_indexes

    @staticmethod
    def find_string_in_path(path_to_check, list_of_strings):
        found_result = [string_elem in path_to_check for string_elem in list_of_strings]
        return found_result

    @staticmethod
    def build_path_wo_indexes_and_tag_info(path_parts, tag_name, tag_value):
        path_parts_new = [csts.find_dict_index_compiled.sub('', part) for part in path_parts]
        path_wo_indexes = tuple([csts.root_main_tag] + path_parts_new +
                                [tag_name, tag_value])
        return path_wo_indexes

    def find_intersection_left_right(self, flag_is_dict, found_result, left_side_paths_wo_indexes,
                                     complete_dict_path, path_to_be_checked):
        if any(found_result):
            # In this case, it's a string, and tag is part of it
            tag_name = csts.tags_to_check[found_result.index(True)]
            r_value_of_tag = complete_dict_path

            if flag_is_dict:
                r_value_of_tag = eval("complete_dict_path['" + tag_name + "']")

            # Remove all indexes _<number>
            if r_value_of_tag is not None:
                r_path_parts = path_to_be_checked.split(".")

                if not flag_is_dict:
                    r_path_parts.pop()
                # Remove all indexes _<number>
                r_path_wo_indexes = self.build_path_wo_indexes_and_tag_info(r_path_parts, tag_name, r_value_of_tag)
                left_side_intersection = tuple({r_path_wo_indexes} & set(left_side_paths_wo_indexes))

                if left_side_intersection:
                    r_path_parts_modified = [csts.find_dict_index_compiled.sub(r'[\1]', part) for part in r_path_parts]
                    path_to_append = ".".join(r_path_parts_modified)
                    self.paths_already_treated_list = (self.modes_common_obj.
                                                       append_and_remove_duplicates(self.paths_already_treated_list,
                                                                                    path_to_append))

    def xmldiff_path_to_xml_path(self, xmldiff_path_dict):
        """
        This method converts xmldiff path in autosar_lib_xxx.py (generateDS) path
        :param xmldiff_path_dict:
        :return:
        """
        xmldiff_path_dict_parts = list(
            map(lambda x: x.replace("'", "").replace("]", ""), xmldiff_path_dict.split('][')))
        xmldiff_path_dict_parts.pop(0)

        xml_path_parts = list(map(self.modes_common_obj.convert_dict_to_xml, xmldiff_path_dict_parts))

        dict_path_subpaths = []
        last_path = ".".join(xmldiff_path_dict_parts)

        for index, xml_path_fraction in enumerate(xmldiff_path_dict_parts):
            search_index_xml_element = re.search("_\d+", xml_path_fraction)
            if search_index_xml_element:
                # Index will be always at the end of the tag
                dict_path_subpaths.append(".".join(xmldiff_path_dict_parts[:index + 1]))

        if last_path not in dict_path_subpaths:
            dict_path_subpaths.append(last_path)

        xml_paths = list(map(self.modes_common_obj.convert_dict_to_xml, dict_path_subpaths))

        return xml_path_parts, xml_paths, dict_path_subpaths, xmldiff_path_dict_parts

    def get_attributes(self, root, attributes_dict):
        """
        This method will find tags of xml. Tags are class attribute tuples that follow some criteria:
        * First tuple element (attribute name) always in upper case and don't end with _nsprefix_
        * Second tuple element (attribute content) is not empty
        :param root:
        :param attributes_dict:
        :return:
        """
        raw_attributes_list = inspect.getmembers(root)

        attributes_list = list(filter(self.filter_attributes, raw_attributes_list))

        for index, attribute in enumerate(attributes_list):
            self.treat_attributes(attribute, attributes_dict, root)

    @staticmethod
    def filter_attributes(attribute):
        """
        This method is a filter for attributes
        :param attribute:
        :return:
        """
        return (not attribute[0].endswith('_nsprefix_') and
                attribute[0].isupper() and
                attribute[1] is not None and attribute[1])

    def treat_attributes(self, attribute, attributes_dict, root):
        # valueOf_ means that it's a single attribute (string)
        if hasattr(attribute[1], "valueOf_"):
            attributes_dict[attribute[0]] = attribute[1].valueOf_
        # Attributes that end with "S" : they have elements inside (lists)
        elif attribute[0].endswith("S"):
            if attribute[0] not in attributes_dict:
                attributes_dict[attribute[0]] = {}

            if isinstance(attribute[1], list):
                self.attribute_as_list(root, attribute, attributes_dict)
            else:
                self.get_attributes(eval("root." + attribute[0]), attributes_dict[attribute[0]])
        # Some attributes don't end with "S" but they have elements inside
        elif isinstance(attribute[1], list):
            self.attribute_as_list(root, attribute, attributes_dict)
        # Other cases, not yet treated or partially treated
        else:
            if attribute[0] not in attributes_dict:
                attributes_dict[attribute[0]] = {}
            self.get_attributes(attribute[1], attributes_dict[attribute[0]])

    def attribute_as_list(self, root, attribute, attributes_dict):
        for index_attr, attr in enumerate(attribute[1]):
            attributes_dict[attribute[0] + "_" + str(index_attr)] = {}
            self.get_attributes((eval("root." + attribute[0]))[index_attr],
                                attributes_dict[attribute[0] + "_" + str(index_attr)])

    def build_xml_dict_(self, xml_root):
        parent_ar_package = xml_root.AR_PACKAGES
        root_dict = dict()
        root_dict['AR_PACKAGES'] = {}

        if parent_ar_package is not None:
            ar_package_list = parent_ar_package.AR_PACKAGE
            root_dict['AR_PACKAGES'] = {}
            for index, sub_ar_package in enumerate(ar_package_list):
                root_dict['AR_PACKAGES']['AR_PACKAGE' + "_" + str(index)] = {}
                self.get_attributes(ar_package_list[index],
                                    root_dict['AR_PACKAGES']['AR_PACKAGE' + "_" + str(index)])

        return root_dict

    def build_xml_dict(self, xml_root):
        root_lxml = xml_root.to_etree(None, name_="AUTOSAR", mapping_={}, nsmap_=csts.nsmap1)
        xml_string = etree.tostring(root_lxml, pretty_print=True, encoding='utf-8', method="xml"
                                    ).decode('utf-8')
        # convert xml into dict
        xml_dict = xmltodict.parse(xml_string)

        # transform dict into current dict format => this transformation will be used until to find a way to adapt the
        # strategy to new format
        new_xml_dict = dict()
        self.transform_dict(xml_dict[csts.root_main_tag], new_xml_dict)

        return new_xml_dict

    def transform_dict(self, base_dictionary, new_dictionary):
        for key, value in base_dictionary.items():
            # Rename key
            new_key = key.replace("-", "_")

            if isinstance(value, dict):
                # there is only one element
                self.transform_value_if_dict(key, value, new_dictionary, base_dictionary)
            elif isinstance(value, list):
                # more than one element
                self.transform_value_if_list(key, value, new_dictionary)
            elif value is None:
                new_dictionary[new_key] = dict()
            else:
                if not key.startswith('@'):
                    new_dictionary[new_key] = base_dictionary[key]

    def transform_value_if_dict(self, key, value, new_dictionary, base_dictionary):
        new_key = key.replace("-", "_")
        if '#text' in value.keys():
            new_dictionary[new_key] = base_dictionary[key]['#text']
        else:
            if ((not key.endswith("S") and
                 not key.endswith("REF") and
                 key != 'TYPE-MAPPING' and
                 key != 'SENDER-REC-RECORD-TYPE-MAPPING') or
                    (key == 'ECUC-MODULE-CONFIGURATION-VALUES')):
                new_key = "_".join([new_key, "0"])
            new_dictionary[new_key] = dict()
            self.transform_dict(value, new_dictionary[new_key])

    def transform_value_if_list(self, key, value, new_dictionary):
        for index, elem in enumerate(value):
            new_key = "_".join([key.replace("-", "_"), str(index)])
            new_dictionary[new_key] = dict()
            self.transform_dict(elem, new_dictionary[new_key])

