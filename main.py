"""
    Main startup script for the chats.
    The main purpose of this script is to
    handle which chats we are currently connected to.

"""

from top_chans import TopChans
from chan_conn import ChanConn
import time
import sys
import thread
import logging

class Main:
  update_delay_minutes = 5 # Time between each channel update
  update_delay_seconds = 60*update_delay_minutes
  num_channels         = 30 # Numer of channels to parse
  current_channels     = [] # Channels we currently check
  channel_threads      = {}
  tc = None
  logger = None

  def __init__(self):
    reload(sys)
    sys.setdefaultencoding('utf8') # this is needed for the write to work with utf8
    self.logger = self.setup_log()
    self.tc = TopChans()
    self.main()

  def main(self):
    while True: # Main loop
      start_time = time.time() # Time in seconds
      top_chans = self.tc.top_channels_names(self.num_channels)
      add_chans = list(set(top_chans).difference(self.current_channels))
      rem_chans = list(set(self.current_channels).difference(top_chans))
      self.remove_channels(rem_chans)
      self.add_channels(add_chans)
      self.logger.debug("Adding channels: %s" % add_chans)
      self.logger.debug("Removing channels: %s" % rem_chans)

      # Sleep before next update
      if start_time + self.update_delay_seconds > time.time():
        time.sleep((start_time + self.update_delay_seconds) - time.time())

  def remove_channels(self, chans):
    for c in chans:
      t = self.channel_threads[c]
      if not t == None:
        t.stop()
      self.channel_threads.pop(c, None)
      self.current_channels.remove(c)

  def add_channels(self, chans):
    for c in chans:
      t = ChanConn(c)
      self.current_channels.append(c)
      self.channel_threads[c] = t
      t.start()
      self.logger.debug("Added channel: %s" % c)

  def setup_log(self):
    logger = logging.getLogger('main_log')
    logger.setLevel(logging.DEBUG)
    dh = logging.FileHandler('log/debug.log', mode='w')
    eh = logging.FileHandler('log/error.log', mode='w')
    formatter = logging.Formatter('%(asctime)s %(message)s')
    dh.setFormatter(formatter)
    eh.setFormatter(formatter)
    eh.setLevel(logging.ERROR)
    logger.addHandler(dh)
    logger.addHandler(eh)
    return logger

# Starting calls
if __name__ == '__main__':
  Main()
