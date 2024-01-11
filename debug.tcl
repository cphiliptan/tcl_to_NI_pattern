w 7f 00; # write 0x7f 0x00
r 7f 00; # read 0x7f 0x00
r 08 48; # SPI_CTL5 Default 0x48
w 08 4b; # SPI_CTL5
r 08 4b; # SPI_CTL5 readback after write
