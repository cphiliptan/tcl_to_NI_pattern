#Tune the clock to 80MHz
w 7f 00; # page 0x0
w 04 04; # tune the OSC clock
w 07 AA; # depending the freq setting


#Temperature Measurement
w 7f 00;
w 50 03; # start temp sensor sequence
w 50 00; # stop temp sensor sequence

#Selection 1
w 7f 00; # page 0x0
w 17 40; # selection 1

w 2f 00; # smaller cap for IPTAT, ICTAT
w 32 40; # bigger cap INOM 

Selection 0
w 7f 00; # page 0x0
w 17 00; # selection 0

w 2f 03; # bigger cap for IPTAT, ICTAT
w 32 40; # bigger cap INOM

