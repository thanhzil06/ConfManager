import argparse

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

arg = main_parser.parse_args()

parser = argparse.ArgumentParser(parents=[main_parser], add_help=False)

if arg.tool_mode == 'Merger':
    # Inputs for Merger mode
    pass
else:
    # Inputs for Updater mode
    parser.add_argument('-ws', '--workspace',
                            help='customer workspace',
                            required=arg.tool_mode,
                            dest='cust_ws')
args = parser.parse_args()