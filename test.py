import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import RPi.GPIO as GPIO

start_time = time.time()

#setup button
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

sample_rate = 1

def toggle_sample_rate(channel):
    global sample_rate
    if (sample_rate == 5):
        sample_rate = 10
    elif (sample_rate == 10):
        sample_rate = 1
    elif (sample_rate == 1):
        sample_rate = 5

GPIO.add_event_detect(25, GPIO.RISING, callback=toggle_sample_rate, bouncetime=200)

def print_temp_values():
    global start_time, chan, sample_rate
    elapsed = 0
    last_time_stamp = 0
    print('Runtime Temp Reading Temp')
    #only let loop run for 60 seconds at max
    while elapsed < 60:
        time.sleep(0.1)
        elapsed = time.time() - start_time
        elapsed = int(elapsed)
        if ((elapsed - last_time_stamp) % sample_rate == 0):
            print(str(elapsed)+'s      ' + str(chan.value) + '         ' + str(calculate_temp()))
            last_time_stamp = elapsed
            time.sleep(1)
    

def calculate_temp():
    global chan
    return (chan.voltage - 0.5)/0.01


if __name__ == "__main__":
    thread = threading.Thread(target=print_temp_values)
    thread.daemon = True
    thread.start()
    while True:
        time.sleep(0.1)
