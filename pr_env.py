#!/usr/bin/env python
import argparse
import psutil
import sys
from pathlib import Path
import subprocess


def define_parser_with_arguments():
    description_text = "Prints different information about the given <PROCESS_ID> \
\nor if none given the current process.\n\
If no option is given it is assumed that\
all options were given."

    parser = argparse.ArgumentParser(description=description_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     usage="%(prog)s [-h|--help] [-p|--pid] [-f|--homefolder] [<PROCESS_ID>]")

    parser.add_argument("-p", "--pid", type=int,
                        help="Show a list of all the parent process ids of the given <PROCESS_ID>.")
    parser.add_argument("-f", "--homefolder", type=str,
                        help="Show the path to the process owner‘s homefolder.")
    return parser.parse_args()


def get_user_name(child_pid):
    user_name = subprocess.run(["ps", "-o", "user=", "-p", "%i" % child_pid], capture_output=True, text=True)
    return user_name.stdout.replace("\n", "")


def get_given_process_info_as_list(pid: int) -> list[object]:
    return [psutil.Process(pid)]


def get_all_parents_info_as_list(pid: int) -> list[object]:
    return psutil.Process(pid).parents()


args = define_parser_with_arguments()

if __name__ == "__main__":
    pid = int(sys.argv[-1])
    if args.homefolder:
        user = get_user_name(int(pid))
        if user == "root":
            print("/root")
        else:
            print(str(Path.home()) + "/")
    if args.pid:
        if not psutil.pid_exists(pid):
            print("Invalid <PROCESS-ID>")
        else:
            process_info_list = get_given_process_info_as_list(pid) + get_all_parents_info_as_list(pid)
            print(process_info_list)
