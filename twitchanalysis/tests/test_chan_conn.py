import unittest
from mock import patch
from twitchanalysis.chan_conn import ChanConn

class ChanConnTestClass(unittest.TestCase):

  def setUp(self):
    self.name = "A_channel"
    self.cred = {}
    self.cred['T_NICK'] = "nick"
    self.cred['T_PASS'] = "pass"
    self.chan = ChanConn(self.name)

  @patch('twitchanalysis.credentials')
  def test_connection(self):
    test_patch.return_value = self.cred
    ret = self.chan.connect()
    self.assertEqual(False, True)

  # def test_join_channel(self):
  #   return False
  #
  # def test_run(self):
  #   return False
  #
  # def test_parse_json(self):
  #   return False
  #
  # def perform(self):
  #   return False
  #
  # def send(self):
  #   return False
  #
  # def stop(self):
  #   return False
  #
  # def test_handle_exit(self):
  #   return False
