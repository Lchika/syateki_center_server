import sys
import pathlib
import json
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_debug import logger
from common.c_messenger import Sender, get_port, ProcessId


class ApiDisplayer:
    def disp_connectivity(self, connectables):
        d_message = {'func': 'disp_connectivity', 'connectables': connectables}
        self.__send_mess(d_message)
        return True
    
    def kill(self):
        d_message = {'func': 'kill'}
        self.__send_mess(d_message)
        return True
            
    def __send_mess(self, d_mess):
        self.__sender = Sender()
        j_message = json.dumps(d_mess)
        self.__sender.send(ProcessId.DISPLAYER, j_message)
