import sys
import socket
import string
class IRCClient:
	socket = None
	nickname = "Brohunt"
	connected = False
	def __init__(self):
		HOST="irc.twitch.tv"
		PORT=6667
		NICK="Brohunt"
		PASS="oauth:mzcxmidfng6xzaig70f6cplz80gujw"
		file_raw = "raw_output.txt"
		file_filtered = "filtered_output.txt"
		file_raw = open(file_raw, 'a')
		file_filtered = open(file_filtered, 'a')


		self.socket = socket.socket()
		self.socket.connect((HOST, PORT))
		self.send("PASS %s" % PASS)
		self.send("NICK %s" % NICK)
		self.send("JOIN #froggen")
		self.send("JOIN #tsm_theoddone")

		while True:
			buf = self.socket.recv(4096)
			lines = buf.split("\n")
			for data in lines:
				data = str(data).strip()
				if data == '':
					continue
				file_raw.write(data + "\n")
				parsed = self.parse_data(data)
				if parsed != None:
					file_filtered.write(parsed['nick'] + "\n")
					file_filtered.write(parsed['chan'] + "\n")
					file_filtered.write(parsed['msg'] + "\n")


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

	def send(self, msg):
		print "I>", msg
		self.socket.send(msg+"\r\n")

	#def say(self, msg, to):
		#self.send("PRIVMSG %s :%s" % (to, msg))

	def perform(self):
		self.send("PRIVMSG R : Login <>")
		self.send("MODE %s +x" % self.nickname)
		#for c in self.channels:
		#	self.send("/j %s", c)
		#	print "Tried to joing %s", c
			#self.send("JOIN %s", c)

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
		if data.find('brohunt') != -1:
			return None
		if exclam_index == -1 or hashtag_index == -1 or msg_colon_index == -1:
			return fail_tuple
		else:
			return {'nick' : nickname, 'chan' : chan, 'msg' : msg}


IRCClient()
