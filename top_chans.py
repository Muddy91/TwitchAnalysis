import urllib2
import json

"""
 Module to extract information from top channels
"""


class TopChans:
  url = "https://api.twitch.tv/kraken/streams"
  # Return current top channels in JSON format, number of channels is num
  def top_channels(self, num):
    curr_url = self.url + "?limit=" + str(num) + "&stream_type=live"
    req = urllib2.urlopen(curr_url)
    data = req.read()
    res = self.data_to_json(data)
    return res

  # Convert string data to json
  def data_to_json(self, data):
    return json.loads(data)['streams']

  # Get names of top channels
  def top_channels_names(self, num):
    res = self.top_channels(num)
    names = []
    for r in res:
      names.append(r['channel']['name'])
    return names
