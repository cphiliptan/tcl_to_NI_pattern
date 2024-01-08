# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import re

cmd_add_data_list = []


def open_file(file_name):
    print(f'Opening File: {file_name}')

    file1 = open(file_name, 'r')
    all_lines = file1.readlines()

    count = 0

    line_list = []
    # cmd_add_data_list = []

    # Strips the newline character
    for line in all_lines:
        count += 1
        line = line.strip()

        pattern = r"^[wW]\s+(\w+)\s+(\w+);"

        match = re.search(pattern, line)
        if match:
            line_list.append(line)
            print(line)

            arg1 = hex(int(match.group(1), 16))
            arg2 = hex(int(match.group(2), 16))
            # print(f"{arg1} {arg2}\n")

            cmd_add_data_list.append(["w", arg1, arg2])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    open_file('TS_test.tcl')
    print(*cmd_add_data_list, sep="\n")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
