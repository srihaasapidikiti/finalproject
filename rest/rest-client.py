#
# You probably want to borrow code from your Lab6 solution to send the image
#
from __future__ import print_function
import requests
import json
import sys
import os
addr = 'http://'+sys.argv[1]+':5000'
headers = {'content-type': 'image/png'}
# send http request with image and receive response
image_url = addr + '/api/review?X='+sys.argv[2]
response = requests.post(image_url, headers=headers)
print("Response is", response)
print(json.loads(response.text))
