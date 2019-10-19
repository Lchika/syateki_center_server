import sys
import pathlib
import threading
import unittest
import json
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_messenger import Sender, Receiver

TEST_PROCESS_ID = 1


class TestMessenger(unittest.TestCase):
    def setUp(self):
        print('TestMessenger setup')
        self.receiver = Receiver(TEST_PROCESS_ID)
        d_callbacks = {'message': 't', 'callback': 'est'}
        j_callbacks = json.dumps(d_callbacks)
        self.recv_thread = threading.Thread(target=self.receiver.open, args=(j_callbacks,))
        self.recv_thread.start()
        self.sender = Sender()
    
    def test_send_mess(self):
        d_message = {'message': 't', 'arg1': 'est'}
        j_message = json.dumps(d_message)
        result = self.sender.send(TEST_PROCESS_ID, j_message)
        self.assertEqual(True, result)
    
    def tearDown(self):
        print('TestMessenger teardown')
        self.receiver.close()
        self.recv_thread.join()
        del self.sender


if __name__ == '__main__':
    unittest.main()
