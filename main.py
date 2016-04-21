"""
    Main startup script for the chats.
    The main purpose of this script is to
    handle which chats we are currently connected to.

"""

from top_chans import TopChans
from chan_conn import ChanConn
import time
import thread
tc = TopChans()

class Main:
    update_delay_minutes = 5 # Time between each channel update
    update_delay_seconds = 60*update_delay_minutes
    num_channels         = 30 # Numer of channels to parse
    current_channels     = [] # Channels we currently check
    channel_threads      = {}
    def __init__(self):
        self.main()

    def main(self):
        while True: # Main loop
            start_time = time.time() # Time in seconds
            top_chans = tc.top_channels_names(self.num_channels)
            add_chans = list(set(top_chans).difference(self.current_channels))
            rem_chans = list(set(self.current_channels).difference(top_chans))
            self.remove_channels(rem_chans)
            self.add_channels(add_chans)
            print top_chans
            print "Adding channels: %s" % add_chans
            print "Removing channels: %s" % rem_chans
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
            print "Added channel: %s" % c

# Starting calls
Main()
