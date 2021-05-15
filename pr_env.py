#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from psutil import Process, pid_exists
import sys


def define_parser_with_arguments():
    description_text = "Prints different information about the given <PROCESS_ID> \
                        \nor if none given the current process.\n\
                        If no option is given it is assumed that\
                        all options were given."

    parser = ArgumentParser(description=description_text,
                            formatter_class=RawDescriptionHelpFormatter,
                            usage="%(prog)s [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]")

    pid_help_str = "Show a list of all the parent process ids of the given <PROCESS_ID>."
    parser.add_argument('-p', '--pid', metavar="", type=int, help=pid_help_str)

    homefolder_help_str = "Show the path to the process owner‘s homefolder."
    parser.add_argument('-f', '--homefolder', metavar="", type=int, help=homefolder_help_str)

    parser.add_argument("[<PROCESS_ID>]", nargs='?', default=Process().pid, type=int)
    return parser


def get_given_process_and_parent_info_as_list_of_dicts(pid: int) -> list[dict]:
    current_pid = pid
    process_info = []
    while True:
        process_info += [Process(current_pid).as_dict(attrs=['ppid', 'name', 'username', 'pid', 'cwd', 'status'])]
        if current_pid == 1:
            break
        current_pid = process_info[-1]['ppid']
    return process_info


def print_homefolder_of_process_owner(username):
    if username == 'root':
        return print("/root/")
    else:
        return print(Process(pid).cwd())


def print_all_PPIDs_as_list(list_of_dicts):
    parent_pids = []
    for element in list_of_dicts:
        parent_pids.append(element['ppid'])
    parent_pids.pop()
    print(parent_pids)


def check_for_invalid_flags():
    valid_flags = ['-p', "--pid", "-f", "--homefolder"]
    for flag in sys.argv[1:]:
        if (flag not in valid_flags) and not flag.isalnum():
            sys.stderr.write("Invalid Argument found!\n")
            exit()


if __name__ == "__main__":
    check_for_invalid_flags()
    parser = define_parser_with_arguments()
    args = parser.parse_args()
    if len(sys.argv) == 1:
        pid = parser.get_default("[<PROCESS_ID>]")
        sys.argv.append(pid)
    else:
        pid = sys.argv[-1]
    if not isinstance(int(sys.argv[-1]), int):
        parser.error("PID must be an Integer")
    print(pid)
