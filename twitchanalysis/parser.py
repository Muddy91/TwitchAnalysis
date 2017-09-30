import re

class Parser:
  SPLIT_INDEXES = dict(
    nick = 1,
    chan = 4,
  )

  def parse_data(self, data):
    data_splits = re.split('[!#@:]', data)
    nick = data_splits[self.SPLIT_INDEXES['nick']]
    chan = data_splits[self.SPLIT_INDEXES['chan']].strip()
    msg_delimiter = '#' + chan + ' :'
    msg = re.split(msg_delimiter, data)[-1]
    return { 'nick' : nick, 'chan': chan, 'msg': msg }
