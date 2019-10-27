import time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import sys
import pathlib
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_debug import logger
from common.c_messenger import Receiver, ProcessId

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()


def disp_connecivity(d_mess):
    conn = d_mess['connectables']
    draw.text((x, top + 8), "1:" + strc(conn[0]) + " 2:" + strc(conn[1]) + " 3:" + strc(conn[2]) + " 4:" + strc(conn[3]), font=font, fill=255)
    draw.text((x, top + 16), "5:" + strc(conn[4]) + " 6:" + strc(conn[5]) + " 7:" + strc(conn[6]) + " 8:" + strc(conn[7]), font=font, fill=255)
    draw.text((x, top + 25), "9:" + strc(conn[8]) + " 10:" + strc(conn[9]) + " 11:" + strc(conn[10]) + " 12:" + strc(conn[11]), font=font, fill=255)
    disp.image(image)
    disp.display()


def kill(d_mess):
    sys.exit()


def disp_ip():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    draw.text((x, top), "IP: " + str(IP), font=font, fill=255)
    # Display image.
    disp.image(image)
    disp.display()


def strc(conn):
    return "OK" if conn else "NG"


def run():
    receiver = Receiver(ProcessId.DISPLAYER)
    d_callbacks = {'disp_connectivity': disp_connecivity, 'kill': kill}
    receiver.open(d_callbacks)


if __name__ == '__main__':
    disp_ip()
    run()
