w 3a 5a; # soft reset
wait 10;
w 7f 00; # read page #
r 7f 00; # read page #
r 00 f1; # read Product ID
r 03 03; # SPI_CTL0

w 7f 01; # read page #
r 7f 01; # read page #
wait 10;
r 00 f1; # read Product ID
r 03 1a; # ADC_CTL00

w 7f 02; # read page #
r 7f 02; # read page #
wait 10;
r 00 f1; # read Product ID
r 10 fc; # 0x210
r 11 3f; # 0x211

