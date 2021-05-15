#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from psutil import Process, pid_exists
import sys


def define_parser_with_arguments():
    description_text = "Prints different information about the given <PROCESS_ID> \
                        \nor if none given the current process.\
                        \nIf no option is given it is assumed that\
                        \nall options were given."

    parser = ArgumentParser(description=description_text,
                            formatter_class=RawDescriptionHelpFormatter,
                            usage="%(prog)s [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]")

    pid_help_str = "Show a list of all the parent process ids of the given <PROCESS_ID>."
    parser.add_argument('-p', '--pid', action='store_true', help=pid_help_str)

    homefolder_help_str = "Show the path to the process owner‘s homefolder."
    parser.add_argument('-f', '--homefolder', action='store_true', help=homefolder_help_str)

    parser.add_argument("[<PROCESS_ID>]", nargs='?', default=Process().pid, type=int)
    return parser


def get_given_process_and_parent_info_as_list_of_dicts(pid: int, wanted_info: list[str]) -> list[dict]:
    # ['ppid', 'name', 'username', 'pid', 'cwd', 'status']
    current_pid = pid
    process_info = []
    while True:
        process_info += [Process(current_pid).as_dict(attrs=wanted_info)]
        if current_pid == 1:
            break
        current_pid = process_info[-1]['ppid']
    return process_info


def print_homefolder_of_process_owner(username, pid):
    if username == 'root':
        return sys.stdout.write("/root/")
    else:
        return sys.stdout.write(Process(pid).cwd() + "\n")


def print_all_PPIDs_as_list(list_of_dicts):
    parent_pids = []
    for element in list_of_dicts:
        parent_pids.append(element['ppid'])
    parent_pids.pop()
    sys.stdout.write(str(parent_pids) + "\n")


def check_for_invalid_flags():
    valid_flags = ['-p', "--pid", "-f", "--homefolder", "-h", "--help"]
    for flag in sys.argv[1:]:
        if (flag not in valid_flags) and not flag.isalnum():
            sys.stderr.write("Invalid Argument found!\n")
            exit()


def _set_pid(dest_attr, argv_length):
    if len(sys.argv) == argv_length:
        pid_if_given = sys.argv[-1]
        if pid_exists(int(pid_if_given)):
            args.__setattr__(dest_attr, pid_if_given)
            return pid_if_given
        else:
            sys.stderr.write("Invalid PID!\n")
            exit()
    elif len(sys.argv) < argv_length:
        pid_if_none_given = parser.get_default("[<PROCESS_ID>]")
        args.__setattr__(dest_attr, pid_if_none_given)
        sys.argv.append(pid_if_none_given)
    return pid_if_none_given


def determine_arguments_and_flags_given():
    if not args.pid and not args.homefolder:
        _set_pid('pid', 2)
        _set_pid('homefolder', 2)
        return ["p", "f"]
    elif args.pid and not args.homefolder:
        _set_pid('pid', 3)
        return ["p"]
    elif not args.pid and args.homefolder:
        _set_pid('homefolder', 3)
        return ["f"]
    elif args.pid and args.homefolder:
        _set_pid('pid', 4)
        _set_pid('homefolder', 4)
        return ["p", "f"]


def choose_action_to_do(given_flags):
    for flag in given_flags:
        if flag == "f":
            username = Process(int(args.homefolder)).username()
            print_homefolder_of_process_owner(username, int(args.homefolder))

        if flag == "p":
            dict_of_processes = get_given_process_and_parent_info_as_list_of_dicts(int(args.pid), ['pid', 'ppid'])
            print_all_PPIDs_as_list(dict_of_processes)


if __name__ == "__main__":
    check_for_invalid_flags()
    parser = define_parser_with_arguments()
    args = parser.parse_args()
    given_flags = determine_arguments_and_flags_given()
    choose_action_to_do(given_flags)
