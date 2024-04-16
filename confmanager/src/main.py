from logger.loadlogconf import LoadLogconf
import argparse
import os
from config_handling.configuration_handling import ConfFileHandling
from utils.timer import Timer
from confmanager_modes.confmanager_merger import MergerMode
from confmanager_modes.confmanager_updater import UpdaterMode
from confmanager_modes.confmanager_modes_common import CommonModeUtils
from ecuc_partition_handling.ecuc_partition_updater import EcucPartitionUpdater
import sys
import constants as csts
import glob


@Timer
def main():
    try:
        # Read configuration file
        conf_handler_obj = ConfFileHandling(logger)
        conf_file_path_list = [args.conf_file_path]
        try:
            if conf_file_path_list:
                configuration_data = conf_handler_obj.read_json_configuration_file(conf_file_path_list)

                if args.tool_mode == 'Merger':
                    mode_merger(args.pver_root,
                                args.output_path,
                                configuration_data,
                                args.tool_mode,
                                logger)

                else:  # Mode Updater'
                    for topic in configuration_data.keys():
                        if topic == 'EcuPartition':                              
                            ecuc_partiton_updater(pver=args.pver_root, 
                                                  cust_ws=args.cust_ws, 
                                                  output=args.output_path,
                                                  main_logger=logger)                            
                        else: # Other use cases
                            mode_updater(args.pver_root,
                                        args.output_path,
                                        args.cust_ws,
                                        configuration_data,
                                        args.tool_mode,
                                        logger)
                                
            else:
                raise Exception
        except Exception as error:
            logger.error(error, exc_info=True)
            sys.exit(1)

    except Exception as e:
        logger.error('Unexpected error occurred : ' + str(e), exc_info=True)

def ecuc_partiton_updater(pver, cust_ws, output, main_logger):
    ecuc_partition_obj = EcucPartitionUpdater(pver_path=pver, 
                                              cust_path=cust_ws, 
                                              output_path= output, 
                                              logger=main_logger)
    ecuc_partition_obj.port_delta()

def mode_merger(pver_root, output_path, configuration_data, tool_mode, main_logger):
    """
    Mode Merger
    -----------

    This mode will merge two files and generate a new merged file

    Limitations
    The mode can handle more than two files, but there is a gap: detection of
    duplicated must be improved to have a clean merged file.
    """
    mode = tool_mode.lower()
    modes_common_obj = CommonModeUtils(main_logger)

    root_paths = [pver_root]
    tool_mode_obj = MergerMode(pver_root,
                               output_path,
                               main_logger)
    for topic in configuration_data.keys():
        (target_file,
         files_to_merge_path_list,
         _) = modes_common_obj.prepare_mode_inputs(mode,
                                                   topic,
                                                   configuration_data,
                                                   root_paths)
        # Merge mode does not need the return value of merge_files method
        _ = tool_mode_obj.merge_files(target_file, files_to_merge_path_list)


def mode_updater(pver_root, output_path, cust_ws, configuration_data, tool_mode, main_logger):
    """
    Mode Updater
    -----------

    This mode shall perform the following steps:
    1. Check if there are more than one configured input. If yes, it means that customer included
    additional information in other files than merged one; in this case, a merge must be done, and a
    merged file will be generated in output path and the dictionary used to create this file will be
    returned.
    Note: target_file name for Merge will be Updater target file name + "_merged" suffix
    If not, no merge operation will be perfomed and the old merged file already present in inputs
    will be copied in output path, parsed and transformed in a dict (merged_dict)
    2. Remove all information present in configured "to_ignore" list from merged file. Files in this
    list will be parsed and transformed in a dict. A delta will be performed, and elements in those
    files will be deleted from merged dict.
    3. A new file will be generated in output path.

    """
    mode = tool_mode.lower()
    modes_common_obj = CommonModeUtils(main_logger)
    root_paths = [cust_ws]
    merged_file_dict = dict()

    tool_mode_obj = UpdaterMode(pver_root,
                                output_path,
                                cust_ws,
                                main_logger)
    tool_merger_obj = MergerMode(pver_root,
                                 output_path,
                                 main_logger)

    for topic in configuration_data.keys():
        if topic != 'EcuPartition': 
            (target_file,
            files_to_merge_path_list,
            content_to_remove) = modes_common_obj.prepare_mode_inputs(mode,
                                                                    topic,
                                                                    configuration_data,
                                                                    root_paths)

            if modes_common_obj.check_if_enough_files_for_merge(files_to_merge_path_list):
                # Merge here
                # target_file must finish with "_merged"
                target_file_merge = target_file.replace(".arxml", "_merged.arxml")
                (merged_root,
                merged_file_dict) = tool_merger_obj.merge_files(target_file_merge,
                                                                files_to_merge_path_list)
                
            else:
                # Read the file in files_to_merge_path_list and get the dict
                if not files_to_merge_path_list:
                    main_logger.error("Paths for files listed in \"inputs\" are not found in input folders: please check "
                                    "your configuration file and your input folders")
                    return
                else:
                    (merged_root,
                    merged_file_dict[csts.root_main_tag]) = tool_merger_obj.parse_and_get_dico(files_to_merge_path_list[0])
            tool_mode_obj.update_files(target_file, merged_root, merged_file_dict, content_to_remove)
  

if __name__ == "__main__":
    main_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=('''Link to User guide: https://inside-docupedia.bosch.com/confluence/display/ECSTools/ConfManager\nAutosar XSD\t\t4-3-0\nAUTOSAR_MOD_ECUC\t4-5-0'''))

    main_parser.add_argument('-v', '--version', 
                             help='show program version', 
                             action='version', 
                             version='1.2.0')
    main_parser.add_argument('-m', '--mode',
                             help='modes = Merger, Updater',
                             choices=['Merger', 'Updater'],
                             required=True,
                             dest='tool_mode')
    main_parser.add_argument('-o', '--output',
                             help='folder where merged files and logs are generated',
                             required=True,
                             dest='output_path')
    main_parser.add_argument('-cf', '--conf',
                             help='configuration file path',
                             required=True,
                             dest='conf_file_path')
    main_parser.add_argument('-p', '--pver',
                             help='pver root',
                             required=True,
                             dest='pver_root')
    main_args, _ = main_parser.parse_known_args()

    parser = argparse.ArgumentParser(parents=[main_parser], add_help=False)

    if main_args.tool_mode == 'Merger':
        # Inputs for Merger mode
        pass
    else:
        # Inputs for Updater mode
        parser.add_argument('-ws', '--workspace',
                            help='customer workspace',
                            required=main_args.tool_mode,
                            dest='cust_ws')
    args = parser.parse_args()

    logger = LoadLogconf(logger_choice="dev", output_path=args.output_path).log

    main()
