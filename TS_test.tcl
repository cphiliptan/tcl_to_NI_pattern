#Tune the clock to 80MHz
w 7f 00; # page 0x0

r 00 f1; # read ID
wait 1;

