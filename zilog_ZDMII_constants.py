#! /usr/bin/python
"""
Constants for the Zilog PIR motion detector module ZDMII
Created 9/2/15 by Greg Griffes
"""
# Serial protocol
import serial
ZDMII_BAUD_RATE = 9600
ZDMII_PARITY = serial.PARITY_NONE
ZDMII_DATA_BITS = serial.EIGHTBITS
ZDMII_STOP_BITS = serial.STOPBITS_ONE
##timeout = None: wait forever
##timeout = 0: non-blocking mode (return immediately on read)
##timeout = x: set timeout to x seconds (float allowed)
ZDMII_TIMEOUT = 0.1
ZDMII_FLOW = False      #disable software flow control
ZDMII_RTSCTS = False    #disable hardware (RTS/CTS) flow control
ZDMII_DSRDTR = False    #disable hardware (DSR/DTR) flow control
ZDMII_WTIMEOUT = 0.1    #non-blocking

ZDMII_ACK = (b'\x06')
ZDMII_NACK = (b'\x15')

# Motion Status
ZDMII_READ_MOTION_STATUS = 'a'

# Light Gate Level - control and monitor light level
# Light gate threshold controls when the MD output is disabled by daylight
# Light gate level can be read to determine day from night
# Light gate threshold only affects the MD output, the Motion Status Command
#   can still be used to detect motion during daytime.
# Range is 0 to 255 where 0 is maximum ambient light and 255 is minimum ambient light
# Setting the threshold to 128 means that when the ambient light is lower than 128
#   the MD output will be deactivated
ZDMII_WRITE_LIGHT_THRESHOLD = 'L'
ZDMII_READ_LIGHT_THRESHOLD = 'l'
ZDMII_READ_LIGHT_LEVEL = 'b'

# *MD/*RST pin configuration - configures pin 5 as the:
# Motion Detect output if 'M'
# Reset input if 'R'
# both are active low
# if Motion Detect, output low when motion detected.
# if Reset input, then the module is reset when pin 5 is driven low.
ZDMII_WRITE_MD_RST_CONFIG = 'C'
ZDMII_MD_RST_CONFIG_MD = 'M'
ZDMII_MD_RST_CONFIG_RST = 'R'

# MD activation time - the duration that the MD output is held low when motion is detected
# 0 - output is disabled
# 1-127 = 1 to 127 seconds
# 128 - output is disabled
# 129-255 = 1 to 127 minutes
ZDMII_READ_MD_ACTIVATION_TIME = 'd'
ZDMII_WRITE_MD_ACTIVATION_TIME = 'D'

# Hyper Sense Mode - smaller signal changes cause valid motion events
# Can cause more false detections but can be used as occupancy sensing
ZDMII_READ_HYPERSENSE_SETTING = 'e'
ZDMII_WRITE_HYPERSENSE_SETTING = 'E'
ZDMII_HYPERSENSE_ON = 'Y'
ZDMII_HYPERSENSE_OFF = 'N'

ZDMII_READ_HYPERSENSE_LEVEL = 'g'
ZDMII_WRITE_HYPERSENSE_LEVEL = 'G'
ZDMII_HYPERSENSE_LEVEL_OFF = 0
ZDMII_HYPERSENSE_LEVEL_LOW = 1
ZDMII_HYPERSENSE_LEVEL_MEDIUM = 2
ZDMII_HYPERSENSE_LEVEL_HIGH = 3

# Frequency response - lower frequency sensitivity is reduced when set to high
# Setting to high has the effect of reducing the sensitivity distance
ZDMII_READ_FREQ_RESPONSE = 'f'
ZDMII_WRITE_FREQ_RESPONSE = 'F'
ZDMII_FREQ_RESPONSE_LOW = 'L'
ZDMII_FREQ_RESPONSE_HIGH = 'H'

# Motion Suspend - disables motion detection when set to 'Y'
ZDMII_READ_MOTION_SUSPEND = 'h'
ZDMII_WRITE_MOTION_SUSPEND = 'H'
ZDMII_MOTION_SUSPEND_ON = 'Y'
ZDMII_MOTION_SUSPEND_OFF = 'N'

# Software Revision
# returns two values:
# first: Application Software Version
# second: ZMOTION Software Engine Version
ZDMII_READ_SW_REV = 'i'

# Serial Command mode - switch betwee ASCII Decimal or ASCII exclusive mode
# ASCII Decimal: 0 to 255 = 0x00 to 0xff (one byte)
# ASCII exclusive: 0 to 255 = "000" to "255" (three bytes)
ZDMII_READ_SERIAL_COMMAND = 'k'
ZDMII_WRITE_SERIAL_COMMAND = 'K'
ZDMII_SERIAL_ASCII = 'A'
ZDMII_SERIAL_DECIMAL = 'D'

# Motion Detected Unsolicited Mode
# sends signal when motion is detected without being prompted
ZDMII_READ_UNSOLICITED_MODE = 'm'
ZDMII_UNSOLICITED_MODE_ON = 'Y'
ZDMII_UNSOLICITED_MODE_OFF = 'N'
ZDMII_WRITE_UNSOLICITED_MODE = 'M'
ZDMII_UNSOLICITED_MOTION_DETECTED = 'M'

# MD* Current Active Output Time
# This command directly controls the MD* output pin as a manual override
# 0 or 128 = MD output does not activate
# 1-127 = 1-127 seconds
# 129-255 = 1-127 minutes
ZDMII_READ_MD_ACTIVE_TIME = 'o'
ZDMII_WRITE_MD_ACTIVE_TIME = 'O'

# Ping - Write a value that can be read back to test the device
ZDMII_READ_PING_VALUE = 'p'
ZDMII_WRITE_PING_VALUE = 'P'

# Range setting - relative range of motion detection
# Larger values (0-7) decrease the range of detection
ZDMII_READ_RANGE_SETTING = 'r'
ZDMII_WRITE_RANGE_SETTING = 'R'

# Sensitivity - larger values (0-255) provide lower sensitivity and
#   also has the effect of reducing range
ZDMII_READ_SENSITIVITY = 's'
ZDMII_WRITE_SENSITIVITY = 'S'

# Directional detection - detects the direction of motion (i.e. right to left)
# In dual direction mode when motion is detected a '+' or '-' will be sent
#   along with the Motion Status respons of 'Y' (e.g. "Y-") or with the
#   unsolicited mode 'M' (e.g. "M-")
# In single direction mode, the write command tells the device which direction to look for
# The '+' direction is TBD to TBD
# The '-' direction is TBD to TBD
ZDMII_READ_DUAL_DIRECTION_MODE = 'u'
ZDMII_WRITE_DUAL_DIRECTION_MODE = 'U'
ZDMII_DUAL_DIRECTION_OFF = 'N'
ZDMII_DUAL_DIRECTION_ON = 'Y'
ZDMII_DIRECTION_R2L = '+'
ZDMII_DIRECTION_L2R = '-'
ZDMII_READ_SINGLE_DIRECTION_MODE = 'v'
ZDMII_WRITE_SINGLE_DIRECTION_MODE = 'V'
ZDMII_SINGLE_DIRECTION_OFF = 'A'

# Module reset - all config and status returned to default state
ZDMII_WRITE_MODULE_RESET = 'X'
ZDMII_CONFIRMATION_CODE = '1234'

# Sleep - low power sleep mode
# Exited on any of these conditions:
# - SLP* pin transition
# - any character received on the serial line
# - expiration of the sleep timer
# Writing a 0 to the sleep timer disables the timer
# I am assuming that the timing values for the MD pin are the same for the sleep timer
#    because it is not stated in the manual
# 0 or 128 = sleep timer disabled
# 1-127 = 1-127 seconds
# 129-255 = 1-127 minutes
ZDMII_READ_SLEEP_TIME = 'y'
ZDMII_WRITE_SLEEP_TIME = 'Y'
ZDMII_SLEEP_ENABLE = 'Z'
ZDMII_SLEEP_CONF_CODE = "1234"

