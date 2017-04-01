import urllib2
import json
import credentials as creds
from time import sleep
"""
 Module to extract information from top channels
"""


class TopChans:
  max_retries = 10
  wait_retry_sec = 5
  url = "https://api.twitch.tv/kraken/streams"
  # Return current top channels in JSON format, number of channels is num
  def top_channels(self, num):
    num_retries = 0
    while num_retries < self.max_retries:
      try:
        curr_url = self.url + "?limit=" + str(num) + "&stream_type=live"
        request = urllib2.Request(curr_url, headers={"Client-ID": creds.T_CLIENTID})
        req = urllib2.urlopen(request)
        data = req.read()
        res = self.data_to_json(data)
        return res
      except Exception, e:
        print e
        num_retries = num_retries + 1
        if num_retries < self.max_retries:
          print "Will retry in %d seconds", wait_retry_sec
          sleep(wait_retry_sec)
        else:
          print "Final retry, won't retry again"




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
