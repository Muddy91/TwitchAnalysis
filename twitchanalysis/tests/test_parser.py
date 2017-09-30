import unittest
from twitchanalysis.parser import Parser

class ParserTestClass(unittest.TestCase):

  def parse_input_data(self):
    input_data = """:bab0om!bab0om@bab0om.tmi.twitch.tv PRIVMSG #forsenlol :!roulette all"""
    expected_result = {'nick': "bab0om", 'chan': "forsenlol", 'msg': "!roulette all"}
    parser = Parser()
    result = parser.parse_data(input_data)
    self.assertEqual(expected_result, result)

  def throws_index_error_on_bad_input(self):
    input_data = """badinput"""
    parser = Parser()
    self.assertRaises(IndexError, parser.parse_data, input_data)
