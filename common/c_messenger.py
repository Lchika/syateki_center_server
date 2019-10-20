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
    __PORT = REF_PORT
    __cancel = False

    def __init__(self, process_id):
        self.__PORT = get_port(process_id)
    
    def open(self, callbacks):
        self.__sock = socket(AF_INET, SOCK_STREAM)
        self.__sock.bind((HOST, self.__PORT))
        self.__NUM_THREAD = 4
        self.__sock.listen(self.__NUM_THREAD)

        while True:
            try:
                if self.__cancel:
                    self.__sock.close()
                    break
                conn, addr = self.__sock.accept()
                self.__MAX_MASSAGE = 2048
                mess = conn.recv(self.__MAX_MASSAGE).decode('utf-8')
                conn.close()
                logger().info('message: ' + mess)
                try:
                    d_mess = json.loads(mess)
                    logger().info('json_mess: %s', d_mess)
                    func_name = self.__get_func_name(d_mess)
                    if func_name == '':
                        logger().error('func name is not exist: %s', d_mess)
                        continue
                    if func_name in callbacks:
                        logger().debug('target func is exist: %s', func_name)
                        callbacks[func_name](d_mess)
                    else:
                        logger().error('target func is not exist: %s', func_name)

                except json.JSONDecodeError as e:
                    self.__sock.close()
                    logger().exception('Exception: %s', e)
            
            except InterruptedError as e:
                self.__sock.close()
                logger().exception('Exception: %s', e)
    
    def close(self):
        self.__cancel = True
    
    def __get_func_name(self, d_mess):
        func_key = 'func'
        if func_key in d_mess:
            return d_mess['func']
        else:
            return ''
