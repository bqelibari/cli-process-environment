#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from psutil import Process, pid_exists
import sys


def define_parser_with_flags_as_bool():
    description_text = "Prints different information about the given <PROCESS_ID> or if none given the current process.\
                        \nIf no option is given it is assumed that all options were given."

    parser = ArgumentParser(description=description_text,
                            formatter_class=RawDescriptionHelpFormatter,
                            usage="%(prog)s [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]")

    pid_help_str = "Show a list of all the parent process ids of the given <PROCESS_ID>."
    parser.add_argument('-p', '--pid', action='store_true', help=pid_help_str)

    homefolder_help_str = "Show the path to the process owner‘s homefolder."
    parser.add_argument('-f', '--homefolder', action='store_true', help=homefolder_help_str)

    parser.add_argument("[<PROCESS_ID>]", nargs='?', default=Process().pid, type=int)
    return parser


def check_for_invalid_flags():
    valid_flags = ['-p', "--pid", "-f", "--homefolder", "-h", "--help"]
    for flag in sys.argv[1:]:
        if (flag not in valid_flags) and not flag.isalnum():
            sys.stderr.write("\nINVALID FLAG!\n\n\n")
            parser.exit(status=0, message=print_error_message("\nINVALID FLAG!\n\n"))
            exit()


def determine_arguments_and_set_flag_values(args):
    if not args.pid and not args.homefolder:
        _set_pid('pid', 2)
        _set_pid('homefolder', 2)
    elif args.pid and not args.homefolder:
        _set_pid('pid', 3)
    elif not args.pid and args.homefolder:
        _set_pid('homefolder', 3)
    elif args.pid and args.homefolder:
        _set_pid('pid', 4)
        _set_pid('homefolder', 4)


def _set_pid(destination_attr, argv_length):
    pid_given = len(sys.argv) == argv_length
    pid_not_given = len(sys.argv) < argv_length
    if pid_given:
        pid = sys.argv[-1]
        if pid_exists(int(pid)):
            args.__setattr__(destination_attr, pid)
        else:
            parser.exit(status=0, message=print_error_message("\nTHERE IS NO SUCH PID!\n\n"))
    elif pid_not_given:
        pid = parser.get_default("[<PROCESS_ID>]")
        args.__setattr__(destination_attr, pid)


def get_given_process_and_parent_info_as_list_of_dicts(pid: int, attrs_to_retrieve: list[str]) -> list[dict]:
    current_pid = pid
    process_info = []
    while True:
        process_info += [Process(current_pid).as_dict(attrs=attrs_to_retrieve)]
        if current_pid == 1:
            break
        current_pid = process_info[-1]['ppid']
    return process_info


def print_all_PPIDs_as_list(list_of_dicts):
    parent_pids = []
    for element in list_of_dicts:
        parent_pids.append(element['ppid'])
    parent_pids.pop()
    sys.stdout.write(str(parent_pids) + "\n")


def print_homefolder_of_process_owner(username, pid):
    if username == 'root':
        return sys.stdout.write("/root/\n")
    else:
        return sys.stdout.write(Process(pid).cwd() + "\n")


def print_output_based_on_set_flags(args):
    pid_flag_set = not isinstance(args.pid, bool)
    homefolder_flag_set = not isinstance(args.homefolder, bool)
    if pid_flag_set:
        list_containing_dicts_of_pids = get_given_process_and_parent_info_as_list_of_dicts(int(args.pid), ['pid', 'ppid'])
        print_all_PPIDs_as_list(list_containing_dicts_of_pids)
    if homefolder_flag_set:
        username = Process(int(args.homefolder)).username()
        print_homefolder_of_process_owner(username, int(args.homefolder))


def print_error_message(error_str):
    print(f"{error_str}"
          f"Please make sure your command consists of following Arguments and Flags:\n\n"
          f"{sys.argv[0]} [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]\n"
          f"Please type: {sys.argv[0]} [-h] for additional information.\n")


if __name__ == "__main__":
    check_for_invalid_flags()

    parser = define_parser_with_flags_as_bool()
    args = parser.parse_args()

    determine_arguments_and_set_flag_values(args)
    print_output_based_on_set_flags(args)
