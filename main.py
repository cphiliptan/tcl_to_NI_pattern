# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import pandas as pd
import re

cmd_add_data_list = []


def open_file(file_name):
    print(f'// Opening File: {file_name}')

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
            print("//" + line)

            arg1 = int(match.group(1), 16)
            arg2 = int(match.group(2), 16)
            # print(f"{arg1} {arg2}\n")

            cmd_add_data_list.append(["w", arg1, arg2])

        pattern = r"^[rR]\s+(\w+)\s+(\w+);"
        match = re.search(pattern, line)
        if match:
            line_list.append(line)
            print("//" + line)

            arg1 = int(match.group(1), 16)
            arg2 = int(match.group(2), 16)
            # print(f"{arg1} {arg2}\n")

            cmd_add_data_list.append(["r", arg1, arg2])


def write_spi(add, m_data):
    # write function
    out_string = ""
    ncs = 0
    sclk = 0
    mosi = 0
    miso = "X"
    print(f"// write to address: 0x{add:02x} | 0x80")
    wr_address = add | 0x80
    for bit in range(7, -1, -1):  # 7 to 0
        mosi = (wr_address & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        out_string = ("tset_SPI" + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)
    sclk = 1
    out_string = ("tRead" + "\t\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)
    sclk = 0
    print(f"// write data: 0x{m_data:02x} ")
    for bit in range(7, -1, -1):  # 7 to 0
        mosi = (m_data & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        out_string = ("tset_SPI" + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)


def read_spi(add, m_data):
    # write function
    out_string = ""
    ncs = 0
    sclk = 0
    mosi = 0
    miso = "X"
    print(f"// read address: 0x{add:02x}")
    # wr_address = add | 0x80
    wr_address = add
    for bit in range(7, -1, -1):  # 7 to 0
        mosi = (wr_address & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        out_string = ("tset_SPI" + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)
    sclk = 1
    out_string = ("tRead" + "\t\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)
    sclk = 0
    mosi = 0
    print(f"// read data: 0x{m_data:02x} ")
    for bit in range(7, -1, -1):  # 7 to 0
        miso = (m_data & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        out_string = ("tset_SPI" + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    open_file('TS_test.tcl')
    # print(*cmd_add_data_list, sep="\n")

    action = cmd_add_data_list[0][0]
    address = cmd_add_data_list[0][1]
    data = cmd_add_data_list[0][2]

    for cmd in cmd_add_data_list:
        if cmd[0] == 'w' or cmd[0] == 'W':
            write_spi(cmd[1], cmd[2])
        if cmd[0] == 'r' or cmd[0] == 'R':
            read_spi(cmd[1], cmd[2])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
