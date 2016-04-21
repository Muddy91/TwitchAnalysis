# Twitch Chat Analysis

This project is a study on the entity known as the twitch chat.
This project aims to follow how the twitch chat integrates with the streamers
and with eachother. The exact outcome of this project is still unknown but what we know is that data is fun, twitch is fun, and code is fun.

## Dependencies
* Python 2.7
  - Numpy
  - Boto3
* AWS S3
* Spark

## Usage
To run the project clone the project, create a file called *credentials.py* and enter content as specified in the *Credentials* section. Change working directory to the root folder of the project and from a terminal run: *python main.py*
The machine running this script must contain aws credentials for connection to the AWS S3 bucket.

## Files

__main.py__
The master node of the data gathering process.
Handles all the sub-processes gathering chat data.

**chan_conn.py**
This script handles the connection and gathering of data from a given twitch channel. Each ChanConn object is ran in its own thread.

**top_chans.py**
Functions to extract the current top streams sorted by current viewers (default extracts top 30 channels for data gathering)

**parser.py**
Parses a raw message from the chat and transform it into a suitable json representation.

**S3_handle.py**
Setup the connection to the S3 bucket storage.
Also contains a function to upload a file to the bucket.

## Credentials
To be able to login to the AWS system a *.aws/credentials* file (or equivalent way of authentication to AWS) is needed. To set this up please refer to the official AWS documentation.
To connect to Twitch chat server registered user and oauth connected to said user is needed. The oauth is generated through Twitch. The user and oauth credentials is also needed to be entered in the *credentials.py* file. *T_NICK* is the twitch username and *T_PASS* is the oauth. Summarized it should look like this
*credentials.py*
```python
T_NICK="example-user"
T_PASS="oauth:long-generated-oauth-password"
```
## License
MIT License

Copyright (c) 2016 BRDMR

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

