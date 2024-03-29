# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import numpy as np
# import pandas as pd
import re
import os
from io import StringIO
import sys
from pathlib import Path
import glob

cmd_add_data_list = []
tset_SPI: float = 250e-9
tRead: float = 100e-9
tWait: float = 500e-9
file_format_version: float = 1.1
timeset = 'tset_SPI, tRead, tWait'

tsWrRad: float = 500e-9
tsRad: float = 2e-6
tsclk_ncs: float = 200e-9
tsww_tswr: float = 350e-9


def open_file(file_name_):
    print(f'// Opening File: {file_name_}')

    file1 = open(file_name_, 'r')
    all_lines = file1.readlines()

    count = 0

    line_list = []
    cmd_add_data_list.clear()

    # Strips the newline character
    for line in all_lines:
        count += 1
        line = line.strip()

        pattern = r"^[wW]\s+(\w+)\s+(\w+);"

        match = re.search(pattern, line)
        if match:
            line_list.append(line)
            print("// " + line)

            arg1 = int(match.group(1), 16)
            arg2 = int(match.group(2), 16)
            # print(f"{arg1} {arg2}\n")

            cmd_add_data_list.append(["w", arg1, arg2])

        pattern = r"^[rR]\s+(\w+)\s+(\w+);"
        match = re.search(pattern, line)
        if match:
            line_list.append(line)
            print("// " + line)

            arg1 = int(match.group(1), 16)
            arg2 = int(match.group(2), 16)
            # print(f"{arg1} {arg2}\n")

            cmd_add_data_list.append(["r", arg1, arg2])

        pattern = r"wait\s+([-+]?([0-9]*\.[0-9]+|[0-9]+));"
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            line_list.append(line)
            print("// " + line)

            # arg1 = int(match.group(1), 16)
            arg1 = float(match.group(1))
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
    time_set_name = 'tRead'
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
    time_set_name = 'tRead'
    out_string = (time_set_name + "\t" +
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
        # time_set_name = '\t\t'
        # if bit == 7:
        time_set_name = 'tset_SPI'
        out_string = (time_set_name + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)

    repeat_num = int(tsWrRad / tRead)
    sclk = 1
    out_string = (f'repeat({repeat_num})' + "\t" +
                  "tRead" + "\t" +
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
        # time_set_name = '\t\t'
        # if bit == 7:
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
    repeat_num = int(tsclk_ncs / tRead)
    time_set_name = 'tRead'
    out_string = (f'repeat({repeat_num})' + "\t" +
                  time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";" +
                  "//tsclk_ncs")
    print(out_string)

    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = int(tsww_tswr / tRead)
    time_set_name = 'tRead'
    out_string = (f'repeat({repeat_num})' + "\t" +
                  time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";" +
                  "//tsww_tswr" + "\n")
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
    time_set_name = 'tRead'
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
    time_set_name = 'tRead'
    out_string = (time_set_name + "\t" +
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
        # time_set_name = '\t\t'
        # if bit == 7:
        time_set_name = 'tset_SPI'
        out_string = (time_set_name + "\t" +
                      str(ncs) + "\t" +
                      str(sclk) + "\t" +
                      str(mosi) + "\t" +
                      str(miso) + ";")
        print(out_string)

    repeat_num = int(tsRad / tRead)
    sclk = 1
    out_string = (f'repeat({repeat_num})' + "\t" +
                  "tRead" + "\t" +
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
        # time_set_name = '\t\t'
        # if bit == 7:
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
    repeat_num = int(tsclk_ncs / tRead)
    time_set_name = 'tRead'
    out_string = (f'repeat({repeat_num})' + "\t" +
                  time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";" +
                  "//tsclk_ncs")
    print(out_string)

    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    repeat_num = int(tsww_tswr / tRead)
    time_set_name = 'tRead'
    out_string = (f'repeat({repeat_num})' + "\t" +
                  time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";" +
                  "//tsww_tswr" + "\n")
    print(out_string)


def wait_spi(wait_time_ms):
    # write function
    # out_string = ""
    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"

    wait_time_ms = wait_time_ms / 1e3
    repeat_num = int(wait_time_ms / tWait)
    time_set_name = 'tWait'

    # print(f"// wait_time: {wait_time_ms:d} repeat: {repeat_num:d}")
    print(f"// wait_time_ms: {wait_time_ms * 1e3} repeat: {repeat_num:d} tWait_ns: {tWait * 1e9}")
    out_string = (f'repeat({repeat_num})' + "\t" +
                  time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";" + "\n")
    print(out_string)


def halt_spi():
    # write function
    # out_string = ""
    ncs = 1
    sclk = 1
    mosi = 0
    miso = "X"
    time_set_name = 'tset_SPI'
    out_string = ('halt' + "\t" +
                  time_set_name + "\t" +
                  str(ncs) + "\t" +
                  str(sclk) + "\t" +
                  str(mosi) + "\t" +
                  str(miso) + ";")
    print(out_string)


def store_print_to_var(enable, _buffer):
    print_output = ''

    if enable:
        sys.stdout = _buffer
    else:
        print_output = _buffer.getvalue()  # store print value to this var
        sys.stdout = sys.__stdout__  # restore stdout to default for print()

    return print_output


def convert_tcl_to_pattern(file__name):
    # base_name, ext_name = os.path.splitext(file__name)
    base_name = Path(file__name).stem
    open_file(file__name)
    # print(*cmd_add_data_list, sep="\n")

    # buffer = StringIO()
    # sys.stdout = buffer
    buffer = StringIO()
    store_print_to_var(True, buffer)

    print(f'file_format_version {file_format_version};')
    print(f'timeset {timeset};')
    print(f'pattern {base_name}(_3, _0, _1, _2)' + '\n{')

    print('// tset_SPI:', tset_SPI * 1e9, 'nS')
    print('// tRead:', tRead * 1e9, 'nS')
    print('// tWait:', tWait * 1e9, 'nS')
    print('//NCS\tSCLK\tMOSI\tMISO')
    for cmd in cmd_add_data_list:
        if cmd[0] == 'w':
            write_spi(cmd[1], cmd[2])
        if cmd[0] == 'r':
            read_spi(cmd[1], cmd[2])
        if cmd[0] == 'wait':
            wait_spi(cmd[1])

    halt_spi()

    print('}\n')

    file_output = store_print_to_var(False, buffer)
    print(file_output)

    file_output_name = base_name + '.digipatsrc'
    with open(file_output_name, 'w') as f:
        f.write(file_output)

    # print_output = buffer.getvalue()  # store print value to this var
    # sys.stdout = sys.__stdout__  # restore stdout to default for print()
    # print(print_output)
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    file_name = ''
    if len(sys.argv) > 1:
        print(sys.argv[1])
        file_name = sys.argv[1]
        convert_tcl_to_pattern(file_name)
        pass
    else:
        # file_name = 'debug_1.tcl'
        extension = "tcl"
        files_list = glob.glob(f"*.{extension}")
        print(files_list)
        for fnames in files_list:
            convert_tcl_to_pattern(fnames)
        pass

    # convert_tcl_to_pattern(file_name)

    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
