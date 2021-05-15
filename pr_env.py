#!/usr/bin/env python
from argparse import ArgumentParser, RawDescriptionHelpFormatter, MetavarTypeHelpFormatter
from psutil import Process, pid_exists
import sys
from pathlib import Path
import subprocess


def define_parser_with_arguments():
    description_text = "Prints different information about the given <PROCESS_ID> \
                        \nor if none given the current process.\n\
                        If no option is given it is assumed that\
                        all options were given."

    parser = ArgumentParser(description=description_text,
                            formatter_class=MetavarTypeHelpFormatter,
                            usage="%(prog)s [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]")

    pid_help_str = "Show a list of all the parent process ids of the given <PROCESS_ID>."
    add_argument_to_parser(parser, '-p', '--pid', pid_help_str)

    homefolder_help_str = "Show the path to the process owner‘s homefolder."
    add_argument_to_parser(parser, '-f', '--homefolder', homefolder_help_str)
    return parser.parse_args()


def add_argument_to_parser(parser, short_flag, long_flag, help_str):
    parser.add_argument(short_flag, long_flag, help=help_str)


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


def format_and_print_PID_and_PPID_info(list_of_dicts):
    for element in list_of_dicts:
        print(f"PID: {element['pid']} | Name: {element['name']} | PPID: {element['ppid']} | "
              f"User:{element['username']} | Status: {element['status']}")


if __name__ == "__main__":
    args = define_parser_with_arguments()
    pid = int(sys.argv[-1])
    if args.homefolder:
        print_homefolder_of_process_owner(Process(pid).username())
    if args.pid:
        if not pid_exists(pid):
            print("Invalid <PROCESS-ID>")
        else:
            proc_info_list_of_dicts = get_given_process_and_parent_info_as_list_of_dicts(pid)
            format_and_print_PID_and_PPID_info(proc_info_list_of_dicts)
