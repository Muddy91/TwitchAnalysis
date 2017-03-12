import logging
logger = logging.getLogger('main_log')

def parse_data(data):

  exclam_index = data.find('!')
	# starts at index 1 since every message starts with ':'
  # which is not part of nickname
	nickname = data[1:exclam_index]
	hashtag_index = data.find('#')

	chan_end_index = hashtag_index + data[hashtag_index:].find(':')
	chan = data[hashtag_index:chan_end_index]

	msg_colon_index = chan_end_index + data[chan_end_index:].find(':')
	msg = data[msg_colon_index+1:-1]

	# Did we mess up? Return empty tuple.
	if exclam_index == -1 or \
      hashtag_index == -1 or \
      msg_colon_index == -1 or \
      chan_end_index == hashtag_index-1:
    logger.error("Could not parse: %s " %data)
    return None
	else:
		return {'nick' : nickname, 'chan' : chan, 'msg' : msg}
