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
        sys.stdout.write("Ping:")
        sys.stdout.flush()
        if (self.alive()):
            sys.stdout.write("Reset:")
            sys.stdout.flush()
            if (self.reset()):
                sys.stdout.write("PIR:")
                sys.stdout.flush()
                retries = 0
                status = self.read_character(ZDMII_READ_MOTION_STATUS)
                if (status == 'U' and retries < self.max_retries):     # wait for device to initialize
                    while (status == 'U' and retries < self.max_retries):
                        retries +=1 
                        sys.stdout.write("U")
                        sys.stdout.flush()
                        time.sleep(5)
                        status = self.read_character(ZDMII_READ_MOTION_STATUS)
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
    while True:
        print "Zilog ZDMII main called"
        time.sleep(1)
