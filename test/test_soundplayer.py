import sys
import pathlib
import unittest
import subprocess
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_messenger import Sender, Receiver
from device.a_soundplayer import ApiSoundPlayer


class TestSoundPlayer(unittest.TestCase):
    def setUp(self):
        print('TestSoundPlayer setup')
        command = ['python', str(pathlib.Path(__file__).parent.parent.resolve()) + '/device/t_soundplayer.py']
        res = subprocess.call(command)
        print('res = ' + res)
        self.soundplayer = ApiSoundPlayer()
    
    def test_play_file(self):
        print(sys._getframe().f_code.co_name + ' start')
        result = self.soundplayer.play_file(1)
        self.assertEqual(True, result)
    
    def test_kill(self):
        print(sys._getframe().f_code.co_name + ' start')
        result = self.soundplayer.kill()
        self.assertEqual(True, result)
    
    def tearDown(self):
        print('TestSoundPlayer tearDown')
        del self.soundplayer


if __name__ == '__main__':
    unittest.main()
