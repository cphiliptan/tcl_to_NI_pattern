w 3a 5a; # soft reset
wait 10;
r 00 f1; # read Product ID
r 7f 00; # read page
w 7f 01; # write to page
r 7f 01; # read page

