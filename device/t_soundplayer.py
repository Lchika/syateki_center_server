import sys
import pathlib
import serial
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_debug import logger
from common.c_messenger import Receiver, get_port, ProcessId

s = serial.Serial('/dev/serial0', 9600, timeout=10)


def play_file(d_mess):
    file_num = d_mess['file_num']
    s.write(serial.to_bytes([0xAA, 0x07, 0x02, 0x00, file_num, 0xB3 + file_num]))


def kill(d_mess):
    sys.exit()


def run():
    receiver = Receiver(ProcessId.SOUNDPLAYER)
    d_callbacks = {'play_file': play_file, 'kill': kill}
    receiver.open(d_callbacks)


if __name__ == '__main__':
    run()
