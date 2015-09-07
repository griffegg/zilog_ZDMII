#!/usr/bin/env python
import serial, time, sys
from binascii import unhexlify
from zilog_ZDMII_constants import *

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

# Is the device talking?
        print 'Initializing Zilog ZDMII on port '+self.portname
        sys.stdout.write(".")
        sys.stdout.flush()
        if (self.alive()):
            sys.stdout.write(".")
            sys.stdout.flush()
            if (self.reset()):
                sys.stdout.write(".")
                sys.stdout.flush()
                retries = 0
                result, status = self.read_motion_status()
                if (result == True):
                    if (status == 'U' and retries < self.max_retries):     # wait for device to initialize
                        while (status == 'U' and retries < self.max_retries):
                            retries +=1 
                            sys.stdout.write(".")
                            sys.stdout.flush()
                            time.sleep(5)
                            result, status = self.read_motion_status()
#                            status = 'U'    # test code
                        if (retries == self.max_retries):
                            print('Max Motion Status == U retries exceeded! Device has not stabilized.'+\
                                      '[zilog_ZDMII on port '+str(self.portname)+']' )
        print '\r\n'
# Done with initialization
                    
    def __del__(self):
        self.ZDMII_port.close()
        print 'Zilog ZDMII on port '+self.portname+' closed'

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

    def alive(self):
        cur_ping_value = 0
        new_ping_value = 4
        ack_response = 0
        result = False
        retries = 0

        while (retries < self.max_retries and result == False):
            retries += 1
            self.ZDMII_port.write(ZDMII_WRITE_PING_VALUE)
            cur_ping_value = self.ZDMII_port.read(1)
    #        print('Current ping value returned: '+str(cur_ping_value))
    # Python seems to get confused when trying to add a 0x01 to the current
    #    ping value. The operator and data types are getting mixed
    ##        if (cur_ping_value < b'0xff'):
    ##            new_ping_value = cur_ping_value + 1
                
            new_ping = self.single_int_to_string(new_ping_value)
    #        print('New ping: '+str(new_ping))
            
            self.ZDMII_port.write(str(new_ping))
            ack_response = self.ZDMII_port.read(1)
            if (ack_response == ZDMII_ACK):
    #            print('Successful ping')
                self.ZDMII_port.write(ZDMII_READ_PING_VALUE)
                cur_ping_value = self.ZDMII_port.read(1)
    #            print('Current ping value returned: '+str(cur_ping_value))
                if (cur_ping_value == new_ping):
#                    result = False  # test code
                    result = True
                else:
                    print('Ping failed! Sent: '+str(new_ping)+\
                          ' Received: '+str(cur_ping_value)+\
                          '[zilog_ZDMII on port '+str(self.portname)+']' )
            else:
                print('Ping ACK failed! Response: '+str(ack_response)+\
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
            self.ZDMII_port.write(ZDMII_WRITE_MODULE_RESET)
            self.ack_response = 0
            self.ack_response = self.ZDMII_port.read(1)
            if (self.ack_response == ZDMII_ACK):
    #            print('Reset Command ACK received')
                self.ZDMII_port.write(ZDMII_CONFIRMATION_CODE)
                time.sleep(2)   # give the device time to reset
                self.ack_response = 0
                self.ack_response = self.ZDMII_port.read(1)
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

    def read_motion_status(self):
        result = False
        motion_status = 0
        
        self.ZDMII_port.write(ZDMII_READ_MOTION_STATUS)
        motion_status = self.ZDMII_port.read(1)
#        print('Motion status: '+motion_status)
        if (motion_status == 'U' or \
            motion_status == 'Y' or \
            motion_status == 'N'):
            result = True
        else:
            print('Motion Status failed: '+motion_status+\
                      '[zilog_ZDMII on port '+str(self.portname)+']')

        return result, motion_status

    def write_light_threshold(self, thresh):
        cur_value = 0
        new_value = 0
        ack_response = 0
        result = False
        
        self.ZDMII_port.write(ZDMII_READ_LIGHT_THRESHOLD)
        cur_value = self.ZDMII_port.read(1)
#        print('Cur thresh: '+"%d"%ord(cur_value))

        new_thresh = self.single_int_to_string(thresh)
#        print('New thresh: '+"%d"%thresh)

        self.ZDMII_port.write(ZDMII_WRITE_LIGHT_THRESHOLD)
        cur_thresh = self.ZDMII_port.read(1)
        self.ZDMII_port.write(new_thresh)
        self.ack_response = self.ZDMII_port.read(1)
        if (self.ack_response == ZDMII_ACK):
            self.ZDMII_port.write(ZDMII_READ_LIGHT_THRESHOLD)
            cur_thresh = self.ZDMII_port.read(1)
            if (cur_thresh == new_thresh):
#                print('Successful Light threshold change')
                return True
            else:
                print('thresh write failed: Should be:'+"%d"%ord(new_thresh)+\
                      ' Is: '+"%d"%ord(cur_thresh)+\
                          ' [zilog_ZDMII on port '+str(self.portname)+']')
                return False
        else:
            print('thresh ACK failed: '+str(self.ack_response)+\
                      '[zilog_ZDMII on port '+str(self.portname)+']')
            return False

if __name__ == '__main__':
    zdmii = zilog_ZDMII("/dev/ttyAMA0")
    while True:
        print "Zilog ZDMII main called"
        time.sleep(1)
