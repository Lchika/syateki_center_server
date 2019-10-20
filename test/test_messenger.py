import sys
import pathlib
import threading
import unittest
import json
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_messenger import Sender, Receiver

TEST_PROCESS_ID = 1


def func1(json_mess):
    print('exec func1')


def func2(json_mess):
    print('exec func2')


def func3(json_mess):
    print('exec func3')


class TestMessenger(unittest.TestCase):
    def setUp(self):
        print('TestMessenger setup')
        self.receiver = Receiver(TEST_PROCESS_ID)
        d_callbacks = {'func1': func1, 'func2': func2, 'func3': func3}
        self.recv_thread = threading.Thread(target=self.receiver.open, args=(d_callbacks,))
        self.recv_thread.start()
        self.sender = Sender()
    
    def test_send_mess_regular(self):
        print(sys._getframe().f_code.co_name + ' start')
        d_message = {'func': 'func2', 'arg': 'test'}
        j_message = json.dumps(d_message)
        result = self.sender.send(TEST_PROCESS_ID, j_message)
        self.assertEqual(True, result)
    
    def test_send_mess_nostring(self):
        print(sys._getframe().f_code.co_name + ' start')
        d_message = {}
        j_message = json.dumps(d_message)
        result = self.sender.send(TEST_PROCESS_ID, j_message)
        self.assertEqual(True, result)

    def test_send_mess_invalid_func(self):
        print(sys._getframe().f_code.co_name + ' start')
        d_message = {'func': 'func4', 'arg': 'test'}
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
