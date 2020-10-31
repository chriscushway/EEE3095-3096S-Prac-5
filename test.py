import busio
import digitalio
import time
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import RPi.GPIO as GPIO

start_time = time.time()

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)

sample_rate = 5 #set sampling rate to 5 as default

def setup_GPIO():
    #setup button
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(24, GPIO.RISING, callback=toggle_sample_rate, bouncetime=200)

# toggle sampling rates which can either be 1,5 or 10
def toggle_sample_rate(channel):
    global sample_rate
    if (sample_rate == 5):
        sample_rate = 10
    elif (sample_rate == 10):
        sample_rate = 1
    elif (sample_rate == 1):
        sample_rate = 5

def print_temp_values():
    global start_time, chan, sample_rate
    elapsed = 0
    last_time_stamp = 0
    print('Runtime Temp Reading Temp')
    #only let loop run for 60 seconds at max
    while elapsed < 60:
        time.sleep(0.1)
        elapsed = int(time.time() - start_time)
        if ((elapsed - last_time_stamp) % sample_rate == 0):
            print(str(elapsed)+'s      ' + str(chan.value) + '         ' + str(calculate_temp()))
            last_time_stamp = elapsed
            time.sleep(1)
    

# function to convert the voltage on the adc channel into temperature in C
def calculate_temp():
    global chan
    return (chan.voltage - 0.5)/0.01

if __name__ == "__main__":
    setup_GPIO()
    thread = threading.Thread(target=print_temp_values)
    thread.daemon = True #make thread die when program dies
    thread.start()
    try:
        while True:
            time.sleep(0.1)
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
