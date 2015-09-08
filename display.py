#! /usr/bin/python
"""
Created 9/2/15 by Greg Griffes
"""
import time
from zilog_ZDMII_constants import *
from zilog_ZDMII import zilog_ZDMII

zdmii = zilog_ZDMII("/dev/ttyAMA0")
md_rst = 'U'

while True:

    current_light_threshold = zdmii.read_integer(ZDMII_READ_LIGHT_THRESHOLD)
    print('Current light threshold: '+"%d"%current_light_threshold)
    zdmii.write_integer_with_ack(ZDMII_WRITE_LIGHT_THRESHOLD, 200)
    current_light_threshold = zdmii.read_integer(ZDMII_READ_LIGHT_THRESHOLD)
    print('Current light threshold: '+"%d"%current_light_threshold)
    zdmii.write_integer_with_ack(ZDMII_WRITE_LIGHT_THRESHOLD, 128)

    current_light_level = zdmii.read_integer(ZDMII_READ_LIGHT_LEVEL)
    print('Current light level: '+"%d"%current_light_level)

    zdmii.write_character_with_ack(ZDMII_WRITE_MD_RST_CONFIG, ZDMII_MD_RST_CONFIG_MD)
    md_rst = zdmii.read_character(ZDMII_READ_MD_RST_CONFIG)
    if (md_rst == ZDMII_MD_RST_CONFIG_MD):
        print('MD*/RST* pin configured as Motion Detect (MD) output('+str(md_rst)+')')
    elif (md_rst == ZDMII_MD_RST_CONFIG_RST):
        print('MD*/RST* pin configured as Reset (RST) input('+str(md_rst)+')')
    else:
        print('MD*/RST* configuration unknown!('+str(md_rst)+')')

    zdmii.write_character_with_ack(ZDMII_WRITE_MD_RST_CONFIG, ZDMII_MD_RST_CONFIG_RST)
    md_rst = zdmii.read_character(ZDMII_READ_MD_RST_CONFIG)
    if (md_rst == ZDMII_MD_RST_CONFIG_MD):
        print('MD*/RST* pin configured as Motion Detect (MD) output('+str(md_rst)+')')
    elif (md_rst == ZDMII_MD_RST_CONFIG_RST):
        print('MD*/RST* pin configured as Reset (RST) input('+str(md_rst)+')')
    else:
        print('MD*/RST* configuration unknown!('+str(md_rst)+')')

    activation_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVATION_TIME)
    print('Activation time: '+"%d"%activation_time)
    zdmii.write_integer_with_ack(ZDMII_WRITE_MD_ACTIVATION_TIME, 200)
    activation_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVATION_TIME)
    print('Activation time: '+"%d"%activation_time)
    zdmii.write_integer_with_ack(ZDMII_WRITE_MD_ACTIVATION_TIME, 10)

    hypersense_setting = zdmii.read_character(ZDMII_READ_HYPERSENSE_SETTING)
    print('Hypersense setting: '+hypersense_setting)

    time.sleep(3)

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
