#! /usr/bin/python
"""
Created 9/2/15 by Greg Griffes
"""

from zilog_ZDMII import zilog_ZDMII

zdmii = zilog_ZDMII("/dev/ttyAMA0")

##portname = "/dev/ttyAMA0"
##baudrate = 9600
##numberofbytes = 1
##
##while True:
##    port = serial.Serial(portname, baudrate)
###    port.write(b'\x61')
##    port.write('a')
##    data = port.read(numberofbytes)
##    if (data == 'U'):
##        print "Zilog PIR not ready"
##    elif (data == 'N'):
##        time.sleep(0.01)
###        print "NO motion"
##    elif (data == 'Y'):
##        print "MOTION!"
##    else:
##        print "Unknown code '"+str(data)+"' received from Zilog PIR"
##    time.sleep(0.25)
##    
##
##port.close()
