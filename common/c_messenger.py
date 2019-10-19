from socket import socket, AF_INET, SOCK_STREAM
from enum import IntEnum, auto
import json
from .c_debug import logger

HOST = 'localhost'
REF_PORT = 50000


class ProcessId(IntEnum):
    DISPLAYER = 0
    SOUNDPLAYER = auto()
    WEBSERVER = auto()


def get_port(process_id):
    return REF_PORT + process_id


class Sender:
    def send(self, process_id, message):
        while True:
            try:
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.connect((HOST, get_port(process_id)))

                self.sock.send(message.encode('utf-8'))

                self.sock.close()
                break

            except InterruptedError as e:
                logger().exception('Exception: %s', e)
                return False
        return True


class Receiver:
    PORT = REF_PORT
    cancel = False

    def __init__(self, process_id):
        self.PORT = get_port(process_id)
    
    def open(self, callbacks):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((HOST, self.PORT))
        self.NUM_THREAD = 4
        self.sock.listen(self.NUM_THREAD)

        while True:
            try:
                if self.cancel:
                    self.sock.close()
                    break
                conn, addr = self.sock.accept()
                self.MAX_MASSAGE = 2048
                mess = conn.recv(self.MAX_MASSAGE).decode('utf-8')
                conn.close()
                logger().info('message: ' + mess)
                try:
                    json_mess = json.loads(mess)
                    logger().info('json_mess: %s', json_mess)
                
                except json.JSONDecodeError as e:
                    self.sock.close()
                    logger().exception('Exception: %s', e)
            
            except InterruptedError as e:
                self.sock.close()
                logger().exception('Exception: %s', e)
    
    def close(self):
        self.cancel = True
