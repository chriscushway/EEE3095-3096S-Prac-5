import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

print('Raw ADC Value: ', chan.value)
print('ADC Voltage: ' + str(chan.voltage) + 'V')

value = 0
sampleRate = 5

def testFunct():
    if(value%sampleRate == 0):
        print('Yea we did it mate')

while True:
    time.sleep(1)
    temp = (chan.voltage - 0.5) * 100
    print('temp is ' + str(temp) + 'C')