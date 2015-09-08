#! /usr/bin/python
"""
Created 9/2/15 by Greg Griffes
"""
import time
from zilog_ZDMII_constants import *
from zilog_ZDMII import zilog_ZDMII

zdmii = zilog_ZDMII("/dev/ttyAMA0")
md_rst = 'U'

print('*********************')
print('Initial RESET values:')
print('*********************')
# Software Revision
sw_revision = [0]*2
zdmii.port_write(ZDMII_READ_SW_REV)
sw_revision = zdmii.ZDMII_port.read(2)
time.sleep(ZDMII_COMM_DELAY)
print('Software Revision: App:'+"%d"%ord(sw_revision[0])+' ZDM:'+"%d"%ord(sw_revision[1]))

# Light Threshold
current_light_threshold = zdmii.read_integer(ZDMII_READ_LIGHT_THRESHOLD)
print('Current light threshold: '+"%d"%current_light_threshold)
current_light_level = zdmii.read_integer(ZDMII_READ_LIGHT_LEVEL)
print('Current light level: '+"%d"%current_light_level)

# MD*/RST* Pin
md_rst = zdmii.read_character(ZDMII_READ_MD_RST_CONFIG)
if (md_rst == ZDMII_MD_RST_CONFIG_MD):
    print('MD*/RST* pin configured as Motion Detect (MD) output('+str(md_rst)+')')
elif (md_rst == ZDMII_MD_RST_CONFIG_RST):
    print('MD*/RST* pin configured as Reset (RST) input('+str(md_rst)+')')
else:
    print('MD*/RST* configuration unknown!('+str(md_rst)+')')

# MD Activation time
activation_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVATION_TIME)
print('Activation time: '+"%d"%activation_time)

# Hypersense mode
hypersense_setting = zdmii.read_character(ZDMII_READ_HYPERSENSE_SETTING)
print('Hypersense setting: '+hypersense_setting)
hypersense_level = zdmii.read_character(ZDMII_READ_HYPERSENSE_LEVEL)
print('Hypersense level: '+hypersense_level)

# Frequency response
freq_resp = zdmii.read_character(ZDMII_READ_FREQ_RESPONSE)
if (freq_resp == ZDMII_FREQ_RESPONSE_LOW):
    print('Frequency response set to low('+str(freq_resp)+')')
elif (freq_resp == ZDMII_FREQ_RESPONSE_HIGH):
    print('Frequency response set to high('+str(freq_resp)+')')
else:
    print('Frequency response unknown!('+str(freq_resp)+')')

# Motion Suspend
motion_susp = zdmii.read_character(ZDMII_READ_MOTION_SUSPEND)
if (motion_susp == ZDMII_MOTION_SUSPEND_ON):
    print('Motion supsend is ON('+str(motion_susp)+')')
elif (motion_susp == ZDMII_MOTION_SUSPEND_OFF):
    print('Motion suspend is OFF('+str(motion_susp)+')')
else:
    print('Motion suspend is unknown!('+str(motion_susp)+')')

# Serial Command Mode
serial_cmd_mode = zdmii.read_character(ZDMII_READ_SERIAL_COMMAND)
if (serial_cmd_mode == ZDMII_SERIAL_ASCII):
    print('Serial Command mode is ASCII('+str(serial_cmd_mode)+')')
elif (serial_cmd_mode == ZDMII_SERIAL_DECIMAL):
    print('Serial Command mode is decimal('+str(serial_cmd_mode)+')')
else:
    print('Serial Command mode is unknown!('+str(serial_cmd_mode)+')')

# Motion Detected Unsolicited mode
motion_det_unsol = zdmii.read_character(ZDMII_READ_UNSOLICITED_MODE)
if (motion_det_unsol == ZDMII_UNSOLICITED_MODE_ON):
    print('Motion detected unsolicited is ON('+str(motion_det_unsol)+')')
elif (motion_det_unsol == ZDMII_UNSOLICITED_MODE_OFF):
    print('Motion detected unsolicited is OFF('+str(motion_det_unsol)+')')
else:
    print('Motion detected unsolicited is unknown!('+str(motion_det_unsol)+')')

# MD* pin active time
md_active_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVE_TIME)
print('MD* active output time: '+"%d"%md_active_time)

# Ping
ping = zdmii.read_integer(ZDMII_READ_PING_VALUE)
print('Ping value: '+"%d"%ping)

# Range
range_setting = zdmii.read_integer(ZDMII_READ_RANGE_SETTING)
print('Range setting: '+"%d"%range_setting)

# Sensitivity
sensitivity = zdmii.read_integer(ZDMII_READ_SENSITIVITY)
print('Sensitivity setting: '+"%d"%sensitivity)

# Dual Direction mode
dual_dir = zdmii.read_character(ZDMII_READ_DUAL_DIRECTION_MODE)
if (dual_dir == ZDMII_DUAL_DIRECTION_ON):
    print('Dual direction mode is ON('+str(dual_dir)+')')
elif (dual_dir == ZDMII_DUAL_DIRECTION_OFF):
    print('Dual direction mode is OFF('+str(dual_dir)+')')
else:
    print('Dual direction mode is unknown!('+str(dual_dir)+')')

# Single Direction mode
single_dir = zdmii.read_character(ZDMII_READ_SINGLE_DIRECTION_MODE)
if (single_dir == ZDMII_DIRECTION_R2L):
    print('Single direction mode is R2L('+str(single_dir)+')')
elif (single_dir == ZDMII_DIRECTION_L2R):
    print('Single direction mode is L2R('+str(single_dir)+')')
elif (single_dir == ZDMII_SINGLE_DIRECTION_OFF):
    print('Single direction mode is OFF('+str(single_dir)+')')
else:
    print('Single direction mode is unknown!('+str(single_dir)+')')

# Sleep mode
sleep_time = zdmii.read_integer(ZDMII_READ_SLEEP_TIME)
print('Sleep time setting: '+"%d"%sleep_time)

# Main loop
while True:

    print('*********************')
    print('      Test Code      ')
    print('*********************')
    current_light_threshold = zdmii.read_integer(ZDMII_READ_LIGHT_THRESHOLD)
    print('Current light threshold: '+"%d"%current_light_threshold)
    zdmii.write_integer(ZDMII_WRITE_LIGHT_THRESHOLD, 200)
    current_light_threshold = zdmii.read_integer(ZDMII_READ_LIGHT_THRESHOLD)
    print('Current light threshold: '+"%d"%current_light_threshold)
    zdmii.write_integer(ZDMII_WRITE_LIGHT_THRESHOLD, 128)

    current_light_level = zdmii.read_integer(ZDMII_READ_LIGHT_LEVEL)
    print('Current light level: '+"%d"%current_light_level)

    zdmii.write_character(ZDMII_WRITE_MD_RST_CONFIG, ZDMII_MD_RST_CONFIG_MD)
    md_rst = zdmii.read_character(ZDMII_READ_MD_RST_CONFIG)
    if (md_rst == ZDMII_MD_RST_CONFIG_MD):
        print('MD*/RST* pin configured as Motion Detect (MD) output('+str(md_rst)+')')
    elif (md_rst == ZDMII_MD_RST_CONFIG_RST):
        print('MD*/RST* pin configured as Reset (RST) input('+str(md_rst)+')')
    else:
        print('MD*/RST* configuration unknown!('+str(md_rst)+')')

    zdmii.write_character(ZDMII_WRITE_MD_RST_CONFIG, ZDMII_MD_RST_CONFIG_RST)
    md_rst = zdmii.read_character(ZDMII_READ_MD_RST_CONFIG)
    if (md_rst == ZDMII_MD_RST_CONFIG_MD):
        print('MD*/RST* pin configured as Motion Detect (MD) output('+str(md_rst)+')')
    elif (md_rst == ZDMII_MD_RST_CONFIG_RST):
        print('MD*/RST* pin configured as Reset (RST) input('+str(md_rst)+')')
    else:
        print('MD*/RST* configuration unknown!('+str(md_rst)+')')

    activation_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVATION_TIME)
    print('Activation time: '+"%d"%activation_time)
    zdmii.write_integer(ZDMII_WRITE_MD_ACTIVATION_TIME, 200)
    activation_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVATION_TIME)
    print('Activation time: '+"%d"%activation_time)
    zdmii.write_integer(ZDMII_WRITE_MD_ACTIVATION_TIME, 10)

    hypersense_setting = zdmii.read_character(ZDMII_READ_HYPERSENSE_SETTING)
    print('Hypersense setting: '+hypersense_setting)
    zdmii.write_character(ZDMII_WRITE_HYPERSENSE_SETTING, ZDMII_HYPERSENSE_ON)
    hypersense_setting = zdmii.read_character(ZDMII_READ_HYPERSENSE_SETTING)
    print('Hypersense setting: '+hypersense_setting)

    zdmii.write_integer(ZDMII_WRITE_HYPERSENSE_LEVEL, ZDMII_HYPERSENSE_LEVEL_OFF)
    hypersense_level = zdmii.read_character(ZDMII_READ_HYPERSENSE_LEVEL)
    print('Hypersense level: '+hypersense_level)

    zdmii.write_integer(ZDMII_WRITE_HYPERSENSE_LEVEL, ZDMII_HYPERSENSE_LEVEL_LOW)
    hypersense_level = zdmii.read_character(ZDMII_READ_HYPERSENSE_LEVEL)
    print('Hypersense level: '+hypersense_level)

    zdmii.write_integer(ZDMII_WRITE_HYPERSENSE_LEVEL, ZDMII_HYPERSENSE_LEVEL_MEDIUM)
    hypersense_level = zdmii.read_character(ZDMII_READ_HYPERSENSE_LEVEL)
    print('Hypersense level: '+hypersense_level)

    zdmii.write_integer(ZDMII_WRITE_HYPERSENSE_LEVEL, ZDMII_HYPERSENSE_LEVEL_HIGH)
    hypersense_level = zdmii.read_character(ZDMII_READ_HYPERSENSE_LEVEL)
    print('Hypersense level: '+hypersense_level)
    
    zdmii.write_character(ZDMII_WRITE_HYPERSENSE_SETTING, ZDMII_HYPERSENSE_OFF)

    zdmii.write_character(ZDMII_WRITE_FREQ_RESPONSE, ZDMII_FREQ_RESPONSE_LOW)
    freq_resp = zdmii.read_character(ZDMII_READ_FREQ_RESPONSE)
    if (freq_resp == ZDMII_FREQ_RESPONSE_LOW):
        print('Frequency response set to low('+str(freq_resp)+')')
    elif (freq_resp == ZDMII_FREQ_RESPONSE_HIGH):
        print('Frequency response set to high('+str(freq_resp)+')')
    else:
        print('Frequency response unknown!('+str(freq_resp)+')')

    zdmii.write_character(ZDMII_WRITE_FREQ_RESPONSE, ZDMII_FREQ_RESPONSE_HIGH)
    freq_resp = zdmii.read_character(ZDMII_READ_FREQ_RESPONSE)
    if (freq_resp == ZDMII_FREQ_RESPONSE_LOW):
        print('Frequency response set to low('+str(freq_resp)+')')
    elif (freq_resp == ZDMII_FREQ_RESPONSE_HIGH):
        print('Frequency response set to high('+str(freq_resp)+')')
    else:
        print('Frequency response unknown!('+str(freq_resp)+')')

# Motion Detection Suspend
    zdmii.write_character(ZDMII_WRITE_MOTION_SUSPEND, ZDMII_MOTION_SUSPEND_ON)
    motion_susp = zdmii.read_character(ZDMII_READ_MOTION_SUSPEND)
    if (motion_susp == ZDMII_MOTION_SUSPEND_ON):
        print('Motion supsend is ON('+str(motion_susp)+')')
    elif (motion_susp == ZDMII_MOTION_SUSPEND_OFF):
        print('Motion suspend is OFF('+str(motion_susp)+')')
    else:
        print('Motion suspend is unknown!('+str(motion_susp)+')')

    zdmii.write_character(ZDMII_WRITE_MOTION_SUSPEND, ZDMII_MOTION_SUSPEND_OFF)
    motion_susp = zdmii.read_character(ZDMII_READ_MOTION_SUSPEND)
    if (motion_susp == ZDMII_MOTION_SUSPEND_ON):
        print('Motion supsend is ON('+str(motion_susp)+')')
    elif (motion_susp == ZDMII_MOTION_SUSPEND_OFF):
        print('Motion suspend is OFF('+str(motion_susp)+')')
    else:
        print('Motion suspend is unknown!('+str(motion_susp)+')')

# Serial Interface Command Mode
#    zdmii.write_character(ZDMII_WRITE_SERIAL_COMMAND, ZDMII_SERIAL_DECIMAL)
    serial_cmd_mode = zdmii.read_character(ZDMII_READ_SERIAL_COMMAND)
    if (serial_cmd_mode == ZDMII_SERIAL_ASCII):
        print('Serial Command mode is ASCII('+str(serial_cmd_mode)+')')
    elif (serial_cmd_mode == ZDMII_SERIAL_DECIMAL):
        print('Serial Command mode is decimal('+str(serial_cmd_mode)+')')
    else:
        print('Serial Command mode is unknown!('+str(serial_cmd_mode)+')')

# Motion Detected Unsolicited Mode
    zdmii.write_character(ZDMII_WRITE_UNSOLICITED_MODE, ZDMII_UNSOLICITED_MODE_ON)
    motion_det_unsol = zdmii.read_character(ZDMII_READ_UNSOLICITED_MODE)
    if (motion_det_unsol == ZDMII_UNSOLICITED_MODE_ON):
        print('Motion detected unsolicited is ON('+str(motion_det_unsol)+')')
    elif (motion_det_unsol == ZDMII_UNSOLICITED_MODE_OFF):
        print('Motion detected unsolicited is OFF('+str(motion_det_unsol)+')')
    else:
        print('Motion detected unsolicited is unknown!('+str(motion_det_unsol)+')')

    zdmii.write_character(ZDMII_WRITE_UNSOLICITED_MODE, ZDMII_UNSOLICITED_MODE_OFF)
    motion_det_unsol = zdmii.read_character(ZDMII_READ_UNSOLICITED_MODE)
    if (motion_det_unsol == ZDMII_UNSOLICITED_MODE_ON):
        print('Motion detected unsolicited is ON('+str(motion_det_unsol)+')')
    elif (motion_det_unsol == ZDMII_UNSOLICITED_MODE_OFF):
        print('Motion detected unsolicited is OFF('+str(motion_det_unsol)+')')
    else:
        print('Motion detected unsolicited is unknown!('+str(motion_det_unsol)+')')

# MD* Current Active Output Time
    zdmii.write_integer(ZDMII_WRITE_MD_ACTIVE_TIME, 200)
    md_active_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVE_TIME)
    print('MD* active output time: '+"%d"%md_active_time)
    zdmii.write_integer(ZDMII_WRITE_MD_ACTIVE_TIME, 20)
    md_active_time = zdmii.read_integer(ZDMII_READ_MD_ACTIVE_TIME)
    print('MD* active output time: '+"%d"%md_active_time)

# Ping
    zdmii.write_integer(ZDMII_WRITE_PING_VALUE, 200)
    ping = zdmii.read_integer(ZDMII_READ_PING_VALUE)
    print('Ping value: '+"%d"%ping)
    zdmii.write_integer(ZDMII_WRITE_PING_VALUE, 20)
    ping = zdmii.read_integer(ZDMII_READ_PING_VALUE)
    print('Ping value: '+"%d"%ping)

# Range Setting
    zdmii.write_integer(ZDMII_WRITE_RANGE_SETTING, 7)
    range_setting = zdmii.read_integer(ZDMII_READ_RANGE_SETTING)
    print('Range setting: '+"%d"%range_setting)
    zdmii.write_integer(ZDMII_WRITE_RANGE_SETTING, 0)
    range_setting = zdmii.read_integer(ZDMII_READ_RANGE_SETTING)
    print('Range setting: '+"%d"%range_setting)

# Sensitivity
    zdmii.write_integer(ZDMII_WRITE_SENSITIVITY, 200)
    sensitivity = zdmii.read_integer(ZDMII_READ_SENSITIVITY)
    print('Sensitivity setting: '+"%d"%sensitivity)
    zdmii.write_integer(ZDMII_WRITE_SENSITIVITY, 20)
    sensitivity = zdmii.read_integer(ZDMII_READ_SENSITIVITY)
    print('Sensitivity setting: '+"%d"%sensitivity)

# Dual Direction mode
    zdmii.write_character(ZDMII_WRITE_DUAL_DIRECTION_MODE, ZDMII_DUAL_DIRECTION_ON)
    dual_dir = zdmii.read_character(ZDMII_READ_DUAL_DIRECTION_MODE)
    if (dual_dir == ZDMII_DUAL_DIRECTION_ON):
        print('Dual direction mode is ON('+str(dual_dir)+')')
    elif (dual_dir == ZDMII_DUAL_DIRECTION_OFF):
        print('Dual direction mode is OFF('+str(dual_dir)+')')
    else:
        print('Dual direction mode is unknown!('+str(dual_dir)+')')

    zdmii.write_character(ZDMII_WRITE_DUAL_DIRECTION_MODE, ZDMII_DUAL_DIRECTION_OFF)
    dual_dir = zdmii.read_character(ZDMII_READ_DUAL_DIRECTION_MODE)
    if (dual_dir == ZDMII_DUAL_DIRECTION_ON):
        print('Dual direction mode is ON('+str(dual_dir)+')')
    elif (dual_dir == ZDMII_DUAL_DIRECTION_OFF):
        print('Dual direction mode is OFF('+str(dual_dir)+')')
    else:
        print('Dual direction mode is unknown!('+str(dual_dir)+')')

# Single Direction mode
    zdmii.write_character(ZDMII_WRITE_SINGLE_DIRECTION_MODE, ZDMII_DIRECTION_L2R)
    single_dir = zdmii.read_character(ZDMII_READ_SINGLE_DIRECTION_MODE)
    if (single_dir == ZDMII_DIRECTION_R2L):
        print('Single direction mode is R2L('+str(single_dir)+')')
    elif (single_dir == ZDMII_DIRECTION_L2R):
        print('Single direction mode is L2R('+str(single_dir)+')')
    elif (single_dir == ZDMII_SINGLE_DIRECTION_OFF):
        print('Single direction mode is OFF('+str(single_dir)+')')
    else:
        print('Single direction mode is unknown!('+str(single_dir)+')')

    zdmii.write_character(ZDMII_WRITE_SINGLE_DIRECTION_MODE, ZDMII_DIRECTION_R2L)
    single_dir = zdmii.read_character(ZDMII_READ_SINGLE_DIRECTION_MODE)
    if (single_dir == ZDMII_DIRECTION_R2L):
        print('Single direction mode is R2L('+str(single_dir)+')')
    elif (single_dir == ZDMII_DIRECTION_L2R):
        print('Single direction mode is L2R('+str(single_dir)+')')
    else:
        print('Single direction mode is unknown!('+str(single_dir)+')')

# Sleep time
    zdmii.write_integer(ZDMII_WRITE_SLEEP_TIME, 200)
    sleep_time = zdmii.read_integer(ZDMII_READ_SLEEP_TIME)
    print('Sleep time setting: '+"%d"%sleep_time)
    zdmii.write_integer(ZDMII_WRITE_SLEEP_TIME, 0)
    sleep_time = zdmii.read_integer(ZDMII_READ_SLEEP_TIME)
    print('Sleep time setting: '+"%d"%sleep_time)

# Sleep enable


    # unsolicited mode
##    zdmii.write_character(ZDMII_WRITE_UNSOLICITED_MODE, ZDMII_UNSOLICITED_MODE_ON)
##    while True:
##        if serial.inWaiting > 0:
##            data = serial.read()
##            print data
        
    time.sleep(3)
