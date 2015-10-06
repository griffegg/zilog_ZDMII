#!/usr/bin/env python
"""
This is a class driver for the Zilog Detection Module II Passive Infrared Motion Detector
Written in Python 3.3 for the Raspberry Pi 2

See http://github.com/griffegg/zilog_ZDMII for test code and sample code

Connect to the Raspberry Pi as follows but
WARNING! Wiring the ZDM backwards will turn it into toast.
ZDM pin 1: Ground
ZDM pin 2: 3.3VDC
ZDM pin 3: TXD
ZDM pin 4: RXD with a 100K pullup resistor
ZDM pin 5: not connected
ZDM pin 6: 100K pullup and photo resistor to ground
ZDM pin 7: 10K pullup
ZDM pin 8: Ground

Also, you will need to stop the Raspian Linux OS from using the console port (serial port)
Do this by visiting the Adafruit "Freeing UART on the Pi"
https://learn.adafruit.com/adafruit-nfc-rfid-on-raspberry-pi/freeing-uart-on-the-pi

Also, you can test your serial port by doing a loop-back. This is where you wire TXD to RXD
and run a program like Minicom to see that when you type a character it gets printed on the
screen
"""
import serial, time, sys
from binascii import unhexlify
from zilog_ZDMII_constants import *

INIT_PASSED = True

class zilog_ZDMII(object):

    def __init__(self, portname):
        self.portname = portname
        self.ping_response = 0
        self.ack_response = 0
#        print 'Zilog ZDMII PIR Motion Detector on port '+self.portname+' created'
        self.max_retries = 10
      
# configure the serial connections (the parameters differs on the device you are connecting to)
        self.ZDMII_port = serial.Serial(
            port =      self.portname,
            baudrate =  ZDMII_BAUD_RATE,
            bytesize =  ZDMII_DATA_BITS,
            parity =    ZDMII_PARITY,
            stopbits =  ZDMII_STOP_BITS,
            timeout =   ZDMII_TIMEOUT,
            xonxoff =   ZDMII_FLOW,
            rtscts =    ZDMII_RTSCTS,
            dsrdtr =    ZDMII_DSRDTR,
            writeTimeout = ZDMII_WTIMEOUT     #timeout for write
        )
        print 'Serial port setup: '
        print 'port =      '+str(self.portname)
        print 'baudrate =  '+str(ZDMII_BAUD_RATE)
        print 'bytesize =  '+str(ZDMII_DATA_BITS)
        print 'parity =    '+str(ZDMII_PARITY)
        print 'stopbits =  '+str(ZDMII_STOP_BITS)
        print 'timeout =   '+str(ZDMII_TIMEOUT)
        print 'xonxoff =   '+str(ZDMII_FLOW)
        print 'rtscts =    '+str(ZDMII_RTSCTS)
        print 'dsrdtr =    '+str(ZDMII_DSRDTR)
        print 'writeTimeout = '+str(ZDMII_WTIMEOUT)

        retries = 0
        status = ''
# Is the device talking?
        print 'Initializing Zilog ZDMII on port '+self.portname
        sys.stdout.write("Ping:")
        sys.stdout.flush()
        if (self.alive()):
##            sys.stdout.write("Reset:")
##            sys.stdout.flush()
##            if (self.reset()):
##                sys.stdout.write("PIR:")
##                sys.stdout.flush()
            status = self.read_character(ZDMII_READ_MOTION_STATUS)
            if (status == 'U' and retries < self.max_retries):     # wait for device to initialize
                while (status == 'U' and retries < self.max_retries):
                    retries +=1 
                    sys.stdout.write("U")
                    sys.stdout.flush()
                    time.sleep(5)
                    status = self.read_character(ZDMII_READ_MOTION_STATUS)
    #                            status = 'U'    # test code
        if (status == '' or retries == self.max_retries):
            print('Max Motion Status == U retries exceeded! Device has not stabilized.'+\
                              '[zilog_ZDMII on port '+str(self.portname)+']' )
            print 'ZDMII status: ('+str(status)+')'
            INIT_PASSED = False
        
# Done with initialization
                    
    def __del__(self):
        self.ZDMII_port.close()
        print 'Zilog ZDMII on port '+self.portname+' closed'

    def init_success(self):
        return INIT_PASSED

    def single_int_to_string(self, int_value):
        import struct
        string = ''
        string += struct.pack('!B',int_value)
#        print 'single_int_to_string: '+string
        return string

    def int_array_to_string(self, int_values):
        import struct
        string = ''
        for i in int_values:
            string += struct.pack('!B',i)
#        print 'int_array_to_string: '+string
        return string

    def port_write(self, CMD):
        self.ZDMII_port.write(CMD)
        self.ZDMII_port.flushOutput()
        time.sleep(ZDMII_COMM_DELAY)

    def port_read(self):
        returned_value = self.ZDMII_port.read(1)
        self.ZDMII_port.flushInput()
        time.sleep(ZDMII_COMM_DELAY)
        return returned_value

    def read_integer(self, CMD):
        self.port_write(CMD)
        response = self.port_read()
        return ord(response)

    def read_character(self, CMD):
        self.port_write(CMD)
        response = self.port_read()
        return response

    def write_integer(self, CMD, new_value):
        result = False
        
        new_value_string = self.single_int_to_string(new_value)

        self.port_write(CMD)
        returned_value = self.port_read()
        self.port_write(new_value_string)
        ack_response = self.port_read()
        if (ack_response != ZDMII_ACK):
            print('write_integer ACK failed! Value=('+str(ack_response)+\
                  ') First returned value: ('+str(returned_value)+\
                      ') [zilog_ZDMII on port '+str(self.portname)+']')
            return False
        else:
            return True

    def write_character(self, CMD, new_value):
        result = False
        
        self.port_write(CMD)
        returned_value = self.port_read()
        self.port_write(new_value)
        ack_response = self.port_read()
        if (ack_response != ZDMII_ACK):
            print('write_character ACK failed! Value=('+str(ack_response)+\
                  ') First returned value: ('+str(returned_value)+\
                      ') [zilog_ZDMII on port '+str(self.portname)+']')
            return False
        else:
            return True

    def alive(self):
        cur_ping_value = 0
        new_ping_value = 4
        ack_response = 0
        result = False
        retries = 0

        while (retries < self.max_retries and result == False):
            retries += 1
            result = self.write_integer(ZDMII_WRITE_PING_VALUE, new_ping_value)
            if (result == False):
                print('Ping failed! Sent: '+str(new_ping_value)+\
                      ' Received: '+str(cur_ping_value)+\
                      '[zilog_ZDMII on port '+str(self.portname)+']' )

        if (retries == self.max_retries):
            print('alive retries exceeded![zilog_ZDMII on port '+str(self.portname)+']' )
            
        return result
        
    def reset(self):
        result = False
        retries = 0

        while (retries < self.max_retries and result == False):
            retries += 1
    #        print 'Resetting Zilog ZDMII...'
            self.port_write(ZDMII_WRITE_MODULE_RESET)
            self.ack_response = self.port_read()
            if (self.ack_response == ZDMII_ACK):
    #            print('Reset Command ACK received')
                self.port_write(ZDMII_CONFIRMATION_CODE)
                time.sleep(2)   # give the device time to reset
                self.ack_response = self.port_read()
                if (self.ack_response == ZDMII_ACK):
    #                print('Successful reset')
                    time.sleep(1)   # give the device time to reset
#                    result = False  # test code
                    result = True
            else:
                print('Reset failed: '+str(self.ack_response)+\
                          '[zilog_ZDMII on port '+str(self.portname)+']')

        if (retries == self.max_retries):
            print('Max Reset retries exceeded! [zilog_ZDMII on port '+str(self.portname)+']')
        return result

    def get_sw_revision(self):
        sw_revision = [0]*2
        self.port_write(ZDMII_READ_SW_REV)
        sw_revision = self.ZDMII_port.read(2)
        time.sleep(ZDMII_COMM_DELAY)
        return ord(sw_revision[0]), ord(sw_revision[1])


if __name__ == '__main__':
    zdmii = zilog_ZDMII("/dev/ttyAMA0")
    if (zdmii.init_success()):
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
    else:
        print 'ZDMII ERROR! status = ('+str(status)+')'
