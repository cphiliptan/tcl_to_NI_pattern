# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import numpy as np
# import pandas as pd
import re

cmd_add_data_list = []
tset_SPI: float = 250e-6
tRead: float = 100e-6
tWait: float = 100e-6


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

        pattern = r"wait\s+(\d+);"
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            line_list.append(line)
            print("//" + line)

            arg1 = int(match.group(1), 16)
            arg2 = 0
            # print(f"{arg1} {arg2}\n")

            cmd_add_data_list.append(["wait", arg1, arg2])


def write_spi(add, m_data):
    # write function
    # out_string = ""

    print(f"// write to address: 0x{add:02x} | 0x80")

    # NCS setup start
    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = (time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)

    ncs = 0
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = ("\t\t\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)
    # NCS setup end

    ncs = 0
    sclk = 0
    mosi = 0
    miso = "X"

    wr_address = add | 0x80
    for bit in range(7, -1, -1):  # 7 to 0
        mosi = (wr_address & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        time_set_name = '\t\t'
        if bit == 7:
            time_set_name = 'tset_SPI'
        out_string = (time_set_name + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)
    # sclk = 1
    # out_string = ("tRead" + "\t\t" +
    #               str(ncs) + "\t" +
    #               str(sclk) + "\t" +
    #               str(mosi) + "\t" +
    #               str(miso) + ";")
    # print(out_string)
    sclk = 0
    print(f"// write data: 0x{m_data:02x} ")
    for bit in range(7, -1, -1):  # 7 to 0
        mosi = (m_data & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        time_set_name = '\t\t'
        if bit == 7:
            time_set_name = 'tset_SPI'
        out_string = (time_set_name + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)

    ncs = 0
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = (time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)

    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = ("\t\t\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)


def read_spi(add, m_data):
    # write function
    # out_string = ""

    print(f"// read address: 0x{add:02x}")
    # wr_address = add | 0x80
    wr_address = add

    # NCS setup start
    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = (time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)

    ncs = 0
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = ("\t\t\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)
    # NCS setup end

    ncs = 0
    sclk = 0
    mosi = 0
    miso = "X"
    for bit in range(7, -1, -1):  # 7 to 0
        mosi = (wr_address & pow(2, bit)) >> bit
        # NCS SCLK MOSI MISO
        time_set_name = '\t\t'
        if bit == 7:
            time_set_name = 'tset_SPI'
        out_string = (time_set_name + "\t" +
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
        if miso:
            miso = 'H'
        else:
            miso = 'L'
        # NCS SCLK MOSI MISO
        time_set_name = '\t\t'
        if bit == 7:
            time_set_name = 'tset_SPI'
        out_string = (time_set_name + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)

    ncs = 0
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = (time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)

    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = 2
    time_set_name = 'tset_SPI'
    out_string = ("\t\t\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)


def wait_spi(wait_time_ms):
    # write function
    # out_string = ""
    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = int(wait_time_ms / tWait)

    print(f"// wait_time: {wait_time_ms:d} repeat: {repeat_num:d}")
    out_string = (f'repeat({repeat_num})' + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)


def halt_spi():
    # write function
    # out_string = ""
    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    out_string = ('halt' + "\t" +
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

    print('// tset_SPI:', tset_SPI * 1e6, 'nS')
    print('// tRead:', tRead * 1e6, 'nS')
    print('//NCS\tSCLK\tMOSI\tMISO')
    for cmd in cmd_add_data_list:
        if cmd[0] == 'w':
            write_spi(cmd[1], cmd[2])
        if cmd[0] == 'r':
            read_spi(cmd[1], cmd[2])
        if cmd[0] == 'wait':
            wait_spi(cmd[1])

    halt_spi()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
