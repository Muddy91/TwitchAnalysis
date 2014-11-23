def parse_data(data):
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
	msg = data[msg_colon_index+1:-1]
	#msg = data[msg_colon_index+1:]


	print hashtag_index
	print chan_end_index
	print msg_colon_index
	# Did we mess up? Return empty tuple.
	if exclam_index == -1 or hashtag_index == -1 or msg_colon_index == -1 or chan_end_index == hashtag_index-1:
		return fail_tuple
	else:
		return {'nick' : nickname, 'chan' : chan, 'msg' : msg}

with open('raw_output.txt') as f:
	lines = f.readlines()
	for l in lines:
		parsed = parse_data(l)
		print parsed['msg']
		print parsed['nick']
		print parsed['chan']
