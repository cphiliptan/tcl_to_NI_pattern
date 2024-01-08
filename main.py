# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def open_file(file_name):
    print(f'Opening File: {file_name}')

    file1 = open(file_name, 'r')
    all_lines = file1.readlines()

    count = 0

    line_list = []
    # Strips the newline character
    for line in all_lines:
        count += 1
        line = line.strip()

        # pattern = r"^[wW]"
        # pattern = r"^[wW]"
        pattern = r"^[wW]\s+(\w+)\s+(\w+);"

        match = re.search(pattern, line)
        if match:
            line_list.append(line)
            print(line)

            arg1 = match.group(1)
            arg2 = match.group(2)
            print(f"1st argument: {arg1}, 2nd argument: {arg2}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    open_file('TS_test.tcl')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
