w 3a 5a; # soft reset
wait 10;
w 32 21; # ATST_S_BUF_ON[5]=0x1 ATST_S_CTRL[4:0]=0x1
r 32 21; # ATST_S_BUF_ON[5]=0x1 ATST_S_CTRL[4:0]=0x1
