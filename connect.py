import sys
import socket
import string
import datetime
import sys
import credentials as cred
import json
import threading
import time
class ChanConn(threading.Thread):
        NICK = cred.NICK
        PASS = cred.PASS
        HOST="irc.twitch.tv"
        PORT=6667
	output_path = "/home/brede/Development/TwitchAnalysis/data2/"
	nickname = "brohunt"
        # Initialize the connection.
	def __init__(self, chan):
                self.connected = False
                self.socket = None
                self.file_raw = None
                self.file_filtered = None
                self.active = True
                threading.Thread.__init__(self) # call superclass
                # Setup files
		self.file_raw = self.output_path + str(chan) + ".txt"
		self.file_filtered = self.output_path + str(chan) + "_filtered.txt"
		self.file_raw = open(self.file_raw, 'a')
		self.file_filtered = open(self.file_filtered, 'a')
		self.socket = socket.socket()
                self.connect()
                self.join_chan(chan)

        # Connect to a list of channels
        def join_chan(self, channel):
                channel = "#" + channel
                self.send("JOIN %s" % channel)

        # Connect to irc server
        def connect(self):
		self.socket.connect((self.HOST, self.PORT))
		self.send("PASS %s" % self.PASS)
		self.send("NICK %s" % self.NICK)

        # Run the script and listen to the joined channels
        def run(self):
		while self.active:
                        # Read message from connected channels
			buf = self.socket.recv(4096)
			lines = buf.split("\n")
			timestamp = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
			for data in lines:
				data = str(data).strip()
				if data == '':
					continue
				self.file_raw.write(timestamp + data + "\n")
				parsed = self.parse_json(data, timestamp)
				if parsed != None:
                                        self.file_filtered.write(json.dumps(parsed) + "\n")

				# server ping/pong?
				if data.find('PING') != -1:
					n = data.split(':')[1]
					self.send('PONG :' + n)
					if self.connected == False:
						self.perform()
						self.connected = True

				args = data.split(None, 3)
				if len(args)  != 4:
					continue
				ctx = {}
				ctx['sender'] = args[0][1:]
				ctx['type'] = args[1]
				ctx['target'] = args[2]
				ctx['msg'] = args[3][1:]

				# whom to reply?
				target = ctx['target']
				if ctx['target'] == self.nickname:
					target = ctx['sender'].split("!")[0]

        # This will make the next while-loop to break and the thread to terminate
        def stop(self):
            self.active = False

        # Send a message through the socket
	def send(self, msg):
		self.socket.send(msg+"\r\n")

	def perform(self):
		self.send("PRIVMSG R : Login <>")
		self.send("MODE %s +x" % self.nickname)

        # Convert the read data into a json object
        def parse_json(self, data, time):

            if data.find('PRIVMSG') == -1:
                return None
            if data.find('jtv') != -1:
                return None

            exclam_index = data.find('!')
            # starts at 1 since every message starts with ':' which is not part of nickname
            nickname = data[1:exclam_index]
            hashtag_index = data.find('#')
            chan_end_index = hashtag_index + data[hashtag_index:].find(':')
            chan = data[hashtag_index:chan_end_index]

            msg_start_index = chan_end_index + data[chan_end_index:].find(':')
            msg = data[msg_start_index+1:]

            if exclam_index == -1 or hashtag_index == -1 or msg_start_index == -1:
                return None

            json_dict = {'nick': nickname,
                    'chan': chan,
                    'msg': msg,
                    'time': time
                    }
            return  json_dict

"""
	# Split the data, right now we just care about NICKNAME CHANNEL and MESSAGE
	# This is a simple static parser, just enough for first tries.
	def parse_data(self, data):
		# If sh*t hits the fan, we will just return an empty tuple.
		# Not a nice design choice... but "for now, bro"
		#fail_tuple = {'nick' : "", 'chan' : "", 'msg' : ""}
		fail_tuple = None
		exclam_index = data.find('!')

		# starts at index 1 since every message starts wit ':' which is not part of nickname
		nickname = data[1:exclam_index]
		hashtag_index = data.find('#')

		chan_end_index = hashtag_index + data[hashtag_index:].find(':')
		chan = data[hashtag_index:chan_end_index]

		msg_colon_index = chan_end_index + data[chan_end_index:].find(':')
		msg = data[msg_colon_index+1:]
		#msg = data[msg_colon_index+1:]

		# Did we mess up? Return empty tuple.
		# This does not hold right now, since we add different indexes with each other.
		# PRIVMSG is to check that we actually parse a message.
		# brohunt is to check
		if data.find('PRIVMSG') == -1:
			return None
		if data.find('jtv') != -1:
			return None
		if exclam_index == -1 or hashtag_index == -1 or msg_colon_index == -1:
			return fail_tuple
		else:
			return {'nick' : nickname, 'chan' : chan, 'msg' : msg}
"""

# Start  calls
#ircc = ConnChan("#cdnthe3rd")
